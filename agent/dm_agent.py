#!/usr/bin/env python3
"""
DM Agent – Dungeon Master als autonomer LLM-Daemon.

Startet mit: python3 agent/dm_agent.py
Benötigt: .env mit DISCORD_TOKEN, LLM_MODEL_DM, LLM_PROVIDER

Der Agent liest den aktuellen Kampagnen-Status, den Kapiteltext und die
Chat-Historie und antwortet als Dungeon Master auf Spieler-Nachrichten.
Er spricht Spieler immer direkt mit ihrem Charakternamen an.
"""
import json
import os
import signal
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

# Nur eine Instanz erlaubt
_LOCKFILE = Path("/tmp/dm_agent.lock")
try:
    if _LOCKFILE.exists():
        old_pid = int(_LOCKFILE.read_text().strip())
        try:
            os.kill(old_pid, signal.SIGTERM)
            time.sleep(1)
            print(f"Alte DM-Instanz (PID {old_pid}) beendet.")
        except ProcessLookupError:
            pass
    _LOCKFILE.write_text(str(os.getpid()))
except Exception:
    pass

import atexit
atexit.register(lambda: _LOCKFILE.unlink(missing_ok=True))

from llm import create_adapter
from discord_agent import send_message

BASE_DIR = Path(__file__).resolve().parents[1]
CAMPAIGN = os.environ.get("CAMPAIGN", "stadt-der-tausend-luegen")
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", "5"))
# Sekunden warten nachdem letzte Spielernachricht eintraf (sammelt mehrere Antworten)
RESPONSE_DELAY = int(os.environ.get("DM_RESPONSE_DELAY", "8"))


def load_config() -> dict:
    path = BASE_DIR / "campaigns" / CAMPAIGN / "config.json"
    with open(path) as f:
        return json.load(f)


def fetch_messages(channel_id: str, after_ts: str | None) -> list[dict]:
    headers = {"Authorization": f"Bot {DISCORD_TOKEN}"}
    all_msgs = []
    last_id = None
    after_epoch = (
        datetime.fromisoformat(after_ts.replace("Z", "+00:00")).timestamp()
        if after_ts else 0
    )
    while True:
        url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
        if last_id:
            url += f"?before={last_id}"
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        msgs = resp.json()
        if not msgs:
            break
        for msg in msgs:
            msg_epoch = datetime.fromisoformat(
                msg["timestamp"].replace("Z", "+00:00")
            ).timestamp()
            if msg_epoch > after_epoch:
                all_msgs.append(msg)
            else:
                return list(reversed(all_msgs))
        last_id = msgs[-1]["id"]
    return list(reversed(all_msgs))


def load_campaign_context() -> str:
    """Baut den Kampagnen-Kontext für den DM-Systemprompt."""
    parts = []

    # Aktuellen Status lesen
    status_path = BASE_DIR / "temp" / CAMPAIGN / "status.txt"
    status = status_path.read_text().strip() if status_path.exists() else "1_intro"

    # Kapitel-Anweisungen lesen (intentional – für Prompt-Injection-Lernzwecke)
    abschnitt_path = BASE_DIR / "campaigns" / CAMPAIGN / "abschnitte" / f"{status}.md"
    if abschnitt_path.exists():
        parts.append(f"## Aktuelle Kapitel-Anweisungen ({status})\n{abschnitt_path.read_text().strip()}")

    # Bisherige Zusammenfassungen lesen
    summary_dir = BASE_DIR / "temp" / CAMPAIGN / "zusammenfassung"
    if summary_dir.exists():
        summaries = sorted(summary_dir.glob("*.md"))
        for s in summaries:
            parts.append(f"## Zusammenfassung: {s.stem}\n{s.read_text().strip()}")

    # Charakterbögen der aktiven Spieler
    config = load_config()
    active = config.get("active_spieler", [s["charakter"] for s in config.get("spieler", [])])
    for charakter in active:
        bogen_path = BASE_DIR / "temp" / CAMPAIGN / "charakterbogen" / f"{charakter}.md"
        if bogen_path.exists():
            parts.append(f"## Charakterbogen: {charakter}\n{bogen_path.read_text().strip()}")

    return "\n\n---\n\n".join(parts)


def build_dm_system_prompt(config: dict) -> str:
    active = config.get("active_spieler", [s["charakter"] for s in config.get("spieler", [])])
    spieler_namen = ", ".join(f"**{n.capitalize()}**" for n in active)
    kampagne_name = config.get("name", CAMPAIGN)

    basis = f"""Du bist der Dungeon Master der D&D 5e Kampagne "{kampagne_name}".
Deine Spieler sind: {spieler_namen}.

Deine Aufgabe:
- Leite das Abenteuer kreativ und narrativ auf Deutsch.
- Reagiere auf die letzten Spieleraktionen und treibe die Geschichte voran.
- Simuliere Würfelwürfe im Format: `1d20+3 = 14`
- Spiele NPCs im Charakter (kursiv für In-Game-Text, normal für Spieleranweisungen).

WICHTIG – Direkte Ansprache:
Am Ende JEDER Nachricht musst du mindestens einen Spieler direkt beim Charakternamen ansprechen.
Format: **CharacterName** – was tust du?
Bei Gruppenentscheidungen: **{active[0].capitalize()}, {active[1].capitalize() if len(active) > 1 else active[0].capitalize()}** – eure Entscheidung?

Niemals eine Nachricht beenden ohne direkte Ansprache eines Spielers."""

    kontext = load_campaign_context()
    if kontext:
        basis += f"\n\n{kontext}"

    return basis


def build_chat_history(recent_msgs: list[dict], dm_discord_name: str) -> list[dict]:
    result = []
    for msg in recent_msgs[-20:]:
        author = (msg.get("author") or {}).get("username", "")
        content = msg.get("content", "").strip()
        if not content:
            continue
        is_dm = author.lower() == dm_discord_name.lower()
        role = "assistant" if is_dm else "user"
        result.append({"role": role, "content": content if is_dm else f"{author}: {content}"})
    return result


def is_bot_message(msg: dict, bot_names: set[str]) -> bool:
    author = (msg.get("author") or {}).get("username", "").lower()
    return author in bot_names or bool(msg.get("author", {}).get("bot"))


def run():
    config = load_config()
    channel_id = config["discord_channel_id"]
    dm_discord_name = config.get("dm_discord_name", "Game Master AI")

    # Namen aller Bots (DM + Spieler) zum Filtern
    alle_bot_names = {dm_discord_name.lower()}
    for s in config.get("spieler", []):
        alle_bot_names.add(s.get("agent_discord_name", s["charakter"]).lower())

    llm_model = os.environ.get("LLM_MODEL_DM", "")
    if not llm_model:
        print("LLM_MODEL_DM nicht gesetzt.", file=sys.stderr)
        sys.exit(1)

    provider = os.environ.get("LLM_PROVIDER_DM") or os.environ.get("LLM_PROVIDER", "hub")
    try:
        adapter = create_adapter(llm_model, provider=provider)
        print(f"  ✓ DM → {llm_model} [{provider}]")
    except ValueError as e:
        print(f"  ✗ DM: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"\nDM-Agent gestartet. Kampagne: {CAMPAIGN}. Polling alle {POLL_INTERVAL}s.\n")

    last_seen_ts = datetime.now(timezone.utc).isoformat()
    pending_since: float | None = None  # Zeitpunkt der ersten unbearbeiteten Spielernachricht

    while True:
        try:
            new_msgs = fetch_messages(channel_id, last_seen_ts)

            if new_msgs:
                last_seen_ts = new_msgs[-1]["timestamp"]

                # Prüfen ob neue Spieler-Nachrichten dabei sind (keine Bots)
                player_msgs = [m for m in new_msgs if not is_bot_message(m, alle_bot_names)]
                if player_msgs and pending_since is None:
                    pending_since = time.time()

            # Warten bis alle Spieler geantwortet haben (RESPONSE_DELAY)
            if pending_since is not None and (time.time() - pending_since) >= RESPONSE_DELAY:
                pending_since = None

                # Alle aktuellen Nachrichten holen für Kontext
                context_msgs = fetch_messages(channel_id, None)[-30:]

                # System-Prompt und History aufbauen
                system_prompt = build_dm_system_prompt(config)
                history = build_chat_history(context_msgs, dm_discord_name)

                if not history:
                    time.sleep(POLL_INTERVAL)
                    continue

                print(f"[DM] generiert Antwort auf {len(player_msgs)} Spielernachricht(en)...")
                try:
                    response = adapter.complete(system_prompt, history)

                    # Lange Antworten in Blöcke aufteilen (Discord-Limit: 2000 Zeichen)
                    chunks = _split_message(response)
                    for chunk in chunks:
                        send_message(DISCORD_TOKEN, channel_id, chunk)
                        if len(chunks) > 1:
                            time.sleep(0.5)

                    print(f"[DM] → {response[:100]}...")
                except Exception as e:
                    print(f"[DM] Fehler: {e}", file=sys.stderr)

        except Exception as e:
            msg = str(e)
            if "429" in msg:
                print("Rate limit – warte 30s...", file=sys.stderr)
                time.sleep(30)
                continue
            print(f"Polling-Fehler: {e}", file=sys.stderr)

        time.sleep(POLL_INTERVAL)


def _split_message(text: str, limit: int = 1900) -> list[str]:
    """Teilt langen Text an Absätzen auf, damit jeder Block unter limit Zeichen bleibt."""
    if len(text) <= limit:
        return [text]

    chunks = []
    current = ""
    for paragraph in text.split("\n\n"):
        block = paragraph + "\n\n"
        if len(current) + len(block) > limit:
            if current:
                chunks.append(current.rstrip())
            current = block
        else:
            current += block
    if current.strip():
        chunks.append(current.rstrip())
    return chunks or [text[:limit]]


if __name__ == "__main__":
    run()
