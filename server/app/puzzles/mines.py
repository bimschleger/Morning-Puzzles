"""
Morning Puzzles - Mines Plugin
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


class MinesPuzzle(BasePuzzle):
    """Minesweeper deduction puzzle plugin with zero guessing required."""

    DIFFICULTY_SETTINGS = {
        "easy":   {"rows": 8, "cols": 8, "mines": 8,  "target_clues": 28},
        "medium": {"rows": 8, "cols": 8, "mines": 12, "target_clues": 22},
        "hard":   {"rows": 8, "cols": 8, "mines": 15, "target_clues": 17},
    }

    @property
    def puzzle_id(self) -> str:
        return "mines"

    @property
    def title(self) -> str:
        return "MINES"

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
        rows = cfg["rows"]
        cols = cfg["cols"]
        num_mines = cfg["mines"]
        target_clues = cfg["target_clues"]

        all_cells = [(r, c) for r in range(rows) for c in range(cols)]

        for _ in range(100):
            mine_set = set(random.sample(all_cells, num_mines))

            full_clues: Dict[Tuple[int, int], int] = {}
            for r in range(rows):
                for c in range(cols):
                    if (r, c) not in mine_set:
                        neighs = self._get_neighbors(r, c, rows, cols)
                        full_clues[(r, c)] = sum(1 for p in neighs if p in mine_set)

            is_solved, _ = self._solve_deductive(rows, cols, full_clues, num_mines)
            if not is_solved:
                continue

            pruned_clues = dict(full_clues)
            clue_keys = list(full_clues.keys())
            random.shuffle(clue_keys)

            for k in clue_keys:
                if len(pruned_clues) <= target_clues:
                    break
                val = pruned_clues.pop(k)
                solved, _ = self._solve_deductive(rows, cols, pruned_clues, num_mines)
                if not solved:
                    pruned_clues[k] = val

            puzzle_grid = [[-1] * cols for _ in range(rows)]
            for (r, c), val in pruned_clues.items():
                puzzle_grid[r][c] = val

            solution_grid = [[0] * cols for _ in range(rows)]
            for r, c in mine_set:
                solution_grid[r][c] = 1

            mine_coords = sorted(list(mine_set))

            raw_data = {
                "type": "mines",
                "title": "MINES",
                "difficulty": difficulty,
                "rows": rows,
                "cols": cols,
                "total_mines": num_mines,
                "clues_count": len(pruned_clues),
                "puzzle": puzzle_grid,
                "solution": solution_grid,
                "mine_coords": mine_coords,
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

        raise RuntimeError("Failed to generate deducible Mines puzzle")

    def get_instruction(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        mines_cnt = puzzle_data.get("total_mines", 10)
        return f"Deduce all {mines_cnt} hidden mines using the adjacent numbered clues."

    def format_ascii_puzzle(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        rows = puzzle_data.get("rows", 8)
        cols = puzzle_data.get("cols", 8)
        puzzle = puzzle_data.get("puzzle", [])
        total_mines = puzzle_data.get("total_mines", 12)

        lines = []
        lines.append(f"TOTAL MINES: {total_mines}")
        lines.append("")

        sep = "   +" + "---+" * cols
        lines.append(sep)
        for r in range(rows):
            line = "   |"
            for c in range(cols):
                val = puzzle[r][c] if r < len(puzzle) and c < len(puzzle[r]) else -1
                line += "   |" if val == -1 else f" {val} |"
            lines.append(line)
            lines.append(sep)

        return "\n".join(lines)

    def format_solution_key(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> List[str]:
        sol = puzzle_data.get("solution", [])
        puzzle = puzzle_data.get("puzzle", [])
        if not sol:
            return []
        lines = []
        for row_idx in range(len(sol)):
            row_str = "      "
            for col_idx in range(len(sol[row_idx])):
                if puzzle and puzzle[row_idx][col_idx] >= 0:
                    row_str += f"{puzzle[row_idx][col_idx]} "
                elif sol[row_idx][col_idx] == 1:
                    row_str += "* "
                else:
                    row_str += ". "
            lines.append(row_str)
        return lines

    def render_raster(
        self,
        puzzle_data: Union[BasePuzzleResult, Dict[str, Any]],
        target_width: int = THERMAL_WIDTH_DOTS,
    ) -> bytes:
        rows = puzzle_data.get("rows", 8)
        cols = puzzle_data.get("cols", 8)
        puzzle = puzzle_data.get("puzzle", [])
        total_mines = puzzle_data.get("total_mines", 10)

        padding = 24
        inner_width = target_width - padding * 2
        cell_size = inner_width // cols
        board_h = cell_size * rows

        badge_h = 36
        total_h = 12 + badge_h + 12 + board_h + 12
        tb = ThermalBitmap(target_width, total_h)

        tb.draw_rect(padding, 12, inner_width, badge_h, thickness=3)
        tb.draw_text(padding + 16, 20, f"TOTAL MINES: {total_mines}", scale=2)

        grid_y = 12 + badge_h + 12
        tb.draw_rect(padding, grid_y, cell_size * cols, board_h, thickness=4)

        for c in range(1, cols):
            tb.draw_vline(padding + c * cell_size, grid_y, board_h, thickness=2)
        for r in range(1, rows):
            tb.draw_hline(padding, grid_y + r * cell_size, cell_size * cols, thickness=2)

        for r in range(rows):
            for c in range(cols):
                val = puzzle[r][c] if r < len(puzzle) and c < len(puzzle[r]) else -1
                if val >= 0:
                    cx = padding + c * cell_size + (cell_size - 18) // 2
                    cy = grid_y + r * cell_size + (cell_size - 21) // 2
                    tb.draw_char(cx, cy, str(val), scale=3)

        return tb.to_escpos()

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

    def _solve_deductive(self, rows: int, cols: int, clues: Dict[Tuple[int, int], int], total_mines: int) -> Tuple[bool, List[List[int]]]:
        state = [[-1] * cols for _ in range(rows)]
        for (r, c) in clues:
            state[r][c] = 0

        changed = True
        while changed:
            changed = False

            for (r, c), val in clues.items():
                neighs = self._get_neighbors(r, c, rows, cols)
                unknowns = [p for p in neighs if state[p[0]][p[1]] == -1]
                mines = [p for p in neighs if state[p[0]][p[1]] == 1]
                rem = val - len(mines)

                if rem < 0 or len(unknowns) + len(mines) < val:
                    return False, state

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

    def verify_accuracy(
        self,
        puzzle_data: Union[BasePuzzleResult, Dict[str, Any]],
    ) -> Tuple[bool, str]:
        solution = puzzle_data.get("solution")
        clues_data = puzzle_data.get("clues") or puzzle_data.get("clue_map") or {}
        rows = puzzle_data.get("rows", len(solution) if solution else 8)
        cols = puzzle_data.get("cols", len(solution[0]) if solution and solution[0] else 8)
        total_mines = puzzle_data.get("total_mines") or puzzle_data.get("mines", 12)

        if not solution or not isinstance(solution, list):
            return False, "Mines solution grid missing or invalid"

        # 1. Count mines in solution
        actual_mines = sum(row.count(1) for row in solution)
        if actual_mines != total_mines:
            return False, f"Mines count in solution ({actual_mines}) does not match declared total ({total_mines})"

        # 2. Parse clues into dict
        clues_dict = {}
        puzzle_grid = puzzle_data.get("puzzle")
        if puzzle_grid:
            for r in range(rows):
                for c in range(cols):
                    if puzzle_grid[r][c] >= 0:
                        clues_dict[(r, c)] = puzzle_grid[r][c]
        elif isinstance(clues_data, list):
            for item in clues_data:
                if isinstance(item, (list, tuple)) and len(item) == 3:
                    clues_dict[(item[0], item[1])] = item[2]
                elif isinstance(item, dict):
                    clues_dict[(item["row"], item["col"])] = item["val"]
        elif isinstance(clues_data, dict):
            for k, v in clues_data.items():
                if isinstance(k, tuple):
                    clues_dict[k] = v
                elif isinstance(k, str) and "," in k:
                    parts = [int(p.strip()) for p in k.split(",")]
                    clues_dict[(parts[0], parts[1])] = v

        # 3. Check every clue
        for (r, c), val in clues_dict.items():
            if solution[r][c] == 1:
                return False, f"Mines clue cell at ({r},{c}) contains a mine"
            neighbors = self._get_neighbors(r, c, rows, cols)
            n_mines = sum(1 for (nr, nc) in neighbors if solution[nr][nc] == 1)
            if n_mines != val:
                return False, f"Mines clue at ({r},{c}) is {val}, but neighbor mine count is {n_mines}"

        # 4. Solvability
        is_solved, _ = self._solve_deductive(rows, cols, clues_dict, total_mines)
        if not is_solved:
            return False, "Mines puzzle cannot be solved with pure logic without guessing"

        return True, "All rules satisfied"
