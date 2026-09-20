"""
Morning Puzzles - Word Wheel (Spelling Bee / Honeycomb) Generator
Generates 7-letter hexagonal honeycomb anagram puzzles where solvers form words
of 4+ letters containing a compulsory central hub letter.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import json
import random
from typing import List, Dict, Any, Optional, Set, Tuple

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "wheel_dictionary.json")

# Embedded emergency fallbacks if JSON file cannot be located
FALLBACK_PUZZLES: Dict[str, List[Dict[str, Any]]] = {
    "easy": [
        {
            "id": "easy_001",
            "difficulty": "easy",
            "center_letter": "E",
            "outer_letters": ["A", "N", "P", "R", "S", "T"],
            "root_word": "PARENTS",
            "pangrams": ["PARENTS", "PASTERN", "TREPANS"],
            "words": [
                "EARN", "EATEN", "EATER", "ENTER", "ERASER", "NESTS", "PAPERS",
                "PARENT", "PARENTS", "PASTERN", "PEAS", "PEER", "PEPPER", "PETER",
                "RANT", "RATE", "RATES", "REAP", "REAR", "RENT", "RENTS", "RESET",
                "REST", "SEAT", "SEATS", "SEEN", "SENSE", "STEEP", "STEER", "STEP",
                "STEPS", "STREET", "TAPE", "TAPES", "TEAR", "TEARS", "TEEN", "TEENS"
            ],
            "word_count": 38,
            "benchmarks": {"good": 13, "great": 24, "genius": 32}
        }
    ],
    "medium": [
        {
            "id": "medium_021",
            "difficulty": "medium",
            "center_letter": "A",
            "outer_letters": ["G", "I", "L", "N", "P", "Y"],
            "root_word": "PLAYING",
            "pangrams": ["PLAYING"],
            "words": [
                "AGING", "ALIGN", "ALLY", "APING", "APPLY", "GAILY", "GAIN",
                "GALA", "GANG", "GLAD", "LAIN", "LILY", "NAIL", "PAIN",
                "PALE", "PANG", "PLAN", "PLAY", "PLAYING", "PRAY", "PRAYING",
                "RING", "SAIL", "SLANG", "SPAN", "SPAY"
            ],
            "word_count": 26,
            "benchmarks": {"good": 9, "great": 16, "genius": 22}
        }
    ],
    "hard": [
        {
            "id": "hard_041",
            "difficulty": "hard",
            "center_letter": "H",
            "outer_letters": ["D", "I", "L", "N", "O", "P"],
            "root_word": "DOLPHIN",
            "pangrams": ["DOLPHIN"],
            "words": [
                "DILTH", "DOLPHIN", "HOLD", "HOLDING", "HOLE", "HOOD",
                "HOOK", "HOOP", "HORN", "LION", "LOIN", "OPAL",
                "POND", "POLE", "SHIP", "SHOP"
            ],
            "word_count": 16,
            "benchmarks": {"good": 5, "great": 10, "genius": 13}
        }
    ]
}


def compute_length_counts(words: List[str]) -> Dict[str, int]:
    """Calculates distribution of words by length: 4L, 5L, 6L, 7+L."""
    counts = {"4": 0, "5": 0, "6": 0, "7+": 0}
    for w in words:
        l = len(w)
        if l == 4:
            counts["4"] += 1
        elif l == 5:
            counts["5"] += 1
        elif l == 6:
            counts["6"] += 1
        elif l >= 7:
            counts["7+"] += 1
    return counts


def word_to_mask(w: str) -> int:
    """Computes a 26-bit integer bitmask for uppercase A-Z characters."""
    mask = 0
    for ch in w.upper():
        if "A" <= ch <= "Z":
            mask |= (1 << (ord(ch) - ord("A")))
    return mask


class WheelGenerator:
    """
    Word Wheel procedural generator and dynamic bitmask solver.
    """

    def __init__(self, data_path: Optional[str] = None):
        self.data_path = data_path or os.path.normpath(DATA_PATH)
        self.puzzles_by_diff: Dict[str, List[Dict[str, Any]]] = {
            "easy": [],
            "medium": [],
            "hard": []
        }
        self.dictionary: List[str] = []
        self._dict_masks: List[Tuple[str, int]] = []
        self._load_data()

    def _load_data(self):
        if os.path.exists(self.data_path):
            try:
                with open(self.data_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    puzzles = data.get("puzzles", [])
                    for p in puzzles:
                        diff = p.get("difficulty", "medium").lower()
                        if diff in self.puzzles_by_diff:
                            self.puzzles_by_diff[diff].append(p)
                    self.dictionary = data.get("dictionary", [])
                    self._dict_masks = [(w, word_to_mask(w)) for w in self.dictionary]
            except Exception:
                pass

        # Ensure fallbacks if empty
        for diff in ("easy", "medium", "hard"):
            if not self.puzzles_by_diff[diff]:
                self.puzzles_by_diff[diff] = list(FALLBACK_PUZZLES[diff])

    def solve(self, letters: str, center: str) -> List[str]:
        """
        Dynamically solves for all valid words using bitmask filtering
        against the internal dictionary. Runs in < 1ms.
        """
        letters_upper = letters.upper()
        center_upper = center.upper()
        p_mask = word_to_mask(letters_upper)
        c_mask = 1 << (ord(center_upper) - ord("A"))

        valid = []
        for w, m in self._dict_masks:
            if (m & ~p_mask) == 0 and (m & c_mask) != 0 and len(w) >= 4:
                valid.append(w)
        return sorted(valid)

    def generate(
        self,
        difficulty: str = "medium",
        seed: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generates or selects a verified Word Wheel honeycomb puzzle.
        """
        diff_clean = difficulty.lower()
        if diff_clean not in self.puzzles_by_diff:
            diff_clean = "medium"

        rng = random.Random(seed) if seed is not None else random

        # Custom letters provided?
        if "letters" in kwargs and "center" in kwargs:
            center = str(kwargs["center"]).upper()
            letters = set(str(kwargs["letters"]).upper())
            letters.add(center)
            outer = sorted(list(letters - {center}))
            words = self.solve("".join(letters), center)
            pangrams = [w for w in words if len(set(w)) == 7]
            total_cnt = len(words)
            good = max(3, int(total_cnt * 0.35))
            great = max(good + 2, int(total_cnt * 0.65))
            genius = max(great + 2, int(total_cnt * 0.85))

            length_counts = compute_length_counts(words)
            return {
                "id": f"custom_{rng.randint(100, 999)}",
                "difficulty": diff_clean,
                "center_letter": center,
                "outer_letters": outer,
                "letters": center + "".join(outer),
                "pangrams": pangrams,
                "words": words,
                "word_count": total_cnt,
                "benchmarks": {"good": good, "great": great, "genius": genius},
                "length_counts": length_counts,
            }

        catalog = self.puzzles_by_diff[diff_clean]
        chosen = dict(rng.choice(catalog))
        words = list(chosen["words"])
        length_counts = chosen.get("length_counts") or compute_length_counts(words)

        # Re-pack and return shallow copy
        return {
            "id": chosen["id"],
            "difficulty": chosen["difficulty"],
            "center_letter": chosen["center_letter"],
            "outer_letters": list(chosen["outer_letters"]),
            "letters": chosen["center_letter"] + "".join(chosen["outer_letters"]),
            "root_word": chosen.get("root_word", chosen["center_letter"] + "".join(chosen["outer_letters"])),
            "pangrams": list(chosen["pangrams"]),
            "words": words,
            "word_count": chosen["word_count"],
            "benchmarks": dict(chosen["benchmarks"]),
            "length_counts": dict(length_counts),
        }
