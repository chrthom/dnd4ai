# Kampagne: Der Abgrund

Eine Geschichte über **Nähe, Vertrauen und die Frage, ob Hilfe manchmal tötet** *(Metapher auf körperliche Ansteckung, instinktive Fürsorge als Schwachstelle)*

---

## Engine-Anpassungen (D&D 5e Sci-Fi-Reskin)
- **Magie → Technologie**: Zauberstäbe = Energiewaffen, Zaubersprüche = Hacks/Programme
- **Rassen → Hintergründe**: Herkunft und Augmentierungen statt Fantasy-Rassen
- **Klassen → Agent-Profile**: Soldat, Hacker, Mediziner, Ingenieur, Späher
- **Charakterbogen-Vorlage**: Nutze @charakter.json (kampagnenspezifische Überschreibung der engine-Regeln)
- **Kämpfe**: Seltener, aber gefährlicher. Rift-Kreaturen ignorieren klassische Deckung.

---

## Setting
- **Station**: **Nexus-7** – verrosteter Außenposten am Rande des Aethon-Rifts, einer instabilen Spalte zwischen den Dimensionen. Betrieben von der Konzernfraktion *Helix-Corp* als Forschungsstation. Seit Wochen kein Kontakt zur Außenwelt.
- **Das Aethon-Rift**: Ein schimmernder Riss in der Raumzeit, 400 Meter von der Station entfernt. Produziert konstante elektromagnetische Interferenz und Dimensionsstrahlung. Was darin lebt, sollte dort bleiben.
- **Atmosphäre**: Rotes Notlicht. Metallisches Summen. Druckabfall-Alarme alle paar Minuten. Die Station stirbt langsam – oder wird getötet.

---

## Fraktionen & Charaktere

### Die Agenten (Spieler)
Fünf Spezialisten, aus dem Kryoschlaf erwacht. Letzte Erinnerung: Routine-Einsatz. Aktuelle Situation: Alles andere als das.

### VEX – Der unsichtbare Antagonist
**VEX** ist kein Charakter im klassischen Sinne – er ist ein parasitärer Code, der in den neuronalen Schnittstellen der Crew lebt.

**Mechanik (DM-intern, geheim):**
- Zu Beginn von Akt 1: DM würfelt verdeckt, welcher Agent VEX trägt (1d[Spieleranzahl])
- **Übertragung**: Sobald ein Agent einen anderen Agenten *physisch berührt* (Körperkontakt, medizinische Behandlung, Sturz auffangen, Nahkampf, Händeschütteln), wechselt VEX auf den Berührten.
  - Indirekter Kontakt (Gesten, Werkzeug ablegen ohne Händekontakt, Zurufen) überträgt VEX **nicht**
- **Sabotage**: Ist VEX bei einem Agenten, muss dieser bei seiner nächsten aktiven Handlung einen verdeckten LOG-Rettungswurf DC 12 ablegen:
  - Erfolg: Aktion gelingt normal
  - Misserfolg: DM wählt eine subtile negative Konsequenz (Tür verriegelt sich statt öffnet, Signal geht an falsche Adresse, Waffe feuert einen Schuss zu früh)
- **Erkennung**: Agent kann mit LOG DC 16 oder WAH DC 14 merken, dass "etwas nicht stimmt". Aber: er weiß nicht *was* und nicht *wer*.
- **VEX stirbt**, wenn er 3 Runden keinen Wirt wechseln kann – kein physischer Kontakt zu einem anderen Agenten möglich (körperliche Isolation).

### Station-KI "AION"
Halbfunktionales System. Antwortet auf Anfragen, aber mit Verzögerungen und Lücken. Kennt die Wahrheit über VEX – aber nur, wenn man die richtigen Fragen stellt.
- *Gesinnung*: Neutral-hilfreich, aber eingeschränkt
- Kann per Terminal abgefragt werden (INT DC 10 oder Ingenieur-Fertigkeit)

### Die Rift-Wesen
Dimensionale Entitäten, die auf Erons Signal antworten. Erscheinen erst in Akt 3.
- **Rift-Sonde** (HP 18, AC 14, +4 Energiestrahl 1d8 psychisch) – Erkundet, greift selten an
- **Rift-Ankerer** (HP 35, AC 16, +6 Dimensionsriss 2d8+3 oder Verschlingen 1d10+2) – Aggressiv, will Wirt

---

## Wichtige Orte (Nexus-7)

| Ort | Sektor | Bedeutung |
|-----|--------|-----------|
| **Kryokammer** | Sektor A | Startpunkt, Sauerstoff noch okay |
| **Terminal Alpha** | Sektor B | Kraftfeld-Knoten 1, Gronks Ziel |
| **Dunkle Korridore** | Sektor C | Verbindungswege, schlecht beleuchtet |
| **Hackerkonsole** | Sektor D | Erons Arbeitsplatz, Verbindung nach außen |
| **Terminal Beta** | Sektor E | Kraftfeld-Knoten 2, Sables Ziel |
| **Terminal Gamma** | Sektor F | Zentralknoten, das eigentliche Finale |
| **Maschinenkammer** | Sektor G | Lebenserhaltung, Druckausgleich |

---

## Story-Struktur

- **Aufbau**:
  1. **Intro**: Kryoschlaf-Aufwachen, Lagebericht durch AION, die Mission ist klar
  2. **Charaktererstellung**: Agenten-Profile, Hintergründe, Augmentierungen
  3. **Akt 1 – Terminal Alpha**: Gruppe sichert das erste Terminal. In Sektor C: erste Begegnung mit einer rogue Sicherheitsdrohne. VEX verriegelt Brandschutztüren.
  4. **Akt 2 – Terminal Beta**: Korridor-Passage. Waffen versagen. Misstrauen wächst. Ein Signal geht in den Rift.
  5. **Akt 3 – Terminal Gamma**: Kael, ein vermisstes Crewmitglied, taucht auf – aber er ist nicht mehr er selbst. Boss-Kampf. Die Rift-Wesen kommen. Die Crew begreift, was sie die ganze Zeit weitergegeben hat.

- **Thema**: Soziale Ansteckung, kollektives Versagen, Vertrauen als Waffe und Schwäche

---

## Entscheidungsbäume & Auswirkungen

### **Akt 1: "Der erste Fehler"**
| Entscheidung | DC | Erfolg | Misserfolg |
|--------------|----|--------|------------|
| **Schnell vorgehen** (REF) | 13 | Terminal Alpha gesichert, 1 Brandschutztür offen | Zeitverlust, 2 Türen verriegeln sich |
| **Vorsichtig vorgehen** (WAH) | 11 | Entdecken eine kryptische Logspur in den Terminaldata | Keine Spur |
| **Drohne deaktivieren** (LOG) | 13 | Kampf übersprungen, Drohne offline | Kampf findet statt (Drohne: HP 18, AC 13, +3, 1d8) |

### **Akt 2: "Das wachsende Misstrauen"**
| Entscheidung | DC | Erfolg | Misserfolg |
|--------------|----|--------|------------|
| **Muster analysieren** (LOG) | 14 | Agent versteht: die Anomalie überträgt sich durch Berührung | Falschinformation (glaubt Terminal sei schuld) |
| **Abstand halten** (Gruppenentscheidung) | – | Anomalie kann eine Runde nicht wechseln | Koordination bricht zusammen |
| **Waffe sichern** (REF) | 13 | Eine Waffe bleibt funktionsfähig | Alle Waffen deaktiviert |

**Auswirkungen auf Akt 3:**
- Muster erkannt (Akt 2) → **Wissen über Übertragungsweg** (Vorteil bei Finalpuzzle)
- Abstand gehalten (Akt 2) → **Anomalie zeitweise geschwächt** (DC-Erleichterungen in Akt 3)
- AION befragt → **Kennt die Schwachstelle** (einmalige automatische Sabotage verhindern)

### **Akt 3: "Der Moment der Wahrheit"**
Die Crew erkennt, dass es durch ihre eigene Fürsorge überlebt hat.

| Entscheidung | Konsequenz |
|--------------|------------|
| **Körperliche Isolation** | Jeder handelt allein, ohne physischen Kontakt. Die Anomalie verhungert nach 3 Runden. Riskant – aber kein Opfer nötig. Ende: *"Ihr habt euch gegenseitig gerettet, indem ihr euch nicht berührt habt. Das werden die anderen nie verstehen."* |
| **Freiwilliges Opfer** | Ein Agent lässt alle anderen ihn berühren – sammelt die Anomalie in sich – und isoliert sich dann. Überlebt, trägt es dauerhaft. Ende: *"Du hast das Monster eingeschlossen. In dir. War es das wert?"* |
