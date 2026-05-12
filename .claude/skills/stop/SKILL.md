---
name: stop
description: Alle laufenden D&D-Agenten sofort beenden (DM, Player, Summary). Sendet optional eine Abschlussnachricht in Discord.
---

Beende alle laufenden D&D-Agenten sofort.

Führe folgende Schritte aus:

1. Beende alle Agent-Prozesse via Lockfiles:
   ```bash
   for lockfile in /tmp/player_agent.lock /tmp/dm_agent.lock; do
     if [ -f "$lockfile" ]; then
       pid=$(cat "$lockfile")
       kill "$pid" 2>/dev/null && echo "Beendet PID $pid ($lockfile)" || echo "Prozess $pid nicht aktiv"
       rm -f "$lockfile"
     fi
   done
   ```

2. Prüfe ob noch Python-Agenten laufen und beende sie:
   ```bash
   pkill -f "player_agent.py" 2>/dev/null || true
   pkill -f "dm_agent.py" 2>/dev/null || true
   pkill -f "summary_agent.py" 2>/dev/null || true
   ```

3. Sende eine kurze Abschlussnachricht in Discord:
   ```bash
   echo "*(Das Abenteuer ruht. Die Agenten wurden gestoppt.)*" | python3 .claude/skills/go/scripts/send_message.py
   ```

4. Bestätige dem Nutzer welche Prozesse beendet wurden.
