#!/usr/bin/env python3
"""
Fetch Messages Skript für go/SKILL.md
Führt Schritte 1-3 aus:
1. Lese temp/chat.md und ermittle den Zeitstempel der letzten Nachricht.
2. Nutze die Discord API, um alle Nachrichten zu holen, die nach dem Zeitstempel gesendet wurden.
3. Speichere die neuen Nachrichten inkl. Verfasser und Zeitstempel in temp/chat.md ab.
"""
import os
import sys
import requests
from datetime import datetime, timezone

DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
CHANNEL_ID = '1499794887011340392'
BASE_DIR = '/home/christopher/Dokumente/dnd4ai'


def get_last_timestamp():
    """Liest den letzten Zeitstempel aus chat.md"""
    chat_path = f'{BASE_DIR}/temp/chat.md'
    if not os.path.exists(chat_path):
        return None
    with open(chat_path, 'r') as f:
        for line in f:
            if line.startswith('## Last Updated:'):
                return line.split(': ')[1].strip()
    return None


def format_timestamp(ts):
    """Formatiert Discord-Timestamp für chat.md (2026-05-01T13:52:03.954Z)"""
    if '+' in ts:
        ts = ts.replace('+00:00', 'Z')
    if '.' not in ts:
        ts = ts + '.000Z'
    else:
        parts = ts.split('.')
        ts = parts[0] + '.' + parts[1][:3] + 'Z'
    return ts


def fetch_new_messages(after_timestamp):
    """Holt alle Nachrichten nach dem gegebenen Zeitstempel"""
    after = datetime.fromisoformat(after_timestamp.replace('Z', '+00:00')).timestamp()
    
    all_messages = []
    last_id = None
    
    while True:
        url = f'https://discord.com/api/v10/channels/{CHANNEL_ID}/messages'
        if last_id:
            url += f'?before={last_id}'
        
        response = requests.get(url, headers={'Authorization': f'Bot {DISCORD_TOKEN}'})
        if response.status_code != 200:
            print(f"Fehler beim Abrufen: {response.status_code} - {response.text}", file=sys.stderr)
            break
            
        messages = response.json()
        
        if not messages:
            break
        
        for msg in messages:
            msg_time = datetime.fromisoformat(msg['timestamp'].replace('Z', '+00:00')).timestamp()
            if msg_time > after:
                all_messages.append(msg)
            else:
                # Nachrichten sind chronologisch absteigend
                return all_messages
        
        last_id = messages[-1]['id']
    
    return all_messages


def append_to_chat(msg_dict):
    """Fügt eine Nachricht an chat.md an und aktualisiert Last Updated"""
    timestamp = format_timestamp(msg_dict['timestamp'])
    author = msg_dict['author']['username']
    content = msg_dict['content']
    
    chat_path = f'{BASE_DIR}/temp/chat.md'
    
    with open(chat_path, 'r') as f:
        file_content = f.read()
    
    # Füge neue Nachricht hinzu
    new_entry = f"\n---\n\n### {timestamp} - {author}\n\`\`\`\n{content}\n\`\`\`\n"
    file_content = file_content.rstrip() + new_entry
    
    # Aktualisiere Last Updated
    file_content = file_content.replace(
        '## Last Updated: ' + get_last_timestamp(),
        f'## Last Updated: {timestamp}'
    )
    
    with open(chat_path, 'w') as f:
        f.write(file_content)


def main():
    """Hauptfunktion - führt Schritte 1-3 aus"""
    last_ts = get_last_timestamp()
    
    if not last_ts:
        print("Kein Last Updated Zeitstempel in chat.md gefunden.", file=sys.stderr)
        sys.exit(1)
    
    print(f"Letzter Zeitstempel: {last_ts}", flush=True)
    
    new_msgs = fetch_new_messages(last_ts)
    
    if new_msgs:
        print(f"Gefunden: {len(new_msgs)} neue Nachricht(en)", flush=True)
        for msg in reversed(new_msgs):  # Älteste zuerst
            append_to_chat(msg)
            print(f"  - {msg['timestamp']} von {msg['author']['username']}: {msg['content'][:50]}...")
    else:
        print("Keine neuen Nachrichten.", flush=True)
    
    sys.exit(0)


if __name__ == '__main__':
    main()
