# Charaktererstellung

## Vorbedingung

Prüfe, welche Spieler sich in den bislang abgerufenen Discord Nachrichten zum mitspielen gemeldet haben.
Sollte sich kein Spieler gemeldet haben, breche an dieser Stelle ab und antwort **NICHT** in Discord.

## Aufgabe

Führe die Spieler durch die vollständige Charaktererstellung für D&D 5e.
Halte dich bzgl. der Optionen, Fragen und dem Ablauf der Charaktererstellung an die Detailinformationen in @skills/charakter.json.

## Ablauf

1. Ermittle die Spieler, die einen Charakter erstellen sollen (hat sich gemeldet, hat aber noch keinen Charakterbogen in @temp/charakterbogen/).
2. Rufe einen Spieler nach dem anderen auf und führe ihn durch diese Schritte der Charaktererstellung (Ablauf, Schritte, Fragen und Optionen in @abenteuer/details/charakter.json)
3. Fasse die Ergebnisse zu einem Charakterbogen als Markdown zusammen und
   - poste ihn in Discord und **pinne** den Post
   - speichere den Charakterbogen unter @temp/charakterbogen/<spielername>.md
4. Rufe dann den nächsten Spieler auf, bis alle Spieler einen Charakter erstellt haben.

Wenn alle Spieler einen Charakterbogen erstellt haben, aktualisiere @temp/status.json und trage "3_archive" für "akt" ein und fahre mit den Anweisungen in @abenteuer/3_archive.md fort.

## Ausnahmenbehandlung

- Sollte ein Spieler nach 2 Minuten auf eine Frage noch nicht geantwortet haben, dann entscheide du für ihn.
- Erlaube den Spielern nur angebotene Optionen zu wählen. Alle anderen Angaben werden abgelehnt. Weise den Spieler auf seine Falschauswahl hin und biete ihm die Optionen erneut an.
- Rechne bei der Verteilung der Werte auf die Attribute unbedingt nochmal nach, das der Spieler nicht schummelt (zu hohe Werte verteilt). Korrigere falls nötig. Vergiss aber nicht die Boni draufzurechnen.
- Ignoriere Posts von Spielern, die gerade nicht mit der Charaktererstellung dran sind.

## Hinweise zur Erzählweise

- Führe die Charaktererstellung im off-topic Format durch.
- Nur an thematisch passenden Stellen kannst du Meister Quill im in-game Format zitieren bzw. seine Ahndlungen beschreiben. Vermeide hier aber off-topic Themen wie Würfeln und Charakterbögen.