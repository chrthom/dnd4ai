#!/usr/bin/env python3
"""
Player Agent – steuert alle LLM-Spieler-Charaktere in Discord.

Startet mit: python3 agent/player_agent.py
Benötigt: .env mit DISCORD_TOKEN, DISCORD_TOKEN_<CHARAKTER>, LLM_PROVIDER,
          LLM_MODEL_<CHARAKTER>, AI_HUB_URL/AI_HUB_TOKEN oder Anbieter-Keys
"""
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

# .env immer relativ zum Projektroot laden, egal von wo gestartet wird
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

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

GROUP_TRIGGERS = ["was tut die gruppe", "wer möchte handeln", "was macht ihr"]

def should_respond(charakter: str, agent_name: str, message_content: str) -> bool:
    """Prüft ob dieser Charakter auf die Nachricht reagieren soll."""
    lower = message_content.lower()
    if any(trigger in lower for trigger in GROUP_TRIGGERS):
        return True
    return charakter.lower() in lower or agent_name.lower() in lower

# --- Nachrichten-History für LLM ---

def build_messages(recent_msgs: list[dict], charakter: str) -> list[dict]:
    """Baut die message-History für den LLM aus den letzten Discord-Nachrichten."""
    result = []
    for msg in recent_msgs[-20:]:  # max. 20 Nachrichten Kontext
        author = (msg.get("author") or {}).get("username", "")
        content = msg.get("content", "").strip()
        if not content:
            continue
        # Eigene Nachrichten als "assistant", alle anderen als "user"
        role = "assistant" if author.lower() == charakter.lower() else "user"
        result.append({"role": role, "content": f"{author}: {content}"})
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
            adapters[charakter] = create_adapter(llm_id)
            print(f"  ✓ {charakter} → {llm_id}")
        except ValueError as e:
            print(f"  ✗ {charakter}: {e}", file=sys.stderr)

    print(f"\nPlayer-Bot gestartet. Kampagne: {CAMPAIGN}. Polling alle {POLL_INTERVAL}s.\n")

    last_seen_ts = datetime.now(timezone.utc).isoformat()

    while True:
        try:
            new_msgs = fetch_messages(channel_id, last_seen_ts)

            if new_msgs:
                last_seen_ts = new_msgs[-1]["timestamp"]

                for msg in new_msgs:
                    content = msg.get("content", "")
                    author = (msg.get("author") or {}).get("username", "")

                    if msg.get("author", {}).get("bot"):
                        continue

                    for s in spieler:
                        charakter = s["charakter"]
                        agent_name = s.get("agent_discord_name", charakter)
                        token_env = s.get("discord_token_env", "")
                        agent_token = os.environ.get(token_env, "") if token_env else ""
                        adapter = adapters.get(charakter)

                        if not adapter or not agent_token:
                            continue
                        if not should_respond(charakter, agent_name, content):
                            continue

                        personality = load_personality(charakter)
                        system_prompt = build_system_prompt(charakter, personality)

                        context_msgs = fetch_messages(channel_id, None)[-20:]
                        messages = build_messages(context_msgs, charakter)
                        messages.append({"role": "user", "content": f"{author}: {content}"})

                        print(f"[{charakter}] antwortet auf: {content[:60]}...")
                        try:
                            response = adapter.complete(system_prompt, messages)
                            send_message(agent_token, channel_id, response)
                            print(f"[{charakter}] → {response[:80]}...")
                        except Exception as e:
                            print(f"[{charakter}] Fehler: {e}", file=sys.stderr)

        except Exception as e:
            print(f"Polling-Fehler: {e}", file=sys.stderr)

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    run()
