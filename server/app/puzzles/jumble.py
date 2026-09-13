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

        words = puzzle_data.get("words", [])
        scrambled = puzzle_data.get("scrambled", words)
        circles = puzzle_data.get("circles", [])

        clue_height = 44
        cell_height = 58
        word_gap = 16

        if HAS_PILLOW:
            try:
                font_box = ImageFont.truetype("Courier.ttf", 26)
                font_riddle = ImageFont.truetype("Arial.ttf", 20)
                font_label = ImageFont.truetype("Arial.ttf", 16)
            except IOError:
                font_box = ImageFont.load_default()
                font_riddle = ImageFont.load_default()
                font_label = ImageFont.load_default()

            total_height = 900
            img = Image.new("L", (target_width, total_height), 255)
            draw = ImageDraw.Draw(img)
            cur_y = 12

            for i in range(min(4, len(scrambled))):
                scram = scrambled[i]
                scram_text = scram.get("scrambled", "") if isinstance(scram, dict) else str(scram)
                circ = scram.get("circles", []) if isinstance(scram, dict) else (circles[i] if i < len(circles) else [])
                length = max(1, len(scram_text))
                col_pos = [padding + int(round(c * inner_width / float(length))) for c in range(length + 1)]

                draw.rectangle([padding, cur_y, padding + inner_width, cur_y + clue_height], outline=0, width=3)
                for c in range(length):
                    cx0 = col_pos[c]
                    cx1 = col_pos[c + 1]
                    col_w = cx1 - cx0
                    if c > 0:
                        draw.line([cx0, cur_y, cx0, cur_y + clue_height], fill=160, width=2)
                    draw.text((cx0 + col_w // 2 - 8, cur_y + 8), scram_text[c], fill=0, font=font_box)

                ans_y = cur_y + clue_height
                for c in range(length):
                    cx0 = col_pos[c]
                    cx1 = col_pos[c + 1]
                    col_w = cx1 - cx0
                    draw.rectangle([cx0, ans_y, cx1, ans_y + cell_height], outline=0, width=3)
                    if c in circ:
                        radius = min(col_w, cell_height) // 2 - 5
                        draw.ellipse([cx0 + col_w // 2 - radius, ans_y + cell_height // 2 - radius,
                                      cx0 + col_w // 2 + radius, ans_y + cell_height // 2 + radius], outline=0, width=3)

                cur_y = ans_y + cell_height + word_gap

            draw.line([padding, cur_y, padding + inner_width, cur_y], fill=140, width=2)
            cur_y += 16
            draw.text((padding, cur_y), "RIDDLE CLUE:", fill=0, font=font_label)
            cur_y += 24
            riddle_text = f'"{puzzle_data.get("riddle", puzzle_data.get("clue", ""))}"'
            draw.text((padding + 8, cur_y), riddle_text, fill=0, font=font_riddle)
            cur_y += 32

            draw.text((padding, cur_y), "Discovered letters scratchpad:", fill=80, font=font_label)
            cur_y += 24
            for _ in range(2):
                draw.line([padding, cur_y, padding + inner_width, cur_y], fill=160, width=2)
                cur_y += 30

            cur_y += 6
            draw.text((padding, cur_y), "Answer:", fill=0, font=font_label)
            cur_y += 24

            ans_box = cell_height
            answer_words = str(puzzle_data.get("answer", "")).split(" ")
            for w in answer_words:
                start_x = padding + 10
                for c in range(len(w)):
                    bx = start_x + c * (ans_box + 4)
                    draw.rectangle([bx, cur_y, bx + ans_box, cur_y + ans_box], outline=0, width=3)
                    radius = ans_box // 2 - 5
                    draw.ellipse([bx + ans_box // 2 - radius, cur_y + ans_box // 2 - radius,
                                  bx + ans_box // 2 + radius, cur_y + ans_box // 2 + radius], outline=0, width=3)
                cur_y += ans_box + 14

            return pil_to_escpos(img.crop((0, 0, target_width, min(cur_y + 10, total_height))))

        # Pure Python Fallback
        total_h = 750
        tb = ThermalBitmap(target_width, total_h)
        cur_y = 12

        for i in range(min(4, len(scrambled))):
            scram = scrambled[i]
            scram_text = scram.get("scrambled", "") if isinstance(scram, dict) else str(scram)
            circ = scram.get("circles", []) if isinstance(scram, dict) else (circles[i] if i < len(circles) else [])
            length = max(1, len(scram_text))
            col_pos = [padding + int(round(c * inner_width / float(length))) for c in range(length + 1)]

            tb.draw_rect(padding, cur_y, inner_width, clue_height, thickness=3)
            for c in range(length):
                cx0 = col_pos[c]
                cx1 = col_pos[c + 1]
                col_w = cx1 - cx0
                if c > 0:
                    tb.draw_vline(cx0, cur_y, clue_height, thickness=2)
                tb.draw_char(cx0 + col_w // 2 - 9, cur_y + 8, scram_text[c], scale=3)

            ans_y = cur_y + clue_height
            for c in range(length):
                cx0 = col_pos[c]
                cx1 = col_pos[c + 1]
                col_w = cx1 - cx0
                tb.draw_rect(cx0, ans_y, col_w, cell_height, thickness=3)
                if c in circ:
                    radius = min(col_w, cell_height) // 2 - 5
                    tb.draw_circle(cx0 + col_w // 2, ans_y + cell_height // 2, radius, thickness=3)

            cur_y = ans_y + cell_height + word_gap

        tb.draw_hline(padding, cur_y, inner_width, thickness=2)
        cur_y += 24
        tb.draw_text(padding, cur_y, "SCRATCHPAD:", scale=2)
        cur_y += 24
        for _ in range(2):
            tb.draw_hline(padding, cur_y, inner_width, thickness=2)
            cur_y += 30

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
