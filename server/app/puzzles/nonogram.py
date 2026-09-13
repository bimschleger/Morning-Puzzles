"""
Morning Puzzles - Nonogram Plugin
Encapsulates generation, canonical instruction formatting, ASCII layout,
solution key formatting, and 576-dot thermal raster rendering.
"""

import random
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


class NonogramPuzzle(BasePuzzle):
    """Nonogram (Picross) puzzle plugin."""

    DIFFICULTY_SIZES = {
        "easy": (5, 5),
        "medium": (10, 10),
        "hard": (15, 15),
    }

    @property
    def puzzle_id(self) -> str:
        return "nonogram"

    @property
    def title(self) -> str:
        return "NONOGRAM"

    @property
    def has_difficulty(self) -> bool:
        return True

    @property
    def supported_difficulties(self) -> List[str]:
        return ["easy", "medium", "hard"]

    def generate(
        self,
        difficulty: str = "medium",
        density: float = 0.55,
        seed: Optional[int] = None,
        **kwargs,
    ) -> BasePuzzleResult:
        if seed is not None:
            random.seed(seed)

        difficulty = difficulty.lower()
        rows, cols = self.DIFFICULTY_SIZES.get(difficulty, (10, 10))

        board = [[0] * cols for _ in range(rows)]
        for r in range(rows):
            for c in range(cols):
                board[r][c] = 1 if random.random() < density else 0

        row_clues = [self._extract_line_clues(board[r]) for r in range(rows)]
        col_clues = [self._extract_line_clues([board[r][c] for r in range(rows)]) for c in range(cols)]

        ascii_text = self.format_ascii_puzzle({
            "row_clues": row_clues,
            "col_clues": col_clues,
            "rows": rows,
            "cols": cols,
        })
        instruction = self.get_instruction({"difficulty": difficulty})

        raw_data = {
            "type": "nonogram",
            "difficulty": difficulty,
            "rows": rows,
            "cols": cols,
            "row_clues": row_clues,
            "col_clues": col_clues,
            "solution": board,
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
        return "Shade blocks of cells matching each clue in order, separated by at least one empty cell."

    def format_ascii_puzzle(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        row_clues = puzzle_data.get("row_clues", [])
        col_clues = puzzle_data.get("col_clues", [])
        rows = puzzle_data.get("rows", len(row_clues))
        cols = puzzle_data.get("cols", len(col_clues))

        if not row_clues or not col_clues:
            return ""

        lines = []
        max_row_clue_len = max(len(" ".join(map(str, c))) for c in row_clues)
        max_col_clues = max(len(c) for c in col_clues)

        for clue_idx in range(max_col_clues):
            line_str = " " * (max_row_clue_len + 3)
            for c in range(cols):
                clue_list = col_clues[c]
                pad = max_col_clues - len(clue_list)
                if clue_idx >= pad:
                    val = clue_list[clue_idx - pad]
                    line_str += f"{val:2} "
                else:
                    line_str += "   "
            lines.append(line_str)

        lines.append(" " * (max_row_clue_len + 1) + "+-" + "---" * cols)

        for r in range(rows):
            clue_str = " ".join(map(str, row_clues[r]))
            prefix = f"{clue_str:>{max_row_clue_len}} | "
            slots = " . " * cols
            lines.append(prefix + slots)

        return "\n".join(lines)

    def format_solution_key(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> List[str]:
        sol = puzzle_data.get("solution", [])
        if not sol:
            return []
        lines = []
        for row in sol:
            lines.append("      " + " ".join("* " if c == 1 else ". " for c in row))
        return lines

    def render_raster(
        self,
        puzzle_data: Union[BasePuzzleResult, Dict[str, Any]],
        target_width: int = THERMAL_WIDTH_DOTS,
    ) -> bytes:
        size = puzzle_data.get("rows", puzzle_data.get("size", 5))
        row_clues = puzzle_data.get("row_clues", [])
        col_clues = puzzle_data.get("col_clues", [])
        solution = puzzle_data.get("solution", puzzle_data.get("grid", []))

        padding = 24
        inner_width = target_width - padding * 2

        cell_size = 76 if size <= 5 else (50 if size <= 8 else (40 if size <= 10 else 26))
        major_interval = 4 if size == 8 else 5
        grid_size = cell_size * size
        row_clue_width = inner_width - grid_size

        max_col_clues = max((len(c) for c in col_clues), default=1)
        col_clue_item_h = max(24, int(cell_size * 0.55))
        col_clue_height = max(50, max_col_clues * col_clue_item_h + 16)
        total_height = 12 + col_clue_height + grid_size + 12

        if HAS_PILLOW:
            img = Image.new("L", (target_width, total_height), 255)
            draw = ImageDraw.Draw(img)

            try:
                font_clue = ImageFont.truetype("Courier.ttf", int(cell_size * 0.45))
            except IOError:
                font_clue = ImageFont.load_default()

            grid_x = padding + row_clue_width
            grid_y = 12 + col_clue_height

            draw.rectangle([padding, 12, grid_x, grid_y], fill=240, outline=0, width=3)
            draw.rectangle([grid_x, 12, grid_x + grid_size, grid_y], outline=0, width=3)

            for c in range(size):
                col_cx = grid_x + c * cell_size + cell_size // 2
                clues = col_clues[c] if c < len(col_clues) else [0]
                for k, val in enumerate(clues):
                    dist_from_bottom = (len(clues) - 1 - k) * col_clue_item_h
                    val_y = grid_y - 12 - dist_from_bottom
                    draw.text((col_cx - 6, val_y), str(val), fill=0, font=font_clue)
                if c > 0:
                    is_major = (c % major_interval == 0)
                    draw.line([grid_x + c * cell_size, 12, grid_x + c * cell_size, grid_y], fill=0 if is_major else 180, width=3 if is_major else 1)

            draw.rectangle([padding, grid_y, grid_x, grid_y + grid_size], outline=0, width=3)
            row_clue_char_w = max(18, int(cell_size * 0.45))
            for r in range(size):
                row_cy = grid_y + r * cell_size + cell_size // 2 - int(cell_size * 0.22)
                clues = row_clues[r] if r < len(row_clues) else [0]
                for k, val in enumerate(clues):
                    dist_from_right = (len(clues) - 1 - k) * row_clue_char_w
                    val_x = grid_x - 14 - dist_from_right
                    draw.text((val_x, row_cy), str(val), fill=0, font=font_clue)
                if r > 0:
                    is_major = (r % major_interval == 0)
                    draw.line([padding, grid_y + r * cell_size, grid_x, grid_y + r * cell_size], fill=0 if is_major else 180, width=3 if is_major else 1)


            for i in range(size + 1):
                is_major = (i % major_interval == 0) or (i == size)
                w = 4 if is_major else 1
                color = 0 if is_major else 160
                draw.line([grid_x, grid_y + i * cell_size, grid_x + grid_size, grid_y + i * cell_size], fill=color, width=w)
                draw.line([grid_x + i * cell_size, grid_y, grid_x + i * cell_size, grid_y + grid_size], fill=color, width=w)

            draw.rectangle([padding, 12, padding + inner_width, grid_y + grid_size], outline=0, width=5)
            return pil_to_escpos(img)

        # Pure Python Fallback
        tb = ThermalBitmap(target_width, total_height)
        grid_x = padding + row_clue_width
        grid_y = 12 + col_clue_height

        tb.draw_rect(padding, 12, row_clue_width, col_clue_height, thickness=3)
        tb.draw_rect(grid_x, 12, grid_size, col_clue_height, thickness=3)
        tb.draw_rect(padding, grid_y, row_clue_width, grid_size, thickness=3)
        tb.draw_rect(grid_x, grid_y, grid_size, grid_size, thickness=4)

        for c in range(size):
            clues = col_clues[c] if c < len(col_clues) else [0]
            col_cx = grid_x + c * cell_size + cell_size // 2 - 6
            for k, val in enumerate(clues):
                dist = (len(clues) - 1 - k) * col_clue_item_h
                tb.draw_char(col_cx, grid_y - 18 - dist, str(val), scale=2)

        for r in range(size):
            clues = row_clues[r] if r < len(row_clues) else [0]
            row_cy = grid_y + r * cell_size + cell_size // 2 - 7
            for k, val in enumerate(clues):
                dist = (len(clues) - 1 - k) * 16
                tb.draw_char(grid_x - 18 - dist, row_cy, str(val), scale=2)

        for i in range(size + 1):
            is_maj = (i % major_interval == 0)
            tb.draw_hline(grid_x, grid_y + i * cell_size, grid_size, thickness=3 if is_maj else 1)
            tb.draw_vline(grid_x + i * cell_size, grid_y, grid_size, thickness=3 if is_maj else 1)

        return tb.to_escpos()

    @staticmethod
    def _extract_line_clues(line: List[int]) -> List[int]:
        clues = []
        count = 0
        for val in line:
            if val == 1:
                count += 1
            elif count > 0:
                clues.append(count)
                count = 0
        if count > 0:
            clues.append(count)
        return clues if clues else [0]

    def verify_accuracy(
        self,
        puzzle_data: Union[BasePuzzleResult, Dict[str, Any]],
    ) -> Tuple[bool, str]:
        solution = puzzle_data.get("solution") or puzzle_data.get("board")
        row_clues = puzzle_data.get("row_clues")
        col_clues = puzzle_data.get("col_clues")

        if not solution or not isinstance(solution, list):
            return False, "Nonogram solution grid missing or invalid"
        rows = len(solution)
        cols = len(solution[0]) if rows > 0 else 0
        if rows < 5 or cols < 5:
            return False, f"Nonogram grid too small: {rows}x{cols}"
        if not row_clues or len(row_clues) != rows:
            return False, f"Nonogram row clues count ({len(row_clues) if row_clues else 0}) mismatches rows ({rows})"
        if not col_clues or len(col_clues) != cols:
            return False, f"Nonogram col clues count ({len(col_clues) if col_clues else 0}) mismatches cols ({cols})"

        # 1. Verify row clues match solution runs
        for r in range(rows):
            expected = self._extract_line_clues(solution[r])
            actual = row_clues[r]
            if actual != expected:
                return False, f"Nonogram row {r} clues {actual} do not match solution runs {expected}"

        # 2. Verify col clues match solution runs
        for c in range(cols):
            col_vals = [solution[r][c] for r in range(rows)]
            expected = self._extract_line_clues(col_vals)
            actual = col_clues[c]
            if actual != expected:
                return False, f"Nonogram col {c} clues {actual} do not match solution runs {expected}"

        # 3. Verify non-trivial density
        total_cells = rows * cols
        shaded_cells = sum(sum(row) for row in solution)
        if shaded_cells == 0:
            return False, "Nonogram board has 0 shaded cells (empty)"
        if shaded_cells == total_cells:
            return False, "Nonogram board is 100% full (trivial)"

        return True, "All rules satisfied"
