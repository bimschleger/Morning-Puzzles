"""
Morning Puzzles - Sudoku Plugin
Encapsulates generation, canonical instruction formatting, ASCII layout,
solution key formatting, and 576-dot thermal raster rendering.
"""

import random
from typing import List, Tuple, Optional, Dict, Any, Union

from .base import BasePuzzle, BasePuzzleResult
from ..renderer.canvas import (
    THERMAL_WIDTH_DOTS,
    HAS_PILLOW,
    pil_to_escpos,
    ThermalBitmap,
)

if HAS_PILLOW:
    from PIL import Image, ImageDraw, ImageFont


class SudokuPuzzle(BasePuzzle):
    """Sudoku 9x9 puzzle plugin with unique solution guarantees."""

    DIFFICULTY_CLUES = {
        "easy": 38,
        "medium": 30,
        "hard": 25,
    }

    @property
    def puzzle_id(self) -> str:
        return "sudoku"

    @property
    def title(self) -> str:
        return "SUDOKU"

    @property
    def has_difficulty(self) -> bool:
        return True

    @property
    def supported_difficulties(self) -> List[str]:
        return ["easy", "medium", "hard"]

    def generate(self, difficulty: str = "medium", seed: Optional[int] = None, **kwargs) -> BasePuzzleResult:
        if seed is not None:
            random.seed(seed)

        difficulty = difficulty.lower()
        target_clues = self.DIFFICULTY_CLUES.get(difficulty, 30)

        # 1. Generate full solved 9x9 board
        solution_board = [[0] * 9 for _ in range(9)]
        self._fill_board(solution_board)

        # 2. Clone board to create puzzle by removing numbers
        puzzle_board = [row[:] for row in solution_board]

        # Cells to try removing
        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)

        clues_remaining = 81
        for r, c in cells:
            if clues_remaining <= target_clues:
                break

            temp = puzzle_board[r][c]
            puzzle_board[r][c] = 0

            # Count solutions to verify uniqueness
            solutions = self._count_solutions(puzzle_board, max_count=2)
            if solutions != 1:
                puzzle_board[r][c] = temp
            else:
                clues_remaining -= 1

        ascii_text = self.format_ascii_puzzle({"grid": puzzle_board})
        instruction = self.get_instruction({"difficulty": difficulty})

        raw_data = {
            "type": "sudoku",
            "difficulty": difficulty,
            "clues_count": clues_remaining,
            "grid": puzzle_board,
            "solution": solution_board,
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
        return "Fill every row, column, and 3x3 box with digits 1-9 without repeating."

    def format_ascii_puzzle(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        board = puzzle_data.get("grid", [])
        lines = []
        for r in range(9):
            if r in (3, 6):
                lines.append("------+-------+------")
            row_chars = []
            for c in range(9):
                if c in (3, 6):
                    row_chars.append("|")
                val = board[r][c] if r < len(board) and c < len(board[r]) else 0
                row_chars.append(str(val) if val != 0 else ".")
            lines.append(" ".join(row_chars))
        return "\n".join(lines)

    def format_solution_key(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> List[str]:
        sol = puzzle_data.get("solution", [])
        if not sol:
            return []
        lines = []
        for row in sol:
            lines.append("      " + " ".join(str(x) for x in row))
        return lines

    def render_raster(
        self,
        puzzle_data: Union[BasePuzzleResult, Dict[str, Any]],
        target_width: int = THERMAL_WIDTH_DOTS,
    ) -> bytes:
        board = puzzle_data.get("grid", [])
        padding = 24
        board_size = target_width - padding * 2
        cell_size = board_size / 9.0

        if HAS_PILLOW:
            total_height = int(padding + board_size + padding)
            img = Image.new("L", (target_width, total_height), 255)
            draw = ImageDraw.Draw(img)

            try:
                font_digit = ImageFont.truetype("Courier.ttf", int(cell_size * 0.6))
            except IOError:
                font_digit = ImageFont.load_default()

            for i in range(10):
                pos = padding + i * cell_size
                is_major = (i % 3 == 0)
                w = 4 if is_major else 1
                color = 0 if is_major else 180
                draw.line([padding, pos, padding + board_size, pos], fill=color, width=w)
                draw.line([pos, padding, pos, padding + board_size], fill=color, width=w)

            for r in range(9):
                for c in range(9):
                    val = board[r][c] if r < len(board) and c < len(board[r]) else 0
                    if val != 0:
                        cx = padding + c * cell_size + cell_size // 2 - int(cell_size * 0.16)
                        cy = padding + r * cell_size + cell_size // 2 - int(cell_size * 0.32)
                        draw.text((cx, cy), str(val), fill=0, font=font_digit)

            return pil_to_escpos(img)

        # Pure Python ThermalBitmap Fallback
        c_size = board_size // 9
        total_h = padding + c_size * 9 + padding
        tb = ThermalBitmap(target_width, total_h)

        for i in range(10):
            pos = padding + i * c_size
            is_major = (i % 3 == 0)
            tb.draw_hline(padding, pos, c_size * 9, thickness=4 if is_major else 1)
            tb.draw_vline(pos, padding, c_size * 9, thickness=4 if is_major else 1)

        for r in range(9):
            for c in range(9):
                val = board[r][c] if r < len(board) and c < len(board[r]) else 0
                if val != 0:
                    cx = padding + c * c_size + (c_size - 18) // 2
                    cy = padding + r * c_size + (c_size - 21) // 2
                    tb.draw_char(cx, cy, str(val), scale=3)

        return tb.to_escpos()

    # --- Solver & Generator Helpers ---
    def _is_valid(self, board: List[List[int]], row: int, col: int, num: int) -> bool:
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
        box_r, box_c = (row // 3) * 3, (col // 3) * 3
        for r in range(box_r, box_r + 3):
            for c in range(box_c, box_c + 3):
                if board[r][c] == num:
                    return False
        return True

    def _fill_board(self, board: List[List[int]]) -> bool:
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    nums = list(range(1, 10))
                    random.shuffle(nums)
                    for num in nums:
                        if self._is_valid(board, r, c, num):
                            board[r][c] = num
                            if self._fill_board(board):
                                return True
                            board[r][c] = 0
                    return False
        return True

    def _count_solutions(self, board: List[List[int]], max_count: int = 2) -> int:
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    count = 0
                    for num in range(1, 10):
                        if self._is_valid(board, r, c, num):
                            board[r][c] = num
                            count += self._count_solutions(board, max_count)
                            board[r][c] = 0
                            if count >= max_count:
                                return count
                    return count
        return 1

    def verify_accuracy(
        self,
        puzzle_data: Union[BasePuzzleResult, Dict[str, Any]],
    ) -> Tuple[bool, str]:
        puzzle = puzzle_data.get("puzzle") or puzzle_data.get("grid")
        solution = puzzle_data.get("solution")
        if not puzzle or len(puzzle) != 9 or any(len(r) != 9 for r in puzzle):
            return False, "Sudoku puzzle grid must be 9x9"
        if not solution or len(solution) != 9 or any(len(r) != 9 for r in solution):
            return False, "Sudoku solution grid must be 9x9"

        # 1. Verify solution validity
        digits = set(range(1, 10))
        for r in range(9):
            if set(solution[r]) != digits:
                return False, f"Sudoku solution row {r} does not contain digits 1-9"
        for c in range(9):
            col_vals = {solution[r][c] for r in range(9)}
            if col_vals != digits:
                return False, f"Sudoku solution col {c} does not contain digits 1-9"
        for br in (0, 3, 6):
            for bc in (0, 3, 6):
                box_vals = {solution[r][c] for r in range(br, br + 3) for c in range(bc, bc + 3)}
                if box_vals != digits:
                    return False, f"Sudoku solution box at ({br},{bc}) does not contain digits 1-9"

        # 2. Verify givens consistency
        clue_count = 0
        for r in range(9):
            for c in range(9):
                val = puzzle[r][c]
                if val != 0:
                    clue_count += 1
                    if val != solution[r][c]:
                        return False, f"Sudoku given clue at ({r},{c})={val} mismatches solution={solution[r][c]}"
        if clue_count < 17:
            return False, f"Sudoku has fewer than 17 clues ({clue_count}), impossible to have unique solution"

        # 3. Verify unique solvability
        test_board = [row[:] for row in puzzle]
        sols = self._count_solutions(test_board, max_count=2)
        if sols == 0:
            return False, "Sudoku puzzle has no valid solutions"
        if sols > 1:
            return False, "Sudoku puzzle has multiple solutions (not unique)"

        return True, "All rules satisfied"
