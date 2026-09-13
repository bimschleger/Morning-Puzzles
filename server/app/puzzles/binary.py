"""
Morning Puzzles - Binary (Takuzu / Binairo) Plugin
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


class BinaryPuzzle(BasePuzzle):
    """Binary (Takuzu / Binairo) puzzle plugin."""

    DIFFICULTY_SETTINGS = {
        "easy": {"size": 6, "target_clues": 16, "max_rule": 2},
        "medium": {"size": 8, "target_clues": 28, "max_rule": 2},
        "hard": {"size": 8, "target_clues": 22, "max_rule": 3},
    }

    @property
    def puzzle_id(self) -> str:
        return "binary"

    @property
    def title(self) -> str:
        return "BINARY"

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
            is_solved, _, _ = self._solve_deductive(puzzle, size, max_rule)
            if is_solved:
                clues_remaining -= 1
            else:
                puzzle[r][c] = saved

        raw_data = {
            "type": "binary",
            "title": "BINARY",
            "difficulty": difficulty,
            "size": size,
            "puzzle": puzzle,
            "solution": solution,
            "clues_count": clues_remaining,
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

    def get_instruction(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        b_diff = str(puzzle_data.get("difficulty", "medium"))
        b_size = puzzle_data.get("size", 8)
        if b_size == 6 or b_diff.lower() == "easy":
            return "Fill each row and column with three 0s and three 1s, with no more than two consecutive of each type."
        return "Fill each row and column with four 0s and four 1s, with no more than two consecutive of each type."

    def format_ascii_puzzle(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        size = puzzle_data.get("size", 8)
        puzzle = puzzle_data.get("puzzle", [])
        if not puzzle:
            return ""

        lines = []
        sep = "   +" + "---+" * size
        lines.append(sep)
        for r in range(size):
            line = "   |"
            for c in range(size):
                v = puzzle[r][c] if r < len(puzzle) and c < len(puzzle[r]) else -1
                line += "   |" if v == -1 else f" {v} |"
            lines.append(line)
            lines.append(sep)
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
        size = puzzle_data.get("size", 8)
        puzzle = puzzle_data.get("puzzle", [])

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
            for pr in range(r):
                if grid[pr] == row_cand:
                    return False
            for c in range(n):
                val = row_cand[c]
                if r >= 2 and grid[r - 1][c] == val and grid[r - 2][c] == val:
                    return False
                col_count = sum(1 for pr in range(r) if grid[pr][c] == val) + 1
                if col_count > half:
                    return False
                if r == n - 1:
                    col_c = [grid[pr][c] for pr in range(n - 1)] + [val]
                    for pc in range(c):
                        col_pc = [grid[pr][pc] for pr in range(n - 1)] + [row_cand[pc]]
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

    def _solve_deductive(self, grid: List[List[int]], n: int, max_rule: int = 3) -> Tuple[bool, List[List[int]], Set[int]]:
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

            # Rule 3: Line uniqueness
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

    def verify_accuracy(
        self,
        puzzle_data: Union[BasePuzzleResult, Dict[str, Any]],
    ) -> Tuple[bool, str]:
        puzzle = puzzle_data.get("puzzle")
        solution = puzzle_data.get("solution")
        if not puzzle or not isinstance(puzzle, list):
            return False, "Binary puzzle grid missing or invalid"
        if not solution or not isinstance(solution, list):
            return False, "Binary solution grid missing or invalid"
        n = len(puzzle)
        if n % 2 != 0 or len(solution) != n or any(len(r) != n for r in puzzle) or any(len(r) != n for r in solution):
            return False, f"Binary grid must be square of even size, got {n}"

        half = n // 2

        # 1. Verify solution counts and constraints
        for r in range(n):
            row = solution[r]
            if any(val not in (0, 1) for val in row):
                return False, f"Binary solution row {r} contains non-binary values"
            if row.count(0) != half or row.count(1) != half:
                return False, f"Binary solution row {r} does not have equal 0s and 1s"
            for c in range(n - 2):
                if row[c] == row[c + 1] == row[c + 2]:
                    return False, f"Binary solution row {r} has 3 consecutive identical values at col {c}"

        for c in range(n):
            col = [solution[r][c] for r in range(n)]
            if col.count(0) != half or col.count(1) != half:
                return False, f"Binary solution col {c} does not have equal 0s and 1s"
            for r in range(n - 2):
                if col[r] == col[r + 1] == col[r + 2]:
                    return False, f"Binary solution col {c} has 3 consecutive identical values at row {r}"

        # 2. Row and Column uniqueness
        row_tuples = [tuple(solution[r]) for r in range(n)]
        if len(set(row_tuples)) != n:
            return False, "Binary solution contains duplicate rows"
        col_tuples = [tuple(solution[r][c] for r in range(n)) for c in range(n)]
        if len(set(col_tuples)) != n:
            return False, "Binary solution contains duplicate columns"

        # 3. Givens match solution
        for r in range(n):
            for c in range(n):
                val = puzzle[r][c]
                if val != -1 and val != solution[r][c]:
                    return False, f"Binary given at ({r},{c})={val} mismatches solution={solution[r][c]}"

        # 4. Solvability
        is_solved, solved_grid, _ = self._solve_deductive(puzzle, n, max_rule=3)
        if not is_solved:
            return False, "Binary puzzle could not be logically solved"
        if solved_grid != solution:
            return False, "Binary logically solved grid does not match solution"

        return True, "All rules satisfied"
