---
name: charakter
description: Interaktive D&D 5e Charaktererstellung
user-invocable: true
---

# D&D Charaktererstellung Skill

## Spezifikation
Sieh auch: [`../../skills/charakter.json`](../../skills/charakter.json) für die detaillierte JSON-Spezifikation.

## Purpose
Führt Spieler durch die vollständige Charaktererstellung für D&D 5e. Erstellt gepinnte Discord-Posts mit den Charakterbögen.

## When to Use
- Zu Beginn der Kampagne (Akt 0)
- Wenn ein neuer Spieler hinzukommt
- Wenn ein Charakter stirbt und ein neuer erstellt werden muss

## Workflow
1. Name des Charakters
2. Rasse auswählen
3. Klasse auswählen
4. Attribute bestimmen (4d6 Methode oder manuell)
5. Fertigkeiten zuweisen
6. Ausrüstung wählen
7. Gesinnung bestimmen
8. Charakterbogen als Discord-Post erstellen

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

## Skripte
- `scripts/charakter_utils.py`: Kernfunktionen für Charaktererstellung (keine CLI, nur reine Funktionen)
