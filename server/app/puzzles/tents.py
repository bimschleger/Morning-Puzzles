"""
Morning Puzzles - Tents (Tents and Trees) Plugin
Encapsulates generation, canonical instruction formatting, ASCII layout,
solution key formatting, and 576-dot thermal raster rendering.
"""

import random
import textwrap
from typing import List, Tuple, Optional, Dict, Any, Set, Union

from .base import BasePuzzle, BasePuzzleResult
from ..renderer.canvas import (
    THERMAL_WIDTH_DOTS,
    ThermalBitmap,
)


class TentsPuzzle(BasePuzzle):
    """Tents and Trees puzzle plugin."""

    DIFFICULTY_SETTINGS = {
        "easy":   {"size": 6, "tents": 4},
        "medium": {"size": 8, "tents": 8},
        "hard":   {"size": 8, "tents": 11},
    }

    @property
    def puzzle_id(self) -> str:
        return "tents"

    @property
    def title(self) -> str:
        return "TENTS"

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

        diff_key = difficulty.lower()
        if diff_key not in self.DIFFICULTY_SETTINGS:
            diff_key = "medium"

        settings = self.DIFFICULTY_SETTINGS[diff_key]
        size = settings["size"]
        target_tents = settings["tents"]

        max_attempts = 150
        for _ in range(max_attempts):
            all_cells = [(r, c) for r in range(size) for c in range(size)]
            random.shuffle(all_cells)

            tent_positions: List[Tuple[int, int]] = []
            occupied_tent_influence: Set[Tuple[int, int]] = set()

            for r, c in all_cells:
                if len(tent_positions) >= target_tents:
                    break
                if (r, c) not in occupied_tent_influence:
                    tent_positions.append((r, c))
                    occupied_tent_influence.add((r, c))
                    for nr, nc in self._all_neighbors(r, c, size):
                        occupied_tent_influence.add((nr, nc))

            if len(tent_positions) < target_tents:
                continue

            tree_positions: List[Tuple[int, int]] = []
            used_cells = set(tent_positions)
            success = True

            tent_set = set(tent_positions)
            for tr, tc in tent_positions:
                adj = [p for p in self._ortho_neighbors(tr, tc, size) if p not in used_cells and p not in tent_set]
                if not adj:
                    success = False
                    break
                tree_choice = random.choice(adj)
                tree_positions.append(tree_choice)
                used_cells.add(tree_choice)

            if not success or len(tree_positions) != target_tents:
                continue

            row_counts = [0] * size
            col_counts = [0] * size
            for tr, tc in tent_positions:
                row_counts[tr] += 1
                col_counts[tc] += 1

            sol_count = self._count_solutions(size, tree_positions, row_counts, col_counts, max_count=2)
            if sol_count == 1:
                puzzle_grid = [[0] * size for _ in range(size)]
                for tr, tc in tree_positions:
                    puzzle_grid[tr][tc] = 1

                solution_grid = [[0] * size for _ in range(size)]
                for tr, tc in tree_positions:
                    solution_grid[tr][tc] = 1
                for tr, tc in tent_positions:
                    solution_grid[tr][tc] = 2

                raw_data = {
                    "type": "tents",
                    "title": "TENTS",
                    "difficulty": diff_key,
                    "size": size,
                    "rows": size,
                    "cols": size,
                    "row_clues": row_counts,
                    "col_clues": col_counts,
                    "trees": [list(p) for p in sorted(tree_positions)],
                    "tents": [list(p) for p in sorted(tent_positions)],
                    "tree_count": len(tree_positions),
                    "num_tents": len(tent_positions),
                    "puzzle": puzzle_grid,
                    "solution": solution_grid,
                }
                ascii_text = self.format_ascii_puzzle(raw_data)
                raw_data["text"] = ascii_text
                instruction = self.get_instruction(raw_data)

                return BasePuzzleResult(
                    puzzle_type=self.puzzle_id,
                    title=self.title,
                    difficulty=diff_key,
                    instruction=instruction,
                    raw_data=raw_data,
                )

        raise RuntimeError(f"Failed to generate unique Tents puzzle for {difficulty} in {max_attempts} attempts")

    def get_instruction(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        num_tents = puzzle_data.get("num_tents", len(puzzle_data.get("tents", [])))
        return f"Pitch {num_tents} tents next to trees without tents touching, matching row and column counts."

    def format_ascii_puzzle(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        size = puzzle_data.get("size", 8)
        row_clues = puzzle_data.get("row_clues", [0] * size)
        col_clues = puzzle_data.get("col_clues", [0] * size)
        grid = puzzle_data.get("puzzle", [])
        if not grid:
            return ""

        lines = []
        col_header = "       " + " ".join(str(c) for c in col_clues)
        lines.append(col_header)
        sep = "     +" + "--" * size + "+"
        lines.append(sep)

        for r in range(size):
            row_str = f"   {row_clues[r]} |"
            for c in range(size):
                cell = grid[r][c] if r < len(grid) and c < len(grid[r]) else 0
                row_str += " T" if cell == 1 else " ."
            row_str += " |"
            lines.append(row_str)

        lines.append(sep)
        return "\n".join(lines)

    def format_solution_key(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> List[str]:
        sol = puzzle_data.get("solution", [])
        tents = puzzle_data.get("tents", [])
        lines = []
        if sol:
            for row in sol:
                row_str = "      "
                for cell in row:
                    if cell == 1:
                        row_str += "T "
                    elif cell == 2:
                        row_str += "^ "
                    else:
                        row_str += ". "
                lines.append(row_str)
        if tents:
            tents_str = "Tents at: " + "  ".join(f"({tr+1},{tc+1})" for tr, tc in sorted(tents))
            for line in textwrap.wrap(tents_str, 46):
                lines.append(line)
        return lines

    def render_raster(
        self,
        puzzle_data: Union[BasePuzzleResult, Dict[str, Any]],
        target_width: int = THERMAL_WIDTH_DOTS,
    ) -> bytes:
        size = puzzle_data.get("size", 8)
        row_clues = puzzle_data.get("row_clues", [0] * size)
        col_clues = puzzle_data.get("col_clues", [0] * size)
        puzzle = puzzle_data.get("puzzle", [])

        padding = 24
        inner_width = target_width - padding * 2
        total_cols = size + 1
        cell_size = inner_width // total_cols
        board_h = cell_size * (size + 1)
        total_h = padding + board_h + padding

        tb = ThermalBitmap(target_width, total_h)

        gx = padding
        gy = padding

        puzzle_x = gx + cell_size
        puzzle_y = gy + cell_size
        puzzle_w = cell_size * size
        puzzle_h = cell_size * size
        tb.draw_rect(puzzle_x, puzzle_y, puzzle_w, puzzle_h, thickness=4)

        for i in range(1, size):
            tb.draw_vline(puzzle_x + i * cell_size, puzzle_y, puzzle_h, thickness=2)
            tb.draw_hline(puzzle_x, puzzle_y + i * cell_size, puzzle_w, thickness=2)

        for c in range(size):
            clue = col_clues[c] if c < len(col_clues) else 0
            cx = puzzle_x + c * cell_size + (cell_size - 18) // 2
            cy = gy + (cell_size - 21) // 2
            tb.draw_char(cx, cy, str(clue), scale=3)

        for r in range(size):
            clue = row_clues[r] if r < len(row_clues) else 0
            cx = gx + (cell_size - 18) // 2
            cy = puzzle_y + r * cell_size + (cell_size - 21) // 2
            tb.draw_char(cx, cy, str(clue), scale=3)

        for r in range(size):
            for c in range(size):
                is_tree = (r < len(puzzle) and c < len(puzzle[r]) and puzzle[r][c] == 1)
                cx = puzzle_x + c * cell_size + cell_size // 2
                cy = puzzle_y + r * cell_size + cell_size // 2

                if is_tree:
                    trunk_w = max(4, cell_size // 10)
                    trunk_h = max(6, cell_size // 6)
                    tb.fill_rect(cx - trunk_w // 2, cy + cell_size // 4 - trunk_h, trunk_w, trunk_h, color=1)

                    for tier in range(3):
                        tier_top = cy - cell_size // 3 + tier * (cell_size // 6)
                        tier_base = tier_top + cell_size // 4
                        half_w = (tier + 1) * (cell_size // 7)
                        for y in range(tier_top, tier_base):
                            prog = (y - tier_top) / float(max(1, tier_base - tier_top))
                            cur_w = int(half_w * prog)
                            tb.draw_hline(cx - cur_w, y, cur_w * 2 + 1, thickness=1, color=1)

        return tb.to_escpos()

    def _ortho_neighbors(self, r: int, c: int, size: int) -> List[Tuple[int, int]]:
        res = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < size and 0 <= nc < size:
                res.append((nr, nc))
        return res

    def _all_neighbors(self, r: int, c: int, size: int) -> List[Tuple[int, int]]:
        res = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < size and 0 <= nc < size:
                    res.append((nr, nc))
        return res

    def _count_solutions(
        self,
        size: int,
        trees: List[Tuple[int, int]],
        row_counts: List[int],
        col_counts: List[int],
        max_count: int = 2,
    ) -> int:
        tree_set = set(trees)
        num_trees = len(trees)

        tent_candidates: Set[Tuple[int, int]] = set()
        tree_adj: Dict[Tuple[int, int], List[Tuple[int, int]]] = {}
        for tr, tc in trees:
            adj = [p for p in self._ortho_neighbors(tr, tc, size) if p not in tree_set]
            tree_adj[(tr, tc)] = adj
            tent_candidates.update(adj)

        cand_list = sorted(list(tent_candidates))
        row_rem = list(row_counts)
        col_rem = list(col_counts)

        if sum(row_counts) != num_trees or sum(col_counts) != num_trees:
            return 0

        placed_tents: Set[Tuple[int, int]] = set()
        solutions_found = 0

        def can_place(r: int, c: int) -> bool:
            if row_rem[r] <= 0 or col_rem[c] <= 0:
                return False
            for nr, nc in self._all_neighbors(r, c, size):
                if (nr, nc) in placed_tents:
                    return False
            return True

        def has_valid_matching(tent_set: Set[Tuple[int, int]]) -> bool:
            if len(tent_set) != num_trees:
                return False
            tent_l = list(tent_set)
            t_adj: List[List[int]] = []
            for tr, tc in trees:
                t_adj.append([i for i, tp in enumerate(tent_l) if tp in tree_adj[(tr, tc)]])

            match: Dict[int, int] = {}
            for u in range(num_trees):
                vis: Set[int] = set()

                def dfs(node: int) -> bool:
                    for v in t_adj[node]:
                        if v not in vis:
                            vis.add(v)
                            if v not in match or dfs(match[v]):
                                match[v] = node
                                return True
                    return False

                if not dfs(u):
                    return False
            return len(match) == num_trees

        def search(idx: int, needed: int):
            nonlocal solutions_found
            if solutions_found >= max_count:
                return

            if needed == 0:
                if all(rem == 0 for rem in row_rem) and all(rem == 0 for rem in col_rem):
                    if has_valid_matching(placed_tents):
                        solutions_found += 1
                return

            if idx >= len(cand_list):
                return

            rem_cands = len(cand_list) - idx
            if rem_cands < needed:
                return

            r, c = cand_list[idx]

            if can_place(r, c):
                placed_tents.add((r, c))
                row_rem[r] -= 1
                col_rem[c] -= 1

                search(idx + 1, needed - 1)

                placed_tents.remove((r, c))
                row_rem[r] += 1
                col_rem[c] += 1

            search(idx + 1, needed)

        search(0, num_trees)
        return solutions_found
