---
name: akt3-abgrund
description: Akt 3 – Terminal Gamma & Finale (Kampagne Der Abgrund)
user-invocable: true
---

## **Ausgabe-Regel (IMPORTANT)**
- **Dieser Skill wird durch `/akt 3` im KI-Chat aufgerufen (wenn ACTIVE_STORY=der-abgrund)**
- Alle Ausgaben gehen **EXKLUSIV** in Discord-Channel `abenteuer`

# Akt 3: Terminal Gamma – Der Abgrund antwortet

## Spezifikation
Siehe @../akte/akt_3.json für vollständige Konfiguration inkl. Abschlusstexte.

## Auswirkungen aus vorherigen Akten
| Bedingung | Auswirkung |
|-----------|------------|
| VEX-Muster erkannt (Akt 2) | Vorteil auf LOG DC beim Finalversuch |
| Kommunikation eingeschränkt (Akt 2) | VEX-Sabotage-DC auf 8 gesenkt für 1 Runde |
| AION befragt (Akt 1 oder 2) | Einmalig: Eine Sabotage automatisch verhindern |
| Sables Waffe gerettet (Akt 2) | +1 verfügbare Waffe gegen Rift-Ankerer |

## Workflow
1. AION enthüllt VEX' Mechanik
2. Rift-Sonden erscheinen
3. Moralisches Dilemma: Kommunikationsstille oder Freiwilliges Opfer
4. Finale: Terminal Gamma aktivieren
5. Abschlusstext aus akt_3.json (Ende A oder Ende B)
