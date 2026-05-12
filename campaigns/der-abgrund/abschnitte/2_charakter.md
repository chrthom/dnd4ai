# Charaktererstellung: Agent-Profile

## Vorbedingung

Prüfe, welche Spieler sich in den bislang abgerufenen Discord Nachrichten zum Mitspielen gemeldet haben.
Sollte sich kein Spieler gemeldet haben, breche an dieser Stelle ab und antworte **NICHT** in Discord.

## Aufgabe

Führe die Spieler durch die Charaktererstellung als Agenten von Nexus-7.
Halte dich an die Detailinformationen in @../charakter.json (kampagnenspezifische Regeln – überschreibt engine/regeln/charakter.json).

## Ablauf

1. Ermittle die Spieler ohne Charakterbogen (noch nicht in temp/charakterbogen/).
2. Rufe einen Spieler nach dem anderen auf:
   - Schritt 1: Name & Codename
   - Schritt 2: Hintergrund wählen (6 Optionen aus charakter.json)
   - Schritt 3: Agent-Profil wählen (5 Optionen)
   - Schritt 4: Attribute würfeln (DM würfelt 4d6 drop lowest, 6×) und zuweisen
   - Schritt 5: Ausrüstung vergeben (automatisch laut Profil)
3. Charakterbogen als Markdown zusammenfassen und:
   - In Discord posten und **pinnen**
   - Unter temp/charakterbogen/<spielername>.md speichern
4. Nächsten Spieler aufrufen.

**VEX-Setup (DM-intern, geheim, NICHT in Discord posten):**
Nach Abschluss aller Charakterbögen: Würfle verdeckt 1d[Spieleranzahl]. Dieser Agent trägt VEX zu Beginn. Notiere es in temp/vex_host.txt (NICHT in Discord).

## Charakterbogen-Template

```
**Agent:** [Codename] / [Discord-Name]
===
**Hintergrund:** [z.B. Militärisch Ausgebildet]
**Profil:** [z.B. Soldat]
**Trefferpunkte:** [Max HP] / [Max HP]
**Rüstungsklasse (AC):** [12 + REF-Mod]
**Initiative:** [REF-Mod]
**Attribute:** PHYS [X] | REF [X] | AUS [X] | LOG [X] | WAH [X] | SOZ [X]
**Ausrüstung:** [laut Profil]
**Spezialfähigkeit:** [aus Profil + Hintergrund]
```

## Erzählweise

- Führe die Charaktererstellung off-topic durch, aber mit thematisch passenden Kommentaren von AION.
- AION scannt die Agenten "offiziell" – nutze das als In-Game-Framing für die Fragen.
- Beispiel: "AION scannt: *Militärisches Muster erkannt. Profil: Soldat. Bestätigen?*"

## Wenn alle Bögen erstellt sind

Überschreibe temp/status.txt: "3_terminal_alpha". Fahre fort mit campaigns/$ACTIVE_STORY/abschnitte/3_terminal_alpha.md.
