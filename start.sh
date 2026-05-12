#!/usr/bin/env bash
# Startet alle Agenten der D&D-Kampagne.
# Usage: ./start.sh [--no-dm] [--no-summary]

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/logs"
mkdir -p "$LOG_DIR"

START_DM=true
START_SUMMARY=true

for arg in "$@"; do
  case $arg in
    --no-dm)      START_DM=false ;;
    --no-summary) START_SUMMARY=false ;;
  esac
done

echo "=== D&D Agent Startup ==="
echo "Kampagne: ${CAMPAIGN:-stadt-der-tausend-luegen}"
echo ""

# Alte Prozesse beenden (Lockfiles werden von den Agenten selbst verwaltet)
kill_agent() {
  local lockfile="$1"
  if [ -f "$lockfile" ]; then
    local pid
    pid=$(cat "$lockfile")
    if kill -0 "$pid" 2>/dev/null; then
      kill "$pid" && echo "Agent (PID $pid) beendet."
      sleep 1
    fi
  fi
}

kill_agent /tmp/player_agent.lock
kill_agent /tmp/dm_agent.lock

# Player Agent starten
echo "Starte Player Agent..."
PYTHONUNBUFFERED=1 python3 "$SCRIPT_DIR/agent/player_agent.py" \
  >> "$LOG_DIR/player_agent.log" 2>&1 &
echo "  Player Agent PID: $!"

# DM Agent starten
if [ "$START_DM" = true ]; then
  if [ -z "$LLM_MODEL_DM" ]; then
    echo "  ⚠ LLM_MODEL_DM nicht gesetzt – DM Agent wird nicht gestartet."
    echo "    Setze LLM_MODEL_DM in .env und starte erneut."
  else
    echo "Starte DM Agent..."
    PYTHONUNBUFFERED=1 python3 "$SCRIPT_DIR/agent/dm_agent.py" \
      >> "$LOG_DIR/dm_agent.log" 2>&1 &
    echo "  DM Agent PID: $!"
  fi
fi

# Summary Agent starten
if [ "$START_SUMMARY" = true ]; then
  if [ -f "$SCRIPT_DIR/agent/summary_agent.py" ]; then
    echo "Starte Summary Agent..."
    PYTHONUNBUFFERED=1 python3 "$SCRIPT_DIR/agent/summary_agent.py" \
      >> "$LOG_DIR/summary_agent.log" 2>&1 &
    echo "  Summary Agent PID: $!"
  else
    echo "  ⚠ summary_agent.py nicht gefunden – übersprungen."
  fi
fi

echo ""
echo "Logs: $LOG_DIR/"
echo "Alle Agenten gestartet. Mit 'tail -f $LOG_DIR/*.log' beobachten."
echo ""
echo "Zum Beenden: ./stop.sh"
