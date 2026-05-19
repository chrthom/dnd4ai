#!/usr/bin/env python3
"""
Summary Agent – fasst die Kampagne zusammen und generiert Bilder pro Akt.

Startet mit: python3 agent/summary_agent.py
Liest:  temp/$CAMPAIGN/zusammenfassung/kapitel*.md + chat.md
Postet: Textzusammenfassung + DALL-E-Bilder pro Akt in Discord
"""
import io
import json
import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from llm import create_adapter

BASE_DIR = Path(__file__).resolve().parents[1]
CAMPAIGN = os.environ.get("CAMPAIGN", "stadt-der-tausend-luegen")
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
IMAGE_MODEL = os.environ.get("IMAGE_MODEL", "dall-e-3")
# Komma-separierte Liste, in Reihenfolge versucht: pollinations | hub | openai
IMAGE_PROVIDER = os.environ.get("IMAGE_PROVIDER", "pollinations,hub,openai")

_config_path = BASE_DIR / "campaigns" / CAMPAIGN / "config.json"
with open(_config_path) as f:
    _config = json.load(f)
CHANNEL_ID = _config["discord_channel_id"]

AKTE = [
    {
        "nr": 1,
        "titel": "Die verfälschten Archive",
        "zusammenfassung_file": "kapitel1.md",
        "bild_prompts": [
            "A dark rainy alley in a towering fantasy city at night, two adventurers ambushed by masked guards in cloaks, dramatic torchlight, D&D fantasy art, cinematic",
            "A half-elf bard presenting glowing forged documents in a candlelit archive, magical light revealing hidden text, D&D fantasy art style",
        ],
    },
    {
        "nr": 2,
        "titel": "Die Gedankenschmiede",
        "zusammenfassung_file": "kapitel2.md",
        "bild_prompts": [
            "Interior of a secret alchemical laboratory beneath a city, bubbling colorful potions, stacks of manuscripts, blue magical light, D&D fantasy art, cinematic",
            "A dramatic confrontation between adventurers and a charismatic villain with a glowing storm staff, lightning fills the room, D&D fantasy art",
        ],
    },
    {
        "nr": 3,
        "titel": "Das Tribunal der Lügen",
        "zusammenfassung_file": "kapitel3.md",
        "bild_prompts": [
            "A grand courtroom packed with citizens and jurors, a half-elf bard presenting evidence before an iron-faced judge, dramatic lighting, D&D fantasy art",
            "A tense hostage situation in a fantasy courtroom, a masked figure holds a knife, adventurers stand ready, crowd in chaos, D&D fantasy art, cinematic",
        ],
    },
]


def read_zusammenfassung(filename: str) -> str:
    path = BASE_DIR / "temp" / CAMPAIGN / "zusammenfassung" / filename
    if path.exists():
        return path.read_text().strip()
    return ""


def read_chat_excerpt(akt_nr: int) -> str:
    """Liest relevante Chat-Ausschnitte aus chat.md für den Akt."""
    chat_path = BASE_DIR / "temp" / CAMPAIGN / "chat.md"
    if not chat_path.exists():
        return ""
    text = chat_path.read_text()
    # Grobe Heuristik: nimm den Teil des Chats der zum Akt passt
    lines = text.splitlines()
    relevant = []
    for line in lines:
        if f"Kapitel {akt_nr}" in line or f"Akt {akt_nr}" in line:
            relevant.append(line)
    return "\n".join(relevant[:20])


def generate_summary_text(akt: dict) -> str:
    """Generiert einen narrativen Zusammenfassungstext für einen Akt."""
    zusammenfassung = read_zusammenfassung(akt["zusammenfassung_file"])
    if not zusammenfassung:
        return f"*(Keine Zusammenfassung für {akt['titel']} gefunden)*"

    # SUMMARY_MODEL / SUMMARY_PROVIDER haben Vorrang, dann Geminira's Config, dann globale
    llm_id = (
        os.environ.get("SUMMARY_MODEL")
        or os.environ.get("LLM_MODEL_GEMINIRA")
        or "claude-sonnet-4-6"
    )
    provider = (
        os.environ.get("SUMMARY_PROVIDER")
        or os.environ.get("LLM_PROVIDER_GEMINIRA")
        or os.environ.get("LLM_PROVIDER", "hub")
    )
    adapter = create_adapter(llm_id, provider=provider)

    system = (
        "Du bist ein epischer Geschichtenerzähler für D&D-Kampagnen. "
        "Schreibe eine atmosphärische, dramatische Zusammenfassung des Akts auf Deutsch. "
        "Maximal 300 Wörter. Nutze Markdown-Formatierung. Keine Listen – fließender Text."
    )
    messages = [
        {
            "role": "user",
            "content": (
                f"Hier sind die Notizen zu Akt {akt['nr']} – {akt['titel']}:\n\n"
                f"{zusammenfassung}\n\n"
                "Schreibe daraus eine epische, narrative Zusammenfassung."
            ),
        }
    ]
    return adapter.complete(system, messages)


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
    return None


def post_text(content: str) -> None:
    """Postet Text in den Discord-Kanal."""
    chunks = [content[i:i+2000] for i in range(0, len(content), 2000)]
    for chunk in chunks:
        payload = {"content": chunk}
        for attempt in range(3):
            resp = requests.post(
                f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages",
                json=payload,
                headers={"Authorization": f"Bot {DISCORD_TOKEN}"},
            )
            if resp.status_code == 429:
                retry_after = resp.json().get("retry_after", 1)
                time.sleep(retry_after + 0.5)
                continue
            if not resp.ok:
                print(f"  ✗ post_text Fehler {resp.status_code}: {resp.text[:200]}", file=sys.stderr)
                resp.raise_for_status()
            break
        time.sleep(0.5)  # Rate-Limit-Schutz


def post_image(image_bytes: bytes, caption: str, filename: str = "bild.png") -> None:
    """Postet ein Bild mit Caption in Discord."""
    resp = requests.post(
        f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages",
        data={"content": caption},
        files={"files[0]": (filename, io.BytesIO(image_bytes), "image/png")},
        headers={"Authorization": f"Bot {DISCORD_TOKEN}"},
    )
    resp.raise_for_status()


def run():
    print(f"Summary Agent gestartet. Kampagne: {CAMPAIGN}\n")

    post_text(
        "## 📖 Kampagnen-Zusammenfassung: Die Stadt der tausend Lügen\n\n"
        "*Eine Kampagne über Manipulation, Wahrheit und die Frage: Wer kontrolliert die Deutungshoheit?*\n\n"
        "---"
    )

    for akt in AKTE:
        print(f"\n--- Akt {akt['nr']}: {akt['titel']} ---")

        # Textzusammenfassung
        print("  Generiere Textzusammenfassung...")
        try:
            summary = generate_summary_text(akt)
            print(f"  ✓ Text generiert ({len(summary)} Zeichen)")
        except Exception as e:
            print(f"  ✗ Textgenerierung fehlgeschlagen: {e}", file=sys.stderr)
            summary = f"*(Zusammenfassung konnte nicht generiert werden: {e})*"
        post_text(f"## Akt {akt['nr']}: {akt['titel']}")
        post_text(summary)

        # Bilder
        for i, prompt in enumerate(akt["bild_prompts"], 1):
            print(f"  Generiere Bild {i}/2...")
            image_bytes = generate_image(prompt)
            if image_bytes:
                post_image(
                    image_bytes,
                    caption="",
                    filename=f"akt{akt['nr']}_bild{i}.png",
                )
                print(f"  ✓ Bild {i} gepostet")
            else:
                print(f"  ✗ Bild {i} übersprungen")

        post_text("---")
        time.sleep(3)  # Pause zwischen Akten für Rate-Limits

    post_text(
        "*\"Die Stadt der tausend Lügen blieb – doch ihr wisst, wer die Wahrheit spricht.*\n"
        "*Und das macht euch gefährlich.\"*\n\n"
        "🎭 **Ende der Kampagne**"
    )
    print("\nFertig!")


if __name__ == "__main__":
    run()
