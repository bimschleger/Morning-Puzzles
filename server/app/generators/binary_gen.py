"""
Binary (Takuzu / Binairo) Puzzle Generator and Solver
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

class BinaryGenerator:
    """
    Procedural generator for Binary Puzzles (Takuzu / Binairo / IBM chuk-gym #4).
    Rules:
    1. Each cell contains 0 or 1.
    2. No more than two identical numbers may be adjacent (no 000 or 111).
    3. Each row and column has an equal count of 0s and 1s (N/2 each).
    4. Each row is unique, and each column is unique.
    5. Exactly one unique solution deducible without guessing.
    """

    DIFFICULTY_SETTINGS = {
        "easy": {"size": 6, "target_clues": 16, "max_rule": 2},
        "medium": {"size": 8, "target_clues": 28, "max_rule": 2},
        "hard": {"size": 8, "target_clues": 22, "max_rule": 3},
    }

    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)

    def _get_valid_lines(self, n: int) -> List[List[int]]:
        half = n // 2
        valid = []
        for i in range(1 << n):
            bits = [(i >> (n - 1 - k)) & 1 for k in range(n)]
            if sum(bits) != half:
                continue
            has_trio = False
            for k in range(n - 2):
                if bits[k] == bits[k + 1] == bits[k + 2]:
                    has_trio = True
                    break
            if not has_trio:
                valid.append(bits)
        return valid

    def _generate_full_board(self, n: int) -> Optional[List[List[int]]]:
        half = n // 2
        valid_lines = self._get_valid_lines(n)
        grid = [[-1] * n for _ in range(n)]

        def can_place_row(r: int, row_cand: List[int]) -> bool:
            # Rule 4: Row uniqueness
            for pr in range(r):
                if grid[pr] == row_cand:
                    return False
            # Check column constraints
            for c in range(n):
                val = row_cand[c]
                # Trio check in column
                if r >= 2 and grid[r - 1][c] == val and grid[r - 2][c] == val:
                    return False
                # Count check in column
                col_count = sum(1 for pr in range(r) if grid[pr][c] == val) + 1
                if col_count > half:
                    return False
                # If last row, check column uniqueness
                if r == n - 1:
                    col_c = [grid[pr][c] for pr in range(n - 1)] + [val]
                    for pc in range(c):
                        col_pc = [grid[pr][pc] for pr in range(n)]
                        if col_c == col_pc:
                            return False
            return True

        def backtrack(r: int) -> bool:
            if r == n:
                return True
            cands = list(valid_lines)
            random.shuffle(cands)
            for cand in cands:
                if can_place_row(r, cand):
                    grid[r] = cand[:]
                    if backtrack(r + 1):
                        return True
                    grid[r] = [-1] * n
            return False

        if backtrack(0):
            return grid
        return None

    def solve_deductive(self, grid: List[List[int]], n: int, max_rule: int = 3) -> Tuple[bool, List[List[int]], Set[int]]:
        g = [row[:] for row in grid]
        half = n // 2
        changed = True
        rules_used = set()

        while changed:
            changed = False

            # Rule 1: Trio avoidance
            for r in range(n):
                for c in range(n - 2):
                    v = [g[r][c], g[r][c + 1], g[r][c + 2]]
                    if v[0] == v[1] != -1 and v[2] == -1:
                        g[r][c + 2] = 1 - v[0]
                        changed = True
                        rules_used.add(1)
                    if v[1] == v[2] != -1 and v[0] == -1:
                        g[r][c] = 1 - v[1]
                        changed = True
                        rules_used.add(1)
                    if v[0] == v[2] != -1 and v[1] == -1:
                        g[r][c + 1] = 1 - v[0]
                        changed = True
                        rules_used.add(1)

            for c in range(n):
                for r in range(n - 2):
                    v = [g[r][c], g[r + 1][c], g[r + 2][c]]
                    if v[0] == v[1] != -1 and v[2] == -1:
                        g[r + 2][c] = 1 - v[0]
                        changed = True
                        rules_used.add(1)
                    if v[1] == v[2] != -1 and v[0] == -1:
                        g[r][c] = 1 - v[1]
                        changed = True
                        rules_used.add(1)
                    if v[0] == v[2] != -1 and v[1] == -1:
                        g[r + 1][c] = 1 - v[0]
                        changed = True
                        rules_used.add(1)

            if changed:
                continue

            # Rule 2: Line count
            for r in range(n):
                c0, c1 = g[r].count(0), g[r].count(1)
                if c0 == half and c1 < half:
                    for c in range(n):
                        if g[r][c] == -1:
                            g[r][c] = 1
                            changed = True
                            rules_used.add(2)
                elif c1 == half and c0 < half:
                    for c in range(n):
                        if g[r][c] == -1:
                            g[r][c] = 0
                            changed = True
                            rules_used.add(2)

            for c in range(n):
                col = [g[r][c] for r in range(n)]
                c0, c1 = col.count(0), col.count(1)
                if c0 == half and c1 < half:
                    for r in range(n):
                        if g[r][c] == -1:
                            g[r][c] = 1
                            changed = True
                            rules_used.add(2)
                elif c1 == half and c0 < half:
                    for r in range(n):
                        if g[r][c] == -1:
                            g[r][c] = 0
                            changed = True
                            rules_used.add(2)

            if changed:
                continue

            # Rule 3: Line uniqueness (Rule 4 from binarypuzzle.com)
            if max_rule >= 3:
                for r in range(n):
                    if g[r].count(-1) == 2 and g[r].count(0) == half - 1 and g[r].count(1) == half - 1:
                        e = [c for c in range(n) if g[r][c] == -1]
                        ta = g[r][:]
                        ta[e[0]], ta[e[1]] = 0, 1
                        if any(g[o] == ta for o in range(n) if o != r and -1 not in g[o]):
                            g[r][e[0]], g[r][e[1]] = 1, 0
                            changed = True
                            rules_used.add(3)
                        else:
                            tb = g[r][:]
                            tb[e[0]], tb[e[1]] = 1, 0
                            if any(g[o] == tb for o in range(n) if o != r and -1 not in g[o]):
                                g[r][e[0]], g[r][e[1]] = 0, 1
                                changed = True
                                rules_used.add(3)

                for c in range(n):
                    col = [g[r][c] for r in range(n)]
                    if col.count(-1) == 2 and col.count(0) == half - 1 and col.count(1) == half - 1:
                        e = [r for r in range(n) if col[r] == -1]
                        ta = col[:]
                        ta[e[0]], ta[e[1]] = 0, 1
                        match_a = any(
                            [g[r][oc] for r in range(n)] == ta
                            for oc in range(n)
                            if oc != c and all(g[r][oc] != -1 for r in range(n))
                        )
                        if match_a:
                            g[e[0]][c], g[e[1]][c] = 1, 0
                            changed = True
                            rules_used.add(3)
                        else:
                            tb = col[:]
                            tb[e[0]], tb[e[1]] = 1, 0
                            match_b = any(
                                [g[r][oc] for r in range(n)] == tb
                                for oc in range(n)
                                if oc != c and all(g[r][oc] != -1 for r in range(n))
                            )
                            if match_b:
                                g[e[0]][c], g[e[1]][c] = 0, 1
                                changed = True
                                rules_used.add(3)

        is_solved = all(g[r][c] != -1 for r in range(n) for c in range(n))
        return is_solved, g, rules_used

    def generate(self, difficulty: str = "medium") -> Dict[str, Any]:
        difficulty = difficulty.lower()
        cfg = self.DIFFICULTY_SETTINGS.get(difficulty, self.DIFFICULTY_SETTINGS["medium"])
        size = cfg["size"]
        target_clues = cfg["target_clues"]
        max_rule = cfg["max_rule"]

        solution = self._generate_full_board(size)
        if not solution:
            raise RuntimeError("Failed to generate full binary board")

        puzzle = [row[:] for row in solution]
        coords = [(r, c) for r in range(size) for c in range(size)]
        random.shuffle(coords)

        clues_remaining = size * size
        for r, c in coords:
            if clues_remaining <= target_clues:
                break
            saved = puzzle[r][c]
            puzzle[r][c] = -1
            is_solved, _, _ = self.solve_deductive(puzzle, size, max_rule)
            if is_solved:
                clues_remaining -= 1
            else:
                puzzle[r][c] = saved

        return {
            "title": "BINARY",
            "difficulty": difficulty.upper(),
            "size": size,
            "puzzle": puzzle,
            "solution": solution,
            "clues_count": clues_remaining
        }

    def format_ascii(self, puzzle_data: Dict[str, Any]) -> str:
        size = puzzle_data["size"]
        puzzle = puzzle_data["puzzle"]
        lines = []
        lines.append(f"--- BINARY ---")
        lines.append(f"DIFFICULTY: {puzzle_data['difficulty']}")
        lines.append("")

        sep = "   +" + "---+" * size
        lines.append(sep)
        for r in range(size):
            line = "   |"
            for c in range(size):
                v = puzzle[r][c]
                line += "   |" if v == -1 else f" {v} |"
            lines.append(line)
            lines.append(sep)

        return "\n".join(lines)
