#!/usr/bin/env python3
"""
Postet die Akt-Zusammenfassung (Text + Bilder) sequentiell in Discord.
Liest Textblöcke aus akt{N}_text.md und Bilder aus akt{N}_bilder.json.
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

DISCORD_TOKEN = os.environ['DISCORD_TOKEN']

with open(os.path.join(BASE_DIR, 'campaigns', CAMPAIGN, 'config.json')) as f:
    config = json.load(f)
CHANNEL_ID = config['discord_channel_id']
NAECHSTER_AKT = int(AKT_NR) + 1


def sende_nachricht(text):
    if len(text) > 2000:
        text = text[:1997] + "..."
    data = json.dumps({'content': text}).encode('utf-8')
    req = urllib.request.Request(
        f'https://discord.com/api/v10/channels/{CHANNEL_ID}/messages',
        data=data,
        headers={
            'Authorization': f'Bot {DISCORD_TOKEN}',
            'Content-Type': 'application/json',
        },
        method='POST',
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
        print(f"  Nachricht gesendet: id={result.get('id')}")


def sende_bild(bild_pfad, beschriftung=""):
    with open(bild_pfad, 'rb') as f:
        bild_daten = f.read()

    import io
    boundary = b'----WebKitFormBoundary7MA4YWxkTrZu0gW'
    body = b''
    body += b'--' + boundary + b'\r\n'
    body += b'Content-Disposition: form-data; name="file"; filename="scene.png"\r\n'
    body += b'Content-Type: image/png\r\n\r\n'
    body += bild_daten + b'\r\n'
    if beschriftung:
        body += b'--' + boundary + b'\r\n'
        body += b'Content-Disposition: form-data; name="content"\r\n\r\n'
        body += beschriftung.encode('utf-8') + b'\r\n'
    body += b'--' + boundary + b'--\r\n'

    req = urllib.request.Request(
        f'https://discord.com/api/v10/channels/{CHANNEL_ID}/messages',
        data=body,
        headers={
            'Authorization': f'Bot {DISCORD_TOKEN}',
            'Content-Type': f'multipart/form-data; boundary={boundary.decode()}',
        },
        method='POST',
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
        print(f"  Bild gesendet: id={result.get('id')}")


def lade_textbloecke():
    text_path = os.path.join(ZUSAMMENFASSUNG_DIR, f'akt{AKT_NR}_text.md')
    if not os.path.exists(text_path):
        print(f"Fehler: {text_path} nicht gefunden.", file=sys.stderr)
        sys.exit(1)
    with open(text_path, 'r', encoding='utf-8') as f:
        inhalt = f.read()

    bloecke = []
    aktueller_block = []
    for zeile in inhalt.split('\n'):
        if zeile.startswith('### Szene') and aktueller_block:
            bloecke.append('\n'.join(aktueller_block).strip())
            aktueller_block = []
        elif not zeile.startswith('## Akt') and not zeile.startswith('### Szene'):
            aktueller_block.append(zeile)
    if aktueller_block:
        bloecke.append('\n'.join(aktueller_block).strip())

    return [b for b in bloecke if b]


def lade_bild_pfade():
    index_path = os.path.join(ZUSAMMENFASSUNG_DIR, f'akt{AKT_NR}_bilder.json')
    if not os.path.exists(index_path):
        print(f"Fehler: {index_path} nicht gefunden.", file=sys.stderr)
        sys.exit(1)
    with open(index_path, 'r') as f:
        return json.load(f)


def lade_prompts():
    prompts_path = os.path.join(ZUSAMMENFASSUNG_DIR, f'akt{AKT_NR}_prompts.json')
    with open(prompts_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    print(f"Sende Zusammenfassung für Akt {AKT_NR} an Discord...")

    daten = lade_prompts()
    textbloecke = lade_textbloecke()
    bild_pfade = lade_bild_pfade()

    # Header
    sende_nachricht(f"## Akt {AKT_NR} – Zusammenfassung: {daten['titel']}")

    # Bilder und Textblöcke abwechselnd
    for i, (bild_pfad, textblock) in enumerate(zip(bild_pfade, textbloecke), 1):
        print(f"Szene {i}/4:")
        sende_bild(bild_pfad)
        if textblock:
            sende_nachricht(textblock)

    # Abschluss
    uebergang = daten.get('uebergang', '')
    abschluss = (
        f"---\n*{uebergang}*\n\n"
        f"**Zwischen den Akten – Anpassungsphase**\n"
        f"Jeder Charakter kann jetzt:\n"
        f"- Einen Fertigkeitspunkt anpassen\n"
        f"- Eine neue Ausrüstung kaufen (falls Gold vorhanden)\n"
        f"- Verbündete kontaktieren\n\n"
        f"*Wenn ihr bereit seid für Akt {NAECHSTER_AKT}: Schreibt **bereit** in den Chat.*"
    )
    sende_nachricht(abschluss)

    print(f"\nZusammenfassung Akt {AKT_NR} vollständig gepostet.")


if __name__ == '__main__':
    main()
