"""
Morning Puzzles - Wheel (Word Wheel / Honeycomb) Puzzle Plugin
Implements BasePuzzle contract for 7-letter hexagonal honeycomb anagram puzzles.
Encapsulates generation, canonical instruction formatting, ASCII layout,
solution key representation, and 576-dot thermal raster rendering.
"""

import os
import math
import textwrap
from typing import List, Dict, Any, Optional, Union, Tuple

from .base import BasePuzzle, BasePuzzleResult
from ..generators.wheel_gen import WheelGenerator
from ..renderer.canvas import (
    THERMAL_WIDTH_DOTS,
    HAS_PILLOW,
    pil_to_escpos,
    ThermalBitmap,
)

if HAS_PILLOW:
    from PIL import Image, ImageDraw, ImageFont


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
        return f"Find {cnt}+ words using center letter {center} and outer letters, including a 7-letter pangram."

    def format_ascii_puzzle(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        center = str(puzzle_data.get("center_letter", "E")).upper()
        outer = list(puzzle_data.get("outer_letters", ["A", "B", "C", "D", "F", "G"]))
        while len(outer) < 6:
            outer.append(" ")

        o = [str(x).upper() for x in outer[:6]]
        benchmarks = puzzle_data.get("benchmarks", {"good": 10, "great": 18, "genius": 25})
        b_good = benchmarks.get("good", 10)
        b_great = benchmarks.get("great", 18)
        b_genius = benchmarks.get("genius", 25)

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

        lines: List[str] = []
        if pangrams:
            p_text = "PANGRAM: " + ", ".join(pangrams)
            for l in textwrap.wrap(p_text, width=46):
                lines.append(l)

        lines.append(f"TOTAL WORDS: {cnt}")

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
        b_good = benchmarks.get("good", 10)
        b_great = benchmarks.get("great", 18)
        b_genius = benchmarks.get("genius", 25)

        total_height = 368  # Multiple of 8
        xc = target_width // 2
        yc = 135
        hex_radius = 46
        spacing = hex_radius * math.sqrt(3)  # ~79.6px

        # 6 outer hexagon angles (degrees)
        angles_deg = [270, 330, 30, 90, 150, 210]
        outer_coords = []
        for deg in angles_deg:
            rad = math.radians(deg)
            px = xc + spacing * math.cos(rad)
            py = yc + spacing * math.sin(rad)
            outer_coords.append((px, py))

        def get_hex_polygon(center_x: float, center_y: float, r: float) -> List[Tuple[float, float]]:
            points = []
            for i in range(6):
                angle = math.radians(60 * i + 30)
                points.append((center_x + r * math.cos(angle), center_y + r * math.sin(angle)))
            return points

        if HAS_PILLOW:
            try:
                font_hub = ImageFont.truetype("Courier.ttf", 36)
                font_letter = ImageFont.truetype("Courier.ttf", 32)
                font_label = ImageFont.truetype("Arial.ttf", 18)
            except IOError:
                font_hub = ImageFont.load_default()
                font_letter = ImageFont.load_default()
                font_label = ImageFont.load_default()

            img = Image.new("L", (target_width, total_height), 255)
            draw = ImageDraw.Draw(img)

            # Draw outer 6 hexagons
            for idx, (px, py) in enumerate(outer_coords):
                poly = get_hex_polygon(px, py, hex_radius)
                draw.polygon(poly, outline=0, fill=255)
                # Draw letter
                letter_ch = outer[idx]
                bbox = draw.textbbox((0, 0), letter_ch, font=font_letter)
                tw = bbox[2] - bbox[0]
                th = bbox[3] - bbox[1]
                draw.text((px - tw / 2, py - th / 2 - 2), letter_ch, fill=0, font=font_letter)

            # Draw center hexagon with double-thick frame
            center_poly = get_hex_polygon(xc, yc, hex_radius)
            draw.polygon(center_poly, outline=0, fill=255)
            center_inner = get_hex_polygon(xc, yc, hex_radius - 4)
            draw.polygon(center_inner, outline=0, fill=255)

            # Draw center letter (bold)
            bbox_c = draw.textbbox((0, 0), center, font=font_hub)
            tw_c = bbox_c[2] - bbox_c[0]
            th_c = bbox_c[3] - bbox_c[1]
            draw.text((xc - tw_c / 2, yc - th_c / 2 - 3), center, fill=0, font=font_hub)

            # Draw Target Benchmarks box
            box_y = 260
            box_h = 36
            box_w = 420
            box_x = (target_width - box_w) // 2
            draw.rectangle([box_x, box_y, box_x + box_w, box_y + box_h], outline=0, width=2)
            bench_text = f"GOOD: {b_good}    GREAT: {b_great}    GENIUS: {b_genius}+"
            bbox_b = draw.textbbox((0, 0), bench_text, font=font_label)
            bw = bbox_b[2] - bbox_b[0]
            bh = bbox_b[3] - bbox_b[1]
            draw.text((xc - bw / 2, box_y + (box_h - bh) / 2 - 2), bench_text, fill=0, font=font_label)

            # Ruled lines for writing words
            rule_y1 = 320
            rule_y2 = 348
            line_w = 200
            gap_line = 36
            x1_a = xc - line_w - gap_line // 2
            x1_b = x1_a + line_w
            x2_a = xc + gap_line // 2
            x2_b = x2_a + line_w
            draw.line([x1_a, rule_y1, x1_b, rule_y1], fill=0, width=1)
            draw.line([x2_a, rule_y1, x2_b, rule_y1], fill=0, width=1)
            draw.line([x1_a, rule_y2, x1_b, rule_y2], fill=0, width=1)
            draw.line([x2_a, rule_y2, x2_b, rule_y2], fill=0, width=1)

            return pil_to_escpos(img)

        # Pure Python Fallback
        bmp = ThermalBitmap(target_width, total_height)
        cell_size = 54

        # Draw outer 6 cells as framed boxes
        for idx, (px, py) in enumerate(outer_coords):
            bx = int(px - cell_size // 2)
            by = int(py - cell_size // 2)
            bmp.draw_rect(bx, by, cell_size, cell_size, thickness=2, color=1)
            bmp.draw_char(bx + cell_size // 2 - 5, by + cell_size // 2 - 7, outer[idx], scale=2, color=1)

        # Center cell (double outline)
        cbx = int(xc - cell_size // 2)
        cby = int(yc - cell_size // 2)
        bmp.draw_rect(cbx, cby, cell_size, cell_size, thickness=3, color=1)
        bmp.draw_char(cbx + cell_size // 2 - 5, cby + cell_size // 2 - 7, center, scale=2, color=1)

        # Benchmarks box
        box_y = 260
        box_h = 36
        box_w = 420
        box_x = (target_width - box_w) // 2
        bmp.draw_rect(box_x, box_y, box_w, box_h, thickness=2, color=1)
        bench_text = f"GOOD: {b_good}  GREAT: {b_great}  GENIUS: {b_genius}+"
        bmp.draw_text(xc - len(bench_text) * 4, box_y + 12, bench_text, scale=1, color=1)

        # Ruled lines
        bmp.draw_hline(box_x, 320, 190, thickness=1, color=1)
        bmp.draw_hline(xc + 20, 320, 190, thickness=1, color=1)
        bmp.draw_hline(box_x, 348, 190, thickness=1, color=1)
        bmp.draw_hline(xc + 20, 348, 190, thickness=1, color=1)

        return bmp.to_escpos()

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

        return True, "All rules satisfied"
