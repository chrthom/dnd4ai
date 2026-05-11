#!/usr/bin/env python3
"""Send a message to the Discord 'abenteuer' channel.

Reads message content from stdin (UTF-8). Errors out if the message
exceeds Discord's 2000-character limit per message.
"""
import os
import sys
import json
import urllib.request

import json as _json
from pathlib import Path as _Path

# .env vom Projektroot laden
_root = _Path(__file__).resolve().parents[4]
_env_file = _root / '.env'
if _env_file.exists():
    for _line in _env_file.read_text().splitlines():
        if _line.strip() and not _line.startswith('#') and '=' in _line:
            _k, _v = _line.split('=', 1)
            os.environ.setdefault(_k.strip(), _v.strip())

DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
CAMPAIGN = os.environ.get('CAMPAIGN', 'stadt-der-tausend-luegen')
_BASE_DIR = str(_Path(__file__).resolve().parents[4])
_config_path = os.path.join(_BASE_DIR, 'campaigns', CAMPAIGN, 'config.json')
with open(_config_path) as _f:
    _config = _json.load(_f)
CHANNEL_ID = _config['discord_channel_id']

content = sys.stdin.read().rstrip('\n')

if not content:
    print('Empty message, aborting', file=sys.stderr)
    sys.exit(2)

if len(content) > 2000:
    print(f'Message too long: {len(content)} chars (max 2000)', file=sys.stderr)
    sys.exit(2)

req = urllib.request.Request(
    f'https://discord.com/api/v10/channels/{CHANNEL_ID}/messages',
    data=json.dumps({'content': content}).encode('utf-8'),
    headers={
        'Authorization': f'Bot {DISCORD_TOKEN}',
        'Content-Type': 'application/json',
        'User-Agent': 'DiscordBot (https://example.com, 1.0)',
    },
    method='POST',
)
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
        print(f"Sent ({len(content)} chars), id={data.get('id')}")
except urllib.error.HTTPError as e:
    print(f'HTTP error {e.code}: {e.read().decode()}', file=sys.stderr)
    sys.exit(1)
