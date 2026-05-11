#!/usr/bin/env python3
"""
Generiert 4 DALL-E 3 Bilder für die Akt-Zusammenfassung.
Liest Bild-Prompts aus akt{N}_prompts.json, speichert PNG-Dateien.
"""
import os
import sys
import json
import urllib.request
from pathlib import Path

BASE_DIR = str(Path(__file__).resolve().parents[4])
CAMPAIGN = os.environ.get('CAMPAIGN', 'stadt-der-tausend-luegen')
AKT_NR = os.environ.get('AKT_NR', '1')
ZUSAMMENFASSUNG_DIR = os.path.join(BASE_DIR, 'temp', CAMPAIGN, 'zusammenfassung')
BILDER_DIR = os.path.join(ZUSAMMENFASSUNG_DIR, 'bilder')

from openai import OpenAI


def lade_prompts():
    prompts_path = os.path.join(ZUSAMMENFASSUNG_DIR, f'akt{AKT_NR}_prompts.json')
    if not os.path.exists(prompts_path):
        print(f"Fehler: {prompts_path} nicht gefunden. Zuerst generate_summary.py ausführen.", file=sys.stderr)
        sys.exit(1)
    with open(prompts_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def generiere_bild(client, prompt, szene_nr):
    bild_path = os.path.join(BILDER_DIR, f'akt{AKT_NR}_szene_{szene_nr}.png')

    print(f"Generiere Bild {szene_nr}/4: {prompt[:60]}...")

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    bild_url = response.data[0].url

    urllib.request.urlretrieve(bild_url, bild_path)
    print(f"Gespeichert: {bild_path}")
    return bild_path


def main():
    os.makedirs(BILDER_DIR, exist_ok=True)

    daten = lade_prompts()
    prompts = daten['bild_prompts']

    if len(prompts) != 4:
        print(f"Warnung: Erwartet 4 Prompts, gefunden {len(prompts)}", file=sys.stderr)

    client = OpenAI()
    bild_pfade = []

    for i, prompt in enumerate(prompts, 1):
        pfad = generiere_bild(client, prompt, i)
        bild_pfade.append(pfad)

    index_path = os.path.join(ZUSAMMENFASSUNG_DIR, f'akt{AKT_NR}_bilder.json')
    with open(index_path, 'w') as f:
        json.dump(bild_pfade, f, indent=2)

    print(f"\nAlle {len(bild_pfade)} Bilder generiert. Index: {index_path}")


if __name__ == '__main__':
    main()
