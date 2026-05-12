#!/usr/bin/env bash
# Beendet alle laufenden D&D-Agenten.

stop_agent() {
  local name="$1"
  local lockfile="$2"
  if [ -f "$lockfile" ]; then
    local pid
    pid=$(cat "$lockfile")
    if kill -0 "$pid" 2>/dev/null; then
      kill "$pid"
      echo "  $name (PID $pid) beendet."
    else
      echo "  $name nicht mehr aktiv."
    fi
    rm -f "$lockfile"
  else
    echo "  $name: kein Lockfile gefunden."
  fi
}

echo "=== D&D Agent Shutdown ==="
stop_agent "Player Agent"  /tmp/player_agent.lock
stop_agent "DM Agent"      /tmp/dm_agent.lock
echo "Fertig."
