#!/usr/bin/env python3
"""
D&D 5e Würfel-Skript für Discord
Unterstützt: 1d20, 2d6+3, 4d6 (Charaktererstellung), etc.
"""

import sys
import random
import re
from typing import List, Tuple


def parse_expression(expr: str) -> List[Tuple[int, int, int]]:
    """Parsed einen Würfelausdruck in (Anzahl, Seiten, Modifier)"""
    parts = [p.strip() for p in expr.split(',')]
    results = []
    
    for part in parts:
        # Pattern: [Anzahl]d[Seiten][+|-][Modifier]
        match = re.match(r'^(\d*)d(\d+)(?:([+\-])(\d+))?$', part)
        if not match:
            raise ValueError(f"Ungültiger Würfelausdruck: '{part}'")
        
        count_str, sides_str, op, mod_str = match.groups()
        count = int(count_str) if count_str else 1
        sides = int(sides_str)
        mod = int(mod_str) if mod_str else 0
        
        if op == '-':
            mod = -mod
        
        if count < 1 or count > 10:
            raise ValueError("Anzahl der Würfel muss zwischen 1 und 10 liegen")
        
        if sides not in [4, 6, 8, 10, 12, 20, 100]:
            raise ValueError(f"Unbekannter Würfeltyp: d{sides}")
        
        results.append((count, sides, mod))
    
    return results


def roll_dice(count: int, sides: int) -> List[int]:
    """Würfelt X Würfel mit Y Seiten"""
    return [random.randint(1, sides) for _ in range(count)]


def format_roll(expr: str, rolls: List[int], total: int) -> str:
    """Formatiert einen einzelnen Würfelwurf"""
    parsed = parse_expression(expr)
    mod = sum(m for _, _, m in parsed)
    
    if len(rolls) == 1:
        return f"**{expr}**: **{total}**"
    elif mod == 0:
        return f"**{expr}**: [{', '.join(map(str, rolls))}] → **{total}**"
    elif mod > 0:
        return f"**{expr}**: [{', '.join(map(str, rolls))}] + {mod} → **{total}**"
    else:
        return f"**{expr}**: [{', '.join(map(str, rolls))}] - {-mod} → **{total}**"


def roll_4d6_drop_lowest() -> Tuple[List[int], int]:
    """4d6 Würfeln, niedrigsten streichen"""
    rolls = roll_dice(4, 6)
    sorted_rolls = sorted(rolls, reverse=True)
    result_rolls = sorted_rolls[:3]
    return result_rolls, sum(result_rolls)


def roll_character_attributes() -> List[int]:
    """Würfelt alle 6 Attribute für Charaktererstellung"""
    attrs = []
    attributes = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']
    
    for attr in attributes:
        rolls, total = roll_4d6_drop_lowest()
        attrs.append((attr, rolls, total))
        print(f"{attr}: {rolls} → {total}")
    
    values = [total for _, _, total in attrs]
    print(f"Sortiert: {', '.join(map(str, sorted(values, reverse=True)))}")
    return values


def main():
    if len(sys.argv) < 2:
        print("Verwendung:")
        print("  Würfeln: python3 wuerfeln.py <Ausdruck> [Ausdruck2,...]")
        print("  Beispiel: python3 wuerfeln.py 1d20+5")
        print("  Beispiel: python3 wuerfeln.py 2d6,1d20")
        print("  Charakter: python3 wuerfeln.py --charakter")
        sys.exit(1)
    
    # Charaktererstellung
    if sys.argv[1] == "--charakter":
        print("Attribute für Charaktererstellung (4d6, niedrigster gestrichen):")
        roll_character_attributes()
        return
    
    # Normale Würfelwürfe
    expression = ' '.join(sys.argv[1:])
    
    try:
        parsed = parse_expression(expression)
    except ValueError as e:
        print(f"⚠️ {e}")
        print("Beispiele: 1d20, 2d6+3, 1d100")
        sys.exit(1)
    
    all_rolls = []
    total = 0
    results = []
    
    for count, sides, mod in parsed:
        rolls = roll_dice(count, sides)
        all_rolls.extend(rolls)
        total += sum(rolls) + mod
    
    # Formatieren
    parts = expression.split(',')
    if len(parts) == 1:
        print(f"Du würfelst {format_roll(expression, all_rolls, total)}")
    else:
        print("Du würfelst:")
        # Aktuell nur einfacher Ausdruck
        # TODO: Mehrere Ausdrücke unterstützt
        print(f"  {format_roll(parts[0].strip(), all_rolls, total)}")


if __name__ == "__main__":
    main()
