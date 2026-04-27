"""
D&D 5e Charakter-Hilfsfunktionen für Eberron
Kernfunktionen für Charaktererstellung (keine interaktive CLI)
"""

import random
from typing import Dict, List, Tuple, Optional, Union


# ─── Konstanten ───

RASSEN = {
    "Mensch": {"boni": {"STR": 1, "DEX": 1, "CON": 1, "INT": 1, "WIS": 1, "CHA": 1}, "besonderheit": "Extra Sprache"},
    "Elf (Hochelf)": {"boni": {"DEX": 2, "INT": 1}, "besonderheit": "Dunkelsicht, Feenblut"},
    "Zwerg": {"boni": {"CON": 2, "STR": 1}, "besonderheit": "Dunkelsicht, Zwergenresilienz"},
    "Halbling": {"boni": {"DEX": 2, "CHA": 1}, "besonderheit": "Glück, Behände"},
    "Ork": {"boni": {"STR": 2, "CON": 1}, "besonderheit": "Drohende Präsenz"},
    "Halfelf": {"boni": {"CHA": 2}, "besonderheit": "Dunkelsicht, Feenblut", "extra_bonus": 2},
    "Gnom": {"boni": {"INT": 2, "CON": 1}, "besonderheit": "Gnomische List"},
    "Drachenblütiger": {"boni": {"CHA": 2, "STR": 1}, "besonderheit": "Drachenatmung (1/Tag)"},
    "Warforged": {"boni": {"CON": 2}, "besonderheit": "Konstrukt", "extra_bonus": 1},
    "Changeling": {"boni": {"CHA": 2}, "besonderheit": "Gestaltwandler (1/Tag)", "extra_bonus": 1},
    "Kalashtar": {"boni": {"WIS": 2, "CHA": 1}, "besonderheit": "Telepathie, Geist der Ahnen"}
}

KLASSEN = {
    "Barbar": {"trefferwürfel": "d12", "primär": ["STR", "CON"], "fertigkeiten": ["Athletik", "Einschüchtern"]},
    "Bard": {"trefferwürfel": "d8", "primär": ["CHA", "DEX"], "fertigkeiten": ["Akrobatik", "Auftritt", "Täuschen"]},
    "Druide": {"trefferwürfel": "d8", "primär": ["WIS", "CON"], "fertigkeiten": ["Naturkunde", "Überleben"]},
    "Kleriker": {"trefferwürfel": "d8", "primär": ["WIS", "STR"], "fertigkeiten": ["Heilkunde", "Religion"]},
    "Waldläufer": {"trefferwürfel": "d10", "primär": ["DEX", "WIS"], "fertigkeiten": ["Wildnis", "Überleben", "Wahrnehmung"]},
    "Kämpfer": {"trefferwürfel": "d10", "primär": ["STR", "CON"], "fertigkeiten": ["Athletik", "Einschüchtern"]},
    "Mönch": {"trefferwürfel": "d8", "primär": ["DEX", "WIS"], "fertigkeiten": ["Akrobatik", "Athletik"]},
    "Paladin": {"trefferwürfel": "d10", "primär": ["STR", "CHA"], "fertigkeiten": ["Athletik", "Einschüchtern"]},
    "Schurke": {"trefferwürfel": "d8", "primär": ["DEX", "INT"], "fertigkeiten": ["Heimlichkeit", "Fingerfertigkeit"]},
    "Zauberer": {"trefferwürfel": "d6", "primär": ["INT", "CON"], "fertigkeiten": ["Arkana", "Geschichte"]},
    "Hexenmeister": {"trefferwürfel": "d8", "primär": ["CHA", "CON"], "fertigkeiten": ["Arkana", "Täuschen"]},
    "Artifex": {"trefferwürfel": "d8", "primär": ["INT", "CON"], "fertigkeiten": ["Arkana", "Geschichte", "Handwerk"]}
}

STANDARD_AUSRUESTUNG = {
    "Barbar": ["Großes Schlachtschwert", "Handaxe", "Lederrüstung", "Abenteurerpaket"],
    "Bard": ["Rapier", "Kurzbogen", "Lederpanzer", "Laute", "Abenteurerpaket"],
    "Druide": ["Keule", "Schild", "Lederrüstung", "Druidenfokus", "Abenteurerpaket"],
    "Kleriker": ["Morgenstern", "Schild", "Schupperüstung", "Heiliger Symbol", "Priesterpaket"],
    "Waldläufer": ["Langbogen", "Kurzschwert", "Lederrüstung", "Abenteurerpaket"],
    "Kämpfer": ["Kettenhemd", "Langschwert", "Schild", "Kurzschwert", "Abenteurerpaket"],
    "Mönch": ["Dolch", "Kurzbogen", "Abenteurerpaket"],
    "Paladin": ["Langschwert", "Schild", "Kettenhemd", "Heiliger Symbol", "Abenteurerpaket"],
    "Schurke": ["Kurzbogen", "Dolch x2", "Lederrüstung", "Diebeswerkzeuge", "Abenteurerpaket"],
    "Zauberer": ["Zauberbuch", "Dolch", "Abenteurerpaket"],
    "Hexenmeister": ["Rapier", "Dolch", "Buch der Schatten", "Abenteurerpaket"],
    "Artifex": ["Kriegshammer", "Handkanone", "Werkzeugsatz", "Abenteurerpaket"]
}

GESINNUNGEN = [
    "Gesetzlich Gut (LG)", "Neutral Gut (NG)", "Chaotisch Gut (CG)",
    "Gesetzlich Neutral (LN)", "Echt Neutral (N)", "Chaotisch Neutral (CN)",
    "Gesetzlich Böse (LE)", "Neutral Böse (NE)", "Chaotisch Böse (CE)"
]

ATTRIBUTE = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]


# ─── Kernfunktionen ───

def berechne_modifikator(wert: int) -> int:
    """Berechnet den D&D-Modifikator aus einem Attributswert."""
    return (wert - 10) // 2


def roll_attributes_4d6() -> List[int]:
    """Würfelt 6 Attribute mit der 4d6-Methode (niedrigster wird gestrichen)."""
    def roll_4d6_drop_lowest_single() -> int:
        rolls = sorted([random.randint(1, 6) for _ in range(4)], reverse=True)
        return sum(rolls[:3])
    
    return sorted([roll_4d6_drop_lowest_single() for _ in range(6)], reverse=True)


def wende_rassenboni(attribute: Dict[str, int], rasenname: str, extra_bonus_attr: Optional[str] = None) -> Dict[str, int]:
    """
    Wendet Rassenboni auf Attribute an.
    
    Args:
        attribute: dict mit Attributen (z.B. {"STR": 15, "DEX": 14, ...})
        rasenname: Name der Rasse
        extra_bonus_attr: Attribut für zusätzlichen +1 Bonus (für Warforged/Changeling)
    
    Returns:
        dict mit angepassten Attributen
    """
    if rasenname not in RASSEN:
        return attribute
    
    rasse = RASSEN[rasenname]
    new_attrs = attribute.copy()
    
    # Standardboni
    for attr, bonus in rasse["boni"].items():
        new_attrs[attr] = new_attrs.get(attr, 10) + bonus
    
    # Extra-Bonus für Warforged/Changeling
    if "extra_bonus" in rasse:
        bonus_attr = extra_bonus_attr or ATTRIBUTE[0]  # Standard: erstes Attribut
        new_attrs[bonus_attr] = new_attrs.get(bonus_attr, 10) + rasse["extra_bonus"]
    
    return new_attrs


def berechne_hp(klasse: str, con_mod: int, level: int = 1) -> int:
    """Berechnet die Trefferpunkte."""
    trefferwürfel = KLASSEN.get(klasse, {}).get("trefferwürfel", "d8")
    Seiten = int(trefferwürfel.replace("d", ""))
    
    # Durchschnittswert des Trefferwürfels
    through_wert = (Seiten + 1) // 2
    
    # HP = Level * (durchschnittswert + CON-Mod) + Start-HP
    if level == 1:
        return Seiten + con_mod  # Maximale HP auf Level 1
    return (level * (through_wert + con_mod)) + con_mod


def berechne_ac(rüstung: str, dex_mod: int, schild: bool = False, sonstige: int = 0) -> int:
    """Berechnet die Rüstungsklasse (AC)."""
    # Vereinfachte Berechnung
    ac_tabelle = {
        "ungerüstet": 10 + dex_mod,
        "leder": 11 + dex_mod,
        "studded leather": 12 + dex_mod,
        "kettenhemd": 14 + min(dex_mod, 2),
        "schupperüstung": 15 + min(dex_mod, 2),
        "plattenrüstung": 18,
    }
    
    basis_ac = ac_tabelle.get(rüstung.lower(), 10)
    if schild:
        basis_ac += 2
    
    return basis_ac + sonstige


def generiere_charakter(rasse: str, klasse: str, attribute_werte: List[int], 
                      name: str = "Unbekannt", gesinnung: str = "Echt Neutral",
                      extra_bonus_attr: Optional[str] = None) -> Dict:
    """
    Generiert einen vollständigen Charakterbogen.
    
    Args:
        rasse: Rassenname
        klasse: Klassenname
        attribute_werte: Liste von 6 Attributswerten (sortiert oder unsortiert)
        name: Charaktername
        gesinnung: Gesinnung
        extra_bonus_attr: Attribut für zusätzlichen Rassenbonus
    
    Returns:
        dict mit vollständigem Charakterbogen
    """
    # Attribute zuweisen (sortiert auf primäre Attribute)
    primäre = KLASSEN.get(klasse, {}).get("primär", [])
    attribute = {}
    
    # Sortierte Werte zuweisen (höchste Werte auf primäre Attribute)
    sorted Werte = sorted(attribute_werte, reverse=True)
    for i, attr in enumerate(ATTRIBUTE):
        if i < len(primäre) and attr in primäre:
            attribute[attr] = sorted Werte[i]
        else:
            attribute[attr] = sorted Werte[len(primäre) + (i - len(primäre))]
    
    # Rassenboni anwenden
    attribute = wende_rassenboni(attribute, rasse, extra_bonus_attr)
    
    # Modifikatoren berechnen
    for attr in ATTRIBUTE:
        attribute[f"{attr}_mod"] = berechne_modifikator(attribute[attr])
    
    # HP, AC, Initiative berechnen
    con_mod = attribute["CON_mod"]
    dex_mod = attribute["DEX_mod"]
    hp = berechne_hp(klasse, con_mod)
    ac = berechne_ac("kettenhemd", dex_mod, schild=True)  # Standard
    initiative = dex_mod
    
    # Fertigkeiten
    fertigkeiten = {}
    for f in KLASSEN.get(klasse, {}).get("fertigkeiten", []):
        # Standardmäßig mit primärem Attributsmodifikator
        primär_attr = primäre[0] if primäre else "INT"
        fertigkeiten[f] = attribute.get(f"{primär_attr}_mod", 0)
    
    # Ausrüstung
    ausrüstung = STANDARD_AUSRUESTUNG.get(klasse, [])
    
    return {
        "name": name,
        "rasse": rasse,
        "klasse": klasse,
        "level": 1,
        "gesinnung": gesinnung,
        "attribute": attribute,
        "HP": {"aktuell": hp, "max": hp},
        "AC": ac,
        "initiative": initiative,
        "fertigkeiten": fertigkeiten,
        "ausruestung": ausrüstung
    }


def formatiere_charakterbogen(char: Dict) -> str:
    """Formatiert einen Charakter als Discord-Post."""
    lines = []
    lines.append(f"**Name:** {char.get('name', 'Unbekannt')}")
    lines.append("===")
    lines.append(f"**Rasse:** {char.get('rasse', '?')} | **Klasse:** {char.get('klasse', '?')} | **Level:** {char.get('level', 1)}")
    lines.append(f"**Gesinnung:** {char.get('gesinnung', 'Neutral')}")
    lines.append(f"**Trefferpunkte:** {char.get('HP', {}).get('aktuell', 0)}/{char.get('HP', {}).get('max', 0)}")
    lines.append(f"**Rüstungsklasse (AC):** {char.get('AC', 10)}")
    lines.append(f"**Initiative:** +{char.get('initiative', 0)}")
    
    # Attribute
    attrs = {k: v for k, v in char.get('attribute', {}).items() if not k.endswith('_mod')}
    attr_str = " | ".join([f"{k} {v}" for k, v in attrs.items()])
    lines.append(f"**Attribute:** {attr_str}")
    
    # Fertigkeiten
    skills = char.get('fertigkeiten', {})
    if skills:
        skill_str = ", ".join([f"{k} +{v}" for k, v in skills.items()])
        lines.append(f"**Fertigkeiten:** {skill_str}")
    
    # Ausrüstung
    equip = char.get('ausruestung', [])
    if equip:
        lines.append(f"**Ausrüstung:** {', '.join(equip)}")
    
    return "\n".join(lines)
