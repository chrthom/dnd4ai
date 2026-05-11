import json
import urllib.request
import urllib.error


def send_message(token: str, channel_id: str, content: str) -> None:
    """Postet eine Nachricht als Bot mit eigenem Token. Splittet bei >2000 Zeichen."""
    chunks = [content[i:i+2000] for i in range(0, len(content), 2000)]
    for chunk in chunks:
        payload = json.dumps({"content": chunk}).encode()
        req = urllib.request.Request(
            f"https://discord.com/api/v10/channels/{channel_id}/messages",
            data=payload,
            headers={
                "Authorization": f"Bot {token}",
                "Content-Type": "application/json",
                "User-Agent": "DiscordBot (https://example.com, 1.0)",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req) as resp:
                if resp.status not in (200, 204):
                    raise RuntimeError(f"Discord API returned {resp.status}")
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"Discord API error {e.code}: {e.read().decode()}") from e
