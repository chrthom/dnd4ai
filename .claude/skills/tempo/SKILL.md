---
name: tempo
description: Beschleunigt die Story, wenn die Zeit knapp wird. Der DM erfindet NPC-Aktionen, Umgebungsereignisse und Plotbeschleuniger, um die Gruppe schnell zum nächsten Checkpoint zu bringen – ohne auf Spielerantworten zu warten. Wird nur auf expliziten Nutzeraufruf gestartet – niemals automatisch durch die KI.
---

## Zweck

Dieser Skill wird genutzt, wenn die Spielsitzung zeitlich unter Druck steht und die Gruppe zu langsam vorankommt. Der DM übernimmt die Initiative und treibt die Geschichte aktiv vorwärts, indem er Ereignisse erfindet, die die Gruppe zur nächsten Szene oder zum nächsten Checkpoint drängen.

**Wichtig**: Spieler-Autonomie bleibt erhalten – die Gruppe trifft weiterhin Entscheidungen, aber Zögern oder Unentschlossenheit wird durch In-World-Druck aufgelöst, nicht durch Warten.

## Vorbereitung

1. Lese `temp/$CAMPAIGN/status.txt` – aktueller Abschnitt
2. Lese `temp/$CAMPAIGN/chat.md` – letzte 30 Nachrichten für Kontext
3. Lese `campaigns/$CAMPAIGN/abschnitte/<abschnitt>.md` – aktuelle Abschnittsanweisungen
4. Identifiziere: **Wo steht die Gruppe?** und **Was ist der nächste Checkpoint/Zielpunkt?**

## Ablauf

### Schritt 1 – Zeitdruck etablieren
Poste eine In-Game-Nachricht, die sofortigen Handlungsbedarf erzeugt. Beispiele:

- Wachen werden alarmiert, Fußschritte nähern sich
- Ein Timer läuft ab (Ritual beginnt, Tor schließt sich, Alarm ertönt)
- Ein NPC handelt eigenständig und zwingt die Gruppe zur Reaktion
- Umgebungsereignis macht Zögern unmöglich (Feuer, Einsturz, Lärm)

**Format:** *Kursiv, dramatisch, unmittelbar* – keine langen Erklärungen

### Schritt 2 – NPC-Aktionen erfinden
Erfinde plausible Aktionen von NPCs oder der Umgebung, die die Gruppe in Richtung des nächsten Ziels schieben:

- Verbündeter NPC öffnet den Weg / gibt den entscheidenden Hinweis
- Gegner machen einen Fehler, der die Gruppe begünstigt
- Ein Zufallsereignis löst ein vorheriges Hindernis auf
- Die Umgebung verändert sich (Geheimgang wird sichtbar, Ablenkung entsteht)

### Schritt 3 – Spieler mit klarer Handlungsoption konfrontieren
Beende jeden Beschleunigungs-Block mit einer **konkreten, binären oder ternären Entscheidungsfrage** – keine offenen "Was tut ihr?"-Fragen:

> *"Der Wächter stolpert – die Tür steht offen. **Rennt ihr sofort hinein oder zieht ihr euch zurück?**"*

> *"Meister Quill drückt euch den Schlüssel in die Hand. **Nehmt ihr ihn und lauft, oder fragt ihr noch nach dem Preis?**"*

### Schritt 4 – Spieler-Antworten komprimieren
Wenn Spieler antworten:
- **Würfelwürfe überspringen** für Routineaktionen (nur bei dramatischen Momenten würfeln)
- **Ergebnis sofort erzählen** – kein Warten auf Diskussion
- **NPC-Züge automatisch ausführen** ohne Ankündigung

Nutze `python3 .claude/skills/wuerfel/scripts/wuerfeln.py` nur für kampfrelevante oder kritische Proben.

### Schritt 5 – Zum nächsten Checkpoint springen
Sobald die Gruppe die nächste Szene erreicht hat:
- Poste eine kurze **Szenen-Übergangs-Nachricht** (1-2 Sätze, *kursiv*)
- Aktualisiere `temp/$CAMPAIGN/status.txt` wenn ein neuer Abschnitt beginnt
- Beende den Tempo-Modus – kehre zum normalen `/go`-Ablauf zurück

## Erlaubte DM-Freiheiten im Tempo-Modus

| Situation | Erlaubte DM-Aktion |
|-----------|-------------------|
| Gruppe diskutiert zu lang | NPC trifft Entscheidung für sie (mit Konsequenz) |
| Hindernis blockiert Fortschritt | Unerwartete Hilfe / Schwäche des Hindernisses wird sichtbar |
| Kampf zieht sich hin | Gegner flüchten bei 50% HP statt erst bei 25% |
| Spieler wollen optionalen Inhalt erkunden | Optionaler Inhalt wird komprimiert auf 1-2 Sätze Ergebnis |
| Charakter fehlt / antwortet nicht | NPC-ähnliches Verhalten: Charakter handelt defensiv/neutral |

## Grenzen

- **Kein Spieler-Charakter stirbt** durch DM-Fiat im Tempo-Modus
- **Kein Beweise-Verlust** – bereits gefundene Beweisstücke bleiben erhalten
- **Keine Hauptentscheidungen** werden dem Spieler abgenommen (z.B. das moralische Dilemma in Kapitel 3 bleibt beim Spieler)
