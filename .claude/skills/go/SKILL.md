---
name: go
description: Rollenspiel als Dungeon Master starten oder fortsetzen. Holt neue Discord-Nachrichten und steuert die nächste Spielphase.
---

Nutze die Umgebungsvariablen `DISCORD_TOKEN` und `CAMPAIGN` (Default: `stadt-der-tausend-luegen`), um mit der Discord API im Spielkanal zu kommunizieren.

Die Kampagnenkonfiguration liegt in `campaigns/$CAMPAIGN/config.json` (Channel ID, Spieler-Bots etc.).

Sollte `temp/$CAMPAIGN/status.txt` noch nicht existieren, dann erstelle es bitte mit diesem Inhalt `1_intro` und lege auch `temp/$CAMPAIGN/chat.md` an.
Ansonsten lese alle Dateien unter `temp/$CAMPAIGN/` (auch in Subordnern) ein sowie die relevanten Dateien in `campaigns/$CAMPAIGN/players/`.

Führe folgende Schritte aus:
1. Führe `python3 .claude/skills/go/scripts/fetch_messages.py` aus, um:
   - `temp/$CAMPAIGN/chat.md` zu lesen und den Zeitstempel der letzten Nachricht zu ermitteln
   - Alle Nachrichten von Discord zu holen, die nach diesem Zeitstempel gesendet wurden
   - Die neuen Nachrichten inkl. Verfasser und Zeitstempel in `temp/$CAMPAIGN/chat.md` zu speichern
   - **Exit-Codes**: `0` = neue Nachrichten gefunden, `1` = keine neuen Nachrichten
2. Analysiere die neuen Nachrichten in `temp/$CAMPAIGN/chat.md`
3. Orientiere dich an den Anweisungen in `campaigns/$CAMPAIGN/abschnitte/<abschnitt>.md` (Abschnitt aus `temp/$CAMPAIGN/status.txt`)
   - Spielregeln und Mechaniken liegen in `engine/regeln/` (kampf.json, charakter.json, charakter_setup.json)
   - Akt-Details (NPCs, Checkpoints, Fallen) liegen in `campaigns/$CAMPAIGN/akte/akt_N.json`
   - Spieler-Charakterbögen und Persönlichkeitsprofile liegen in `campaigns/$CAMPAIGN/players/<name>/`
4. Sende passende Nachrichten in Discord. Poste bei Bedarf in mehreren Message-Blocks (Discord-Limit: 2000 Zeichen)
5. **WICHTIG – Polling auf Spieler-Antworten**: Solltest du auf Antworten warten (KI-Spieler reagieren oft innerhalb von Sekunden), dann nutze **NICHT** wiederholte `sleep`-Aufrufe oder `ScheduleWakeup`. Stattdessen:

   ```bash
   until python3 .claude/skills/go/scripts/fetch_messages.py; do sleep 5; done
   ```

   Starte diesen Befehl per Bash mit `run_in_background: true`. Die Schleife pollt alle 5 Sekunden und beendet sich, sobald neue Nachrichten eintreffen — du wirst dann automatisch benachrichtigt. Cache bleibt warm (kein Wakeup ohne Arbeit), Latenz ≤ 5s.

   Sobald die Schleife endet:
   - Lies `temp/$CAMPAIGN/chat.md` (die neuen Nachrichten sind bereits angehängt)
   - Setze ab Schritt 2 fort
   - Wiederhole, bis die aktuelle Anweisung vollständig erfüllt ist (z.B. alle Spieler haben geantwortet, Spielzug abgeschlossen)

   **Polling beenden**: Sobald die Spielphase abgeschlossen ist (Kapitel zu Ende, Pause, Tribunal entschieden), starte keine neue Schleife mehr.

   **Polling-Intervall anpassen**:
   - Standard: `sleep 5` — passt für aktive KI-Spielzüge
   - Sehr aktive Phase mit mehreren parallelen KI-Antworten: `sleep 2`
   - Lange Bedenkphasen / Pausen: `sleep 30`
