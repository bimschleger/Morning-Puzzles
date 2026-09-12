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

        formatted_text = self._format_ascii_text(ciphertext, author)

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

        lines = []
        if clue_str:
            lines.append("   " + clue_str)
            lines.append("")
        lines.append(self._format_ascii_text(ciphertext, author))
        return "\n".join(lines)

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
        inner_width = target_width - padding * 2
        ciphertext = str(puzzle_data.get("ciphertext", "")).strip()
        author = str(puzzle_data.get("author", "")).strip()

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
        total_h = header_gap + len(lines) * (row_height + row_gap) + author_height + tracker_height + scratchpad_height + 40

        if HAS_PILLOW:
            try:
                font_cipher = ImageFont.truetype("Courier.ttf", 26)
                font_label = ImageFont.truetype("Arial.ttf", 16)
                font_author = ImageFont.truetype("Arial.ttf", 18)
                font_tracker = ImageFont.truetype("Courier.ttf", 15)
            except IOError:
                font_cipher = ImageFont.load_default()
                font_label = ImageFont.load_default()
                font_author = ImageFont.load_default()
                font_tracker = ImageFont.load_default()

            img = Image.new("L", (target_width, total_h), 255)
            draw = ImageDraw.Draw(img)
            cur_y = 16

            for line_str in lines:
                line_len = len(line_str)
                char_w = inner_width / max(1, line_len)
                char_w = min(char_w, 24.0)

                start_x = padding + (inner_width - line_len * char_w) / 2.0
                slot_y = cur_y + 26
                char_y = cur_y + 36

                for idx, ch in enumerate(line_str):
                    cx = start_x + idx * char_w
                    if ch.isalpha():
                        draw.line([cx + 3, slot_y, cx + char_w - 3, slot_y], fill=120, width=2)
                    draw.text((cx + char_w / 2.0 - 7, char_y), ch, fill=0, font=font_cipher)

                cur_y += row_height + row_gap

            if author:
                draw.text((padding + 12, cur_y), f"-- {author}", fill=0, font=font_author)
                cur_y += author_height

            for dx in range(padding, padding + inner_width, 8):
                draw.line([dx, cur_y, min(dx + 4, padding + inner_width), cur_y], fill=140, width=2)
            cur_y += 18

            draw.text((padding, cur_y), "ALPHABET TRACKER:", fill=0, font=font_label)
            cur_y += 22

            letters_az = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            col_w = inner_width / 26.0
            for i, let in enumerate(letters_az):
                lx = padding + i * col_w
                draw.text((lx + col_w / 2.0 - 5, cur_y), let, fill=0, font=font_tracker)
                draw.line([lx + 1, cur_y + 22, lx + col_w - 2, cur_y + 22], fill=140, width=2)

            cur_y += 38
            draw.text((padding, cur_y), "SCRATCHPAD:", fill=80, font=font_label)
            cur_y += 24
            for _ in range(4):
                for dx in range(padding, padding + inner_width, 10):
                    draw.line([dx, cur_y, min(dx + 5, padding + inner_width), cur_y], fill=160, width=2)
                cur_y += 26

            return pil_to_escpos(img.crop((0, 0, target_width, min(cur_y + 10, total_h))))

        # Pure Python Fallback
        tb = ThermalBitmap(target_width, total_h)
        cur_y = 16

        for line_str in lines:
            line_len = len(line_str)
            char_w = int(inner_width / max(1, line_len))
            char_w = min(char_w, 24)
            start_x = padding + int((inner_width - line_len * char_w) / 2)

            slot_y = cur_y + 24
            char_y = cur_y + 34

            for idx, ch in enumerate(line_str):
                cx = start_x + idx * char_w
                if ch.isalpha():
                    tb.draw_hline(cx + 3, slot_y, max(1, char_w - 6), thickness=2)
                tb.draw_text(cx + 4, char_y, ch, scale=2, color=1)

            cur_y += row_height + row_gap

        if author:
            tb.draw_text(padding + 12, cur_y, f"-- {author}", scale=1, color=1)
            cur_y += author_height

        for dx in range(padding, padding + inner_width, 8):
            tb.draw_hline(dx, cur_y, 4, thickness=2)
        cur_y += 18

        tb.draw_text(padding, cur_y, "ALPHABET TRACKER:", scale=1, color=1)
        cur_y += 20
        col_w = int(inner_width / 26)
        letters_az = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i, let in enumerate(letters_az):
            lx = padding + i * col_w
            tb.draw_text(lx + 2, cur_y, let, scale=1, color=1)
            tb.draw_hline(lx + 1, cur_y + 16, max(1, col_w - 2), thickness=1)

        cur_y += 32
        tb.draw_text(padding, cur_y, "SCRATCHPAD:", scale=1, color=1)
        cur_y += 22
        for _ in range(4):
            for dx in range(padding, padding + inner_width, 10):
                tb.draw_hline(dx, cur_y, 5, thickness=1)
            cur_y += 24

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

    def _format_ascii_text(self, ciphertext: str, author: str = "") -> str:
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
