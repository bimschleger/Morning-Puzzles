"""
Morning Puzzles - Ladder Puzzle Plugin
Implements BasePuzzle contract for Word Ladder / Doublets.
Encapsulates generation, canonical instruction formatting, ASCII layout,
solution key representation, and 576-dot thermal raster rendering.
"""

import os
import textwrap
from typing import List, Dict, Any, Optional, Union

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

        path_str = " -> ".join(solution)
        return textwrap.wrap(path_str, 46)

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

        tile_size = 52 if word_len == 4 else 46
        gap_y = 14
        box_width = word_len * tile_size

        num_width = 36
        gap_x = 14
        total_content_w = num_width + gap_x + box_width
        start_x = (target_width - total_content_w) // 2
        num_x = start_x + num_width
        box_x = start_x + num_width + gap_x

        margin_top = 24
        ladder_height = total_rungs * tile_size + (total_rungs - 1) * gap_y
        total_height = margin_top + ladder_height + margin_top
        # Align height to multiple of 8
        total_height = (total_height + 7) & ~7

        if HAS_PILLOW:
            try:
                font_letter = ImageFont.truetype("Courier.ttf", 32)
                font_num = ImageFont.truetype("Arial.ttf", 20)
            except IOError:
                font_letter = ImageFont.load_default()
                font_num = ImageFont.load_default()

            img = Image.new("L", (target_width, total_height), 255)
            draw = ImageDraw.Draw(img)

            # Draw each rung: step number + word boxes
            for r in range(total_rungs):
                ry = margin_top + r * (tile_size + gap_y)

                # Number indicator (e.g. "1.")
                num_text = f"{r + 1}."
                draw.text((num_x - 26, ry + tile_size // 2 - 12), num_text, fill=0, font=font_num)

                # Word for this rung
                if r == 0:
                    rung_word = start_word
                elif r == total_rungs - 1:
                    rung_word = target_word
                else:
                    rung_word = ""

                # Draw word box frame and dividers
                draw.rectangle([box_x, ry, box_x + box_width, ry + tile_size], outline=0, width=2)
                for c in range(1, word_len):
                    div_x = box_x + c * tile_size
                    draw.line([div_x, ry, div_x, ry + tile_size], fill=0, width=1)

                # Letter characters inside boxes
                if rung_word:
                    for c in range(word_len):
                        tx = box_x + c * tile_size
                        ch = rung_word[c]
                        draw.text((tx + tile_size // 2 - 9, ry + tile_size // 2 - 14), ch, fill=0, font=font_letter)

            return pil_to_escpos(img)

        # Pure Python Fallback
        bmp = ThermalBitmap(target_width, total_height)
        for r in range(total_rungs):
            ry = margin_top + r * (tile_size + gap_y)
            num_text = f"{r + 1}."
            bmp.draw_text(num_x - 26, ry + tile_size // 2 - 8, num_text, scale=2, color=1)

            if r == 0:
                rung_word = start_word
            elif r == total_rungs - 1:
                rung_word = target_word
            else:
                rung_word = ""

            bmp.draw_rect(box_x, ry, box_width, tile_size, thickness=2, color=1)
            for c in range(1, word_len):
                div_x = box_x + c * tile_size
                bmp.draw_vline(div_x, ry, tile_size, thickness=1, color=1)

            if rung_word:
                for c in range(word_len):
                    tx = box_x + c * tile_size
                    bmp.draw_char(tx + tile_size // 2 - 6, ry + tile_size // 2 - 8, rung_word[c], scale=2, color=1)

        return bmp.to_escpos()
