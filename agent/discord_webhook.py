import json
import urllib.request
import urllib.error


def post(webhook_url: str, username: str, content: str) -> None:
    """Post a message via Discord webhook, splitting if over 2000 chars."""
    chunks = [content[i:i+2000] for i in range(0, len(content), 2000)]
    for chunk in chunks:
        payload = json.dumps({"username": username, "content": chunk}).encode()
        req = urllib.request.Request(
            webhook_url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req) as resp:
                if resp.status not in (200, 204):
                    raise RuntimeError(f"Webhook returned {resp.status}")
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"Webhook error {e.code}: {e.read().decode()}") from e
