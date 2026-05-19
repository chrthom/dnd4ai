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
3. **Tod & Gruppencheck** (vor jeder weiteren Aktion, basierend auf `engine/regeln/tod.json`):
   - **Charakter auf 0 HP**: Todesrettungswürfe starten (1d20 je Zug). Format: `💀 **{name}** liegt bewusstlos! Todesrettungswurf: 1d20 = {X} → {Y}✅ / {Z}❌`. Verbündete können mit DC 10 Heilkunde-Wurf (Zug opfern) sofort stabilisieren. Bei 3 Misserfolgen → Tod (`tod.json → charakter_tod`): Charakter verliert 1 Level, scheidet für dieses Kapitel aus, kehrt zu Beginn des nächsten Kapitels zurück. Charakterbogen aktualisieren, Off-Game in Discord ankündigen.
   - **Alle aktiven Charaktere auf 0 HP / Kapitelziel unerreichbar**: Deus-Ex-Machina auslösen (`tod.json → gruppen_niederlage`):
     1. Schweregrad bestimmen (leicht/mittel/schwer)
     2. Narrative Rettungsoption auswählen und In-Game beschreiben
     3. Alle aktiven Charaktere auf 1 HP setzen
     4. Permanente Konsequenz(en) anwenden und Off-Game ankündigen: `⚠️ **Deus Ex Machina** – Die Gruppe wurde gerettet, aber es gibt einen Preis:`
     5. Charakterbögen + `temp/$CAMPAIGN/` aktualisieren
     6. Story am nächsten Checkpoint fortsetzen
4. Orientiere dich an den Anweisungen in `campaigns/$CAMPAIGN/abschnitte/<abschnitt>.md` (Abschnitt aus `temp/$CAMPAIGN/status.txt`)
   - Spielregeln und Mechaniken liegen in `engine/regeln/` (kampf.json, charakter.json, charakter_setup.json, tod.json)
   - Akt-Details (NPCs, Checkpoints, Fallen) liegen in `campaigns/$CAMPAIGN/akte/akt_N.json`
   - Spieler-Charakterbögen und Persönlichkeitsprofile liegen in `campaigns/$CAMPAIGN/players/<name>/`
5. Sende passende Nachrichten in Discord. Poste bei Bedarf in mehreren Message-Blocks (Discord-Limit: 2000 Zeichen)
6. **WICHTIG – Polling auf Spieler-Antworten**: Solltest du auf Antworten warten (KI-Spieler reagieren oft innerhalb von Sekunden), dann nutze **NICHT** wiederholte `sleep`-Aufrufe oder `ScheduleWakeup`. Stattdessen:

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
