#!/usr/bin/env python3
"""
Image Agent – generiert Bilder für D&D-Szenen und postet sie in Discord.

Kann standalone aufgerufen werden oder von anderen Agenten (summary_agent, dm_agent) importiert.

Nutzung:
  from image_agent import generate_image, post_image
  img_bytes = generate_image("A dragon in a throne room")
  post_image(img_bytes, "A mighty dragon!", channel_id)
"""
import io
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

# Config
IMAGE_MODEL = os.environ.get("IMAGE_MODEL", "dall-e-3")
IMAGE_PROVIDER = os.environ.get("IMAGE_PROVIDER", "pollinations,hub,openai")
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN", "")


def _generate_via_pollinations(prompt: str) -> bytes | None:
    """Kostenlose Bildgenerierung via Pollinations.ai – kein API-Key nötig.
    Nutzt Flux-Modell (schnell + gute Qualität)."""
    import urllib.parse
    encoded = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&model=flux&nologo=true"
    try:
        resp = requests.get(url, timeout=120)
        resp.raise_for_status()
        return resp.content
    except Exception as e:
        print(f"  ✗ pollinations: {e}", file=sys.stderr)
        return None


def _generate_via_openai_compatible(prompt: str, api_key: str, url: str, provider_name: str) -> bytes | None:
    """Generiert Bild via OpenAI-kompatible API (Hub DALL-E, OpenAI, Mistral, etc.)."""
    try:
        resp = requests.post(
            url,
            json={"model": IMAGE_MODEL, "prompt": prompt, "n": 1, "size": "1024x1024"},
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            timeout=60,
        )
        if resp.status_code == 400 and "budget" in resp.text.lower():
            print(f"  ✗ {provider_name}: Budget überschritten", file=sys.stderr)
            return None
        resp.raise_for_status()
        image_url = resp.json()["data"][0]["url"]
        img_resp = requests.get(image_url, timeout=30)
        img_resp.raise_for_status()
        return img_resp.content
    except Exception as e:
        print(f"  ✗ {provider_name}: {e}", file=sys.stderr)
        return None


def _generate_via_custom(prompt: str, provider_name: str) -> bytes | None:
    """Custom Image Provider via Env-Variablen steuerbar.

    Env-Schema für Custom-Provider:
      IMAGE_PROVIDER_<NAME>_URL=https://api.example.com/images
      IMAGE_PROVIDER_<NAME>_API_KEY=your_key_here
      IMAGE_PROVIDER_<NAME>_MODEL=model_name (optional, default: IMAGE_MODEL)

    Beispiel für Mistral:
      IMAGE_PROVIDER_MISTRAL_URL=https://api.mistral.ai/v1/images/generations
      IMAGE_PROVIDER_MISTRAL_API_KEY=your_mistral_key
      IMAGE_PROVIDER_MISTRAL_MODEL=pixtral (optional)
    """
    env_prefix = f"IMAGE_PROVIDER_{provider_name.upper()}"
    api_key = os.environ.get(f"{env_prefix}_API_KEY", "")
    api_url = os.environ.get(f"{env_prefix}_URL", "")
    model = os.environ.get(f"{env_prefix}_MODEL", IMAGE_MODEL)

    if not api_key or not api_url:
        print(f"  ✗ {provider_name}: missing {env_prefix}_API_KEY or {env_prefix}_URL", file=sys.stderr)
        return None

    return _generate_via_openai_compatible(prompt, api_key, api_url, provider_name)


def generate_image(prompt: str) -> bytes | None:
    """Generiert ein Bild. Provider-Reihenfolge per IMAGE_PROVIDER steuerbar.

    Vordefinierte Provider:
      pollinations → kostenlos, Flux-Modell, kein Key
      hub          → adesso AI Hub (DALL-E)
      openai       → OpenAI direkt (DALL-E)

    Custom Provider (Mistral, etc.):
      <name>       → via IMAGE_PROVIDER_<NAME>_URL, IMAGE_PROVIDER_<NAME>_API_KEY
    """
    order = [p.strip() for p in IMAGE_PROVIDER.split(",")]

    for provider_name in order:
        if provider_name == "pollinations":
            result = _generate_via_pollinations(prompt)
        elif provider_name == "hub" and os.environ.get("AI_HUB_TOKEN"):
            result = _generate_via_openai_compatible(
                prompt,
                os.environ.get("AI_HUB_TOKEN", ""),
                f"{os.environ.get('AI_HUB_URL','').rstrip('/')}/images/generations",
                "hub",
            )
        elif provider_name == "openai" and os.environ.get("OPENAI_API_KEY"):
            result = _generate_via_openai_compatible(
                prompt,
                os.environ.get("OPENAI_API_KEY", ""),
                "https://api.openai.com/v1/images/generations",
                "openai",
            )
        elif os.environ.get(f"IMAGE_PROVIDER_{provider_name.upper()}_URL"):
            # Custom Provider: mistral, replicate, etc.
            result = _generate_via_custom(prompt, provider_name)
        else:
            continue
        if result:
            return result

    print("  ✗ Kein Image-Provider konnte Bild generieren", file=sys.stderr)
    return None


def post_image(image_bytes: bytes, caption: str, channel_id: str = "", token: str = "", filename: str = "bild.png") -> None:
    """Postet ein Bild mit Caption in Discord.

    Args:
        image_bytes: Bild-Daten (PNG, JPEG)
        caption: Text-Caption unter dem Bild
        channel_id: Discord Channel ID (falls nicht gesetzt, kommt aus Campaign Config)
        token: Discord Bot Token (nutzt DISCORD_TOKEN env var falls nicht gesetzt)
        filename: Dateiname des Bildes im Upload
    """
    if not token:
        token = DISCORD_TOKEN
    if not token:
        print("  ✗ Kein Discord Token gesetzt (DISCORD_TOKEN env var)", file=sys.stderr)
        return

    if not channel_id:
        # Fallback: aus Campaign Config laden
        try:
            import json
            campaign = os.environ.get("CAMPAIGN", "stadt-der-tausend-luegen")
            config_path = Path(__file__).resolve().parents[1] / "campaigns" / campaign / "config.json"
            with open(config_path) as f:
                config = json.load(f)
            channel_id = config.get("discord_channel_id", "")
        except:
            pass

    if not channel_id:
        print("  ✗ Keine Channel ID gesetzt", file=sys.stderr)
        return

    try:
        resp = requests.post(
            f"https://discord.com/api/v10/channels/{channel_id}/messages",
            data={"content": caption},
            files={"files[0]": (filename, io.BytesIO(image_bytes), "image/png")},
            headers={"Authorization": f"Bot {token}"},
        )
        resp.raise_for_status()
    except Exception as e:
        print(f"  ✗ Discord post failed: {e}", file=sys.stderr)


if __name__ == "__main__":
    # Quick test: generate and display info
    print("Image Agent – Standalone Test")
    print(f"IMAGE_PROVIDER: {IMAGE_PROVIDER}")
    print(f"IMAGE_MODEL: {IMAGE_MODEL}")
    print("\nGeneriere Test-Bild...")

    img = generate_image("A fantasy tavern scene, D&D art style, cozy warm lighting")
    if img:
        print(f"✓ Erfolgreich generiert ({len(img)} bytes)")
    else:
        print("✗ Fehler bei Generierung")
