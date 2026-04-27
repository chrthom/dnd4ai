---
name: wuerfel
description: Führe D&D 5e Würfelwürfe aus und formatiere die Ergebnisse für den Discord-Chat
user-invocable: true
---

# D&D Würfel Skill

## Spezifikation
Sieh auch: [`../../skills/wuerfel.json`](../../skills/wuerfel.json) für die detaillierte JSON-Spezifikation.

## Purpose
Simuliert Würfelwürfe für Dungeons & Dragons 5e und gibt die Ergebnisse formatiert aus. Unterstützt Standard-D&D-Notation (1d20, 2d6+3 etc.).

## When to Use
- Spielerwürfe für Angriffe, Schaden, Proben
- KI-Würfe für NPCs
- Charaktererstellung (4d6 Methode)
- Zufällige Ereignisse

## Workflow
- Expression parsen (Anzahl Würfel, Seiten, Modifier)
- Zufallszahlen generieren
- Summe + Modifier berechnen
- Ergebnis formatiert ausgeben

## Code Usage

```bash
# Einfacher Würfelwurf
python3 .vibe/skills/wuerfel/scripts/wuerfeln.py "1d20"
# Ausgabe: Du würfelst **1d20**: **17**

# Mit Modifier
python3 .vibe/skills/wuerfel/scripts/wuerfeln.py "2d6+3"

# Mehrere Würfel gleichzeitig (Initiative)
python3 .vibe/skills/wuerfel/scripts/wuerfeln.py "1d20+2,1d20+1,1d20"

# Charaktererstellung (4d6, niedrigster gestrichen)
python3 .vibe/skills/wuerfel/scripts/wuerfeln.py --charakter
```

## Skripte
- `scripts/wuerfeln.py`: Hauptskript für alle Würfelwürfe
