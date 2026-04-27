---
name: charakter
description: Interaktive D&D 5e Charaktererstellung
user-invocable: true
---

## **Ausgabe-Regel (IMPORTANT)**
- **Dieser Skill wird durch `/charakter erstellen` im KI-Chat aufgerufen**
- **Die KI antwortet NICHT im KI-Chat** – der gesamte interaktive Dialog findet **EXKLUSIV** in Discord-Channel `abenteuer-1` statt
- **Bei Aufruf:** Schritt-für-Schritt-Anleitung wird in `abenteuer-1` gepostet (Rasse → Klasse → Attribute → etc.)
- **Ergebnis:** Erstellter Charakterbogen wird als **gepinnter Post** in `abenteuer-1` veröffentlicht + JSON-Speicherung in `/decisions/characters/`

# D&D Charaktererstellung Skill

## Spezifikation
Sieh auch: [`../../skills/charakter.json`](../../skills/charakter.json) für die detaillierte JSON-Spezifikation mit allen Rassen, Klassen und Schritten.

## Purpose
Führt Spieler durch die vollständige Charaktererstellung für D&D 5e. Erstellt gepinnte Discord-Posts mit den Charakterbögen. Wird typischerweise nach dem Intro aufgerufen, wenn Meister Quill fragt: *"Wer seid ihr?"*

## When to Use
- Zu Beginn der Kampagne, wenn Meister Quill fragt: *"Wer seid ihr?"*
- Wenn ein neuer Spieler zur Gruppe hinzukommt
- Wenn ein Charakter stirbt und ein neuer erstellt werden muss

## Workflow
1. Spieler entscheiden: Sollen alle gleichzeitig oder nacheinander Charaktere erstellen?
2. Für jeden Spieler:
   - Name des Charakters
   - Rasse auswählen (10 Optionen: Mensch, Elf, Dunkelelf, Zwerg, Halbling, Halbork, Halbelf, Gnom, Drachenblütiger, Tiefling)
   - Klasse auswählen (11 Optionen: Barbar, Barde, Druide, Kleriker, Waldläufer, Kämpfer, Mönch, Paladin, Schurke, Zauberer, Hexenmeister)
   - Attribute bestimmen (4d6, niedrigster wird gestrichen) und zuweisen
   - Fertigkeiten bestimmen
   - Ausrüstung wählen
   - Gesinnung festlegen
3. Charakterbogen als Markdown in Discord posten und pinnen
4. Alle Spieler bestätigen Fertigstellung
5. **Übergang zu Akt 1:** Meister Quill gibt den Auftrag

## Verbindung zu anderen Skills
- Wird durch `/charakter erstellen` aufgerufen
- wird typischerweise nach dem `intro`-Skill verwendet
- Führt zu `akt1`-Skill nach Abschluss

## Code Usage

```python
from .vibe.skills.charakter.scripts.charakter_utils import (
    generiere_charakter,
    formatiere_charakterbogen,
    roll_attributes_4d6
)

# Attribute würfeln
attribute = roll_attributes_4d6()

# Charakter erstellen
char = generiere_charakter(
    rasse="Zwerg",
    klasse="Kämpfer",
    attribute_werte=attribute,
    name="Gromm Eisenfaust",
    gesinnung="Gesetzlich Gut"
)

# Als Discord-Post formatieren
sheet = formatiere_charakterbogen(char)
print(sheet)
```

## Ausgabeformat (Discord-Post)
```markdown
**Name:** Gromm Eisenfaust
===
**Rasse:** Zwerg | **Klasse:** Kämpfer | **Level:** 1
**Gesinnung:** Gesetzlich Gut

**Attribute:** STR 17 | DEX 14 | CON 15 | INT 12 | WIS 10 | CHA 8

**Fertigkeiten:** Athletik +3, Wahrnehmung +1

**Ausrüstung:** Kettenhemd, Langschwert, Schild
```

## Beispieldialog
```
*Meister Quill schiebt eine leere Pergamentrolle über den Tisch und mustert die Gruppe mit wachsamem Blick.*

**"Wer seid ihr?"** *fragt er mit tiefer, aber freundlicher Stimme.* **"Bevor wir weitermachen, brauche ich euren Namen... und mehr als das. Ich brauche eure Geschichten."**

*Die KI beginnt die Charaktererstellung:*

KI: Gromm, du bist als Erster dran. Welche Rasse möchtest du spielen? (Mensch, Elf, Dunkelelf, Zwerg, Halbling, Halbork, Halbelf, Gnom, Drachenblütiger, Tiefling)
Spieler: Zwerg
KI: Gute Wahl! Zwerge erhalten +2 CON und +1 STR. Welche Klasse? (Barbar, Barde, Druide, Kleriker, Waldläufer, Kämpfer, Mönch, Paladin, Schurke, Zauberer, Hexenmeister)
Spieler: Kämpfer
KI: Perfekt. Jetzt würfeln wir deine Attribute mit 4d6 (höchste 3).
...

*Nach Abschluss aller Charakterbögen:*

*Meister Quill nickt zufrieden, als der letzte Charakterbogen gepostet wird. Er mustert die Gruppe mit wachsamem Blick, während er eine vergilbte Karte auf dem Tisch ausrollt.*

**"Gut. Ich sehe..."** *er liest die Namen* **"...einen Zwergen-Kämpfer, einen Elfen-Waldläufer und einen Halbork-Barbaren. Eine... interessante Zusammenstellung."**

*Er schiebt die Karte in die Mitte des Tisches. Darauf eingezeichnet: ein Weg durch die Gassen von Morgrave, markiert mit einem roten X.*

**"Die Harpers haben herausgefunden, dass die Manipulationen unserer Archive von jemandem in dieser Richtung ausgehen. Wir brauchen Beweise. Und wir brauchen sie heute Nacht. Die Wächter der Narrative sind bereits hinter uns her."**

*Er senkt die Stimme* **"Was sagt ihr? Nehmt ihr den Auftrag an?"**

**/akt 1** zum Starten des ersten Akts eingeben.
```

## Ausgabe nach Abschluss
- Jeder Charakterbogen wird als gepinnter Discord-Post erstellt
- Automatische Berechnungen: Trefferpunkte, Initiative, Angriffsboni, Rettungswürfe
- Checkpoint: "Charaktererstellung abgeschlossen" wird erreicht

## Skripte
- `scripts/charakter_utils.py`: Kernfunktionen für Charaktererstellung (keine CLI, nur reine Funktionen)

## Referenzierte Dateien
- [`../../skills/charakter.json`](../../skills/charakter.json) – Komplette Spezifikation mit allen Rassen, Klassen und Schritten
