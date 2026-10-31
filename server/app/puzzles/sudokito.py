"""
Morning Puzzles - Sudokito Plugin
Encapsulates generation, canonical instruction formatting, ASCII layout,
solution key formatting, and 576-dot thermal raster rendering for 6x6 mini-sudoku.
"""

import random
from typing import List, Tuple, Optional, Dict, Any, Union

from .base import BasePuzzle, BasePuzzleResult
from ..renderer.canvas import (
    THERMAL_WIDTH_DOTS,
    ThermalBitmap,
)


class SudokitoPuzzle(BasePuzzle):
    """Sudokito 6x6 mini-sudoku puzzle plugin with 2x3 regions and unique solution guarantees."""

    DIFFICULTY_CLUES = {
        "easy": 18,
        "medium": 14,
        "hard": 11,
    }

    @property
    def puzzle_id(self) -> str:
        return "sudokito"

    @property
    def title(self) -> str:
        return "SUDOKITO"

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
        target_clues = self.DIFFICULTY_CLUES.get(difficulty, 14)

        # 1. Generate full solved 6x6 board
        solution_board = [[0] * 6 for _ in range(6)]
        self._fill_board(solution_board)

        # 2. Clone board to create puzzle by removing numbers
        puzzle_board = [row[:] for row in solution_board]

        # Cells paired with 180-degree rotational symmetry
        # (r, c) paired with (5 - r, 5 - c)
        pairs: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []
        visited = set()
        for r in range(6):
            for c in range(6):
                if (r, c) not in visited:
                    sym_r, sym_c = 5 - r, 5 - c
                    pairs.append(((r, c), (sym_r, sym_c)))
                    visited.add((r, c))
                    visited.add((sym_r, sym_c))

        random.shuffle(pairs)

        clues_remaining = 36
        # First pass: symmetric pair removal
        for (r1, c1), (r2, c2) in pairs:
            if clues_remaining <= target_clues:
                break

            v1, v2 = puzzle_board[r1][c1], puzzle_board[r2][c2]
            puzzle_board[r1][c1] = 0
            puzzle_board[r2][c2] = 0

            sols = self._count_solutions(puzzle_board, max_count=2)
            if sols != 1:
                puzzle_board[r1][c1] = v1
                puzzle_board[r2][c2] = v2
            else:
                clues_remaining -= 2

        # Second pass: if target is odd (e.g. 11), try single cell removals
        if clues_remaining > target_clues:
            single_cells = [(r, c) for r in range(6) for c in range(6) if puzzle_board[r][c] != 0]
            random.shuffle(single_cells)
            for r, c in single_cells:
                if clues_remaining <= target_clues:
                    break
                temp = puzzle_board[r][c]
                puzzle_board[r][c] = 0
                if self._count_solutions(puzzle_board, max_count=2) != 1:
                    puzzle_board[r][c] = temp
                else:
                    clues_remaining -= 1

        ascii_text = self.format_ascii_puzzle({"grid": puzzle_board})
        instruction = self.get_instruction({"difficulty": difficulty})

        raw_data = {
            "type": "sudokito",
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
        return "Fill every row, column, and 2x3 box with digits 1-6 without repeating."

    def format_ascii_puzzle(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        board = puzzle_data.get("grid", [])
        lines = []
        for r in range(6):
            if r in (2, 4):
                lines.append("------+------")
            row_chars = []
            for c in range(6):
                if c == 3:
                    row_chars.append("|")
                val = board[r][c] if r < len(board) and c < len(board[r]) else 0
                row_chars.append(str(val) if val != 0 else ".")
            lines.append(" ".join(row_chars))
        return "\n".join(lines)

    def render_raster(
        self,
        puzzle_data: Union[BasePuzzleResult, Dict[str, Any]],
        target_width: int = THERMAL_WIDTH_DOTS,
    ) -> bytes:
        board = puzzle_data.get("grid") or puzzle_data.get("puzzle") or []
        padding = 24
        board_size = target_width - padding * 2
        c_size = board_size // 6
        total_h = padding + c_size * 6 + padding
        tb = ThermalBitmap(target_width, total_h)

        # Draw grid lines: 4px for outer frame and 2x3 box boundaries; 1px for inner dividers
        for i in range(7):
            pos = padding + i * c_size
            is_major = (i % 2 == 0)
            tb.draw_hline(padding, pos, c_size * 6, thickness=4 if is_major else 1)

        for i in range(7):
            pos = padding + i * c_size
            is_major = (i % 3 == 0)
            tb.draw_vline(pos, padding, c_size * 6, thickness=4 if is_major else 1)

        for r in range(6):
            for c in range(6):
                val = board[r][c] if r < len(board) and c < len(board[r]) else 0
                if val != 0:
                    cx = padding + c * c_size + (c_size - 18) // 2
                    cy = padding + r * c_size + (c_size - 21) // 2
                    tb.draw_char(cx, cy, str(val), scale=3)

        return tb.to_escpos()

    # --- Solver & Generator Helpers ---
    def _is_valid(self, board: List[List[int]], row: int, col: int, num: int) -> bool:
        for i in range(6):
            if board[row][i] == num or board[i][col] == num:
                return False
        box_r, box_c = (row // 2) * 2, (col // 3) * 3
        for r in range(box_r, box_r + 2):
            for c in range(box_c, box_c + 3):
                if board[r][c] == num:
                    return False
        return True

    def _fill_board(self, board: List[List[int]]) -> bool:
        for r in range(6):
            for c in range(6):
                if board[r][c] == 0:
                    nums = list(range(1, 7))
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
        for r in range(6):
            for c in range(6):
                if board[r][c] == 0:
                    count = 0
                    for num in range(1, 7):
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
        if not puzzle or len(puzzle) != 6 or any(len(r) != 6 for r in puzzle):
            return False, "Sudokito puzzle grid must be 6x6"
        if not solution or len(solution) != 6 or any(len(r) != 6 for r in solution):
            return False, "Sudokito solution grid must be 6x6"

        # 1. Verify solution validity
        digits = set(range(1, 7))
        for r in range(6):
            if set(solution[r]) != digits:
                return False, f"Sudokito solution row {r} does not contain digits 1-6"
        for c in range(6):
            col_vals = {solution[r][c] for r in range(6)}
            if col_vals != digits:
                return False, f"Sudokito solution col {c} does not contain digits 1-6"
        for br in (0, 2, 4):
            for bc in (0, 3):
                box_vals = {solution[r][c] for r in range(br, br + 2) for c in range(bc, bc + 3)}
                if box_vals != digits:
                    return False, f"Sudokito solution box at ({br},{bc}) does not contain digits 1-6"

        # 2. Verify givens consistency
        clue_count = 0
        for r in range(6):
            for c in range(6):
                val = puzzle[r][c]
                if val != 0:
                    clue_count += 1
                    if val != solution[r][c]:
                        return False, f"Sudokito given clue at ({r},{c})={val} mismatches solution={solution[r][c]}"
        if clue_count < 8:
            return False, f"Sudokito has fewer than 8 clues ({clue_count}), impossible to have unique solution"

        # 3. Verify unique solvability
        test_board = [row[:] for row in puzzle]
        sols = self._count_solutions(test_board, max_count=2)
        if sols == 0:
            return False, "Sudokito puzzle has no valid solutions"
        if sols > 1:
            return False, "Sudokito puzzle has multiple solutions (not unique)"

        return True, "All rules satisfied"
