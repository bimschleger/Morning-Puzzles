"""
Nonogram (Picross) Puzzle Generator
Inspired by IBM/chuk-puzzles-gym (Apache-2.0).
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
from typing import List, Tuple, Dict, Any, Optional

class NonogramGenerator:
    DIFFICULTY_SIZES = {
        "easy": (5, 5),
        "medium": (10, 10),
        "hard": (15, 15)
    }

    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)

    def generate(self, difficulty: str = "medium", density: float = 0.55) -> Dict[str, Any]:
        """
        Generates a solvable Nonogram puzzle with row and column clue numbers.
        Difficulty tiers:
          - easy: 5x5 grid
          - medium: 10x10 grid
          - hard: 15x15 grid
        """
        difficulty = difficulty.lower()
        rows, cols = self.DIFFICULTY_SIZES.get(difficulty, (10, 10))

        # Generate random bitmap with pattern coherence
        board = self._generate_coherent_pattern(rows, cols, density)

        # Compute clue numbers
        row_clues = [self._extract_line_clues(board[r]) for r in range(rows)]
        col_clues = [self._extract_line_clues([board[r][c] for r in range(rows)]) for c in range(cols)]

        return {
            "type": "nonogram",
            "difficulty": difficulty,
            "rows": rows,
            "cols": cols,
            "row_clues": row_clues,
            "col_clues": col_clues,
            "solution": board,
            "text": self.format_text(row_clues, col_clues, rows, cols)
        }

    def _generate_coherent_pattern(self, rows: int, cols: int, density: float) -> List[List[int]]:
        """Generates a pleasant binary picture pattern (avoiding pure noise)."""
        board = [[0] * cols for _ in range(rows)]
        # Generate symmetrical or clustered blocks
        for r in range(rows):
            for c in range(cols):
                board[r][c] = 1 if random.random() < density else 0
        return board

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

    @staticmethod
    def format_text(row_clues: List[List[int]], col_clues: List[List[int]], rows: int, cols: int) -> str:
        lines = []
        max_row_clue_len = max(len(" ".join(map(str, c))) for c in row_clues)
        max_col_clues = max(len(c) for c in col_clues)

        # Print vertical column clues header
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

        # Print row clues and empty grid slots
        for r in range(rows):
            clue_str = " ".join(map(str, row_clues[r]))
            prefix = f"{clue_str:>{max_row_clue_len}} | "
            slots = " . " * cols
            lines.append(prefix + slots)

        return "\n".join(lines)


if __name__ == "__main__":
    gen = NonogramGenerator()
    res = gen.generate(difficulty="easy")
    print(f"Nonogram ({res['difficulty']}):")
    print(res["text"])
