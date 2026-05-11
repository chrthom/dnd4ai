#!/usr/bin/env python3
"""
Generiert eine narrative Zusammenfassung eines Aktes via Claude API.
Liest Entscheidungsprotokoll + Chat-History, erzeugt Sprechtext + Bild-Prompts.
"""
import os
import sys
import json
from pathlib import Path

BASE_DIR = str(Path(__file__).resolve().parents[4])
CAMPAIGN = os.environ.get('CAMPAIGN', 'stadt-der-tausend-luegen')
AKT_NR = os.environ.get('AKT_NR', '1')
TEMP_DIR = os.path.join(BASE_DIR, 'temp', CAMPAIGN)
ZUSAMMENFASSUNG_DIR = os.path.join(TEMP_DIR, 'zusammenfassung')

import anthropic


def lese_protokoll():
    protokoll_path = os.path.join(ZUSAMMENFASSUNG_DIR, f'kapitel{AKT_NR}.md')
    if os.path.exists(protokoll_path):
        with open(protokoll_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "(Kein Entscheidungsprotokoll vorhanden)"


def lese_chat_auszug(max_zeilen=200):
    chat_path = os.path.join(TEMP_DIR, 'chat.md')
    if not os.path.exists(chat_path):
        return "(Kein Chat-Protokoll vorhanden)"
    with open(chat_path, 'r', encoding='utf-8') as f:
        zeilen = f.readlines()
    return ''.join(zeilen[-max_zeilen:])


def generiere_zusammenfassung(protokoll, chat_auszug):
    client = anthropic.Anthropic()

    system_prompt = """Du bist ein epischer Geschichtenerzähler für ein D&D 5e Abenteuer in der Welt Eberron.
Deine Aufgabe: Erstelle eine cineastische Zusammenfassung eines Spielaktes.

Format deiner Antwort (JSON):
{
  "titel": "Kurzer dramatischer Aktitel",
  "textbloecke": [
    "~120 Wörter narrative Beschreibung Szene 1",
    "~120 Wörter narrative Beschreibung Szene 2",
    "~120 Wörter narrative Beschreibung Szene 3",
    "~120 Wörter narrative Beschreibung Szene 4"
  ],
  "bild_prompts": [
    "DALL-E 3 prompt für Szene 1 auf Englisch: fantasy illustration, D&D 5e, Eberron steampunk, ...",
    "DALL-E 3 prompt für Szene 2 auf Englisch: ...",
    "DALL-E 3 prompt für Szene 3 auf Englisch: ...",
    "DALL-E 3 prompt für Szene 4 auf Englisch: ..."
  ],
  "uebergang": "Ein Satz der auf den nächsten Akt hinweist"
}

Schreibe die Textblöcke als packenden Sprechtext (nicht als trockene Zusammenfassung).
Die Bild-Prompts auf Englisch, Stil: 'fantasy illustration, epic, detailed, Eberron steampunk aesthetic'."""

    user_message = f"""Akt-Nummer: {AKT_NR}

Entscheidungsprotokoll:
{protokoll}

Chat-Auszug (letzte Spielrunden):
{chat_auszug}

Erstelle jetzt die Zusammenfassung."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    return json.loads(response.content[0].text)


def speichere_ergebnisse(daten):
    os.makedirs(ZUSAMMENFASSUNG_DIR, exist_ok=True)

    text_path = os.path.join(ZUSAMMENFASSUNG_DIR, f'akt{AKT_NR}_text.md')
    with open(text_path, 'w', encoding='utf-8') as f:
        f.write(f"## Akt {AKT_NR} – {daten['titel']}\n\n")
        for i, block in enumerate(daten['textbloecke'], 1):
            f.write(f"### Szene {i}\n\n{block}\n\n")
        f.write(f"\n---\n*{daten['uebergang']}*\n")

    prompts_path = os.path.join(ZUSAMMENFASSUNG_DIR, f'akt{AKT_NR}_prompts.json')
    with open(prompts_path, 'w', encoding='utf-8') as f:
        json.dump({
            'titel': daten['titel'],
            'bild_prompts': daten['bild_prompts'],
            'uebergang': daten['uebergang']
        }, f, ensure_ascii=False, indent=2)

    print(f"Text gespeichert: {text_path}")
    print(f"Bild-Prompts gespeichert: {prompts_path}")
    return daten['titel']


def main():
    print(f"Generiere Zusammenfassung für Akt {AKT_NR}, Kampagne: {CAMPAIGN}")
    protokoll = lese_protokoll()
    chat_auszug = lese_chat_auszug()
    daten = generiere_zusammenfassung(protokoll, chat_auszug)
    titel = speichere_ergebnisse(daten)
    print(f"Zusammenfassung erstellt: Akt {AKT_NR} – {titel}")


if __name__ == '__main__':
    main()
