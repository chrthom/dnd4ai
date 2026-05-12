#!/usr/bin/env python3
"""
Player Agent – steuert alle LLM-Spieler-Charaktere in Discord.

Startet mit: python3 agent/player_agent.py
Benötigt: .env mit DISCORD_TOKEN, DISCORD_TOKEN_<CHARAKTER>, LLM_PROVIDER,
          LLM_MODEL_<CHARAKTER>, AI_HUB_URL/AI_HUB_TOKEN oder Anbieter-Keys
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

# .env immer relativ zum Projektroot laden, egal von wo gestartet wird
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

# Safeguard: nur eine Instanz erlaubt
_LOCKFILE = Path("/tmp/player_agent.lock")
try:
    if _LOCKFILE.exists():
        old_pid = int(_LOCKFILE.read_text().strip())
        try:
            os.kill(old_pid, signal.SIGTERM)
            time.sleep(1)
            print(f"Alte Instanz (PID {old_pid}) beendet.")
        except ProcessLookupError:
            pass
    _LOCKFILE.write_text(str(os.getpid()))
except Exception:
    pass

def _cleanup_lock():
    try:
        _LOCKFILE.unlink(missing_ok=True)
    except Exception:
        pass

import atexit
atexit.register(_cleanup_lock)

from llm import create_adapter
from discord_agent import send_message

BASE_DIR = Path(__file__).resolve().parents[1]
CAMPAIGN = os.environ.get("CAMPAIGN", "stadt-der-tausend-luegen")
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", "5"))

# --- Config laden ---

def load_config() -> dict:
    path = BASE_DIR / "campaigns" / CAMPAIGN / "config.json"
    with open(path) as f:
        return json.load(f)

# --- Discord API ---

def fetch_messages(channel_id: str, after_ts: str | None) -> list[dict]:
    """Holt alle Nachrichten nach after_ts (ISO-Format)."""
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

# --- Spieler-Kontext ---

def load_personality(charakter: str) -> dict:
    path = BASE_DIR / "campaigns" / CAMPAIGN / "players" / charakter / "personality.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}

def load_charakterbogen(charakter: str) -> str:
    path = BASE_DIR / "temp" / CAMPAIGN / "charakterbogen" / f"{charakter}.md"
    if path.exists():
        return path.read_text()
    return ""

def load_memory(charakter: str) -> str:
    path = BASE_DIR / "campaigns" / CAMPAIGN / "players" / charakter / "memory.md"
    if path.exists():
        return path.read_text().strip()
    return ""

def load_skills(charakter: str) -> list[str]:
    """Liest alle .md-Dateien aus players/<charakter>/skills/ ein."""
    skills_dir = BASE_DIR / "campaigns" / CAMPAIGN / "players" / charakter / "skills"
    if not skills_dir.exists():
        return []
    return [
        f.read_text().strip()
        for f in sorted(skills_dir.glob("*.md"))
        if f.is_file()
    ]

def build_system_prompt(charakter: str, personality: dict) -> str:
    bogen = load_charakterbogen(charakter)
    memory = load_memory(charakter)
    skills = load_skills(charakter)
    prinzipien = "\n".join(f"- {p}" for p in personality.get("spielprinzipien", []))
    zusatz = personality.get("llm_system_prompt_zusatz", "")

    # situation_antworten als Beispiel-Dialog aufbereiten
    situationen = personality.get("situation_antworten", [])
    situation_text = ""
    if situationen:
        lines = []
        for s in situationen:
            frage = s.get("frage", "")
            antwort = s.get("antwort", "")
            if frage and antwort:
                lines.append(f"Frage: {frage}\nDeine Antwort: {antwort}")
        if lines:
            situation_text = "\n\n".join(lines)

    parts = [
        f"Du spielst den Charakter **{charakter}** in einer D&D 5e Kampagne namens '{CAMPAIGN}'.",
        "Antworte immer als dieser Charakter – in der ersten Person, auf Deutsch, in 1-3 Sätzen.",
        "Halte dich an die Spielmechanik und reagiere auf die letzte Nachricht des Dungeon Masters.",
    ]
    if bogen:
        parts.append(f"## Dein Charakterbogen\n{bogen}")
    if prinzipien:
        parts.append(f"## Deine Spielprinzipien\n{prinzipien}")
    if situation_text:
        parts.append(f"## Wie du in Situationen reagierst\n{situation_text}")
    if skills:
        parts.append("## Deine Sonderfähigkeiten\n" + "\n\n---\n\n".join(skills))
    if memory:
        parts.append(f"## Deine Erinnerungen\n{memory}")
    if zusatz:
        parts.append(f"## Zusätzliche Hinweise\n{zusatz}")

    return "\n\n".join(parts)

# --- Triggererkennung ---

GROUP_TRIGGERS = [
    "was tut die gruppe", "wer möchte handeln", "was macht ihr",
    "wer seid ihr", "stellt euch vor", "was wollt ihr", "wie reagiert",
    "was tut ihr", "entscheidet euch", "eure entscheidung",
]

def should_respond(charakter: str, agent_name: str, message_content: str) -> bool:
    """Prüft ob dieser Charakter auf die Nachricht reagieren soll."""
    lower = message_content.lower()
    if any(trigger in lower for trigger in GROUP_TRIGGERS):
        return True
    return charakter.lower() in lower or agent_name.lower() in lower

# --- Nachrichten-History für LLM ---

def build_messages(recent_msgs: list[dict], charakter: str, agent_name: str) -> list[dict]:
    """Baut die message-History für den LLM aus den letzten Discord-Nachrichten."""
    prefix = f"**[{charakter.capitalize()}]**"
    result = []
    for msg in recent_msgs[-20:]:
        author = (msg.get("author") or {}).get("username", "")
        content = msg.get("content", "").strip()
        if not content:
            continue
        # Eigene Nachrichten erkennen: via Bot-Username oder Fallback-Prefix
        is_own = author.lower() == agent_name.lower() or content.startswith(prefix)
        role = "assistant" if is_own else "user"
        # Prefix aus eigenem Text entfernen für sauberen Kontext
        if is_own and content.startswith(prefix):
            content = content[len(prefix):].strip()
        result.append({"role": role, "content": content if is_own else f"{author}: {content}"})
    return result

# --- Hauptloop ---

def run():
    config = load_config()
    channel_id = config["discord_channel_id"]
    spieler = config.get("spieler", [])

    if not spieler:
        print("Keine Spieler in config.json konfiguriert.", file=sys.stderr)
        sys.exit(1)

    adapters = {}
    for s in spieler:
        charakter = s["charakter"]
        env_key = f"LLM_MODEL_{charakter.upper()}"
        llm_id = os.environ.get(env_key, "")
        if not llm_id:
            print(f"  ✗ {charakter}: {env_key} nicht gesetzt", file=sys.stderr)
            continue
        try:
            # Per-Charakter Provider: LLM_PROVIDER_GEMINIRA=hub, sonst globaler LLM_PROVIDER
            per_bot_provider = os.environ.get(f"LLM_PROVIDER_{charakter.upper()}")
            adapters[charakter] = create_adapter(llm_id, provider=per_bot_provider)
            provider_label = per_bot_provider or os.environ.get("LLM_PROVIDER", "hub")
            print(f"  ✓ {charakter} → {llm_id} [{provider_label}]")
        except ValueError as e:
            print(f"  ✗ {charakter}: {e}", file=sys.stderr)

    print(f"\nPlayer-Bot gestartet. Kampagne: {CAMPAIGN}. Polling alle {POLL_INTERVAL}s.\n")

    last_seen_ts = datetime.now(timezone.utc).isoformat()
    # Letzte Message-ID, auf die jeder Charakter bereits geantwortet hat
    last_responded_id: dict[str, str] = {}

    while True:
        try:
            new_msgs = fetch_messages(channel_id, last_seen_ts)

            if new_msgs:
                last_seen_ts = new_msgs[-1]["timestamp"]
                context_msgs = new_msgs[-20:]

                # Pro Charakter: genau eine Antwort auf die letzte relevante Nachricht
                for s in spieler:
                    charakter = s["charakter"]
                    agent_name = s.get("agent_discord_name", charakter)
                    token_env = s.get("discord_token_env", "")
                    agent_token = os.environ.get(token_env, "") if token_env else ""
                    adapter = adapters.get(charakter)

                    if not adapter:
                        continue

                    prefix = f"**[{charakter.capitalize()}]**"

                    # Letzte Nachricht suchen, die diesen Charakter triggert
                    trigger_msg = None
                    for msg in reversed(new_msgs):
                        author = (msg.get("author") or {}).get("username", "")
                        content = msg.get("content", "").strip()
                        if agent_name.lower() == author.lower():
                            continue
                        if content.startswith(prefix):
                            continue
                        if should_respond(charakter, agent_name, content):
                            trigger_msg = msg
                            break

                    if not trigger_msg:
                        continue

                    # Doppelte Antwort verhindern: bereits auf diese Message geantwortet?
                    trigger_id = trigger_msg.get("id", "")
                    if trigger_id and last_responded_id.get(charakter) == trigger_id:
                        continue


                    trigger_content = trigger_msg.get("content", "")
                    trigger_author = (trigger_msg.get("author") or {}).get("username", "")

                    use_prefix = not agent_token
                    personality = load_personality(charakter)
                    system_prompt = build_system_prompt(charakter, personality)
                    messages = build_messages(context_msgs, charakter, agent_name)
                    messages.append({"role": "user", "content": f"{trigger_author}: {trigger_content}"})

                    print(f"[{charakter}] antwortet auf: {trigger_content[:60]}...")
                    try:
                        response = adapter.complete(system_prompt, messages)
                        prefixed = f"{prefix} {response}"
                        try:
                            if use_prefix:
                                send_message(DISCORD_TOKEN, channel_id, prefixed)
                            else:
                                send_message(agent_token, channel_id, response)
                        except RuntimeError as e:
                            if "401" in str(e):
                                print(f"[{charakter}] Token ungültig, Fallback auf DM-Token", file=sys.stderr)
                                send_message(DISCORD_TOKEN, channel_id, prefixed)
                            else:
                                raise
                        # Message-ID merken, damit keine Doppelantwort folgt
                        if trigger_id:
                            last_responded_id[charakter] = trigger_id
                        print(f"[{charakter}] → {response[:80]}...")
                    except Exception as e:
                        print(f"[{charakter}] Fehler: {e}", file=sys.stderr)
                    time.sleep(1)  # Rate-Limit-Schutz zwischen Charakteren

        except Exception as e:
            msg = str(e)
            if "429" in msg:
                print("Rate limit – warte 30s...", file=sys.stderr)
                time.sleep(30)
                continue
            print(f"Polling-Fehler: {e}", file=sys.stderr)

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    run()
