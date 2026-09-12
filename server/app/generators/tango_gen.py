"""
Tango (Binairo+ / Equal & Opposite Binary) Puzzle Generator and Solver
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


class TangoGenerator:
    """
    Procedural generator for Tango / Binairo+ puzzles.
    Rules:
    1. Each cell contains 0 or 1.
    2. Balance: Each row and column contains an equal number of 0s and 1s (N/2 each).
    3. No trios: No three consecutive identical numbers horizontally or vertically (no 000 or 111).
    4. Edge clues:
       - '=' between adjacent cells indicates both cells contain the identical digit.
       - 'x' between adjacent cells indicates both cells contain opposite digits.
    5. Unlike classic Takuzu/Binary, duplicate rows and columns ARE permitted.
    6. Exactly one unique solution deducible without guessing.
    """

    DIFFICULTY_SETTINGS = {
        "easy": {
            "size": 6,
            "target_numbers": 6,
            "target_edges": 6,
        },
        "medium": {
            "size": 6,
            "target_numbers": 4,
            "target_edges": 8,
        },
        "hard": {
            "size": 8,
            "target_numbers": 10,
            "target_edges": 14,
        },
    }

    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)

    def _get_valid_lines(self, n: int) -> List[List[int]]:
        """Returns all 0/1 permutations of length n with sum n/2 and no trios."""
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
        """Generates a complete, valid Tango grid."""
        half = n // 2
        valid_lines = self._get_valid_lines(n)
        grid = [[-1] * n for _ in range(n)]

        def can_place_row(r: int, row_cand: List[int]) -> bool:
            for c in range(n):
                val = row_cand[c]
                # Column trio check
                if r >= 2 and grid[r - 1][c] == val and grid[r - 2][c] == val:
                    return False
                # Column count check
                col_count = sum(1 for pr in range(r) if grid[pr][c] == val) + 1
                if col_count > half:
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

    def _is_candidate_valid(
        self,
        g: List[List[int]],
        edges_h: List[List[int]],
        edges_v: List[List[int]],
        n: int,
        r: int,
        c: int,
        val: int
    ) -> bool:
        """Checks if setting g[r][c] = val violates any local constraints."""
        half = n // 2

        # Check row count
        if g[r].count(val) + 1 > half:
            return False

        # Check col count
        col_vals = [g[pr][c] for pr in range(n)]
        if col_vals.count(val) + 1 > half:
            return False

        # Check row trios
        if c >= 2 and g[r][c - 2] == val and g[r][c - 1] == val:
            return False
        if 0 < c < n - 1 and g[r][c - 1] == val and g[r][c + 1] == val:
            return False
        if c <= n - 3 and g[r][c + 1] == val and g[r][c + 2] == val:
            return False

        # Check col trios
        if r >= 2 and g[r - 2][c] == val and g[r - 1][c] == val:
            return False
        if 0 < r < n - 1 and g[r - 1][c] == val and g[r + 1][c] == val:
            return False
        if r <= n - 3 and g[r + 1][c] == val and g[r + 2][c] == val:
            return False

        # Edge constraints
        # Left edge
        if c > 0:
            e = edges_h[r][c - 1]
            if e == 1 and g[r][c - 1] != -1 and g[r][c - 1] != val:
                return False
            if e == 2 and g[r][c - 1] != -1 and g[r][c - 1] == val:
                return False
        # Right edge
        if c < n - 1:
            e = edges_h[r][c]
            if e == 1 and g[r][c + 1] != -1 and g[r][c + 1] != val:
                return False
            if e == 2 and g[r][c + 1] != -1 and g[r][c + 1] == val:
                return False
        # Top edge
        if r > 0:
            e = edges_v[r - 1][c]
            if e == 1 and g[r - 1][c] != -1 and g[r - 1][c] != val:
                return False
            if e == 2 and g[r - 1][c] != -1 and g[r - 1][c] == val:
                return False
        # Bottom edge
        if r < n - 1:
            e = edges_v[r][c]
            if e == 1 and g[r + 1][c] != -1 and g[r + 1][c] != val:
                return False
            if e == 2 and g[r + 1][c] != -1 and g[r + 1][c] == val:
                return False

        return True

    def solve_deductive(
        self,
        grid: List[List[int]],
        edges_h: List[List[int]],
        edges_v: List[List[int]],
        n: int
    ) -> Tuple[bool, List[List[int]]]:
        """
        Human-like deductive solver. Applies direct edge deductions, trio avoidance,
        equal-sign outer neighbor restrictions, line balancing, and 1-step logic.
        Returns (is_solved, solved_grid).
        """
        g = [row[:] for row in grid]
        half = n // 2
        changed = True

        while changed:
            changed = False

            # Pass 1: Direct edge clues
            for r in range(n):
                for c in range(n - 1):
                    e = edges_h[r][c]
                    if e == 1:  # '='
                        if g[r][c] != -1 and g[r][c + 1] == -1:
                            g[r][c + 1] = g[r][c]
                            changed = True
                        elif g[r][c + 1] != -1 and g[r][c] == -1:
                            g[r][c] = g[r][c + 1]
                            changed = True
                    elif e == 2:  # 'x'
                        if g[r][c] != -1 and g[r][c + 1] == -1:
                            g[r][c + 1] = 1 - g[r][c]
                            changed = True
                        elif g[r][c + 1] != -1 and g[r][c] == -1:
                            g[r][c] = 1 - g[r][c + 1]
                            changed = True

            for r in range(n - 1):
                for c in range(n):
                    e = edges_v[r][c]
                    if e == 1:  # '='
                        if g[r][c] != -1 and g[r + 1][c] == -1:
                            g[r + 1][c] = g[r][c]
                            changed = True
                        elif g[r + 1][c] != -1 and g[r][c] == -1:
                            g[r][c] = g[r + 1][c]
                            changed = True
                    elif e == 2:  # 'x'
                        if g[r][c] != -1 and g[r + 1][c] == -1:
                            g[r + 1][c] = 1 - g[r][c]
                            changed = True
                        elif g[r + 1][c] != -1 and g[r][c] == -1:
                            g[r][c] = 1 - g[r + 1][c]
                            changed = True

            if changed:
                continue

            # Pass 2: Trio avoidance
            for r in range(n):
                for c in range(n - 2):
                    v0, v1, v2 = g[r][c], g[r][c + 1], g[r][c + 2]
                    if v0 == v1 != -1 and v2 == -1:
                        g[r][c + 2] = 1 - v0
                        changed = True
                    if v1 == v2 != -1 and v0 == -1:
                        g[r][c] = 1 - v1
                        changed = True
                    if v0 == v2 != -1 and v1 == -1:
                        g[r][c + 1] = 1 - v0
                        changed = True

            for c in range(n):
                for r in range(n - 2):
                    v0, v1, v2 = g[r][c], g[r + 1][c], g[r + 2][c]
                    if v0 == v1 != -1 and v2 == -1:
                        g[r + 2][c] = 1 - v0
                        changed = True
                    if v1 == v2 != -1 and v0 == -1:
                        g[r][c] = 1 - v1
                        changed = True
                    if v0 == v2 != -1 and v1 == -1:
                        g[r + 1][c] = 1 - v0
                        changed = True

            if changed:
                continue

            # Pass 3: Edge-Trio interaction (Equal sign prevents equal adjacent outer neighbors)
            for r in range(n):
                for c in range(n - 1):
                    if edges_h[r][c] == 1:
                        if c > 0 and g[r][c - 1] != -1:
                            if g[r][c] == -1:
                                g[r][c] = 1 - g[r][c - 1]
                                changed = True
                            if g[r][c + 1] == -1:
                                g[r][c + 1] = 1 - g[r][c - 1]
                                changed = True
                        if c > 0 and g[r][c] != -1 and g[r][c - 1] == -1:
                            g[r][c - 1] = 1 - g[r][c]
                            changed = True
                        if c + 2 < n and g[r][c + 2] != -1:
                            if g[r][c] == -1:
                                g[r][c] = 1 - g[r][c + 2]
                                changed = True
                            if g[r][c + 1] == -1:
                                g[r][c + 1] = 1 - g[r][c + 2]
                                changed = True
                        if c + 2 < n and g[r][c + 1] != -1 and g[r][c + 2] == -1:
                            g[r][c + 2] = 1 - g[r][c + 1]
                            changed = True

            for c in range(n):
                for r in range(n - 1):
                    if edges_v[r][c] == 1:
                        if r > 0 and g[r - 1][c] != -1:
                            if g[r][c] == -1:
                                g[r][c] = 1 - g[r - 1][c]
                                changed = True
                            if g[r + 1][c] == -1:
                                g[r + 1][c] = 1 - g[r - 1][c]
                                changed = True
                        if r > 0 and g[r][c] != -1 and g[r - 1][c] == -1:
                            g[r - 1][c] = 1 - g[r][c]
                            changed = True
                        if r + 2 < n and g[r + 2][c] != -1:
                            if g[r][c] == -1:
                                g[r][c] = 1 - g[r + 2][c]
                                changed = True
                            if g[r + 1][c] == -1:
                                g[r + 1][c] = 1 - g[r + 2][c]
                                changed = True
                        if r + 2 < n and g[r + 1][c] != -1 and g[r + 2][c] == -1:
                            g[r + 2][c] = 1 - g[r + 1][c]
                            changed = True

            if changed:
                continue

            # Pass 4: Line count balance
            for r in range(n):
                c0, c1 = g[r].count(0), g[r].count(1)
                if c0 == half and c1 < half:
                    for c in range(n):
                        if g[r][c] == -1:
                            g[r][c] = 1
                            changed = True
                elif c1 == half and c0 < half:
                    for c in range(n):
                        if g[r][c] == -1:
                            g[r][c] = 0
                            changed = True

            for c in range(n):
                col = [g[r][c] for r in range(n)]
                c0, c1 = col.count(0), col.count(1)
                if c0 == half and c1 < half:
                    for r in range(n):
                        if g[r][c] == -1:
                            g[r][c] = 1
                            changed = True
                elif c1 == half and c0 < half:
                    for r in range(n):
                        if g[r][c] == -1:
                            g[r][c] = 0
                            changed = True

            if changed:
                continue

            # Pass 5: 1-step lookahead deduction
            for r in range(n):
                for c in range(n):
                    if g[r][c] == -1:
                        can_be_0 = self._is_candidate_valid(g, edges_h, edges_v, n, r, c, 0)
                        can_be_1 = self._is_candidate_valid(g, edges_h, edges_v, n, r, c, 1)
                        if not can_be_0 and can_be_1:
                            g[r][c] = 1
                            changed = True
                        elif not can_be_1 and can_be_0:
                            g[r][c] = 0
                            changed = True

        is_solved = all(g[r][c] != -1 for r in range(n) for c in range(n))
        return is_solved, g

    def count_solutions(
        self,
        grid: List[List[int]],
        edges_h: List[List[int]],
        edges_v: List[List[int]],
        n: int,
        limit: int = 2
    ) -> int:
        """Backtracking solver that counts distinct valid solutions up to limit."""
        g = [row[:] for row in grid]
        count = 0
        empty_cells = [(r, c) for r in range(n) for c in range(n) if g[r][c] == -1]

        def backtrack(idx: int) -> bool:
            nonlocal count
            if idx == len(empty_cells):
                count += 1
                return count >= limit

            r, c = empty_cells[idx]
            for val in (0, 1):
                if self._is_candidate_valid(g, edges_h, edges_v, n, r, c, val):
                    g[r][c] = val
                    if backtrack(idx + 1):
                        return True
                    g[r][c] = -1
            return False

        backtrack(0)
        return count

    def generate(self, difficulty: str = "medium") -> Dict[str, Any]:
        """Generates a certified unique and deductively solvable Tango puzzle."""
        difficulty = difficulty.lower()
        cfg = self.DIFFICULTY_SETTINGS.get(difficulty, self.DIFFICULTY_SETTINGS["medium"])
        size = cfg["size"]
        target_numbers = cfg["target_numbers"]
        target_edges = cfg["target_edges"]

        for _ in range(60):
            solution = self._generate_full_board(size)
            if not solution:
                continue

            # Build pool of all potential edges
            all_h = [(r, c) for r in range(size) for c in range(size - 1)]
            all_v = [(r, c) for r in range(size - 1) for c in range(size)]
            all_edges = [('h', r, c) for r, c in all_h] + [('v', r, c) for r, c in all_v]
            random.shuffle(all_edges)

            edges_h = [[0] * (size - 1) for _ in range(size)]
            edges_v = [[0] * size for _ in range(size - 1)]

            for orientation, r, c in all_edges[:target_edges]:
                if orientation == 'h':
                    edges_h[r][c] = 1 if solution[r][c] == solution[r][c + 1] else 2
                else:
                    edges_v[r][c] = 1 if solution[r][c] == solution[r + 1][c] else 2

            # Start with full board of numbers, remove cells one by one
            puzzle = [row[:] for row in solution]
            coords = [(r, c) for r in range(size) for c in range(size)]
            random.shuffle(coords)

            numbers_remaining = size * size
            for r, c in coords:
                if numbers_remaining <= target_numbers:
                    break
                saved = puzzle[r][c]
                puzzle[r][c] = -1
                is_solved, _ = self.solve_deductive(puzzle, edges_h, edges_v, size)
                if is_solved:
                    numbers_remaining -= 1
                else:
                    puzzle[r][c] = saved

            # Verify deductive solvability and strict uniqueness
            is_solved, _ = self.solve_deductive(puzzle, edges_h, edges_v, size)
            if is_solved and numbers_remaining <= target_numbers + 2:
                if self.count_solutions(puzzle, edges_h, edges_v, size, limit=2) == 1:
                    edge_count = (
                        sum(1 for row in edges_h for e in row if e > 0) +
                        sum(1 for row in edges_v for e in row if e > 0)
                    )
                    res = {
                        "title": "TANGO",
                        "difficulty": difficulty.upper(),
                        "size": size,
                        "puzzle": puzzle,
                        "edges_h": edges_h,
                        "edges_v": edges_v,
                        "solution": solution,
                        "numbers_count": numbers_remaining,
                        "edges_count": edge_count,
                    }
                    res["text"] = self.format_ascii(res)
                    return res

        raise RuntimeError(f"Failed to generate valid Tango puzzle for difficulty '{difficulty}'")

    def format_ascii(self, puzzle_data: Dict[str, Any]) -> str:
        """
        Formats an elegant ASCII grid representation with '=' and 'x' on cell borders.
        """
        size = puzzle_data["size"]
        puzzle = puzzle_data["puzzle"]
        edges_h = puzzle_data.get("edges_h", [[0] * (size - 1) for _ in range(size)])
        edges_v = puzzle_data.get("edges_v", [[0] * size for _ in range(size - 1)])

        lines = []
        # Top outer border
        lines.append("+" + "---+" * size)

        for r in range(size):
            # Row cells and vertical dividers
            row_line = "|"
            for c in range(size):
                v = puzzle[r][c]
                val_str = f" {v} " if v in (0, 1) else "   "
                row_line += val_str

                if c < size - 1:
                    # Divider between (r, c) and (r, c+1)
                    e = edges_h[r][c] if r < len(edges_h) and c < len(edges_h[r]) else 0
                    if e == 1:
                        row_line += "="
                    elif e == 2:
                        row_line += "x"
                    else:
                        row_line += "|"
                else:
                    row_line += "|"
            lines.append(row_line)

            # Divider below row r
            if r < size - 1:
                div_line = "+"
                for c in range(size):
                    e = edges_v[r][c] if r < len(edges_v) and c < len(edges_v[r]) else 0
                    if e == 1:
                        div_line += "-=-+"
                    elif e == 2:
                        div_line += "-x-+"
                    else:
                        div_line += "---+"
                lines.append(div_line)
            else:
                # Bottom outer border
                lines.append("+" + "---+" * size)

        return "\n".join(lines)
