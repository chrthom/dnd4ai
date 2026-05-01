---
name: akt2
description: Akt 2 - Die Gedankenschmiede
---

## **Ausgabe-Regel (IMPORTANT)**
- **Dieser Skill wird durch `/akt 2` im KI-Chat aufgerufen**
- **Die KI antwortet NICHT im KI-Chat** – alle Ausgaben gehen **EXKLUSIV** in Discord-Channel `abenteuer-1`
- **Bei Aufruf:** Akt 2-Geschichte (Gedankenschmiede), Fallen, NPCs und Entscheidungscheckpoints werden in `abenteuer-1` gepostet

# Akt 2: Die Gedankenschmiede

## Spezifikation
Siehe auch: [`../../akte/akt_2.json`](../../akte/akt_2.json) für die detaillierte Akt-Konfiguration.

## Purpose
Die Gruppe dringt in Elrond Tusks geheime Gedankenschmiede ein – ein Alchemielabor in Tavick’s Landing, wo er Geschichten "schmiedet" und die Wahrheit von Sharn umformt. Ziel: Beweise für seine Manipulationen finden und ihn möglicherweise stellen.

## When to Use
- Nach Abschluss von Akt 1
- Wenn die Gruppe bereit ist, in Tusks Versteck einzudringen

## Workflow
1. **Ankunft an der Gedankenschmiede**
   - Gruppe findet versteckten Eingang unter der "Bank von Tavick"
   - Drei Wege führen hinein: **Haupteingang** (bewacht), **Lüftungsschächte** (eng), **Geheimgang** (versteckt)

2. **Checkpoint 1: Eingangsweg wählen**
   - **Haupteingang (Täuschung DC 15)**: Warforged-Wachen überreden
   - **Lüftungsschächte (Dex DC 13)**: Eng, aber unentdeckt
   - **Geheimgang (Wis Wahrnehmung DC 14)**: Versteckter Eingang durch Abwasserrohre

3. **Erforschung der Schmiede**
   - Alchemielabor mit kochenden Essenzen
   - Schreibpulte mit halbfertigen "Geschichten" (manipulierte Dokumente)
   - Gefangener Harper-Agent in einer Zelle
   - Tusks Notizen über das Himmelsnetz-Projekt

4. **Checkpoint 2: Gefangenen befragen?**
   - **Befragen (Int/Insight DC 12)**: Wertvolle Infos über Tusks Pläne und Schwäche
   - **Ignorieren**: Keine Zeit verlieren, aber keine zusätzlichen Infos

5. **Begegnung mit Elrond Tusk**
   - Tusk kehrt früher als erwartet zurück
   - Kurzer Kampf – wenn er zu viel Schaden nimmt, aktiviert er Teleportationsring und flieht
   - Hinterlässt den Echo-Kristall

6. **Abschluss**
   - Gruppe findet Beweise gegen Tusk
   - Tusk flieht
   - Übergabe zu Akt 3

## NPCs
- **Elrond Tusk** (CE, Böse) – Hauptantagonist, charismatisch, mit Artefakten
- **Warforged-Wache** (N, Neutral) – Mechanische Wächter
- **Gefangener Harper-Agent** (NG, Neutral Gut) – Hat Informationen über Tusks Pläne
- **Alchemist-Lehrling** (CN, Chaotisch Neutral) – Weiß nicht, was wirklich passiert

## Artefakte in der Schmiede
- **Sturmherrufer-Stab**: Ruft Blitze herbei (Tesla-Parodie)
- **Echo-Kristall**: Verstärkt Stimmen (Twitter-Parodie)
- **Himmelsnetz**: Magisches Satellitennetz (Starlink-Parodie)

## Checkpoint-Auswirkungen
| Weg | Erfolg | Misserfolg |
|-----|--------|------------|
| **Haupteingang** (DC 15) | Wachen durchlassen | Kampf mit 2 Warforged-Wachen |
| **Lüftungsschächte** (DC 13) | Schnell, unentdeckt | Zeit verlieren (1h), Tusk besser vorbereitet |
| **Geheimgang** (DC 14) | Versteckter Eingang | Löst Falle aus (Giftpfeile) |

| Entscheidung | Erfolg | Misserfolg |
|-------------|--------|------------|
| **Befragen** (DC 12) | Kennt Tusks Schwäche (Vorteil im Finalkampf) | Falschinformation |
| **Ignorieren** | Keine Zeit verloren | Keine zusätzlichen Infos |

## Fallen (2)
1. **Giftpfeil-Falle**: Versteckte Bogenmechanismen (Dex DC 13 zum Ausweichen)
2. **Halluzinations-Spiegel**: Zeigt jedem Betrachter eine andere Realität (Weis DC 14 oder 1 Runde verwirrt)

## Code Usage

```bash
# Akt 2 starten
# Die KI folgt dem workflow aus akt_2.json
```

## Ausgabeformat (Discord)

### Ankunft-Szene:
```
*Die Bank von Tavick ist ein unscheinbares Gebäude in Tavick’s Landing – von außen. Doch als ihr euch dem Hintereingang nähert, bemerkt ihr eine seltsame Energie in der Luft. Eine alte Luke im Boden, halb verrostet, führt offenbar hinunter. Drei Möglichkeiten bieten sich an...*

**"Der Haupteingang ist gut beleuchtet und von zwei Warforged bewacht"**, *flüstert Schwester Scribble.* **"Aber dort drüben... die Lüftungsschächte. Eng, aber sie könnten uns unentdeckt reinbringen."** *Sie zeigt auf ein schmales Gitter hoch oben.*

**"Oder..."** *Meister Quill zieht eine vergilbte Bauzeichnung hervor.* **"...der alte Geheimtunnel. Wenn er noch existiert."**
```

### Eingangsentscheidung:
```
**"Welchen Weg wählt die Gruppe?"**
- **Haupteingang (Täuschung DC 15)**: Versuch, die Wachen zu überreden
- **Lüftungsschächte (Dex DC 13)**: Eng, aber schnell
- **Geheimgang (Wis Wahrnehmung DC 14)**: Suche nach verstecktem Eingang
```

### Schmiede-Beschreibung:
```
*Der Raum ist erfüllt von einem seltsamen Summen. Überall blubbern Flaschen mit farbigen Flüssigkeiten, die in keinem natürlichen Spektrum leuchten. An den Wänden hängen Karten von Sharn – doch die Grenzen der Distrikte scheinen sich ständig zu verändern, als wären sie lebendig. Auf einem großen Schreibpult liegt ein halbfertiges Dokument: 'Die wahre Geschichte von König Boranels Tod' – doch die Tinte ist noch feucht, und der Inhalt ist offensichtliche Lügen.*

*In einer Ecke klingelt leise ein Käfig. Ein Verwundeter darin hebt den Kopf.* **"Ihr... ihr seid nicht von Tusk? Dann hilt mir, bitte! Er hat mich hier eingeschlossen, nachdem ich seine Pläne entdeckt habe!"**

*Plötzlich – ein Geräusch von oben! Schritte. Jemand kommt.*
```

### Tusk-Begegnung:
```
*Die Tür fliegt auf. Elrond Tusk betritt den Raum, sein Sturmherrufer-Stab blitzt im Halbdunkel. Er trägt einen Umhang mit eingestickten Schaltkreisen – Runen, die sich langsam bewegen, als wären sie lebendig. Sein Blick fällt auf euch, und ein spätes Erkennen huscht über sein Gesicht.*

**"Ah. Mitarbeiter von Meister...?"** *seine Stimme ist glatt wie Öl, verstärkt durch den Echo-Kristall an seinem Hals.* **"Ich fürchte, es gibt ein Missverständnis. Dies hier ist... geschäftlich."**

*In seiner Hand Materialisiert sich ein dolchartiges Objekt. Seine Finger zucken in Richtung seines Rings – ein Teleportationsartefakt.*
```

### fightszene:
```
*Tusk hebt den Stab. Blitzenergie krakelt durch den Raum!*

*Rollt Initiative!* (Die KI verwaltet den Kampf per kampf-Skill)
```

### Tusk Flucht:
```
*Tusk taumelt zurück, Blut rinnt aus einer Wunde an seiner Schulter. Mit einem verzweifelten Blick auf seinen Ring brüllt er:* **"Dies ist noch nicht vorbei!"**

*Ein greller Blitz – und er ist verschwunden. Nur der Echo-Kristall bleibt zurück, pulsierend auf dem Boden.*

*Auf dem Tisch: Tusks Notizbücher, detaillierte Pläne für die Manipulation Sharns. Und eine Einladung... zum großen Tribunal morgen.*
```

## Auswirkungen auf Akt 3
- **Beweise aus Akt 1**: +2 Beweismittel im Tribunal
- **Gefangener befragt**: Kennt Tusks Schwäche (Vorteil im Kampf)
- **Geheimgang genutzt**: Kennt Hinterausgang in Akt 3

## Übergang zu Akt 3
```
*Zurück bei den Harpers studiert Meister Quill die Beweise, die ihr geborgen habt.*

**"Das sind die Beweise, die wir brauchen!"** *seine Augen leuchten.* **"Tusk wird sich vor dem Tribunal verantworten müssen. Morgen ist die Verhandlung – und das ganze Sharn wird zusehen."**

*Doch Schwester Scribble beißt sich auf die Lippe.* **"Aber... was, wenn er nicht allein ist? Die Wächter der Narrative werden nicht tatenlos zusehen."**

**"Dann müssen wir vorbereitet sein."** *Meister Quill schaut die Gruppe an.* **"Seid ihr bereit, ihm vor ganz Sharn gegenüberzutreten?"**

**/akt 3** zum Fortfahren.
```

## Referenzierte Dateien
- [`../../akte/akt_2.json`](../../akte/akt_2.json) – Detaillierte Akt-Konfiguration
- [`../kampf/SKILL.md`](../kampf/SKILL.md) – Kampfabwicklung
- [`../wuerfel/SKILL.md`](../wuerfel/SKILL.md) – Für Würfelproben
- [`../charakter/SKILL.md`](../charakter/SKILL.md) – Für Charakteränderungen
