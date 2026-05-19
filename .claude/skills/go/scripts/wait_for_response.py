#!/usr/bin/env python3
"""
Polling mit Timeout-Eskalation für go/SKILL.md.

Pollt alle 5 Sekunden auf neue Discord-Nachrichten (via fetch_messages.py).
Beendet sich nach maximal 60 Sekunden, um Claude zu wecken – auch ohne Antwort.

Exit-Codes:
  0  Neue Spielernachricht angekommen (chat.md wurde aktualisiert)
  2  60 Sekunden abgelaufen, noch keine Antwort – erster Hinweis fällig (Soft Nudge)
  3  60 Sekunden abgelaufen, noch keine Antwort – direkte Ansprache fällig (Hard Nudge)

Eskalations-State wird in temp/$CAMPAIGN/nudge_count.txt gespeichert.
Beim ersten Timeout → count=1 → Exit 2 (Soft Nudge nach 1 Minute).
Bei jedem weiteren Timeout → count≥2 → Exit 3 (Hard Nudge nach 2+ Minuten).
Sobald eine Antwort eintrifft, wird nudge_count.txt gelöscht (Reset).
"""
import os
import sys
import subprocess
import time
from pathlib import Path

# .env vom Projektroot laden
_root = Path(__file__).resolve().parents[4]
_env_file = _root / '.env'
if _env_file.exists():
    for _line in _env_file.read_text().splitlines():
        if _line.strip() and not _line.startswith('#') and '=' in _line:
            _k, _v = _line.split('=', 1)
            os.environ.setdefault(_k.strip(), _v.strip())

CAMPAIGN = os.environ.get('CAMPAIGN', 'stadt-der-tausend-luegen')
BASE_DIR = Path(__file__).resolve().parents[4]
CHAT_DIR = BASE_DIR / 'temp' / CAMPAIGN
NUDGE_COUNT_FILE = CHAT_DIR / 'nudge_count.txt'
FETCH_SCRIPT = Path(__file__).parent / 'fetch_messages.py'

SOFT_TIMEOUT = 60   # Sekunden bis zum ersten Hinweis (Soft Nudge)
POLL_INTERVAL = 5   # Sekunden zwischen Discord-Polls


def read_nudge_count() -> int:
    try:
        return int(NUDGE_COUNT_FILE.read_text().strip())
    except Exception:
        return 0


def write_nudge_count(count: int) -> None:
    NUDGE_COUNT_FILE.write_text(str(count))


def reset_nudge_count() -> None:
    try:
        NUDGE_COUNT_FILE.unlink()
    except FileNotFoundError:
        pass


def main():
    deadline = time.monotonic() + SOFT_TIMEOUT

    while time.monotonic() < deadline:
        result = subprocess.run(
            [sys.executable, str(FETCH_SCRIPT)],
            capture_output=True,
        )
        if result.returncode == 0:
            reset_nudge_count()
            sys.exit(0)

        remaining = deadline - time.monotonic()
        if remaining > 0:
            time.sleep(min(POLL_INTERVAL, remaining))

    # Timeout abgelaufen – Eskalationsstufe bestimmen
    count = read_nudge_count() + 1
    write_nudge_count(count)

    if count == 1:
        sys.exit(2)  # Soft Nudge: freundliche Erinnerung
    else:
        sys.exit(3)  # Hard Nudge: direkte Ansprache mit Spielernamen


if __name__ == '__main__':
    main()
