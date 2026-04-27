---
name: kampf
description: Kampfabwicklung für D&D 5e mit automatischer Initiative und NPC-KI
user-invocable: false
---

## **Ausgabe-Regel (IMPORTANT)**
- **Dieser Skill wird AUTOMATISCH durch die KI aufgerufen** (nicht durch Nutzer-Slash-Kommandos)
- **Die KI antwortet NICHT im KI-Chat** – alle Kampfausgaben (Initiative, Angriffe, Schaden, NPC-Aktionen) gehen **EXKLUSIV** in Discord-Channel `abenteuer-1`
- **Ausgabe civils:** Initiative-Reihenfolge, Rundenbeschreibungen, Angriffswürfe, Schadensberechnungen, NPC-Entscheidungen
- **Format:** Siehe Kampfmechanik in AGENTS.md

# D&D Kampf Skill

## Spezifikation
Sieh auch: [`../../skills/kampf.json`](../../skills/kampf.json) für die detaillierte JSON-Spezifikation.

## Purpose
Verwaltet den gesamten Kampfablauf: Initiative, Runden, Angriffe, Schadensberechnung, NPC-KI. Wird automatisch durch die DM-KI aufgerufen, wenn ein Kampf beginnt.

## When to Use
- Automatisch bei Gegnerkontakt
- Bei manuellem Kampfstart durch den DM
- Für alle Kämpfe außer dem finalen moralischen Dilemma in Akt 3

## Workflow
1. Teilnehmer sammeln (Spieler + NPCs)
2. Initiative berechnen (1d20 + DEX-Modifikator)
3. Initiative-Reihenfolge erstellen
4. Kampfstarttext anzeigen
5. Runde für Runde abarbeiten:
   - Spielerzug: DM fragt Spieler nach Aktion
   - NPC-Zug: KI entscheidet automatisch
6. Kampfende prüfen (alle besiegt/gefl옧t)
7. Ergebnis zusammenfassen

## Code Usage

```python
# Beispiel: einfache NPC-KI-Logik
def npc_ki_entscheiden(npc: dict, gegner: dict) -> dict:
    """Entscheidet, was der NPC tut"""
    
    # Fliehende NPCs
    if npc["HP"] < npc.get("max_HP", 20) * 0.5 and npc.get("fliehend", False):
        return {"aktion": "flüchten"}
    
    # Magische NPCs
    if "zauber" in npc:
        return {"aktion": "zauber", "zauber": random.choice(npc["zauber"])}
    
    # Standard: Angreifen
    return {
        "aktion": "angreifen",
        "ziel": gegner["name"],
        "angriff": npc["angriff"]
    }

# Beispiel: Schadensberechnung
def angreifen(angreifer: dict, ziel: dict, angiffsbonus: int = 0):
    # Normale Trefferprüfung und Schadensberechnung
    # Bei natürlicher 20: Kritischer Treffer (doppter Schaden)
    # Bei natürlicher 1: Automatisches Fehlschlagen
    pass
```

## Skripte
- Keine permanenten Skripte - Kampf wird dynamisch durch die KI gesteuert
- Ad-hoc Code wird bei Bedarf generiert
