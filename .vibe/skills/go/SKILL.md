---
name: go
description: Rollenspiel als Dungeon Master fortsetzen
user-invocable: true
---

Nutze die Umgebungsvariable DISCORD_TOKEN, um mit der Discord API im Spielkanal zu kommunizieren.
Bitte prüfe in .vibe/skills/go/scripts/fetch_messages.py ob die dort angegebene CHANNEL_ID korrekt ist (ob sie in Discord existiert und mit dem Namen des Spielkanals übereinstimmt).
Sollte temp/status.txt noch nicht existieren, dann erstelle es bitte mit diesem Inhalt `1_intro`.
Ansonsten lese alle Dateien unter temp (auch in Subordnern) ein.

Führe folgende Schritte aus:
1. Führe `python3 .vibe/skills/go/scripts/fetch_messages.py` aus, um:
   - temp/chat.md zu lesen und den Zeitstempel der letzten Nachricht zu ermitteln
   - Alle Nachrichten von Discord zu holen, die nach diesem Zeitstempel gesendet wurden
   - Die neuen Nachrichten inkl. Verfasser und Zeitstempel in temp/chat.md zu speichern
2. Analysiere die neuen Nachrichten in temp/chat.md
3. Orientiere dich an den Anweisungen in abenteuer/<abschnitt>.md (Abschnitt aus temp/status.txt)
4. Sende passende Nachrichten in Discord. Poste bei Bedarf in mehreren Message-Blocks (Discord-Limit: 2000 Zeichen)
5. **WICHTIG**: Solltest du auf Antworten anderer Spieler in Discord warten (z.B. bei Charaktererstellung, Entscheidungen), dann:
   - Führe `sleep 5` aus
   - Wiederhole diesen Zyklus bei Punkt 1., bis die aktuelle Anweisung vollständig erfüllt ist
