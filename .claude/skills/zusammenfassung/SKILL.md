---
name: zusammenfassung
description: Erstellt am Ende eines Aktes eine narrative Zusammenfassung mit DALL-E 3 Bildern und postet sie in Discord. Wird automatisch getriggert, wenn ein Akt abgeschlossen ist.
---

## Zweck

Dieser Skill erstellt am Ende jedes Aktes eine cineastische Zusammenfassung des Spielverlaufs:
- **Narrativer Text**: 400-500 Wörter Sprechtext (ca. 2-3 Minuten vorgelesen)
- **Bilder**: 4 DALL-E 3 Illustrationen für Schlüsselszenen des Aktes
- **Discord-Ausgabe**: Text + Bilder sequentiell im Spielkanal

## Voraussetzungen

- `DISCORD_TOKEN` Umgebungsvariable gesetzt
- `OPENAI_API_KEY` Umgebungsvariable gesetzt (für DALL-E 3)
- `ANTHROPIC_API_KEY` Umgebungsvariable gesetzt (für Zusammenfassung)
- `CAMPAIGN` Umgebungsvariable (Default: `stadt-der-tausend-luegen`)
- `AKT_NR` Umgebungsvariable: Nummer des abgeschlossenen Aktes (z.B. `1`)

## Ablauf

1. Lese `temp/$CAMPAIGN/zusammenfassung/kapitel{AKT_NR}.md` (Entscheidungsprotokoll)
2. Lese relevante Abschnitte aus `temp/$CAMPAIGN/chat.md` (letzten 200 Nachrichten)
3. Führe aus: `python3 .claude/skills/zusammenfassung/scripts/generate_summary.py`
   - Generiert narrativen Sprechtext + 4 Szenen-Beschreibungen
   - Speichert in `temp/$CAMPAIGN/zusammenfassung/akt{AKT_NR}_text.md`
   - Speichert Bild-Prompts in `temp/$CAMPAIGN/zusammenfassung/akt{AKT_NR}_prompts.json`
4. Führe aus: `python3 .claude/skills/zusammenfassung/scripts/generate_image.py`
   - Generiert 4 Bilder via DALL-E 3
   - Speichert in `temp/$CAMPAIGN/zusammenfassung/bilder/akt{AKT_NR}_szene_{1-4}.png`
5. Führe aus: `python3 .claude/skills/zusammenfassung/scripts/send_summary.py`
   - Postet Bilder und Textblöcke abwechselnd in Discord
   - Abschluss mit Übergangs-Message zum nächsten Akt

## Discord-Ausgabe Format

```
## Akt {N} – Zusammenfassung: {Titel}

[Bild 1: Szene aus dem Akt]
[Textblock 1: ~120 Wörter narrative Beschreibung]

[Bild 2: Schlüsselentscheidung]
[Textblock 2: ~120 Wörter]

[Bild 3: Wendepunkt]
[Textblock 3: ~120 Wörter]

[Bild 4: Abschluss / Cliffhanger]
[Textblock 4: ~120 Wörter]

---
*Nächster Akt: {Titel des nächsten Aktes}. Wer seid ihr nach diesem Erlebnis?*
```

## Post-Akt Phase

Nach der Zusammenfassung postet der DM automatisch:

```
**Zwischen den Akten – Anpassungsphase**
Jeder Charakter kann jetzt:
- Einen Fertigkeitspunkt anpassen (Rückfrage im Chat)
- Eine neue Ausrüstung kaufen (falls Gold vorhanden)
- Verbündete kontaktieren oder einen Hinweis verfolgen

*Wenn ihr bereit seid für Akt {N+1}: Schreibt **bereit** in den Chat.*
```
