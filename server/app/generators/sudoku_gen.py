"""
Sudoku Generator and Solver
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import random
from typing import List, Tuple, Optional, Dict, Any

class SudokuGenerator:
    DIFFICULTY_CLUES = {
        "easy": 38,
        "medium": 30,
        "hard": 25
    }

    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)

    def generate(self, difficulty: str = "medium") -> Dict[str, Any]:
        """Generates a Sudoku puzzle with the given difficulty and a unique solution."""
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
                # Not unique, put it back
                puzzle_board[r][c] = temp
            else:
                clues_remaining -= 1

        return {
            "type": "sudoku",
            "difficulty": difficulty,
            "clues_count": clues_remaining,
            "grid": puzzle_board,
            "solution": solution_board,
            "text": self.format_text(puzzle_board)
        }

    def _is_valid(self, board: List[List[int]], row: int, col: int, num: int) -> bool:
        # Check row and column
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False

        # Check 3x3 box
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

    @staticmethod
    def format_text(board: List[List[int]]) -> str:
        lines = []
        for r in range(9):
            if r in (3, 6):
                lines.append("------+-------+------")
            row_chars = []
            for c in range(9):
                if c in (3, 6):
                    row_chars.append("|")
                val = board[r][c]
                row_chars.append(str(val) if val != 0 else ".")
            lines.append(" ".join(row_chars))
        return "\n".join(lines)


if __name__ == "__main__":
    gen = SudokuGenerator()
    puzzle = gen.generate(difficulty="medium")
    print(f"Generated Sudoku ({puzzle['difficulty']}, {puzzle['clues_count']} clues):")
    print(puzzle["text"])
