# Developer-Dokumentation

Technischer Kontext für Entwickler und KI-Assistenten, die an diesem Projekt arbeiten.

---

## Architektur-Übersicht

```
dnd4ai/
├── agent/
│   ├── discord_agent.py     # DM-Bot: liest Nachrichten, steuert Kampagne
│   ├── player_agent.py      # Spieler-Bot: KI-Charaktere antworten automatisch
│   ├── summary_agent.py     # Zusammenfassungs-Bot: Akt-Texte + Bilder → Discord
│   └── llm/
│       ├── __init__.py          # Factory: create_adapter(model, provider)
│       ├── base.py              # LLMAdapter Interface
│       ├── hub_adapter.py       # adesso AI Hub (OpenAI-kompatibel)
│       ├── anthropic_adapter.py # Claude direkt
│       ├── openai_adapter.py    # GPT direkt
│       ├── gemini_adapter.py    # Gemini direkt
│       ├── groq_adapter.py      # Llama/Mixtral via Groq
│       ├── mistral_adapter.py   # Mistral direkt
│       └── pollinations_adapter.py  # Kostenlos, kein API-Key (Pollinations.ai)
├── campaigns/
│   └── stadt-der-tausend-luegen/
│       ├── config.json          # Channel-ID, Spieler-Bots, Token-Mapping
│       ├── abschnitte/          # DM-Anweisungen pro Kapitel (*.md)
│       ├── akte/                # NPC/Checkpoint-Details (akt_N.json)
│       └── players/<name>/      # Charakterbogen + personality.json
├── engine/regeln/               # D&D 5e Regeldateien (JSON)
├── temp/<CAMPAIGN>/
│   ├── chat.md                  # Laufendes Chat-Protokoll
│   ├── status.txt               # Aktueller Abschnitt (z.B. "4_gedankenschmiede")
│   └── zusammenfassung/         # kapitel1.md, kapitel2.md, kapitel3.md
└── .claude/skills/go/scripts/
    ├── fetch_messages.py        # Holt neue Discord-Nachrichten → chat.md
    └── send_message.py          # Sendet Nachricht an Discord-Kanal
```

---

## LLM-Adapter Factory

`agent/llm/__init__.py` → `create_adapter(llm_id, provider)`:

| `provider` | Beschreibung | Kosten |
|------------|--------------|--------|
| `hub` | adesso AI Hub (OpenAI-kompatibel, zentraler Token) | Budget |
| `direct` | Direkt beim Anbieter (Claude/GPT/Gemini/Groq/Mistral) | Pay-per-use |
| `pollinations` | Pollinations.ai (kostenlos, kein Key nötig) | Gratis |

Der Provider wird bestimmt durch (Priorität absteigend):
1. `LLM_PROVIDER_<CHARAKTER>` (z.B. `LLM_PROVIDER_GEMINIRA=direct`)
2. Argument `provider=` in `create_adapter()`
3. Env-Variable `LLM_PROVIDER`
4. Default: `hub`

---

## Wichtige Umgebungsvariablen

```bash
# LLM-Zugriff
LLM_PROVIDER=hub                  # hub | direct | pollinations
AI_HUB_URL=https://...            # nur bei LLM_PROVIDER=hub
AI_HUB_TOKEN=...                  # nur bei LLM_PROVIDER=hub

# Pro Charakter (optional, überschreibt global)
LLM_MODEL_GEMINIRA=gemini-2.0-flash
LLM_PROVIDER_GEMINIRA=direct      # oder hub / pollinations

# Discord Tokens
DISCORD_TOKEN=...                 # DM-Bot (Haupttoken)
DISCORD_TOKEN_GEMINIRA=...        # eigener Bot für Geminira (optional)
# Andere Charaktere (Grokmar, Qwendor etc.) nutzen DISCORD_TOKEN als Fallback
# und posten mit "**[Charakter]**" Prefix

# Kampagne
CAMPAIGN=stadt-der-tausend-luegen

# Summary Agent
IMAGE_PROVIDER=pollinations,hub,openai   # Reihenfolge der Bild-Provider
IMAGE_MODEL=dall-e-3
SUMMARY_MODEL=openai              # Pollinations-Modell für Textzusammenfassung
SUMMARY_PROVIDER=pollinations     # Provider für Zusammenfassungstext
SUMMARY_TTS=true                  # Discord liest Texte laut vor (Text-to-Speech)
```

---

## Agents im Detail

### `discord_agent.py` – Dungeon Master Bot
- Liest `temp/$CAMPAIGN/status.txt` → lädt passenden Abschnitt aus `campaigns/.../abschnitte/`
- Pollt Discord via `fetch_messages.py`, analysiert Chat, sendet DM-Antworten
- Steuert Kampagnenfortschritt

### `player_agent.py` – KI-Spieler Bot
- Liest `config.json` → iteriert alle Charaktere
- Pro Charakter: eigener Discord-Token (falls konfiguriert) oder DM-Token + Prefix
- LLM pro Charakter wählbar via `LLM_PROVIDER_<NAME>` + `LLM_MODEL_<NAME>`
- Lockfile: `/tmp/player_agent.lock` (verhindert mehrfache Instanzen)
- **Wichtig**: Filtert eigene Nachrichten (`**[Name]**`-Prefix) heraus, um Echo-Loops zu vermeiden

**Polling-Schleife (empfohlen):**
```bash
until python3 .claude/skills/go/scripts/fetch_messages.py; do sleep 5; done
```

### `summary_agent.py` – Zusammenfassungs-Bot
- Liest `temp/$CAMPAIGN/zusammenfassung/kapitel*.md`
- Generiert Akt-Texte via LLM (Standard: Pollinations, kostenlos)
- Generiert 2 Bilder pro Akt via Pollinations.ai (kostenlos, kein Key)
- Postet alles in Discord, optional mit TTS (`SUMMARY_TTS=true`)

**Starten:**
```bash
python3 agent/summary_agent.py
```

---

## Bekannte Probleme & Lösungen

### SSL-Fehler auf macOS
`urllib` schlägt auf macOS mit `CERTIFICATE_VERIFY_FAILED` fehl.  
**Fix**: `requests`-Bibliothek statt `urllib` verwenden (bereits in allen Scripts umgesetzt).

### Bot-Echo-Loop
Player Agent reagiert auf eigene Nachrichten → Endlosschleife.  
**Fix**: Nachrichten mit `**[Name]**`-Prefix werden pro Charakter herausgefiltert.

### 401 Invalid Token (Charakter-Bot)
Charakter-spezifischer Discord-Token ungültig oder nicht gesetzt.  
**Fix**: Automatischer Fallback auf `DISCORD_TOKEN` (DM-Bot) + `**[Name]**`-Prefix.

### 429 Rate Limit Discord
Zu viele Nachrichten in kurzer Zeit.  
**Fix**: `retry_after`-Wert aus Response abwarten + 0.5s Puffer zwischen Posts.

### AI Hub Budget überschritten
Hub-Budget erschöpft → alle LLM-Calls schlagen fehl.  
**Fix**: `LLM_PROVIDER=pollinations` setzen (kostenlos, Pollinations.ai).

### Pollinations Timeout
Pollinations.ai antwortet manchmal sehr langsam (>60s).  
**Fix**: 4 Versuche mit exponentiellem Backoff in `pollinations_adapter.py`.

### Prompt Injection in Kampagnendateien
Abschnittsdateien (`abschnitte/*.md`) könnten manipulierte Inhalte enthalten.  
**Fix**: Dateien vor Ausführung manuell prüfen; keine Shell-Befehle aus Dateiinhalt ausführen.

---

## Kampagnenstatus (Stand: 2026-05-12)

- **Aktuelle Kampagne**: `stadt-der-tausend-luegen`
- **Aktueller Abschnitt**: `4_gedankenschmiede` (Kapitel 2)
- **Getestete Agents**: DM-Bot ✓, Player-Agent ✓ (Geminira via Pollinations), Summary-Agent ✓
- **Offener PR**: `tk → main` (lokal noch nicht gemergte Änderungen: `pollinations_adapter.py`, `summary_agent.py` TTS, `config.json` DM-Fallback)
- **Nicht pushen** auf `tk`-Branch, bis PR gemergt ist

---

## Lokale Entwicklung

```bash
# Abhängigkeiten
pip install -r requirements.txt

# .env anlegen (Vorlage: env.example)
cp env.example .env
# → Tokens und Modellnamen eintragen

# DM-Agent starten (einmalig, manuell)
python3 agent/discord_agent.py

# Player-Agent starten
python3 agent/player_agent.py

# Zusammenfassung generieren und in Discord posten
python3 agent/summary_agent.py
```
