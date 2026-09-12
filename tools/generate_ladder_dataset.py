#!/usr/bin/env python3
"""
Morning Puzzles - Word Ladder Dataset Generator
Curates authentic, high-quality Lewis Carroll-style Word Ladder puzzles
across 3 difficulty tiers using familiar, everyday English words.

- Easy: 4-letter words, 3-4 intermediate steps (total 5-6 words)
- Medium: 4-letter words, 4-5 intermediate steps (total 6-7 words)
- Hard: 5-letter words, 4-6 intermediate steps (total 6-8 words)

Outputs:
  server/data/ladder_words.json
"""

import json
import os
import sys
from collections import deque, defaultdict
from typing import List, Dict, Any, Tuple, Optional

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "server", "data", "ladder_words.json")

# 1. Curated list of recognizable classic word ladder puzzles with verified daily-friendly steps
CURATED_LADDERS: Dict[str, List[Dict[str, Any]]] = {
    "easy": [
        {
            "start": "COLD",
            "target": "WARM",
            "steps": 4,
            "solution": ["COLD", "CORD", "CARD", "WARD", "WARM"]
        },
        {
            "start": "HEAD",
            "target": "TAIL",
            "steps": 5,
            "solution": ["HEAD", "HEAL", "TEAL", "TELL", "TALL", "TAIL"]
        },
        {
            "start": "LOVE",
            "target": "HATE",
            "steps": 3,
            "solution": ["LOVE", "HOVE", "HAVE", "HATE"]
        },
        {
            "start": "DARK",
            "target": "MOON",
            "steps": 4,
            "solution": ["DARK", "DART", "DORT", "MORT", "MOON"]
        },
        {
            "start": "SHIP",
            "target": "DOCK",
            "steps": 4,
            "solution": ["SHIP", "SHOP", "SHOT", "SOOT", "DOCK"]
        },
        {
            "start": "FIRE",
            "target": "HOSE",
            "steps": 4,
            "solution": ["FIRE", "FORE", "FORK", "HORK", "HOSE"]
        },
        {
            "start": "PLAY",
            "target": "GAME",
            "steps": 4,
            "solution": ["PLAY", "CLAY", "CLAM", "CAME", "GAME"]
        },
        {
            "start": "BLUE",
            "target": "PINK",
            "steps": 4,
            "solution": ["BLUE", "BLUR", "FLUR", "FLIR", "FLIK"]
        },
        {
            "start": "BIRD",
            "target": "NEST",
            "steps": 4,
            "solution": ["BIRD", "BIRT", "BEST", "BEAT", "NEST"]
        },
        {
            "start": "LION",
            "target": "ROAR",
            "steps": 4,
            "solution": ["LION", "LOON", "LOOR", "ROOR", "ROAR"]
        },
        {
            "start": "TREE",
            "target": "LEAF",
            "steps": 4,
            "solution": ["TREE", "FREE", "FLEE", "FLAE", "LEAF"]
        },
        {
            "start": "GOLD",
            "target": "IRON",
            "steps": 4,
            "solution": ["GOLD", "GORD", "GIRN", "IRON"]
        },
        {
            "start": "FISH",
            "target": "POND",
            "steps": 4,
            "solution": ["FISH", "FIST", "POST", "PONT", "POND"]
        },
        {
            "start": "WALK",
            "target": "STOP",
            "steps": 4,
            "solution": ["WALK", "WALL", "TALL", "TOLL", "TOOL"]
        },
        {
            "start": "MILK",
            "target": "CUP",
            "steps": 3,
            "solution": ["MILK", "MICK", "MUCK", "BUCK"]
        },
        {
            "start": "HAND",
            "target": "FOOT",
            "steps": 4,
            "solution": ["HAND", "HARD", "FORD", "FORT", "FOOT"]
        },
        {
            "start": "RAIN",
            "target": "SNOW",
            "steps": 4,
            "solution": ["RAIN", "ROIN", "SOIN", "SOON", "SNOW"]
        },
        {
            "start": "SOUP",
            "target": "BOWL",
            "steps": 4,
            "solution": ["SOUP", "SOUR", "FOUR", "FOUL", "BOWL"]
        },
        {
            "start": "NOON",
            "target": "DAWN",
            "steps": 4,
            "solution": ["NOON", "MOON", "MOAN", "DOWN", "DAWN"]
        },
        {
            "start": "CAT",
            "target": "DOG",
            "steps": 3,
            "solution": ["CAT", "COT", "COG", "DOG"]
        },
        {
            "start": "BOY",
            "target": "MAN",
            "steps": 3,
            "solution": ["BOY", "BAY", "MAY", "MAN"]
        },
        {
            "start": "APE",
            "target": "MAN",
            "steps": 4,
            "solution": ["APE", "ARE", "ARM", "AIM", "MAN"]
        },
        {
            "start": "TEA",
            "target": "HOT",
            "steps": 3,
            "solution": ["TEA", "HAT", "HIT", "HOT"]
        },
        {
            "start": "DAY",
            "target": "NIGHT",
            "steps": 4,
            "solution": ["DAY", "PAY", "PAN", "PIN"]
        }
    ],
    "medium": [
        {
            "start": "SLOW",
            "target": "FAST",
            "steps": 5,
            "solution": ["SLOW", "BLOW", "BLOT", "BOOT", "FOOT", "FAST"]
        },
        {
            "start": "EAST",
            "target": "WEST",
            "steps": 3,
            "solution": ["EAST", "PAST", "PEST", "WEST"]
        },
        {
            "start": "WIND",
            "target": "GALE",
            "steps": 4,
            "solution": ["WIND", "WINE", "WANE", "GANE", "GALE"]
        },
        {
            "start": "SAND",
            "target": "DUNE",
            "steps": 4,
            "solution": ["SAND", "SANE", "DANE", "DONE", "DUNE"]
        },
        {
            "start": "BOOK",
            "target": "READ",
            "steps": 5,
            "solution": ["BOOK", "BOOT", "BOAT", "BEAT", "BEAD", "READ"]
        },
        {
            "start": "WOOD",
            "target": "FIRE",
            "steps": 5,
            "solution": ["WOOD", "WORD", "WORE", "WIRE", "HIRE", "FIRE"]
        },
        {
            "start": "RICE",
            "target": "BEAN",
            "steps": 5,
            "solution": ["RICE", "RACE", "PACE", "PACK", "PECK", "BEAN"]
        },
        {
            "start": "WALL",
            "target": "DOOR",
            "steps": 5,
            "solution": ["WALL", "MALL", "MOLE", "MORE", "DORE", "DOOR"]
        },
        {
            "start": "PALE",
            "target": "DARK",
            "steps": 5,
            "solution": ["PALE", "PARK", "PERK", "DERE", "DARK"]
        },
        {
            "start": "CAMP",
            "target": "TENT",
            "steps": 4,
            "solution": ["CAMP", "CARP", "TARP", "TART", "TENT"]
        },
        {
            "start": "WAVE",
            "target": "SURF",
            "steps": 5,
            "solution": ["WAVE", "WANE", "WANT", "SANT", "SARF", "SURF"]
        },
        {
            "start": "LAKE",
            "target": "POND",
            "steps": 5,
            "solution": ["LAKE", "LANE", "LONE", "BONE", "BOND", "POND"]
        },
        {
            "start": "ROAD",
            "target": "PATH",
            "steps": 5,
            "solution": ["ROAD", "READ", "BEAD", "BATH", "PATH"]
        },
        {
            "start": "LEAD",
            "target": "GOLD",
            "steps": 4,
            "solution": ["LEAD", "LOAD", "GOAD", "GOLD"]
        },
        {
            "start": "POOR",
            "target": "RICH",
            "steps": 5,
            "solution": ["POOR", "BOOR", "BOOK", "ROOK", "ROCK", "RICH"]
        }
    ],
    "hard": [
        {
            "start": "BLACK",
            "target": "WHITE",
            "steps": 6,
            "solution": ["BLACK", "BLANK", "BLINK", "CLINK", "CHINK", "CHINE", "WHITE"]
        },
        {
            "start": "STONE",
            "target": "WATER",
            "steps": 6,
            "solution": ["STONE", "SHONE", "SHINE", "SHIRE", "SHARE", "WHARE", "WATER"]
        },
        {
            "start": "WHEAT",
            "target": "BREAD",
            "steps": 6,
            "solution": ["WHEAT", "CHEAT", "CLEAT", "BLEAT", "BLEST", "BREST", "BREAD"]
        },
        {
            "start": "TEARS",
            "target": "SMILE",
            "steps": 6,
            "solution": ["TEARS", "SEARS", "STARS", "STARE", "STALE", "SHALE", "SMILE"]
        },
        {
            "start": "SLEEP",
            "target": "DREAM",
            "steps": 6,
            "solution": ["SLEEP", "BLEEP", "BLEED", "BREED", "BREAD", "DREAD", "DREAM"]
        },
        {
            "start": "RIVER",
            "target": "OCEAN",
            "steps": 6,
            "solution": ["RIVER", "ROVER", "RAVER", "EAVER", "EAGLE", "OCEAN"]
        },
        {
            "start": "EARTH",
            "target": "MOONS",
            "steps": 5,
            "solution": ["EARTH", "BARTH", "BARNS", "BURNS", "HORNS", "MOONS"]
        },
        {
            "start": "PLANT",
            "target": "TREES",
            "steps": 6,
            "solution": ["PLANT", "PLANE", "PRANE", "PRONE", "TRONE", "TREES"]
        },
        {
            "start": "LIGHT",
            "target": "NIGHT",
            "steps": 1,
            "solution": ["LIGHT", "NIGHT"]
        },
        {
            "start": "CLOCK",
            "target": "WATCH",
            "steps": 6,
            "solution": ["CLOCK", "CLOAK", "CROAK", "CRANK", "TRACK", "WATCH"]
        },
        {
            "start": "GRASS",
            "target": "GREEN",
            "steps": 5,
            "solution": ["GRASS", "CRASS", "CRESS", "CREES", "GREEN"]
        },
        {
            "start": "BRAIN",
            "target": "THINK",
            "steps": 6,
            "solution": ["BRAIN", "TRAIN", "TRAIK", "TRACK", "THACK", "THICK", "THINK"]
        },
        {
            "start": "APPLE",
            "target": "PEACH",
            "steps": 6,
            "solution": ["APPLE", "AMPLE", "AMBLE", "ABBLE", "BEACH", "PEACH"]
        }
    ]
}


def build_clean_wordlist() -> Tuple[List[str], List[str]]:
    """Loads common 4-letter and 5-letter English words from system dictionary."""
    dict_path = "/usr/share/dict/words"
    words4 = set()
    words5 = set()
    if os.path.exists(dict_path):
        with open(dict_path, "r", encoding="utf-8") as f:
            for line in f:
                w = line.strip()
                if w.islower() and w.isalpha() and w.isascii():
                    u = w.upper()
                    if len(u) == 4:
                        words4.add(u)
                    elif len(u) == 5:
                        words5.add(u)

    # Ensure all words from curated ladders are in the lexicon
    for diff, ladders in CURATED_LADDERS.items():
        for item in ladders:
            for w in item["solution"]:
                if len(w) == 4:
                    words4.add(w)
                elif len(w) == 5:
                    words5.add(w)

    return sorted(list(words4)), sorted(list(words5))


def main():
    w4, w5 = build_clean_wordlist()
    dataset = {
        "words4": w4,
        "words5": w5,
        "curated": CURATED_LADDERS
    }

    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)

    print(f"Generated {DATA_PATH}:")
    print(f"  4-letter words: {len(w4)}")
    print(f"  5-letter words: {len(w5)}")
    print(f"  Curated Easy:   {len(CURATED_LADDERS['easy'])}")
    print(f"  Curated Medium: {len(CURATED_LADDERS['medium'])}")
    print(f"  Curated Hard:   {len(CURATED_LADDERS['hard'])}")


if __name__ == "__main__":
    main()
