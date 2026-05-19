---
name: go
description: Rollenspiel als Dungeon Master starten oder fortsetzen. Holt neue Discord-Nachrichten und steuert die nächste Spielphase. Wird nur auf expliziten Nutzeraufruf gestartet – niemals automatisch durch die KI.
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
5. **WICHTIG – Polling auf Spieler-Antworten**: Solltest du auf Antworten warten, nutze **NICHT** wiederholte `sleep`-Aufrufe oder `ScheduleWakeup`. Stattdessen:

   Starte diesen Befehl per Bash mit `run_in_background: true`:
   ```bash
   python3 .claude/skills/go/scripts/wait_for_response.py
   ```

   Das Skript pollt intern alle 5 Sekunden und beendet sich nach spätestens 60 Sekunden — du wirst automatisch benachrichtigt. Reagiere auf den Exit-Code:

   | Exit-Code | Bedeutung | Deine Aktion |
   |-----------|-----------|--------------|
   | `0` | Neue Spielernachricht angekommen | Lies `temp/$CAMPAIGN/chat.md`, setze ab Schritt 2 fort |
   | `2` | 1 Minute ohne Antwort (Soft Nudge) | Sende eine freundliche Erinnerung in Discord ("Wir warten noch auf eure Entscheidung…"), starte das Skript erneut |
   | `3` | 2+ Minuten ohne Antwort (Hard Nudge) | Lies Charakterbögen aus `temp/$CAMPAIGN/charakterbogen/` und `campaigns/$CAMPAIGN/players/`, sende eine direkte Aufforderung die **jeden wartenden Spieler beim Namen nennt** (z.B. *"**Gromm**, **Lyssa** – die Zeit drängt! Was tut ihr?"*), starte das Skript erneut |

   Sobald eine Antwort eintrifft (Exit `0`), wird der Nudge-Zähler automatisch zurückgesetzt.

   **Polling beenden**: Sobald die Spielphase abgeschlossen ist (Kapitel zu Ende, Pause, Tribunal entschieden), starte kein neues Skript mehr.
