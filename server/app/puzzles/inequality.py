"""
INEQUALITY Puzzle Plugin (Latin Square with Inequality Operators)
Morning Puzzles standard implementation adhering to Rules 1-16:
- Rule 1: Single-word title '--- INEQUALITY ---', solution key subtitle 'INEQUALITY'
- Rule 2: DIFFICULTY: EASY / MEDIUM / HARD
- Rule 3: Single sentence instruction <= 100 characters
- Rule 4: ESC/POS 48-column solution key with 6-space indented digits
- Rule 6: BasePuzzle plugin interface
- Rule 8: Tri-target visual parity (576-dot 1-bit thermal raster)
- Rule 10: Curated verified dataset with D4 symmetry invariance & opening anchors
- Rule 12: Harmonized cell pitch (88px) & single-frame discipline
- Rule 13: Clean playable cells, no phantom dots
"""

import json
import os
import random
from typing import Any, Dict, List, Optional, Tuple, Union

from .base import BasePuzzle, BasePuzzleResult
from ..renderer.canvas import THERMAL_WIDTH_DOTS, ThermalBitmap

_DATASET_CACHE = None


def _get_inequality_dataset() -> Dict[str, Any]:
    global _DATASET_CACHE
    if _DATASET_CACHE is None:
        data_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "inequality_dataset.json")
        if os.path.exists(data_path):
            with open(data_path, "r", encoding="utf-8") as f:
                _DATASET_CACHE = json.load(f)
        else:
            _DATASET_CACHE = {}
    return _DATASET_CACHE


def transform_inequality(
    size: int,
    givens: List[List[int]],
    edges_h: List[List[int]],
    edges_v: List[List[int]],
    sol: List[List[int]],
    transform_id: int,
) -> Tuple[List[List[int]], List[List[int]], List[List[int]], List[List[int]]]:
    def map_coord(r: int, c: int) -> Tuple[int, int]:
        if transform_id == 0:
            return (r, c)
        if transform_id == 1:
            return (c, size - 1 - r)  # rot90
        if transform_id == 2:
            return (size - 1 - r, size - 1 - c)  # rot180
        if transform_id == 3:
            return (size - 1 - c, r)  # rot270
        if transform_id == 4:
            return (r, size - 1 - c)  # flip_h
        if transform_id == 5:
            return (size - 1 - r, c)  # flip_v
        if transform_id == 6:
            return (c, r)  # transpose
        if transform_id == 7:
            return (size - 1 - c, size - 1 - r)  # anti-transpose
        return (r, c)

    new_sol = [[0] * size for _ in range(size)]
    for r in range(size):
        for c in range(size):
            nr, nc = map_coord(r, c)
            new_sol[nr][nc] = sol[r][c]

    new_givens = []
    for r, c, val in givens:
        nr, nc = map_coord(r, c)
        new_givens.append([nr, nc, val])

    new_edges_h = [[0] * (size - 1) for _ in range(size)]
    new_edges_v = [[0] * size for _ in range(size - 1)]

    for r in range(size):
        for c in range(size - 1):
            if edges_h[r][c] != 0:
                p1 = map_coord(r, c)
                p2 = map_coord(r, c + 1)
                v1, v2 = sol[r][c], sol[r][c + 1]
                if p1[0] == p2[0]:
                    r_new = p1[0]
                    c_left = min(p1[1], p2[1])
                    val_left = v1 if p1[1] < p2[1] else v2
                    val_right = v2 if p1[1] < p2[1] else v1
                    new_edges_h[r_new][c_left] = 1 if val_left < val_right else 2
                else:
                    c_new = p1[1]
                    r_top = min(p1[0], p2[0])
                    val_top = v1 if p1[0] < p2[0] else v2
                    val_bot = v2 if p1[0] < p2[0] else v1
                    new_edges_v[r_top][c_new] = 1 if val_top < val_bot else 2

    for r in range(size - 1):
        for c in range(size):
            if edges_v[r][c] != 0:
                p1 = map_coord(r, c)
                p2 = map_coord(r + 1, c)
                v1, v2 = sol[r][c], sol[r + 1][c]
                if p1[0] == p2[0]:
                    r_new = p1[0]
                    c_left = min(p1[1], p2[1])
                    val_left = v1 if p1[1] < p2[1] else v2
                    val_right = v2 if p1[1] < p2[1] else v1
                    new_edges_h[r_new][c_left] = 1 if val_left < val_right else 2
                else:
                    c_new = p1[1]
                    r_top = min(p1[0], p2[0])
                    val_top = v1 if p1[0] < p2[0] else v2
                    val_bot = v2 if p1[0] < p2[0] else v1
                    new_edges_v[r_top][c_new] = 1 if val_top < val_bot else 2

    return new_givens, new_edges_h, new_edges_v, new_sol


class InequalityPuzzle(BasePuzzle):
    puzzle_id = "inequality"
    title = "INEQUALITY"

    DIFFICULTY_CONFIGS = {
        "easy": {"size": 4, "cell_size": 88, "height": 400},
        "medium": {"size": 5, "cell_size": 88, "height": 488},
        "hard": {"size": 6, "cell_size": 88, "height": 576},
    }

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
        **kwargs: Any,
    ) -> BasePuzzleResult:
        diff_key = difficulty.lower()
        if diff_key not in self.DIFFICULTY_CONFIGS:
            diff_key = "medium"

        cfg = self.DIFFICULTY_CONFIGS[diff_key]
        size = cfg["size"]

        dataset = _get_inequality_dataset()
        puzzles = dataset.get(diff_key, [])

        if not puzzles:
            raise RuntimeError(f"No curated Inequality puzzles found for difficulty '{diff_key}'")

        if seed is not None:
            idx = (seed // 8) % len(puzzles)
            d4_op = seed % 8
        else:
            idx = random.randint(0, len(puzzles) - 1)
            d4_op = random.randint(0, 7)

        base_p = puzzles[idx]
        givens, edges_h, edges_v, sol = transform_inequality(
            size=size,
            givens=base_p["givens"],
            edges_h=base_p["edges_h"],
            edges_v=base_p["edges_v"],
            sol=base_p["solution"],
            transform_id=d4_op,
        )

        grid = [[0] * size for _ in range(size)]
        for r, c, val in givens:
            grid[r][c] = val

        raw_data = {
            "size": size,
            "difficulty": diff_key,
            "givens": givens,
            "puzzle": grid,
            "edges_h": edges_h,
            "edges_v": edges_v,
            "solution": sol,
            "base_index": idx,
            "d4_op": d4_op,
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

    def get_instruction(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        size = puzzle_data.get("size", 5)
        return f"Fill digits 1-{size} in every line while satisfying all inequality signs between adjacent cells."

    def format_ascii_puzzle(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        size = puzzle_data.get("size", 5)
        givens = puzzle_data.get("givens", [])
        edges_h = puzzle_data.get("edges_h", [[0] * (size - 1) for _ in range(size)])
        edges_v = puzzle_data.get("edges_v", [[0] * size for _ in range(size - 1)])

        grid = [[0] * size for _ in range(size)]
        for r, c, val in givens:
            grid[r][c] = val

        lines = []
        for r in range(size):
            # Row with cell contents and horizontal inequality operators
            row_items = []
            for c in range(size):
                cell_char = str(grid[r][c]) if grid[r][c] > 0 else "."
                row_items.append(cell_char)
                if c < size - 1:
                    eh = edges_h[r][c]
                    if eh == 1:
                        row_items.append("<")
                    elif eh == 2:
                        row_items.append(">")
                    else:
                        row_items.append(" ")
            lines.append("      " + " ".join(row_items))

            # Vertical inequality operators between rows
            if r < size - 1:
                v_items = []
                for c in range(size):
                    ev = edges_v[r][c]
                    if ev == 1:
                        v_items.append("^")
                    elif ev == 2:
                        v_items.append("v")
                    else:
                        v_items.append(" ")
                    if c < size - 1:
                        v_items.append(" ")
                lines.append("      " + " ".join(v_items))

        return "\n".join(lines)

    def format_solution_key(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> List[str]:
        sol = puzzle_data.get("solution", [])
        if not sol:
            return []

        lines = []
        for row in sol:
            lines.append("      " + " ".join(str(v) for v in row))
        return lines

    def render_raster(
        self,
        puzzle_data: Union[BasePuzzleResult, Dict[str, Any]],
        target_width: int = THERMAL_WIDTH_DOTS,
    ) -> bytes:
        size = puzzle_data.get("size", 5)
        diff_key = str(puzzle_data.get("difficulty", "medium")).lower()
        cfg = self.DIFFICULTY_CONFIGS.get(diff_key, self.DIFFICULTY_CONFIGS["medium"])

        cell_size = cfg["cell_size"]
        grid_w = size * cell_size
        total_h = cfg["height"]

        grid_x = (target_width - grid_w) // 2
        grid_y = (total_h - grid_w) // 2

        tb = ThermalBitmap(target_width, total_h)

        # Outer grid border (4px)
        tb.draw_rect(grid_x, grid_y, grid_w, grid_w, thickness=4)

        # Inner cell divider lines (1px)
        for i in range(1, size):
            tb.draw_hline(grid_x, grid_y + i * cell_size, grid_w, thickness=1)
            tb.draw_vline(grid_x + i * cell_size, grid_y, grid_w, thickness=1)

        edges_h = puzzle_data.get("edges_h", [])
        edges_v = puzzle_data.get("edges_v", [])

        # Horizontal inequality operators
        for r in range(size):
            for c in range(size - 1):
                eh = edges_h[r][c] if r < len(edges_h) and c < len(edges_h[r]) else 0
                if eh in (1, 2):
                    cx = grid_x + (c + 1) * cell_size
                    cy = grid_y + r * cell_size + cell_size // 2
                    tb.fill_rect(cx - 12, cy - 12, 25, 25, color=0)
                    if eh == 1:  # < (left < right)
                        for d in range(8):
                            tb.set_pixel(cx - 4 + d, cy - d, 1)
                            tb.set_pixel(cx - 4 + d, cy - d + 1, 1)
                            tb.set_pixel(cx - 4 + d, cy + d, 1)
                            tb.set_pixel(cx - 4 + d, cy + d - 1, 1)
                    elif eh == 2:  # > (left > right)
                        for d in range(8):
                            tb.set_pixel(cx + 3 - d, cy - d, 1)
                            tb.set_pixel(cx + 3 - d, cy - d + 1, 1)
                            tb.set_pixel(cx + 3 - d, cy + d, 1)
                            tb.set_pixel(cx + 3 - d, cy + d - 1, 1)

        # Vertical inequality operators
        for r in range(size - 1):
            for c in range(size):
                ev = edges_v[r][c] if r < len(edges_v) and c < len(edges_v[r]) else 0
                if ev in (1, 2):
                    cx = grid_x + c * cell_size + cell_size // 2
                    cy = grid_y + (r + 1) * cell_size
                    tb.fill_rect(cx - 12, cy - 12, 25, 25, color=0)
                    if ev == 1:  # ^ (top < bottom)
                        for d in range(8):
                            tb.set_pixel(cx - d, cy - 4 + d, 1)
                            tb.set_pixel(cx - d + 1, cy - 4 + d, 1)
                            tb.set_pixel(cx + d, cy - 4 + d, 1)
                            tb.set_pixel(cx + d - 1, cy - 4 + d, 1)
                    elif ev == 2:  # v (top > bottom)
                        for d in range(8):
                            tb.set_pixel(cx - d, cy + 3 - d, 1)
                            tb.set_pixel(cx - d + 1, cy + 3 - d, 1)
                            tb.set_pixel(cx + d, cy + 3 - d, 1)
                            tb.set_pixel(cx + d - 1, cy + 3 - d, 1)

        # Given numbers inside cells (scale 3: 15x21px glyph, 18px char width)
        givens = puzzle_data.get("givens", [])
        for r, c, val in givens:
            tx = grid_x + c * cell_size + (cell_size - 18) // 2
            ty = grid_y + r * cell_size + (cell_size - 21) // 2
            tb.draw_text(tx, ty, str(val), scale=3)

        return tb.to_escpos()

    def verify_accuracy(
        self,
        puzzle_data: Union[BasePuzzleResult, Dict[str, Any]],
    ) -> Tuple[bool, str]:
        size = puzzle_data.get("size", 5)
        sol = puzzle_data.get("solution", [])
        givens = puzzle_data.get("givens", [])
        edges_h = puzzle_data.get("edges_h", [])
        edges_v = puzzle_data.get("edges_v", [])

        if len(sol) != size:
            return False, f"Expected {size} rows in solution, found {len(sol)}"

        expected_digits = set(range(1, size + 1))
        for r in range(size):
            if len(sol[r]) != size:
                return False, f"Row {r} length {len(sol[r])} != {size}"
            if set(sol[r]) != expected_digits:
                return False, f"Row {r} digits {sol[r]} do not match {expected_digits}"

        for c in range(size):
            col_vals = [sol[r][c] for r in range(size)]
            if set(col_vals) != expected_digits:
                return False, f"Column {c} digits {col_vals} do not match {expected_digits}"

        for r, c, val in givens:
            if sol[r][c] != val:
                return False, f"Given mismatch at ({r}, {c}): expected {val}, got {sol[r][c]}"

        for r in range(size):
            for c in range(size - 1):
                eh = edges_h[r][c] if r < len(edges_h) and c < len(edges_h[r]) else 0
                if eh == 1 and not (sol[r][c] < sol[r][c + 1]):
                    return False, f"Horizontal edge {r},{c} broken: {sol[r][c]} not < {sol[r][c+1]}"
                if eh == 2 and not (sol[r][c] > sol[r][c + 1]):
                    return False, f"Horizontal edge {r},{c} broken: {sol[r][c]} not > {sol[r][c+1]}"

        for r in range(size - 1):
            for c in range(size):
                ev = edges_v[r][c] if r < len(edges_v) and c < len(edges_v[r]) else 0
                if ev == 1 and not (sol[r][c] < sol[r + 1][c]):
                    return False, f"Vertical edge {r},{c} broken: {sol[r][c]} not < {sol[r+1][c]}"
                if ev == 2 and not (sol[r][c] > sol[r + 1][c]):
                    return False, f"Vertical edge {r},{c} broken: {sol[r][c]} not > {sol[r+1][c]}"

        return True, "All rules satisfied"
