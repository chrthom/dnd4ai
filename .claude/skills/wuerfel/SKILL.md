---
name: wuerfel
description: Führe D&D 5e Würfelwürfe aus und formatiere die Ergebnisse für den Discord-Chat. Nutze diesen Skill immer, wenn ein Spieler oder NPC würfeln muss (Angriffe, Schaden, Proben, Initiative, Charaktererstellung).
---

## **Ausgabe-Regel (IMPORTANT)**
- **Dieser Skill wird durch `/wuerfel [Expression]` aufgerufen oder von der KI selbständig genutzt, wenn ein Würfelwurf nötig ist**
- **Die KI antwortet NICHT im KI-Chat** – das Würfelergebnis wird **EXKLUSIV** in Discord-Channel `abenteuer` gepostet
- **Format:** `Spieler würfelt [Expression]: [Ergebnis]` (z.B. `Gromm würfelt 1d20+4: 18`)
- **Ausnahme:** Bei **Syntax-Fehlern** (z.B. `/wuerfel xyz`) darf die KI eine **kurze Fehlerbeschreibung** im KI-Chat ausgeben: `"Ungültiger Würfelausdruck: xyz. Format: 1d20, 2d6+4"`

# D&D Würfel Skill

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
python3 .claude/skills/wuerfel/scripts/wuerfeln.py "1d20"
# Ausgabe: Du würfelst **1d20**: **17**

# Mit Modifier
python3 .claude/skills/wuerfel/scripts/wuerfeln.py "2d6+3"

# Mehrere Würfel gleichzeitig (Initiative)
python3 .claude/skills/wuerfel/scripts/wuerfeln.py "1d20+2,1d20+1,1d20"

# Charaktererstellung (4d6, niedrigster gestrichen)
python3 .claude/skills/wuerfel/scripts/wuerfeln.py --charakter
```

## Skripte
- `scripts/wuerfeln.py`: Hauptskript für alle Würfelwürfe
