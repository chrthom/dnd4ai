---
name: akt3
description: Akt 3 - Das Tribunal der Lügen & Moralisches Dilemma
user-invocable: true
---

## **Ausgabe-Regel (IMPORTANT)**
- **Dieser Skill wird durch `/akt 3` im KI-Chat aufgerufen**
- **Die KI antwortet NICHT im KI-Chat** – alle Ausgaben gehen **EXKLUSIV** in Discord-Channel `abenteuer-1`
- **Bei Aufruf:** Tribunal-Szene, Beweispräsentation, moralisches Dilemma und Finale werden in `abenteuer-1` gepostet

# Akt 3: Das Tribunal der Lügen

## Spezifikation
Siehe auch: [`../../akte/akt_3.json`](../../akte/akt_3.json) für die detaillierte Akt-Konfiguration.

## Purpose
Öffentliches Tribunal gegen Elrond Tusk. Die Gruppe muss Beweise präsentieren und die Geschworenen überzeugen. Während des Prozesses wird ein zufälliger Spielercharakter von Tusks Anhängern als Geisel genommen. Am Ende stürmen Tusks Anhänger den Saal, was zu einem moralischen Dilemma führt.

## When to Use
- Nach Abschluss von Akt 2
- Wenn die Gruppe bereit ist, Tusk vor Gericht zu stellen

## Workflow
1. **Eröffnung des Tribunals**
   - Lady Justice eröffnet die Verhandlung
   - Tusks Anwalt (Meister Blufford) beginnt mit einer Rede, die die Gruppe als Lügen hinstellt
   - Die Gruppe kann Beweise vorlegen

2. **Beweisphase**
   - Gruppe präsentiert Beweise aus Akt 1 und 2
   - Je mehr Beweise, desto mehr Geschworene sind überzeugt
   - Meister Blufford versucht jeden Beweis zu widerlegen
   - Tusk nutzt den Echo-Kristall, um die Menge aufzuhetzen

3. **Geiselnahme!** (Checkpoint)
   - Plötzlich stürmen 4 Wächter der Narrative den Saal
   - Sie neutralisieren die Wachen und **entführen einen zufälligen Spielercharakter** als Geisel
   - **Moralisches Dilemma**: Geisel retten oder Tusk endgültig stoppen?

4. **Sturm auf das Tribunal**
   - Tusks Anhänger stürmen den Gerichtssaal
   - Zwischen den kämpfenden Massen muss die Gruppe entscheiden

5. **Finale Entscheidung**
   - **Option A**: Spielercharakter retten → Tusk flieht, Gruppe hat Ehre bewahrt
   - **Option B**: Spielercharakter opfern → Tusk wird gefangen, aber Charakter stirbt heldenhaft

## NPCs
- **Elrond Tusk** (CE, Böse) – Hauptantagonist, nutzt Echo-Kristall
- **Lady Justice** (LG, Gesetzlich Gut) – Neutrale Richterin
- **Meister Blufford** (NE, Neutral Böse) – Tusks Anwalt, charismatischer Barde
- **Wächter der Narrative (Elite)** (LE, Gesetzlich Böse) – Doppelgänger, nehmen Geisel
- **Harper-Verbündeter** (NG, Neutral Gut) – Hilft der Gruppe, falls Harpers in Akt 1 überzeugt
- **Bürger von Sharn** (N, Neutral) – Geschworene, können überzeugt werden

## Auswirkungen aus vorherigen Akten
| Bedingung | Auswirkung |
|-----------|------------|
| Beweise aus Akt 1 | +2 Beweismittel in der Beweisphase |
| Harpers in Akt 1 überzeugt | +1 Harper-Verbündeter hilft bei Geiselbefreiung |
| Gefangener in Akt 2 befragt | Kennt Tusks Schwäche (Vorteil im Finalkampf) |
| Geheimgang in Akt 2 genutzt | Kennt Tusks Hinterausgang (kann Flucht blockieren) |

## Checkpoint: Moralisches Dilemma

### Option A: Spielercharakter retten
- **Beschreibung**: Gruppe konzentriert sich darauf, den Freund zu befreien
- **Mechanik**: Wächter mit Geisel haben +2 AC und Vorteil auf Angriffe
- **Erfolg**: Charakter wird gerettet
- **Konsequenz**: Tusk flieht durch Hinterausgang
- **Ende**: "Die Stadt der tausend Lügen blieb – doch ihr wisst, wer die Wahrheit spricht. Und das macht euch gefährlich."

### Option B: Spielercharakter opfern
- **Beschreibung**: Gruppe ignoriert Geisel und stürmt auf Tusk zu
- **Mechanik**: Gefangener Charakter stirbt, wenn Gruppe nicht in 3 Runden handelt
- **Erfolg**: Tusk wird gefangen genommen
- **Konsequenz**: Charakter stirbt heldenhaft
- **Ende**: "Sharn war gerettet. Doch einer von euch war der Preis. War es das wert?"

## Code Usage

```bash
# Akt 3 starten
# Die KI folgt dem workflow aus akt_3.json
# Wichtig: Zufälligen Spielercharakter als Geisel auswählen!
```

## Ausgabeformat (Discord)

### Tribunals-Eröffnung:
```
*Der Große Gerichtssaal von Durgon’s Bridge ist bis auf den letzten Platz gefüllt. Die Luft ist schwer von Vorahnung. Vor euch thront Lady Justice auf ihrem Richtersitz, ihr Blick so scharf wie ein Schwert. Neben ihr steht Tusk, umringt von seinen Anwälten. Sein Echo-Kristall glüht an seinem Hals, seinen Stimmen eine unnatürliche Präsenz verleiht.*

*Meister Blufford, in teuren Roben gekleidet, tritt vor.* **"Hohe Lady Justice, verehrte Geschworene, heute stehen wir vor einer Tragödie höchinizter Verleumdung. Diese... Abenteurer..."** *er wirft einen verächtlichen Blick auf euch* **"...beschuldigen einen der größten Wohltäter Sharns der Lügen! Wo sind die Beweise?"**

*Lady Justice wendet sich euch zu.* **"Die Anklage ist schwer. Sie behaupten, Meister Tusk habe die Geschichte unserer Stadt manipuliert. Was sagt ihr darauf?"**
```

### Beweisphase:
```
*Ihr legt eure Beweise vor: die manipulierten Dokumente aus Akt 1, Tusks Notizen aus der Gedankenschmiede. Die Geschworenen murmeln. Meister Blufford wirbelt herum wie ein Theaterdarsteller auf der Bühne.*

**"Ah, aber versuchen Sie mal, diese Dokumente zu verifizieren! Woher wissen wir, dass SIE sie nicht gefälscht haben?"**

*Tusk hebt den Echo-Kristall. Plötzlich füllt seine Stimme den gesamten Saal, verstärkt und verzerrt.* **"Die Wahrheit ist... was die Mehrzahl glaubt. Und Sharn glaubt an MIR."**

*Die Menge beginnt zu flüstern... dann zu schreien. Einer steht auf. Dann noch einer...*
```

### Geiselnahme:
```
*Plötzlich – Lärm von den Eingängen! Die großen Türen fliegen auf. Vier Gestalten stürmen herein, ihre Gesichter verzerrt von einer unheilvollen Magie. Doppelgänger! Eine von ihnen packt* **<zufälliger Spielercharakter>** *und hält ein Messer an seine/ihr Kehle.*

**"Einen Schritt näher, und euer Freund stirbt!"** *brüllt der Wächter. Seine Stimme ist nicht seine eigene – sie hallt, als käme sie von überall.*

*Lady Justice schlägt mit ihrem Hammer auf.* **"Ordnung im Saal! WACHEN!"** *Doch die Wachen liegen bereits reglos am Boden. Meister Blufford lacht.*

**"Ah, wie... dramatisch. Scheint, als hätte jemand die Geiselnahme geplant."** *Tusk selbst bleibt ruhig, seine Augen funkeln.*

*Die Entscheidung liegt bei euch.*
```

### Dilemma-Frage:
```
**"Die Wächter halten <Name> als Geisel! Was tut die Gruppe?"**
- **Spielercharakter retten**: Konzentriert euch auf die Befreiung eures Kameraden (Wächter haben +2 AC und Vorteil)
- **Spielercharakter opfern**: Ignoriert die Geisel und stürmt direkt auf Tusk zu (Gefangener stirbt nach 3 Runden)
```

### Ende A (Geisel gerettet):
```
*Mit einem letzten, verzweifelten Sturz rollt <Name> frei. Die Gruppe formiert sich um ihn/sie, Bereit, die Wächter zurückzudrängen. Doch in der Verwirrung... verschwindet Tusk. Ein allerletzter Blick, ein spöttisches Lächeln, dann ist er weg. Nur der Echo-Kristall bleibt zurück, zersplittert auf dem Steinboden.*

*Die Menge starrt. Die Wächter, jetzt ohne ihren Meister, weichen zurück. Lady Justice seufzt tief.*

**"Die Stadt der tausend Lügen blieb."** *Ihre Stimme ist müde.* **"Doch ihr... ihr wisst, wer die Wahrheit spricht. Und das macht euch gefährlich."**

*java
Ende der Kampagne... oder der Beginn eines neuen Kapitels?*
```

### Ende B (Charakter geopfert):
```
*Die Gruppe stürmt vorwärts, die Wächter fallen unter euren Schlägen. Doch als ihr Tusk erreicht, ist es zu spät. Ein letzter, verzweifelter Schrei hallt durch den Saal. <Name>... ist nicht mehr.*

*Tusk, umringt und besaß, gibt auf. Meister Blufford wirft den Echo-Kristall zu Boden, wo er in tausend Splitter zerspringt. Die Illusionen verschwinden. Die Menge erkennt die Wahrheit.*

*Lady JusticeNickt.* **"Sharn war gerettet."** *Ihre Stimme bricht leicht.* **"Doch einer von euch war der Preis. War es das wert?"**

*Die Stadt feiert euch als Helden. Doch in euren Herzen... wisst ihr, was ihr verloren habt.*
```

## Übergang / Fortsetzungshinweis
```
*Hinweis für den Spielleiter:*
- **Falls Tusk flieht** (Ende A): Seine Flucht könnte eine Fortsetzung ermöglichen – seine Arbeit am Himmelsnetz geht weiter
- **Falls Tusk gefangen** (Ende B): Ohne seinen Kristall ist seine Macht gebrochen... aber seine Anhänger leben weiter
- **Charakter-Tod**: Sollte nicht permanent sein, wenn die Gruppe das nicht will – aber sollte Konsequenzen haben (z.B. Trauma, Stufe verlieren)
```

## Referenzierte Dateien
- [`../../akte/akt_3.json`](../../akte/akt_3.json) – Detaillierte Akt-Konfiguration
- [`../kampf/SKILL.md`](../kampf/SKILL.md) – Kampfabwicklung
- [`../wuerfel/SKILL.md`](../wuerfel/SKILL.md) – Für Würfelproben
- [`../charakter/SKILL.md`](../charakter/SKILL.md) – Für Charakteränderungen nach dem Tod
