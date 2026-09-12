"""
Mines (Solitaire / Paper Minesweeper) Generator and Solver
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
from typing import List, Tuple, Optional, Dict, Any, Set

class MinesGenerator:
    """
    Procedural generator for Solitaire Paper Minesweeper (Simon Tatham mines.c / puzzle-magazine.com).
    Guarantees 100% solvability by pure human deduction with zero guessing.
    """

    DIFFICULTY_SETTINGS = {
        "easy": {"rows": 8, "cols": 8, "mines": 8, "target_clues": 28},
        "medium": {"rows": 8, "cols": 8, "mines": 12, "target_clues": 22},
        "hard": {"rows": 8, "cols": 8, "mines": 15, "target_clues": 17},
    }

    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)

    def _get_neighbors(self, r: int, c: int, rows: int, cols: int) -> List[Tuple[int, int]]:
        neighbors = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    neighbors.append((nr, nc))
        return neighbors

    def solve_deductive(self, rows: int, cols: int, clues: Dict[Tuple[int, int], int], total_mines: int) -> Tuple[bool, List[List[int]]]:
        """
        Solves using pure deductive logic:
        - Rule 1: Direct saturation (remaining unknown neighbors == remaining mines needed -> all mines)
        - Rule 2: Direct clearing (remaining mines needed == 0 -> all remaining unknown neighbors are safe)
        - Rule 3: Subset difference logic (U_A subset of U_B)
        - Rule 4: Global mine count capacity
        Returns (is_solved, state_grid where -1=unknown, 0=safe, 1=mine).
        """
        state = [[-1] * cols for _ in range(rows)]
        # Clue cells are known safe
        for (r, c) in clues:
            state[r][c] = 0

        changed = True
        while changed:
            changed = False

            # Rules 1 & 2: Local clue saturation & clearing
            for (r, c), val in clues.items():
                neighs = self._get_neighbors(r, c, rows, cols)
                unknowns = [p for p in neighs if state[p[0]][p[1]] == -1]
                mines = [p for p in neighs if state[p[0]][p[1]] == 1]
                rem = val - len(mines)

                if rem < 0 or len(unknowns) + len(mines) < val:
                    return False, state  # Contradiction

                if rem == 0 and unknowns:
                    for ur, uc in unknowns:
                        state[ur][uc] = 0
                        changed = True
                elif rem == len(unknowns) and unknowns:
                    for ur, uc in unknowns:
                        state[ur][uc] = 1
                        changed = True

            if changed:
                continue

            # Rule 3: Subset difference logic between clue pairs
            clue_list = list(clues.items())
            for i in range(len(clue_list)):
                (r1, c1), v1 = clue_list[i]
                n1 = self._get_neighbors(r1, c1, rows, cols)
                u1 = set(p for p in n1 if state[p[0]][p[1]] == -1)
                m1 = sum(1 for p in n1 if state[p[0]][p[1]] == 1)
                rem1 = v1 - m1

                for j in range(len(clue_list)):
                    if i == j:
                        continue
                    (r2, c2), v2 = clue_list[j]
                    n2 = self._get_neighbors(r2, c2, rows, cols)
                    u2 = set(p for p in n2 if state[p[0]][p[1]] == -1)
                    m2 = sum(1 for p in n2 if state[p[0]][p[1]] == 1)
                    rem2 = v2 - m2

                    if u1 and u1.issubset(u2):
                        diff = u2 - u1
                        rem_diff = rem2 - rem1
                        if rem_diff < 0:
                            return False, state
                        if rem_diff == 0 and diff:
                            for dr, dc in diff:
                                state[dr][dc] = 0
                                changed = True
                        elif len(diff) == rem_diff and diff:
                            for dr, dc in diff:
                                state[dr][dc] = 1
                                changed = True
                if changed:
                    break

            if changed:
                continue

            # Rule 4: Global mine capacity
            found_mines = sum(1 for r in range(rows) for c in range(cols) if state[r][c] == 1)
            all_unknowns = [(r, c) for r in range(rows) for c in range(cols) if state[r][c] == -1]
            rem_global = total_mines - found_mines

            if rem_global == 0 and all_unknowns:
                for ur, uc in all_unknowns:
                    state[ur][uc] = 0
                    changed = True
            elif len(all_unknowns) == rem_global and all_unknowns:
                for ur, uc in all_unknowns:
                    state[ur][uc] = 1
                    changed = True

        is_solved = all(state[r][c] != -1 for r in range(rows) for c in range(cols))
        return is_solved, state

    def generate(self, difficulty: str = "medium") -> Dict[str, Any]:
        difficulty = difficulty.lower()
        cfg = self.DIFFICULTY_SETTINGS.get(difficulty, self.DIFFICULTY_SETTINGS["medium"])
        rows = cfg["rows"]
        cols = cfg["cols"]
        num_mines = cfg["mines"]
        target_clues = cfg["target_clues"]

        all_cells = [(r, c) for r in range(rows) for c in range(cols)]

        for _ in range(100):
            mine_set = set(random.sample(all_cells, num_mines))

            # Compute full clues for all non-mine cells
            full_clues: Dict[Tuple[int, int], int] = {}
            for r in range(rows):
                for c in range(cols):
                    if (r, c) not in mine_set:
                        neighs = self._get_neighbors(r, c, rows, cols)
                        full_clues[(r, c)] = sum(1 for p in neighs if p in mine_set)

            # Check if fully solvable with all non-mine clues revealed
            is_solved, _ = self.solve_deductive(rows, cols, full_clues, num_mines)
            if not is_solved:
                continue

            # Iteratively prune clues down to target while preserving solvability
            pruned_clues = dict(full_clues)
            clue_keys = list(full_clues.keys())
            random.shuffle(clue_keys)

            for k in clue_keys:
                if len(pruned_clues) <= target_clues:
                    break
                val = pruned_clues.pop(k)
                solved, _ = self.solve_deductive(rows, cols, pruned_clues, num_mines)
                if not solved:
                    pruned_clues[k] = val  # Restore

            # Build grid for representation (-1 = blank unrevealed, 0..8 = clue number)
            puzzle_grid = [[-1] * cols for _ in range(rows)]
            for (r, c), val in pruned_clues.items():
                puzzle_grid[r][c] = val

            solution_grid = [[0] * cols for _ in range(rows)]
            for r, c in mine_set:
                solution_grid[r][c] = 1

            mine_coords = sorted(list(mine_set))

            return {
                "title": "MINES",
                "difficulty": difficulty.upper(),
                "rows": rows,
                "cols": cols,
                "total_mines": num_mines,
                "clues_count": len(pruned_clues),
                "puzzle": puzzle_grid,
                "solution": solution_grid,
                "mine_coords": mine_coords
            }

        raise RuntimeError("Failed to generate deducible Mines puzzle")

    def format_ascii(self, puzzle_data: Dict[str, Any]) -> str:
        rows = puzzle_data["rows"]
        cols = puzzle_data["cols"]
        puzzle = puzzle_data["puzzle"]
        lines = []
        lines.append("--- MINES ---")
        lines.append(f"DIFFICULTY: {puzzle_data['difficulty']}")
        total_mines = puzzle_data.get('total_mines', 12)
        lines.append(f"Use the numbered clues showing adjacent mine counts to deduce each of the {total_mines} hidden mines across the grid.")
        lines.append(f"TOTAL MINES: {puzzle_data['total_mines']}")
        lines.append("")

        sep = "   +" + "---+" * cols
        lines.append(sep)
        for r in range(rows):
            line = "   |"
            for c in range(cols):
                val = puzzle[r][c]
                line += "   |" if val == -1 else f" {val} |"
            lines.append(line)
            lines.append(sep)

        return "\n".join(lines)
