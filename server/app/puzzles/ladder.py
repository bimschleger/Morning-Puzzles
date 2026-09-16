"""
Morning Puzzles - Ladder Puzzle Plugin
Implements BasePuzzle contract for Word Ladder / Doublets.
Encapsulates generation, canonical instruction formatting, ASCII layout,
solution key representation, and 576-dot thermal raster rendering.
"""

import os
import textwrap
from typing import List, Tuple, Dict, Any, Optional, Union

from .base import BasePuzzle, BasePuzzleResult
from ..generators.ladder_gen import LadderGenerator
from ..renderer.canvas import (
    THERMAL_WIDTH_DOTS,
    HAS_PILLOW,
    pil_to_escpos,
    ThermalBitmap,
)

if HAS_PILLOW:
    from PIL import Image, ImageDraw, ImageFont


class LadderPuzzle(BasePuzzle):
    """Word Ladder puzzle plugin."""

    def __init__(self, data_path: Optional[str] = None):
        self.generator = LadderGenerator(data_path=data_path)

    @property
    def puzzle_id(self) -> str:
        return "ladder"

    @property
    def title(self) -> str:
        return "LADDER"

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
        start_word = str(puzzle_data.get("start_word", "COLD")).upper()
        target_word = str(puzzle_data.get("target_word", "WARM")).upper()
        solution = puzzle_data.get("solution", [])
        intermediate_count = puzzle_data.get("intermediate_count", max(1, len(solution) - 2))

        if intermediate_count == 1:
            count_phrase = "1 English word"
        else:
            count_phrase = f"{intermediate_count} English words"

        return f"Deduce {count_phrase} to link {start_word} to {target_word}, changing 1 letter each step."

    def format_ascii_puzzle(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        start_word = str(puzzle_data.get("start_word", "COLD")).upper()
        target_word = str(puzzle_data.get("target_word", "WARM")).upper()
        solution = puzzle_data.get("solution", [])
        total_rungs = len(solution) if solution else 5
        word_len = len(start_word)

        box_sep = "+---" * word_len + "+"
        pad_len = max(0, (48 - (3 + len(box_sep))) // 2)
        indent = " " * pad_len

        lines: List[str] = []

        for r in range(total_rungs):
            num_str = f"{r + 1}."
            if r == 0:
                cells = "".join(f"| {ch} " for ch in start_word) + "|"
            elif r == total_rungs - 1:
                cells = "".join(f"| {ch} " for ch in target_word) + "|"
            else:
                cells = "|   " * word_len + "|"

            lines.append(f"{indent}   {box_sep}")
            lines.append(f"{indent}{num_str:>2} {cells}")

        # Final bottom border
        lines.append(f"{indent}   {box_sep}")

        return "\n".join(lines)

    def format_solution_key(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> List[str]:
        solution = puzzle_data.get("solution", [])
        if not solution:
            start_word = str(puzzle_data.get("start_word", "COLD"))
            target_word = str(puzzle_data.get("target_word", "WARM"))
            solution = [start_word, target_word]

        return ["      " + str(word).upper() for word in solution]

    def render_raster(
        self,
        puzzle_data: Union[BasePuzzleResult, Dict[str, Any]],
        target_width: int = THERMAL_WIDTH_DOTS,
    ) -> bytes:
        start_word = str(puzzle_data.get("start_word", "COLD")).upper()
        target_word = str(puzzle_data.get("target_word", "WARM")).upper()
        solution = puzzle_data.get("solution", [])
        total_rungs = len(solution) if solution else 5
        word_len = len(start_word)

        tile_size = 66
        gap_y = 14
        box_width = word_len * tile_size

        num_width = 36
        gap_x = 14
        total_content_w = num_width + gap_x + box_width
        start_x = (target_width - total_content_w) // 2
        box_x = start_x + num_width + gap_x

        margin_top = 24
        ladder_height = total_rungs * tile_size + (total_rungs - 1) * gap_y
        total_height = margin_top + ladder_height + margin_top
        # Align height to multiple of 8
        total_height = (total_height + 7) & ~7

        tb = ThermalBitmap(target_width, total_height)

        for r in range(total_rungs):
            ry = margin_top + r * (tile_size + gap_y)

            # Step number on left (scale=2, right-aligned)
            num_text = f"{r + 1}."
            text_x = box_x - gap_x - len(num_text) * 12
            text_y = ry + (tile_size - 14) // 2
            tb.draw_text(text_x, text_y, num_text, scale=2, color=1)

            # Draw 2px outer rectangle for the word box
            tb.draw_rect(box_x, ry, box_width, tile_size, thickness=2, color=1)

            # Draw 1px internal vertical cell dividers
            for c in range(1, word_len):
                div_x = box_x + c * tile_size
                tb.draw_vline(div_x, ry, tile_size, thickness=1, color=1)

            # Start and target word glyphs (scale=3)
            rung_word = ""
            if r == 0:
                rung_word = start_word
            elif r == total_rungs - 1:
                rung_word = target_word

            if rung_word:
                for c in range(word_len):
                    char_x = box_x + c * tile_size + (tile_size - 15) // 2
                    char_y = ry + (tile_size - 21) // 2
                    tb.draw_char(char_x, char_y, rung_word[c], scale=3, color=1)

        return tb.to_escpos()

    def verify_accuracy(
        self,
        puzzle_data: Union[BasePuzzleResult, Dict[str, Any]],
    ) -> Tuple[bool, str]:
        start_word = str(puzzle_data.get("start_word", "")).upper()
        target_word = str(puzzle_data.get("target_word", "")).upper()
        solution = [str(w).upper() for w in puzzle_data.get("solution", [])]

        if not start_word or not target_word:
            return False, "Ladder puzzle missing start or target word"
        if not solution or len(solution) < 3:
            return False, f"Ladder solution must have at least 3 rungs, got {len(solution)}"
        if solution[0] != start_word:
            return False, f"Ladder solution start '{solution[0]}' does not match start_word '{start_word}'"
        if solution[-1] != target_word:
            return False, f"Ladder solution target '{solution[-1]}' does not match target_word '{target_word}'"

        word_len = len(start_word)
        for idx, w in enumerate(solution):
            if len(w) != word_len:
                return False, f"Ladder rung {idx} '{w}' has length {len(w)}, expected {word_len}"

        for idx in range(len(solution) - 1):
            w1 = solution[idx]
            w2 = solution[idx + 1]
            diffs = sum(1 for a, b in zip(w1, w2) if a != b)
            if diffs != 1:
                return False, f"Ladder transition from '{w1}' to '{w2}' differs by {diffs} letters, expected exactly 1"

        return True, "All rules satisfied"
