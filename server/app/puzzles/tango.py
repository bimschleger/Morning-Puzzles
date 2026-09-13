"""
Morning Puzzles - Tango Plugin
Encapsulates generation, canonical instruction formatting, ASCII layout,
solution key formatting, and 576-dot thermal raster rendering.
"""

import random
from typing import List, Tuple, Optional, Dict, Any, Set, Union

from .base import BasePuzzle, BasePuzzleResult
from ..renderer.canvas import (
    THERMAL_WIDTH_DOTS,
    ThermalBitmap,
)


class TangoPuzzle(BasePuzzle):
    """Tango (Binairo+) puzzle plugin."""

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

    @property
    def puzzle_id(self) -> str:
        return "tango"

    @property
    def title(self) -> str:
        return "TANGO"

    @property
    def has_difficulty(self) -> bool:
        return True

    @property
    def supported_difficulties(self) -> List[str]:
        return ["easy", "medium", "hard"]

    def generate(
        self,
        difficulty: str = "medium",
        seed: Optional[int] = None,
        **kwargs,
    ) -> BasePuzzleResult:
        if seed is not None:
            random.seed(seed)

        difficulty = difficulty.lower()
        cfg = self.DIFFICULTY_SETTINGS.get(difficulty, self.DIFFICULTY_SETTINGS["medium"])
        size = cfg["size"]
        target_numbers = cfg["target_numbers"]
        target_edges = cfg["target_edges"]

        for _ in range(60):
            solution = self._generate_full_board(size)
            if not solution:
                continue

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

            puzzle = [row[:] for row in solution]
            coords = [(r, c) for r in range(size) for c in range(size)]
            random.shuffle(coords)

            numbers_remaining = size * size
            for r, c in coords:
                if numbers_remaining <= target_numbers:
                    break
                saved = puzzle[r][c]
                puzzle[r][c] = -1
                is_solved, _ = self._solve_deductive(puzzle, edges_h, edges_v, size)
                if is_solved:
                    numbers_remaining -= 1
                else:
                    puzzle[r][c] = saved

            is_solved, _ = self._solve_deductive(puzzle, edges_h, edges_v, size)
            if is_solved and numbers_remaining <= target_numbers + 2:
                if self._count_solutions(puzzle, edges_h, edges_v, size, limit=2) == 1:
                    edge_count = (
                        sum(1 for row in edges_h for e in row if e > 0) +
                        sum(1 for row in edges_v for e in row if e > 0)
                    )
                    raw_data = {
                        "type": "tango",
                        "title": "TANGO",
                        "difficulty": difficulty,
                        "size": size,
                        "puzzle": puzzle,
                        "edges_h": edges_h,
                        "edges_v": edges_v,
                        "solution": solution,
                        "numbers_count": numbers_remaining,
                        "edges_count": edge_count,
                    }
                    ascii_text = self.format_ascii_puzzle(raw_data)
                    raw_data["text"] = ascii_text
                    instruction = self.get_instruction(raw_data)

                    return BasePuzzleResult(
                        puzzle_type=self.puzzle_id,
                        title=self.title,
                        difficulty=difficulty,
                        instruction=instruction,
                        raw_data=raw_data,
                    )

        raise RuntimeError(f"Failed to generate valid Tango puzzle for difficulty '{difficulty}'")

    def get_instruction(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        t_diff = str(puzzle_data.get("difficulty", "medium"))
        t_size = puzzle_data.get("size", 6)
        if t_size == 6 or t_diff.lower() in ("easy", "medium"):
            return "Fill each line with three 0s and three 1s without trios; = means same, x means opposite."
        return "Fill each line with four 0s and four 1s without trios; = means same, x means opposite."

    def format_ascii_puzzle(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        size = puzzle_data.get("size", 6)
        puzzle = puzzle_data.get("puzzle", [])
        edges_h = puzzle_data.get("edges_h", [[0] * (size - 1) for _ in range(size)])
        edges_v = puzzle_data.get("edges_v", [[0] * size for _ in range(size - 1)])

        lines = []
        lines.append("+" + "---+" * size)

        for r in range(size):
            row_line = "|"
            for c in range(size):
                v = puzzle[r][c] if r < len(puzzle) and c < len(puzzle[r]) else -1
                val_str = f" {v} " if v in (0, 1) else "   "
                row_line += val_str

                if c < size - 1:
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
                lines.append("+" + "---+" * size)

        return "\n".join(lines)

    def format_solution_key(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> List[str]:
        sol = puzzle_data.get("solution", [])
        if not sol:
            return []
        lines = []
        for row in sol:
            lines.append("      " + " ".join(str(c) for c in row))
        return lines

    def render_raster(
        self,
        puzzle_data: Union[BasePuzzleResult, Dict[str, Any]],
        target_width: int = THERMAL_WIDTH_DOTS,
    ) -> bytes:
        size = puzzle_data.get("size", 6)
        puzzle = puzzle_data.get("puzzle", [])
        edges_h = puzzle_data.get("edges_h", [])
        edges_v = puzzle_data.get("edges_v", [])

        padding = 24
        board_size = target_width - padding * 2
        cell_size = board_size // size
        total_h = padding + cell_size * size + padding

        tb = ThermalBitmap(target_width, total_h)
        tb.draw_rect(padding, padding, cell_size * size, cell_size * size, thickness=4)

        for i in range(1, size):
            pos = padding + i * cell_size
            tb.draw_hline(padding, pos, cell_size * size, thickness=2)
            tb.draw_vline(pos, padding, cell_size * size, thickness=2)

        for r in range(size):
            for c in range(size - 1):
                e = edges_h[r][c] if r < len(edges_h) and c < len(edges_h[r]) else 0
                if e in (1, 2):
                    cx = padding + (c + 1) * cell_size
                    cy = padding + r * cell_size + cell_size // 2
                    tb.fill_rect(cx - 8, cy - 8, 17, 17, color=0)
                    if e == 1:
                        tb.draw_hline(cx - 5, cy - 3, 11, thickness=2, color=1)
                        tb.draw_hline(cx - 5, cy + 2, 11, thickness=2, color=1)
                    elif e == 2:
                        for d in range(-4, 5):
                            tb.set_pixel(cx + d, cy + d, 1)
                            tb.set_pixel(cx + d, cy + d + 1, 1)
                            tb.set_pixel(cx + d, cy - d, 1)
                            tb.set_pixel(cx + d, cy - d + 1, 1)

        for r in range(size - 1):
            for c in range(size):
                e = edges_v[r][c] if r < len(edges_v) and c < len(edges_v[r]) else 0
                if e in (1, 2):
                    cx = padding + c * cell_size + cell_size // 2
                    cy = padding + (r + 1) * cell_size
                    tb.fill_rect(cx - 8, cy - 8, 17, 17, color=0)
                    if e == 1:
                        tb.draw_hline(cx - 5, cy - 3, 11, thickness=2, color=1)
                        tb.draw_hline(cx - 5, cy + 2, 11, thickness=2, color=1)
                    elif e == 2:
                        for d in range(-4, 5):
                            tb.set_pixel(cx + d, cy + d, 1)
                            tb.set_pixel(cx + d, cy + d + 1, 1)
                            tb.set_pixel(cx + d, cy - d, 1)
                            tb.set_pixel(cx + d, cy - d + 1, 1)

        for r in range(size):
            for c in range(size):
                val = puzzle[r][c] if r < len(puzzle) and c < len(puzzle[r]) else -1
                if val in (0, 1):
                    cx = padding + c * cell_size + (cell_size - 18) // 2
                    cy = padding + r * cell_size + (cell_size - 21) // 2
                    tb.draw_char(cx, cy, str(val), scale=3)

        return tb.to_escpos()

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
            for c in range(n):
                val = row_cand[c]
                if r >= 2 and grid[r - 1][c] == val and grid[r - 2][c] == val:
                    return False
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
        val: int,
    ) -> bool:
        half = n // 2

        if g[r].count(val) + 1 > half:
            return False

        col_vals = [g[pr][c] for pr in range(n)]
        if col_vals.count(val) + 1 > half:
            return False

        if c >= 2 and g[r][c - 2] == val and g[r][c - 1] == val:
            return False
        if 0 < c < n - 1 and g[r][c - 1] == val and g[r][c + 1] == val:
            return False
        if c <= n - 3 and g[r][c + 1] == val and g[r][c + 2] == val:
            return False

        if r >= 2 and g[r - 2][c] == val and g[r - 1][c] == val:
            return False
        if 0 < r < n - 1 and g[r - 1][c] == val and g[r + 1][c] == val:
            return False
        if r <= n - 3 and g[r + 1][c] == val and g[r + 2][c] == val:
            return False

        if c > 0:
            e = edges_h[r][c - 1]
            if e == 1 and g[r][c - 1] != -1 and g[r][c - 1] != val:
                return False
            if e == 2 and g[r][c - 1] != -1 and g[r][c - 1] == val:
                return False
        if c < n - 1:
            e = edges_h[r][c]
            if e == 1 and g[r][c + 1] != -1 and g[r][c + 1] != val:
                return False
            if e == 2 and g[r][c + 1] != -1 and g[r][c + 1] == val:
                return False
        if r > 0:
            e = edges_v[r - 1][c]
            if e == 1 and g[r - 1][c] != -1 and g[r - 1][c] != val:
                return False
            if e == 2 and g[r - 1][c] != -1 and g[r - 1][c] == val:
                return False
        if r < n - 1:
            e = edges_v[r][c]
            if e == 1 and g[r + 1][c] != -1 and g[r + 1][c] != val:
                return False
            if e == 2 and g[r + 1][c] != -1 and g[r + 1][c] == val:
                return False

        return True

    def _solve_deductive(
        self,
        grid: List[List[int]],
        edges_h: List[List[int]],
        edges_v: List[List[int]],
        n: int,
    ) -> Tuple[bool, List[List[int]]]:
        g = [row[:] for row in grid]
        half = n // 2
        changed = True

        while changed:
            changed = False

            # Pass 1: Direct edge clues
            for r in range(n):
                for c in range(n - 1):
                    e = edges_h[r][c]
                    if e == 1:
                        if g[r][c] != -1 and g[r][c + 1] == -1:
                            g[r][c + 1] = g[r][c]
                            changed = True
                        elif g[r][c + 1] != -1 and g[r][c] == -1:
                            g[r][c] = g[r][c + 1]
                            changed = True
                    elif e == 2:
                        if g[r][c] != -1 and g[r][c + 1] == -1:
                            g[r][c + 1] = 1 - g[r][c]
                            changed = True
                        elif g[r][c + 1] != -1 and g[r][c] == -1:
                            g[r][c] = 1 - g[r][c + 1]
                            changed = True

            for r in range(n - 1):
                for c in range(n):
                    e = edges_v[r][c]
                    if e == 1:
                        if g[r][c] != -1 and g[r + 1][c] == -1:
                            g[r + 1][c] = g[r][c]
                            changed = True
                        elif g[r + 1][c] != -1 and g[r][c] == -1:
                            g[r][c] = g[r + 1][c]
                            changed = True
                    elif e == 2:
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

            # Pass 3: Line count saturation
            for r in range(n):
                c0 = g[r].count(0)
                c1 = g[r].count(1)
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
                col_vals = [g[r][c] for r in range(n)]
                c0 = col_vals.count(0)
                c1 = col_vals.count(1)
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

        is_solved = all(g[r][c] != -1 for r in range(n) for c in range(n))
        return is_solved, g

    def _count_solutions(
        self,
        grid: List[List[int]],
        edges_h: List[List[int]],
        edges_v: List[List[int]],
        n: int,
        limit: int = 2,
    ) -> int:
        g = [row[:] for row in grid]
        empty_cells = [(r, c) for r in range(n) for c in range(n) if g[r][c] == -1]
        count = 0

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

    def verify_accuracy(
        self,
        puzzle_data: Union[BasePuzzleResult, Dict[str, Any]],
    ) -> Tuple[bool, str]:
        puzzle = puzzle_data.get("puzzle")
        solution = puzzle_data.get("solution")
        edges_h = puzzle_data.get("edges_h")
        edges_v = puzzle_data.get("edges_v")
        n = puzzle_data.get("size", len(puzzle) if puzzle else 6)

        if not puzzle or not solution or edges_h is None or edges_v is None:
            return False, "Tango puzzle missing grid or edge data"
        if len(solution) != n or any(len(r) != n for r in solution):
            return False, f"Tango solution grid must be {n}x{n}"

        half = n // 2

        # 1. Row and Col count and trio checks
        for r in range(n):
            row = solution[r]
            if row.count(0) != half or row.count(1) != half:
                return False, f"Tango row {r} does not have equal 0s and 1s"
            for c in range(n - 2):
                if row[c] == row[c + 1] == row[c + 2]:
                    return False, f"Tango row {r} has 3 consecutive identical symbols at col {c}"

        for c in range(n):
            col = [solution[r][c] for r in range(n)]
            if col.count(0) != half or col.count(1) != half:
                return False, f"Tango col {c} does not have equal 0s and 1s"
            for r in range(n - 2):
                if col[r] == col[r + 1] == col[r + 2]:
                    return False, f"Tango col {c} has 3 consecutive identical symbols at row {r}"

        # 2. Edge constraints
        for r in range(n):
            for c in range(n - 1):
                e = edges_h[r][c]
                if e == 1 and solution[r][c] != solution[r][c + 1]:
                    return False, f"Tango '=' horizontal edge at ({r},{c}) violated: {solution[r][c]} != {solution[r][c+1]}"
                elif e == 2 and solution[r][c] == solution[r][c + 1]:
                    return False, f"Tango 'x' horizontal edge at ({r},{c}) violated: {solution[r][c]} == {solution[r][c+1]}"

        for r in range(n - 1):
            for c in range(n):
                e = edges_v[r][c]
                if e == 1 and solution[r][c] != solution[r + 1][c]:
                    return False, f"Tango '=' vertical edge at ({r},{c}) violated: {solution[r][c]} != {solution[r+1][c]}"
                elif e == 2 and solution[r][c] == solution[r + 1][c]:
                    return False, f"Tango 'x' vertical edge at ({r},{c}) violated: {solution[r][c]} == {solution[r+1][c]}"

        # 3. Givens match solution
        for r in range(n):
            for c in range(n):
                val = puzzle[r][c]
                if val != -1 and val != solution[r][c]:
                    return False, f"Tango given at ({r},{c})={val} mismatches solution={solution[r][c]}"

        # 4. Solvability & Uniqueness
        sols = self._count_solutions(puzzle, edges_h, edges_v, n, limit=2)
        if sols == 0:
            return False, "Tango puzzle has no valid solutions"
        if sols > 1:
            return False, "Tango puzzle has multiple valid solutions (not unique)"

        return True, "All rules satisfied"
