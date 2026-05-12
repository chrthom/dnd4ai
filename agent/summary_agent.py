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
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from llm import create_adapter

BASE_DIR = Path(__file__).resolve().parents[1]
CAMPAIGN = os.environ.get("CAMPAIGN", "stadt-der-tausend-luegen")
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
IMAGE_MODEL = os.environ.get("IMAGE_MODEL", "dall-e-3")
IMAGE_PROVIDER = os.environ.get("IMAGE_PROVIDER", "openai")  # openai | hub

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

    llm_id = os.environ.get("LLM_MODEL_GEMINIRA", "claude-sonnet-4-6")
    adapter = create_adapter(llm_id)

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


def generate_image(prompt: str) -> bytes | None:
    """Generiert ein Bild via DALL-E oder AI Hub. Versucht Hub zuerst, dann OpenAI als Fallback."""
    providers = []
    if IMAGE_PROVIDER == "hub" or os.environ.get("AI_HUB_TOKEN"):
        providers.append(("hub", os.environ.get("AI_HUB_TOKEN", ""), f"{os.environ.get('AI_HUB_URL','').rstrip('/')}/images/generations"))
    if os.environ.get("OPENAI_API_KEY"):
        providers.append(("openai", os.environ.get("OPENAI_API_KEY", ""), "https://api.openai.com/v1/images/generations"))

    if not providers:
        print("  ✗ Kein Image-API-Key gesetzt (AI_HUB_TOKEN oder OPENAI_API_KEY)", file=sys.stderr)
        return None

    for provider_name, api_key, url in providers:
        try:
            resp = requests.post(
                url,
                json={"model": IMAGE_MODEL, "prompt": prompt, "n": 1, "size": "1024x1024"},
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                timeout=60,
            )
            if resp.status_code == 400 and "budget" in resp.text.lower():
                print(f"  ✗ {provider_name}: Budget überschritten – versuche nächsten Provider", file=sys.stderr)
                continue
            resp.raise_for_status()
            image_url = resp.json()["data"][0]["url"]
            img_resp = requests.get(image_url, timeout=30)
            img_resp.raise_for_status()
            return img_resp.content
        except Exception as e:
            print(f"  ✗ {provider_name}: {e}", file=sys.stderr)
            continue

    return None


def post_text(content: str) -> None:
    """Postet Text in den Discord-Kanal."""
    # Splitten bei 2000-Zeichen-Limit
    chunks = [content[i:i+2000] for i in range(0, len(content), 2000)]
    for chunk in chunks:
        resp = requests.post(
            f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages",
            json={"content": chunk},
            headers={"Authorization": f"Bot {DISCORD_TOKEN}"},
        )
        resp.raise_for_status()


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
        summary = generate_summary_text(akt)
        post_text(f"## Akt {akt['nr']}: {akt['titel']}\n\n{summary}")

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

    post_text(
        "*\"Die Stadt der tausend Lügen blieb – doch ihr wisst, wer die Wahrheit spricht.*\n"
        "*Und das macht euch gefährlich.\"*\n\n"
        "🎭 **Ende der Kampagne**"
    )
    print("\nFertig!")


if __name__ == "__main__":
    run()
