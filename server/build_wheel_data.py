#!/usr/bin/env python3
"""
Builds server/data/wheel_dictionary.json with:
1. A dictionary of common English words (4-12 letters).
2. Curated and verified 7-letter honeycomb puzzles for Easy, Medium, and Hard tiers.
"""

import os
import sys
import json
from typing import List, Dict, Set, Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.generators.wordsearch_dataset import (
    WORDSEARCH_THEMES_EASY,
    WORDSEARCH_THEMES_MEDIUM,
    WORDSEARCH_THEMES_HARD,
)

# Base list of common words from project datasets
def collect_project_words() -> Set[str]:
    words = set()
    for d in [WORDSEARCH_THEMES_EASY, WORDSEARCH_THEMES_MEDIUM, WORDSEARCH_THEMES_HARD]:
        for theme, wlist in d.items():
            for w in wlist:
                w_clean = w.strip().upper()
                if len(w_clean) >= 4 and w_clean.isalpha():
                    words.add(w_clean)

    jumbles_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "jumbles.json")
    if os.path.exists(jumbles_path):
        with open(jumbles_path, "r", encoding="utf-8") as f:
            for item in json.load(f):
                for w in item.get("words", []):
                    w_clean = w.strip().upper()
                    if len(w_clean) >= 4 and w_clean.isalpha():
                        words.add(w_clean)
                for w in item.get("answer", "").split():
                    w_clean = "".join(ch for ch in w.upper() if ch.isalpha())
                    if len(w_clean) >= 4:
                        words.add(w_clean)

    ladder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "ladder_words.json")
    if os.path.exists(ladder_path):
        with open(ladder_path, "r", encoding="utf-8") as f:
            lw = json.load(f)
            for w in lw.get("words4", []):
                if w.isalpha():
                    words.add(w.upper())
            for w in lw.get("words5", []):
                if w.isalpha():
                    words.add(w.upper())

    # Add common 6-10 letter English words from standard dictionary
    if os.path.exists("/usr/share/dict/words"):
        with open("/usr/share/dict/words", "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                w = line.strip()
                if w.islower() and w.isalpha() and 4 <= len(w) <= 10:
                    words.add(w.upper())

    return words


# 60 curated pangram seeds: (pangram, center_letter, difficulty)
CURATED_PUZZLE_SEEDS = [
    # EASY (Common center vowels, high subword counts: 30-40 words)
    ("PARENTS", "E", "easy"),
    ("GARDENS", "E", "easy"),
    ("FLOWERS", "E", "easy"),
    ("BLANKET", "E", "easy"),
    ("CABINET", "E", "easy"),
    ("PIRATES", "E", "easy"),
    ("ROASTED", "E", "easy"),
    ("HEATING", "E", "easy"),
    ("HELPING", "E", "easy"),
    ("PAINTED", "E", "easy"),
    ("POINTER", "E", "easy"),
    ("MONSTER", "E", "easy"),
    ("WONDERS", "E", "easy"),
    ("HUNTERS", "E", "easy"),
    ("LEOPARD", "E", "easy"),
    ("PANTHER", "E", "easy"),
    ("PELICAN", "E", "easy"),
    ("HARVEST", "E", "easy"),
    ("SECTION", "E", "easy"),
    ("LOBSTER", "E", "easy"),

    # MEDIUM (Balanced consonant/vowel center letters, 18-28 words)
    ("PLAYING", "A", "medium"),
    ("WALKING", "A", "medium"),
    ("BOATING", "O", "medium"),
    ("SURFING", "I", "medium"),
    ("CAMPING", "I", "medium"),
    ("FARMING", "I", "medium"),
    ("CENTRAL", "A", "medium"),
    ("PROJECT", "O", "medium"),
    ("BALCONY", "O", "medium"),
    ("CHIMNEY", "I", "medium"),
    ("CRYSTAL", "A", "medium"),
    ("JOURNEY", "O", "medium"),
    ("MAJESTY", "A", "medium"),
    ("UNIFORM", "O", "medium"),
    ("VAMPIRE", "A", "medium"),
    ("FORTUNE", "O", "medium"),
    ("PENCILS", "I", "medium"),
    ("FURNACE", "A", "medium"),
    ("COURAGE", "O", "medium"),
    ("RAINBOW", "A", "medium"),

    # HARD (Tighter letter combinations, rarer center letters, 12-18 words)
    ("DOLPHIN", "H", "hard"),
    ("TRIUMPH", "U", "hard"),
    ("TRIUMPH", "H", "hard"),
    ("KINGDOM", "K", "hard"),
    ("BREWING", "W", "hard"),
    ("CURLING", "U", "hard"),
    ("DELIGHT", "G", "hard"),
    ("FIGURES", "U", "hard"),
    ("FLAVORS", "V", "hard"),
    ("DRAWING", "W", "hard"),
    ("BASTION", "B", "hard"),
    ("CINEMAS", "M", "hard"),
    ("CITADEL", "D", "hard"),
    ("COLUMNS", "U", "hard"),
    ("CINDERS", "D", "hard"),
    ("ALCOVES", "V", "hard"),
    ("ECLAIRS", "C", "hard"),
    ("OUTRAGE", "G", "hard"),
    ("PROBLEM", "M", "hard"),
    ("ZODIACS", "Z", "hard"),
]


def word_to_mask(w: str) -> int:
    mask = 0
    for ch in w.upper():
        if "A" <= ch <= "Z":
            mask |= (1 << (ord(ch) - ord("A")))
    return mask


def build_dataset():
    print("Collecting project words...")
    all_words = collect_project_words()
    print(f"Total vocabulary collected: {len(all_words)} words.")

    clean_dict = sorted(list(set(w for w in all_words if 4 <= len(w) <= 12 and w.isalpha())))
    for root_word, _, _ in CURATED_PUZZLE_SEEDS:
        if root_word.upper() not in clean_dict:
            clean_dict.append(root_word.upper())
    clean_dict.sort()
    word_masks = [(w, word_to_mask(w)) for w in clean_dict]

    puzzles_data = []

    for idx, (root_word, center, diff) in enumerate(CURATED_PUZZLE_SEEDS):
        letters_set = set(root_word.upper())
        assert len(letters_set) == 7, f"{root_word} has {len(letters_set)} unique letters, expected 7"
        assert center.upper() in letters_set, f"{center} not in {root_word}"

        p_mask = word_to_mask(root_word)
        c_mask = 1 << (ord(center.upper()) - ord("A"))

        outer = sorted(list(letters_set - {center.upper()}))

        valid_words = []
        pangrams = [root_word.upper()]

        for w, m in word_masks:
            if (m & ~p_mask) == 0 and (m & c_mask) != 0 and len(w) >= 4:
                valid_words.append(w)
                if m == p_mask and w != root_word.upper():
                    pangrams.append(w)

        valid_words = sorted(list(set(valid_words)))
        pangrams = sorted(list(set(pangrams)))

        # Subsample/cap words to preserve ideal difficulty quotas
        if diff == "easy" and len(valid_words) > 38:
            pangram_set = set(pangrams)
            other_words = [w for w in valid_words if w not in pangram_set]
            valid_words = sorted(list(pangram_set) + other_words[:38 - len(pangram_set)])
        elif diff == "medium" and len(valid_words) > 26:
            pangram_set = set(pangrams)
            other_words = [w for w in valid_words if w not in pangram_set]
            valid_words = sorted(list(pangram_set) + other_words[:26 - len(pangram_set)])
        elif diff == "hard" and len(valid_words) > 16:
            pangram_set = set(pangrams)
            other_words = [w for w in valid_words if w not in pangram_set]
            valid_words = sorted(list(pangram_set) + other_words[:16 - len(pangram_set)])

        total_cnt = len(valid_words)

        good = max(3, int(total_cnt * 0.35))
        great = max(good + 2, int(total_cnt * 0.65))
        genius = max(great + 2, int(total_cnt * 0.85))

        c4 = sum(1 for w in valid_words if len(w) == 4)
        c5 = sum(1 for w in valid_words if len(w) == 5)
        c6 = sum(1 for w in valid_words if len(w) == 6)
        c7 = sum(1 for w in valid_words if len(w) >= 7)

        puzzle_id = f"{diff}_{idx + 1:03d}"
        puzzles_data.append({
            "id": puzzle_id,
            "difficulty": diff,
            "center_letter": center.upper(),
            "outer_letters": outer,
            "root_word": root_word.upper(),
            "pangrams": pangrams,
            "words": valid_words,
            "word_count": total_cnt,
            "benchmarks": {
                "good": good,
                "great": great,
                "genius": genius
            },
            "length_counts": {
                "4": c4,
                "5": c5,
                "6": c6,
                "7+": c7
            }
        })
        print(f"[{diff.upper()}] {puzzle_id}: center={center} outer={''.join(outer)} -> {total_cnt} words, {len(pangrams)} pangram(s)")

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "wheel_dictionary.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({
            "puzzles": puzzles_data,
            "dictionary": clean_dict[:6500]
        }, f, indent=2)

    print(f"\nSuccessfully generated {len(puzzles_data)} curated honeycombs to {output_path}!")


if __name__ == "__main__":
    build_dataset()
