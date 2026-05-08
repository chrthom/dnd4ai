---
name: go
description: Rollenspiel als Dungeon Master starten oder fortsetzen. Holt neue Discord-Nachrichten und steuert die nächste Spielphase.
---

Nutze die Umgebungsvariable DISCORD_TOKEN, um mit der Discord API im Spielkanal zu kommunizieren.
Bitte prüfe in `.claude/skills/go/scripts/fetch_messages.py` ob die dort angegebene CHANNEL_ID korrekt ist (ob sie in Discord existiert und mit dem Namen des Spielkanals übereinstimmt).
Sollte `temp/status.txt` noch nicht existieren, dann erstelle es bitte mit diesem Inhalt `1_intro`.
Ansonsten lese alle Dateien unter `temp` (auch in Subordnern) ein.

Führe folgende Schritte aus:
1. Führe `python3 .claude/skills/go/scripts/fetch_messages.py` aus, um:
   - `temp/chat.md` zu lesen und den Zeitstempel der letzten Nachricht zu ermitteln
   - Alle Nachrichten von Discord zu holen, die nach diesem Zeitstempel gesendet wurden
   - Die neuen Nachrichten inkl. Verfasser und Zeitstempel in `temp/chat.md` zu speichern
   - **Exit-Codes**: `0` = neue Nachrichten gefunden, `1` = keine neuen Nachrichten
2. Analysiere die neuen Nachrichten in `temp/chat.md`
3. Orientiere dich an den Anweisungen in `abenteuer/<abschnitt>.md` (Abschnitt aus `temp/status.txt`)
4. Sende passende Nachrichten in Discord. Poste bei Bedarf in mehreren Message-Blocks (Discord-Limit: 2000 Zeichen)
5. **WICHTIG – Polling auf Spieler-Antworten**: Solltest du auf Antworten warten (KI-Spieler reagieren oft innerhalb von Sekunden), dann nutze **NICHT** wiederholte `sleep`-Aufrufe oder `ScheduleWakeup`. Stattdessen:

   ```bash
   until python3 .claude/skills/go/scripts/fetch_messages.py; do sleep 5; done
   ```

   Starte diesen Befehl per Bash mit `run_in_background: true`. Die Schleife pollt alle 5 Sekunden und beendet sich, sobald neue Nachrichten eintreffen — du wirst dann automatisch benachrichtigt. Cache bleibt warm (kein Wakeup ohne Arbeit), Latenz ≤ 5s.

   Sobald die Schleife endet:
   - Lies `temp/chat.md` (die neuen Nachrichten sind bereits angehängt)
   - Setze ab Schritt 2 fort
   - Wiederhole, bis die aktuelle Anweisung vollständig erfüllt ist (z.B. alle Spieler haben geantwortet, Spielzug abgeschlossen)

   **Polling beenden**: Sobald die Spielphase abgeschlossen ist (Kapitel zu Ende, Pause, Tribunal entschieden), starte keine neue Schleife mehr.

   **Polling-Intervall anpassen**:
   - Standard: `sleep 5` — passt für aktive KI-Spielzüge
   - Sehr aktive Phase mit mehreren parallelen KI-Antworten: `sleep 2`
   - Lange Bedenkphasen / Pausen: `sleep 30`
