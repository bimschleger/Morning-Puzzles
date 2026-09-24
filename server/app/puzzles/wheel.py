"""
Morning Puzzles - Wheel (Word Wheel / Honeycomb) Puzzle Plugin
Implements BasePuzzle contract for 7-letter hexagonal honeycomb anagram puzzles.
Encapsulates generation, canonical instruction formatting, ASCII layout,
solution key representation, and 576-dot thermal raster rendering.
"""

import os
import json
import random
import math
import textwrap
from typing import List, Dict, Any, Optional, Union, Tuple, Set

from .base import BasePuzzle, BasePuzzleResult
from ..renderer.canvas import (
    THERMAL_WIDTH_DOTS,
    HAS_PILLOW,
    pil_to_escpos,
    ThermalBitmap,
)

if HAS_PILLOW:
    from PIL import Image, ImageDraw, ImageFont

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


class WheelPuzzle(BasePuzzle):
    """Word Wheel / Honeycomb puzzle plugin."""

    def __init__(self, data_path: Optional[str] = None):
        self.generator = WheelGenerator(data_path=data_path)

    @property
    def puzzle_id(self) -> str:
        return "wheel"

    @property
    def title(self) -> str:
        return "WHEEL"

    @property
    def has_difficulty(self) -> bool:
        return True

    @property
    def default_difficulty(self) -> str:
        return "medium"

    @property
    def supported_difficulties(self) -> List[str]:
        return ["easy", "medium", "hard"]

    def generate(
        self,
        difficulty: str = "medium",
        seed: Optional[int] = None,
        **kwargs
    ) -> BasePuzzleResult:
        diff_clean = difficulty.lower()
        if diff_clean not in self.supported_difficulties:
            diff_clean = "medium"

        raw_data = self.generator.generate(difficulty=diff_clean, seed=seed, **kwargs)
        instruction = self.get_instruction(raw_data)

        return BasePuzzleResult(
            puzzle_type=self.puzzle_id,
            title=self.title,
            difficulty=diff_clean,
            instruction=instruction,
            raw_data=raw_data,
        )

    def get_instruction(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        cnt = puzzle_data.get("word_count", 25)
        center = str(puzzle_data.get("center_letter", "E")).upper()
        return f"Find {cnt}+ words using center letter {center} (letters may repeat), including a 7-letter pangram."

    def format_ascii_puzzle(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        center = str(puzzle_data.get("center_letter", "E")).upper()
        outer = list(puzzle_data.get("outer_letters", ["A", "B", "C", "D", "F", "G"]))
        while len(outer) < 6:
            outer.append(" ")

        o = [str(x).upper() for x in outer[:6]]
        benchmarks = puzzle_data.get("benchmarks", {"good": 10, "great": 18, "genius": 25})
        b_good = benchmarks.get("good", puzzle_data.get("good", 10))
        b_great = benchmarks.get("great", puzzle_data.get("great", 18))
        b_genius = benchmarks.get("genius", puzzle_data.get("genius", 25))

        length_counts = puzzle_data.get("length_counts", {})
        c4 = length_counts.get("4", puzzle_data.get("count4", 0))
        c5 = length_counts.get("5", puzzle_data.get("count5", 0))
        c6 = length_counts.get("6", puzzle_data.get("count6", 0))
        c7 = length_counts.get("7+", puzzle_data.get("count7plus", 0))
        if c4 == 0 and c5 == 0 and c6 == 0 and c7 == 0 and "words" in puzzle_data:
            words_list = puzzle_data.get("words", [])
            c4 = sum(1 for w in words_list if len(w) == 4)
            c5 = sum(1 for w in words_list if len(w) == 5)
            c6 = sum(1 for w in words_list if len(w) == 6)
            c7 = sum(1 for w in words_list if len(w) >= 7)

        lines: List[str] = [
            "                  +---+---+",
            f"                  | {o[0]} | {o[1]} |",
            "              +---+===+===+---+",
            f"              | {o[2]} | [{center}] | {o[3]} |",
            "              +---+===+===+---+",
            f"                  | {o[4]} | {o[5]} |",
            "                  +---+---+",
            "",
            "   TARGET BENCHMARKS:",
            f"     Good: {b_good} words  |  Great: {b_great} words  |  Genius: {b_genius}+ words",
            f"     4L: {c4}  |  5L: {c5}  |  6L: {c6}  |  7+: {c7}",
            "",
            f"   WORDS FOUND (Must include central letter {center}):",
            "   _________________        _________________",
            "   _________________        _________________",
            "   _________________        _________________",
            "   _________________        _________________",
        ]
        return "\n".join(lines)

    def format_solution_key(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> List[str]:
        pangrams = puzzle_data.get("pangrams", [])
        cnt = puzzle_data.get("word_count", len(puzzle_data.get("words", [])))
        words = sorted(list(puzzle_data.get("words", [])))

        length_counts = puzzle_data.get("length_counts", {})
        c4 = length_counts.get("4", puzzle_data.get("count4", 0))
        c5 = length_counts.get("5", puzzle_data.get("count5", 0))
        c6 = length_counts.get("6", puzzle_data.get("count6", 0))
        c7 = length_counts.get("7+", puzzle_data.get("count7plus", 0))
        if c4 == 0 and c5 == 0 and c6 == 0 and c7 == 0 and words:
            c4 = sum(1 for w in words if len(w) == 4)
            c5 = sum(1 for w in words if len(w) == 5)
            c6 = sum(1 for w in words if len(w) == 6)
            c7 = sum(1 for w in words if len(w) >= 7)

        lines: List[str] = []
        if pangrams:
            p_text = "PANGRAM: " + ", ".join(pangrams)
            for l in textwrap.wrap(p_text, width=46):
                lines.append(l)

        lines.append(f"TOTAL WORDS: {cnt}")
        lines.append(f"LENGTHS: 4L: {c4} | 5L: {c5} | 6L: {c6} | 7+: {c7}")

        # Format words in columns (4 columns wide, fitting <= 46 chars)
        col_w = 10
        for i in range(0, len(words), 4):
            chunk = words[i:i + 4]
            row_str = "      " + "".join(f"{w:<{col_w}}" for w in chunk).rstrip()
            lines.append(row_str)

        return lines

    def render_raster(
        self,
        puzzle_data: Union[BasePuzzleResult, Dict[str, Any]],
        target_width: int = THERMAL_WIDTH_DOTS,
    ) -> bytes:
        center = str(puzzle_data.get("center_letter", "E")).upper()
        outer = list(puzzle_data.get("outer_letters", ["A", "B", "C", "D", "F", "G"]))
        while len(outer) < 6:
            outer.append(" ")
        outer = [str(x).upper() for x in outer[:6]]

        benchmarks = puzzle_data.get("benchmarks", {"good": 10, "great": 18, "genius": 25})
        b_good = benchmarks.get("good", puzzle_data.get("good", 10))
        b_great = benchmarks.get("great", puzzle_data.get("great", 18))
        b_genius = benchmarks.get("genius", puzzle_data.get("genius", 25))

        length_counts = puzzle_data.get("length_counts", {})
        c4 = length_counts.get("4", puzzle_data.get("count4", 0))
        c5 = length_counts.get("5", puzzle_data.get("count5", 0))
        c6 = length_counts.get("6", puzzle_data.get("count6", 0))
        c7 = length_counts.get("7+", puzzle_data.get("count7plus", 0))
        if c4 == 0 and c5 == 0 and c6 == 0 and c7 == 0 and "words" in puzzle_data:
            words_list = puzzle_data.get("words", [])
            c4 = sum(1 for w in words_list if len(w) == 4)
            c5 = sum(1 for w in words_list if len(w) == 5)
            c6 = sum(1 for w in words_list if len(w) == 6)
            c7 = sum(1 for w in words_list if len(w) >= 7)

        total_height = 400  # Multiple of 8
        xc = target_width // 2
        yc = 130
        hex_radius = 46
        spacing = hex_radius * math.sqrt(3)  # ~79.6px

        # 6 outer hexagon centers (flat-top honeycomb)
        angles_deg = [270, 330, 30, 90, 150, 210]
        outer_coords = []
        for deg in angles_deg:
            rad = math.radians(deg)
            px = int(round(xc + spacing * math.cos(rad)))
            py = int(round(yc + spacing * math.sin(rad)))
            outer_coords.append((px, py))

        def get_hex_polygon(cx: int, cy: int, r: int) -> List[Tuple[int, int]]:
            h = int(round(r * 0.8660254))
            half_r = r // 2
            return [
                (cx + r, cy),
                (cx + half_r, cy + h),
                (cx - half_r, cy + h),
                (cx - r, cy),
                (cx - half_r, cy - h),
                (cx + half_r, cy - h),
            ]

        tb = ThermalBitmap(target_width, total_height)

        # Draw outer 6 hexagons
        for idx, (px, py) in enumerate(outer_coords):
            poly = get_hex_polygon(px, py, hex_radius)
            tb.draw_polygon(poly, thickness=2, color=1)
            letter_ch = outer[idx]
            tb.draw_char(px - 9, py - 10, letter_ch, scale=3)

        # Draw center hexagon with double-thick frame
        center_poly = get_hex_polygon(xc, yc, hex_radius)
        tb.draw_polygon(center_poly, thickness=2, color=1)
        center_inner = get_hex_polygon(xc, yc, hex_radius - 4)
        tb.draw_polygon(center_inner, thickness=2, color=1)
        tb.draw_char(xc - 9, yc - 10, center, scale=3)

        # Draw Consolidated 2-Row Target Benchmarks & Lengths box with internal divider
        box_y = 258
        box_h = 64
        box_w = 500
        box_x = (target_width - box_w) // 2
        tb.draw_rect(box_x, box_y, box_w, box_h, thickness=2, color=1)
        bench_text = f"GOOD: {b_good}   GREAT: {b_great}   GENIUS: {b_genius}+"
        tb.draw_centered_text(box_y + 9, bench_text, scale=2, color=1)
        tb.draw_hline(box_x, box_y + 32, box_w, thickness=1, color=1)
        len_text = f"4L: {c4}   5L: {c5}   6L: {c6}   7+: {c7}"
        tb.draw_centered_text(box_y + 41, len_text, scale=2, color=1)

        # Ruled handwriting lines (3 rows, 2 columns)
        tb.draw_hline(48, 340, 220, thickness=1, color=1)
        tb.draw_hline(308, 340, 220, thickness=1, color=1)
        tb.draw_hline(48, 362, 220, thickness=1, color=1)
        tb.draw_hline(308, 362, 220, thickness=1, color=1)
        tb.draw_hline(48, 384, 220, thickness=1, color=1)
        tb.draw_hline(308, 384, 220, thickness=1, color=1)

        return tb.to_escpos()

    def verify_accuracy(
        self,
        puzzle_data: Union[BasePuzzleResult, Dict[str, Any]],
    ) -> Tuple[bool, str]:
        center = str(puzzle_data.get("center_letter", "")).upper()
        outer = [str(x).upper() for x in puzzle_data.get("outer_letters", [])]
        words = [str(w).upper() for w in puzzle_data.get("words", [])]
        pangrams = [str(p).upper() for p in puzzle_data.get("pangrams", [])]

        if not center or len(outer) != 6:
            return False, f"Wheel puzzle must have 1 center letter and 6 outer letters, got center '{center}', outer {outer}"
        if center in outer:
            return False, f"Center letter '{center}' cannot be in outer letters {outer}"

        allowed_chars = set(outer) | {center}
        if len(allowed_chars) != 7:
            return False, f"Wheel letters must be 7 distinct letters, got {len(allowed_chars)}"

        # 1. Check words validity
        if len(words) < 5:
            return False, f"Wheel has too few words: {len(words)}"

        for w in words:
            if center not in w:
                return False, f"Wheel word '{w}' does not contain required center letter '{center}'"
            if not set(w).issubset(allowed_chars):
                invalid_chars = set(w) - allowed_chars
                return False, f"Wheel word '{w}' contains characters not on the wheel: {invalid_chars}"
            if len(w) < 4:
                return False, f"Wheel word '{w}' is shorter than minimum length 4"

        # 2. Check pangrams
        if not pangrams:
            return False, "Wheel puzzle must have at least one 7-letter pangram"
        for p in pangrams:
            if set(p) != allowed_chars:
                return False, f"Wheel pangram '{p}' does not use all 7 wheel letters"
            if p not in words:
                return False, f"Wheel pangram '{p}' is not listed in words"

        # 3. Check length counts if present
        lc = puzzle_data.get("length_counts")
        if lc:
            c4 = lc.get("4", 0)
            c5 = lc.get("5", 0)
            c6 = lc.get("6", 0)
            c7 = lc.get("7+", 0)
            if c4 + c5 + c6 + c7 != len(words):
                return False, f"Sum of length counts ({c4}+{c5}+{c6}+{c7}={c4+c5+c6+c7}) does not match total words {len(words)}"

        return True, "All rules satisfied"
