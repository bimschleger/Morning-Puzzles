"""
Morning Puzzles - Jumble Plugin
Encapsulates generation, canonical instruction formatting, ASCII layout,
solution key formatting, and 576-dot thermal raster rendering.
"""

import os
import json
import random
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

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "jumbles.json")


class JumblePuzzle(BasePuzzle):
    """Jumble word scramble and cartoon riddle puzzle plugin."""

    def __init__(self, data_path: Optional[str] = None):
        path = data_path or DATA_PATH
        self.puzzles = []
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.puzzles = json.load(f)
            except Exception as e:
                print(f"[JumblePuzzle] Warning: Could not load {path}: {e}")

        if not self.puzzles:
            self.puzzles = [
                {
                    "id": "fallback_001",
                    "diff": "easy",
                    "words": ["ROAST", "PLANT", "LIGHT", "CROWN"],
                    "circles": [[0, 2], [1], [0, 4], [2]],
                    "riddle": "Why did the coffee file a police report?",
                    "answer": "IT GOT MUGGED",
                }
            ]

    @property
    def puzzle_id(self) -> str:
        return "jumble"

    @property
    def title(self) -> str:
        return "JUMBLE"

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
        words_data = []

        for idx, word in enumerate(selected["words"]):
            scrambled = self._scramble(word)
            circles = selected["circles"][idx] if idx < len(selected.get("circles", [])) else []
            words_data.append({
                "original": word,
                "scrambled": scrambled,
                "length": len(word),
                "circle_indices": circles,
                "circles": circles,
            })

        riddle_text = selected.get("riddle") or selected.get("clue", "")
        answer_text = selected["answer"]

        ascii_text = self.format_ascii_puzzle({"words": words_data, "riddle": riddle_text})
        instruction = self.get_instruction({"difficulty": difficulty})

        raw_data = {
            "type": "jumble",
            "id": selected.get("id", ""),
            "difficulty": difficulty,
            "words": words_data,
            "scrambled": words_data,
            "circles": [w["circle_indices"] for w in words_data],
            "clue": riddle_text,
            "riddle": riddle_text,
            "answer": answer_text,
            "text": ascii_text,
        }

        return BasePuzzleResult(
            puzzle_type=self.puzzle_id,
            title=self.title,
            difficulty=difficulty,
            instruction=instruction,
            raw_data=raw_data,
        )

    def get_instruction(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        return "Unscramble each word, then use the circled letters to solve the riddle."

    def format_ascii_puzzle(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        words_data = puzzle_data.get("words", [])
        clue = puzzle_data.get("riddle", puzzle_data.get("clue", ""))
        count = len(words_data)
        lines = []
        lines.append(f"Unscramble these {count} Jumbles, one letter to each square:")
        for item in words_data:
            scrambled = item.get("scrambled", "")
            circles = item.get("circle_indices", item.get("circles", []))
            slot_repr = []
            for idx in range(len(scrambled)):
                slot_repr.append("( )" if idx in circles else "[ ]")
            lines.append(f"   {scrambled:<10} {' '.join(slot_repr)}")

        lines.append("")
        lines.append(f"Riddle: {clue}")
        lines.append("Answer: " + "_ " * 8)
        return "\n".join(lines)

    def format_solution_key(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> List[str]:
        raw_words = puzzle_data.get("words", [])
        words = [w.get("original", str(w)) if isinstance(w, dict) else str(w) for w in raw_words]
        ans = puzzle_data.get("answer", "")
        lines = []
        if words:
            for line in textwrap.wrap("Words:  " + ", ".join(words), 46):
                lines.append(line)
        if ans:
            for line in textwrap.wrap(f"Answer: {ans}", 46):
                lines.append(line)
        return lines

    def render_raster(
        self,
        puzzle_data: Union[BasePuzzleResult, Dict[str, Any]],
        target_width: int = THERMAL_WIDTH_DOTS,
    ) -> bytes:
        padding = 24
        inner_width = target_width - padding * 2

        words_data = puzzle_data.get("words", [])
        scrambled = puzzle_data.get("scrambled", words_data)
        circles = puzzle_data.get("circles", [])

        clue_h = 36
        cell_h = 48
        word_gap = 12
        count = min(4, len(scrambled))

        riddle = puzzle_data.get("riddle") or puzzle_data.get("clue", "")
        answer = puzzle_data.get("answer", "")

        # Tokenize riddle into wrapped lines (~36 chars)
        riddle_str = f'"{riddle}"'
        riddle_lines = textwrap.wrap(riddle_str, width=36)
        if not riddle_lines:
            riddle_lines = [riddle_str]

        # Tokenize answer words
        ans_box = 34
        word_spacing = 14

        def measure_word_w(w: str) -> int:
            w_w = 0
            for ch in w:
                if "A" <= ch <= "Z":
                    w_w += ans_box
                elif ch in ('"', "'"):
                    w_w += 12
                elif ch == "-":
                    w_w += 14
            return w_w

        ans_words = answer.split(" ")
        ans_lines: List[List[str]] = []
        cur_line: List[str] = []
        cur_w = 0

        for w in ans_words:
            w_w = measure_word_w(w)
            needed = w_w if not cur_line else (word_spacing + w_w)
            if cur_w + needed <= inner_width and cur_line:
                cur_line.append(w)
                cur_w += needed
            else:
                if cur_line:
                    ans_lines.append(cur_line)
                cur_line = [w]
                cur_w = w_w
        if cur_line:
            ans_lines.append(cur_line)

        # Calculate exact total height
        total_h = (
            12
            + count * (clue_h + cell_h + word_gap)
            + 20  # divider gap
            + 20 + len(riddle_lines) * 20 + 6  # riddle
            + 20 + 2 * 24 + 4  # scratchpad
            + 22 + len(ans_lines) * (ans_box + 12) + 16  # answer
        )
        total_h = ((total_h + 7) // 8) * 8  # align to 8 dots

        tb = ThermalBitmap(target_width, total_h)
        cur_y = 12

        # 1. Scrambled word clue boxes & answer row
        for i in range(count):
            item = scrambled[i]
            scram_text = item.get("scrambled", "") if isinstance(item, dict) else str(item)
            circ = item.get("circle_indices", item.get("circles", [])) if isinstance(item, dict) else (circles[i] if i < len(circles) else [])
            length = max(1, len(scram_text))

            col_pos = [padding + int(round(c * inner_width / float(length))) for c in range(length + 1)]

            # Clue box
            tb.draw_rect(padding, cur_y, inner_width, clue_h, thickness=2)
            for c in range(length):
                cx0 = col_pos[c]
                cx1 = col_pos[c + 1]
                col_w = cx1 - cx0
                if c > 0:
                    tb.draw_vline(cx0, cur_y, clue_h, thickness=1)
                char_x = cx0 + (col_w - 18) // 2
                char_y = cur_y + (clue_h - 21) // 2
                tb.draw_char(char_x, char_y, scram_text[c], scale=3)

            # Answer row directly below
            ans_y = cur_y + clue_h
            for c in range(length):
                cx0 = col_pos[c]
                cx1 = col_pos[c + 1]
                col_w = cx1 - cx0
                tb.draw_rect(cx0, ans_y, col_w, cell_h, thickness=2)
                if c in circ:
                    r = cell_h // 2 - 4
                    tb.draw_circle(cx0 + col_w // 2, ans_y + cell_h // 2, r, thickness=2)

            cur_y = ans_y + cell_h + word_gap

        # 2. Dashed tear divider
        tb.draw_dashed_hline(padding, cur_y + 2, inner_width, dash_len=6, gap_len=6, thickness=2)
        cur_y += 16

        # 3. Riddle Question
        tb.draw_text(padding, cur_y, "RIDDLE QUESTION:", scale=2)
        cur_y += 20
        for r_line in riddle_lines:
            tb.draw_text(padding + 8, cur_y, r_line, scale=2)
            cur_y += 20
        cur_y += 6

        # 4. Scratchpad
        tb.draw_text(padding, cur_y, "SCRATCHPAD:", scale=2)
        cur_y += 20
        for _ in range(2):
            tb.draw_dashed_hline(padding, cur_y, inner_width, dash_len=6, gap_len=6, thickness=1)
            cur_y += 24
        cur_y += 4

        # 5. Answer layout with segmented letter circles
        tb.draw_text(padding, cur_y, "ANSWER:", scale=2)
        cur_y += 22

        for line_words in ans_lines:
            line_w = sum(measure_word_w(w) for w in line_words) + max(0, len(line_words) - 1) * word_spacing
            start_x = padding + max(0, (inner_width - line_w) // 2)
            ax = start_x

            for w in line_words:
                for ch in w:
                    if "A" <= ch <= "Z":
                        tb.draw_rect(ax, cur_y, ans_box, ans_box, thickness=2)
                        tb.draw_circle(ax + ans_box // 2, cur_y + ans_box // 2, ans_box // 2 - 3, thickness=2)
                        ax += ans_box
                    elif ch in ('"', "'"):
                        tb.draw_char(ax + 2, cur_y + (ans_box - 14) // 2, ch, scale=2)
                        ax += 12
                    elif ch == "-":
                        tb.draw_char(ax + 3, cur_y + (ans_box - 14) // 2, "-", scale=2)
                        ax += 14
                ax += word_spacing
            cur_y += ans_box + 12

        return tb.to_escpos()

    def _scramble(self, word: str) -> str:
        chars = list(word)
        for _ in range(25):
            random.shuffle(chars)
            candidate = "".join(chars)
            if candidate != word:
                return candidate
        return "".join(chars)

    def verify_accuracy(
        self,
        puzzle_data: Union[BasePuzzleResult, Dict[str, Any]],
    ) -> Tuple[bool, str]:
        words_data = puzzle_data.get("words") or puzzle_data.get("scrambled")
        if not words_data or not isinstance(words_data, list):
            return False, "Jumble words data missing or invalid"
        if len(words_data) < 2:
            return False, f"Jumble has too few words: {len(words_data)}"

        riddle = puzzle_data.get("riddle") or puzzle_data.get("clue")
        answer = puzzle_data.get("answer")
        if not riddle or not isinstance(riddle, str):
            return False, "Jumble riddle/clue missing or invalid"
        if not answer or not isinstance(answer, str):
            return False, "Jumble answer missing or invalid"

        # 1. Verify anagrams of each scrambled word
        extracted_circled = []
        for idx, item in enumerate(words_data):
            orig = item.get("original", "")
            scram = item.get("scrambled", "")
            if not orig or not scram:
                return False, f"Jumble word {idx} missing original or scrambled text"
            if sorted(orig.upper()) != sorted(scram.upper()):
                return False, f"Jumble word {idx} scrambled '{scram}' is not an anagram of '{orig}'"
            circles = item.get("circle_indices", item.get("circles", []))
            for c_idx in circles:
                if 0 <= c_idx < len(orig):
                    extracted_circled.append(orig[c_idx].upper())
                else:
                    return False, f"Jumble word {idx} circle index {c_idx} out of range (length {len(orig)})"

        # 2. Verify circled letters can form the answer
        clean_answer = [ch.upper() for ch in answer if ch.isalpha()]
        if sorted(extracted_circled) != sorted(clean_answer):
            return False, f"Jumble circled letters {sorted(extracted_circled)} do not match answer letters {sorted(clean_answer)}"

        return True, "All rules satisfied"
