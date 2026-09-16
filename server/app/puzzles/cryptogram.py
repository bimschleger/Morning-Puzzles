"""
Morning Puzzles - Cryptogram Plugin
Encapsulates generation, canonical instruction formatting, ASCII layout,
solution key formatting, and 576-dot thermal raster rendering.
"""

import os
import json
import random
import string
import textwrap
from typing import List, Tuple, Dict, Any, Optional, Union

from .base import BasePuzzle, BasePuzzleResult
from ..renderer.canvas import (
    THERMAL_WIDTH_DOTS,
    HAS_PILLOW,
    pil_to_escpos,
    ThermalBitmap,
)

if HAS_PILLOW:
    from PIL import Image, ImageDraw, ImageFont

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "cryptograms.json")


class CryptogramPuzzle(BasePuzzle):
    """Cryptogram letter substitution puzzle plugin."""

    def __init__(self, data_path: Optional[str] = None):
        path = data_path or DATA_PATH
        self.puzzles: List[Dict[str, Any]] = []
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.puzzles = json.load(f)
            except Exception as e:
                print(f"[CryptogramPuzzle] Warning: Could not load {path}: {e}")

        if not self.puzzles:
            self.puzzles = [
                {
                    "id": "easy_fallback",
                    "diff": "easy",
                    "phrase": "A JOURNEY OF A THOUSAND MILES BEGINS WITH A SINGLE STEP.",
                    "author": "LAO TZU",
                    "category": "Wisdom",
                },
                {
                    "id": "medium_fallback",
                    "diff": "medium",
                    "phrase": "THE FUTURE BELONGS TO THOSE WHO BELIEVE IN THE BEAUTY OF THEIR DREAMS.",
                    "author": "ELEANOR ROOSEVELT",
                    "category": "Inspiration",
                },
                {
                    "id": "hard_fallback",
                    "diff": "hard",
                    "phrase": "I USED TO THINK I WAS INDECISIVE, BUT NOW I AM NOT SO SURE.",
                    "author": "TOMMY COOPER",
                    "category": "Wit",
                },
            ]

    @property
    def puzzle_id(self) -> str:
        return "cryptogram"

    @property
    def title(self) -> str:
        return "CRYPTOGRAM"

    @property
    def has_difficulty(self) -> bool:
        return True

    @property
    def supported_difficulties(self) -> List[str]:
        return ["easy", "medium", "hard"]

    def generate(
        self,
        difficulty: str = "medium",
        seed: Optional[int] = None,
        **kwargs,
    ) -> BasePuzzleResult:
        if seed is not None:
            random.seed(seed)

        difficulty = difficulty.lower()
        candidates = [p for p in self.puzzles if p.get("diff", "").lower() == difficulty]
        if not candidates:
            candidates = self.puzzles

        selected = random.choice(candidates)
        phrase = selected["phrase"].upper()
        author = selected.get("author", "ANONYMOUS").upper()
        category = selected.get("category", "General")

        plain_to_cipher, cipher_to_plain = self._generate_derangement_key()
        ciphertext = "".join(plain_to_cipher.get(ch, ch) for ch in phrase)

        clue_count = 3 if difficulty == "easy" else (1 if difficulty == "hard" else 2)
        clues = self._select_clues(phrase, plain_to_cipher, clue_count)

        if len(clues) == 1:
            clue_str = f"CLUE: {clues[0]['cipher']} = {clues[0]['plain']}"
        else:
            clue_str = "CLUES: " + ", ".join(f"{c['cipher']} = {c['plain']}" for c in clues)

        formatted_text = self._format_ascii_text(ciphertext, author, clue_str=clue_str)

        raw_data = {
            "type": "cryptogram",
            "title": "CRYPTOGRAM",
            "id": selected.get("id", ""),
            "difficulty": difficulty,
            "phrase": phrase,
            "author": author,
            "category": category,
            "ciphertext": ciphertext,
            "plain_to_cipher": plain_to_cipher,
            "cipher_to_plain": cipher_to_plain,
            "clues": clues,
            "clue_str": clue_str,
            "clue_count": len(clues),
            "text": formatted_text,
            "solution": phrase,
        }
        instruction = self.get_instruction(raw_data)

        return BasePuzzleResult(
            puzzle_type=self.puzzle_id,
            title=self.title,
            difficulty=difficulty,
            instruction=instruction,
            raw_data=raw_data,
        )

    def get_instruction(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        c_diff = str(puzzle_data.get("difficulty", "medium"))
        clue_cnt = puzzle_data.get("clue_count", 3 if c_diff.lower() == "easy" else (1 if c_diff.lower() == "hard" else 2))
        clue_word = "1 letter clue" if clue_cnt == 1 else f"{clue_cnt} letter clues"
        return f"Deduce the hidden phrase using the {clue_word} and substitution logic."

    def format_ascii_puzzle(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        ciphertext = str(puzzle_data.get("ciphertext", "")).strip()
        author = str(puzzle_data.get("author", "")).strip()
        clue_str = puzzle_data.get("clue_str", "")
        return self._format_ascii_text(ciphertext, author, clue_str=clue_str)

    def format_solution_key(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> List[str]:
        phrase = puzzle_data.get("phrase") or puzzle_data.get("solution", "")
        author = puzzle_data.get("author", "")
        lines = []
        if phrase:
            for line in textwrap.wrap(f"Answer: {phrase}", 46):
                lines.append(line)
            if author:
                lines.append(f"-- {author}")
        return lines

    def render_raster(
        self,
        puzzle_data: Union[BasePuzzleResult, Dict[str, Any]],
        target_width: int = THERMAL_WIDTH_DOTS,
    ) -> bytes:
        padding = 24
        inner_width = target_width - padding * 2  # 528
        ciphertext = str(puzzle_data.get("ciphertext", "")).strip()
        author = str(puzzle_data.get("author", "")).strip()
        clue_str = str(puzzle_data.get("clue_str", "")).strip()

        words = ciphertext.split(" ")
        lines: List[str] = []
        curr = ""
        for w in words:
            if not curr:
                curr = w
            elif len(curr) + 1 + len(w) <= 24:
                curr += " " + w
            else:
                lines.append(curr)
                curr = w
        if curr:
            lines.append(curr)

        row_height = 76
        row_gap = 20
        header_gap = 16
        author_height = 36 if author else 0
        tracker_height = 80
        scratchpad_height = 140
        badge_total_h = (36 + 16) if clue_str else 0
        total_h = header_gap + badge_total_h + len(lines) * (row_height + row_gap) + author_height + tracker_height + scratchpad_height + 40
        total_h = ((total_h + 7) // 8) * 8  # Multiple of 8 dots

        tb = ThermalBitmap(target_width, total_h)
        cur_y = 16

        # 0. Clue badge
        if clue_str:
            badge_y = 12
            badge_h = 36
            tb.draw_rect(padding, badge_y, inner_width, badge_h, thickness=2)
            tb.draw_centered_text(badge_y + 11, clue_str, scale=2, color=1)
            cur_y = badge_y + badge_h + 16

        # 1. Ciphertext rows with handwriting slot underlines
        for line_str in lines:
            line_len = len(line_str)
            char_w = min(24, inner_width // max(1, line_len))
            start_x = padding + (inner_width - line_len * char_w) // 2

            slot_y = cur_y + 24
            char_y = cur_y + 34

            for idx, ch in enumerate(line_str):
                cx = start_x + idx * char_w
                if ch.isalpha():
                    bar_w = max(1, char_w - 6)
                    tb.draw_hline(cx + 3, slot_y, bar_w, thickness=2)
                tb.draw_char(cx + 4, char_y, ch, scale=2, color=1)

            cur_y += row_height + row_gap

        # 2. Author line
        if author:
            auth_str = f"-- {author}"
            tb.draw_text(padding + 12, cur_y, auth_str, scale=2, color=1)
            cur_y += author_height

        # 3. Dashed divider
        for dx in range(padding, padding + inner_width, 8):
            w = 4 if dx + 4 <= padding + inner_width else padding + inner_width - dx
            tb.draw_hline(dx, cur_y, w, thickness=2)
        cur_y += 18

        # 4. Alphabet Tracker
        tb.draw_text(padding, cur_y, "ALPHABET TRACKER:", scale=2, color=1)
        cur_y += 20
        col_w = inner_width // 26  # 20 dots per letter
        for i in range(26):
            lx = padding + i * col_w
            tb.draw_char(lx + 4, cur_y, chr(ord('A') + i), scale=2, color=1)
            bar_w = max(1, col_w - 4)
            tb.draw_hline(lx + 2, cur_y + 18, bar_w, thickness=2)

        cur_y += 32

        # 5. Scratchpad (4 handwriting dashed lines)
        tb.draw_text(padding, cur_y, "SCRATCHPAD:", scale=2, color=1)
        cur_y += 22
        for _ in range(4):
            for dx in range(padding, padding + inner_width, 10):
                w = 5 if dx + 5 <= padding + inner_width else padding + inner_width - dx
                tb.draw_hline(dx, cur_y, w, thickness=1)
            cur_y += 26

        return tb.to_escpos()

    def _generate_derangement_key(self) -> Tuple[Dict[str, str], Dict[str, str]]:
        letters = list(string.ascii_uppercase)
        shuffled = letters.copy()
        for _ in range(100):
            random.shuffle(shuffled)
            if all(a != b for a, b in zip(letters, shuffled)):
                break
        else:
            shuffled = letters[1:] + letters[:1]

        p2c = dict(zip(letters, shuffled))
        c2p = dict(zip(shuffled, letters))
        return p2c, c2p

    def _select_clues(self, phrase: str, p2c: Dict[str, str], count: int) -> List[Dict[str, str]]:
        distinct_letters = list(set(ch for ch in phrase if ch in string.ascii_uppercase))
        if not distinct_letters:
            distinct_letters = list(string.ascii_uppercase[:count])

        common_order = ["E", "T", "A", "O", "I", "N", "S", "H", "R", "D", "L", "C", "U", "M", "W", "F", "G", "Y", "P", "B", "V", "K", "J", "X", "Q", "Z"]
        sorted_in_phrase = [ch for ch in common_order if ch in distinct_letters] + [ch for ch in distinct_letters if ch not in common_order]

        count = min(count, len(distinct_letters))
        chosen_plain = random.sample(sorted_in_phrase[:max(count * 2, count)], count)

        clues = []
        for p in chosen_plain:
            c = p2c[p]
            clues.append({"cipher": c, "plain": p})

        clues.sort(key=lambda x: x["cipher"])
        return clues

    def _format_ascii_text(self, ciphertext: str, author: str = "", clue_str: str = "") -> str:
        words = ciphertext.split(" ")
        lines_of_words: List[List[str]] = []
        current_line: List[str] = []
        current_len = 0

        for word in words:
            word_spaced_len = len(word) * 2 - 1 if word else 0
            needed = word_spaced_len + (2 if current_line else 0)
            if current_line and (current_len + needed > 42):
                lines_of_words.append(current_line)
                current_line = [word]
                current_len = word_spaced_len
            else:
                current_line.append(word)
                current_len += needed

        if current_line:
            lines_of_words.append(current_line)

        output_lines: List[str] = []
        if clue_str:
            output_lines.append("   " + clue_str)
            output_lines.append("")

        for line_words in lines_of_words:
            slot_parts = []
            cipher_parts = []
            for word in line_words:
                s_chars = []
                c_chars = []
                for ch in word:
                    if ch in string.ascii_uppercase:
                        s_chars.append("_")
                    else:
                        s_chars.append(" ")
                    c_chars.append(ch)
                slot_parts.append(" ".join(s_chars))
                cipher_parts.append(" ".join(c_chars))

            slot_row = "  ".join(slot_parts)
            cipher_row = "  ".join(cipher_parts)

            output_lines.append("   " + slot_row)
            output_lines.append("   " + cipher_row)
            output_lines.append("")

        if author:
            output_lines.append(f"   -- {author}")
            output_lines.append("")

        output_lines.append("  - - - - - - - - - - - - - - - - - - - - - - - -")
        output_lines.append("  ALPHABET TRACKER:")
        output_lines.append("  A B C D E F G H I J K L M N O P Q R S T U V W X Y Z")
        output_lines.append("  _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _")
        output_lines.append("")
        output_lines.append("  SCRATCHPAD:")
        for _ in range(4):
            output_lines.append("  ______________________________________________")
            output_lines.append("")

        return "\n".join(output_lines)

    def verify_accuracy(
        self,
        puzzle_data: Union[BasePuzzleResult, Dict[str, Any]],
    ) -> Tuple[bool, str]:
        phrase = puzzle_data.get("phrase") or puzzle_data.get("solution")
        ciphertext = puzzle_data.get("ciphertext")
        plain_to_cipher = puzzle_data.get("plain_to_cipher")
        cipher_to_plain = puzzle_data.get("cipher_to_plain")
        clues = puzzle_data.get("clues") or []

        if not phrase or not isinstance(phrase, str):
            return False, "Cryptogram phrase missing or invalid"
        if not ciphertext or not isinstance(ciphertext, str):
            return False, "Cryptogram ciphertext missing or invalid"
        if not plain_to_cipher or not cipher_to_plain:
            return False, "Cryptogram substitution mapping missing"

        # 1. Verify derangement (no self-mapping) and bijection
        for p, c in plain_to_cipher.items():
            if p == c:
                return False, f"Cryptogram has self-mapped letter '{p}' -> '{c}'"
            if cipher_to_plain.get(c) != p:
                return False, f"Cryptogram cipher mapping not bijective for '{p}' <-> '{c}'"

        # 2. Verify ciphertext produces phrase
        decrypted = "".join(cipher_to_plain.get(ch, ch) for ch in ciphertext)
        if decrypted != phrase:
            return False, f"Cryptogram decryption mismatch:\nDecrypted: '{decrypted}'\nExpected:  '{phrase}'"

        # 3. Verify clues match
        for cl in clues:
            p_char = cl.get("plain")
            c_char = cl.get("cipher")
            if plain_to_cipher.get(p_char) != c_char:
                return False, f"Cryptogram clue '{c_char} = {p_char}' does not match cipher mapping"

        return True, "All rules satisfied"
