"""
TOWERS Puzzle Plugin (Skyscrapers / 3D Line-of-Sight Deduction)
Morning Puzzles standard implementation adhering to Rules 1-16:
- Rule 1: Single-word title '--- TOWERS ---', solution key subtitle 'TOWERS'
- Rule 2: DIFFICULTY: EASY / MEDIUM / HARD
- Rule 3: Single sentence instruction <= 100 characters
- Rule 4: ESC/POS 48-column solution key with 6-space indented digits
- Rule 6: BasePuzzle plugin interface
- Rule 8: Tri-target visual parity (576-dot 1-bit thermal raster)
- Rule 10: Curated verified dataset with D4 symmetry invariance & opening anchors
- Rule 12: Harmonized cell pitch
- Rule 13: Floating margin numbers with >= 4-6px padding, clean playable cells
"""

import random
from typing import Any, Dict, List, Optional, Tuple, Union

from .base import (
    BasePuzzle,
    BasePuzzleResult,
    load_curated_dataset,
    select_seeded_d4,
    transform_grid_d4,
)
from ..renderer.canvas import THERMAL_WIDTH_DOTS, ThermalBitmap


def transform_grid(grid: List[List[int]], rot: int, flip: int) -> List[List[int]]:
    return transform_grid_d4(grid, rot, flip, flip_first=True)


def transform_clues(clues: Dict[str, List[int]], rot: int, flip: int) -> Dict[str, List[int]]:
    t = clues["top"][:]
    b = clues["bottom"][:]
    l = clues["left"][:]
    r = clues["right"][:]
    if flip:
        t = list(reversed(t))
        b = list(reversed(b))
        l, r = r, l
    for _ in range(rot):
        new_t = list(reversed(l))
        new_r = t[:]
        new_b = list(reversed(r))
        new_l = b[:]
        t, r, b, l = new_t, new_r, new_b, new_l
    return {"top": t, "bottom": b, "left": l, "right": r}


class TowersPuzzle(BasePuzzle):
    puzzle_id = "towers"
    title = "TOWERS"

    DIFFICULTY_CONFIGS = {
        "easy": {"size": 4, "max_val": 4, "cell_size": 80, "height": 400},
        "medium": {"size": 4, "max_val": 4, "cell_size": 80, "height": 400},
        "hard": {"size": 5, "max_val": 5, "cell_size": 72, "height": 440},
        "extreme": {"size": 5, "max_val": 5, "cell_size": 72, "height": 440},
    }

    @property
    def has_difficulty(self) -> bool:
        return True

    @property
    def supported_difficulties(self) -> List[str]:
        return ["easy", "medium", "hard", "extreme"]

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

        dataset = load_curated_dataset("towers_dataset.json") or {}
        puzzles = dataset.get(diff_key, [])

        if not puzzles:
            raise RuntimeError(f"No curated Towers puzzles found for difficulty '{diff_key}'")

        idx, d4_op = select_seeded_d4(puzzles, seed)

        rot = d4_op % 4
        flip = d4_op // 4

        base_p = puzzles[idx]
        grid_sol = transform_grid(base_p["solution"], rot, flip)
        grid_clues = transform_clues(base_p["clues"], rot, flip)

        raw_data = {
            "size": size,
            "difficulty": diff_key,
            "clues": grid_clues,
            "solution": grid_sol,
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
        return f"Place heights 1-{size} per line so exterior numbers match the count of visible taller buildings."

    def format_ascii_puzzle(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        size = puzzle_data.get("size", 5)
        clues = puzzle_data.get("clues", {})
        top = clues.get("top", [0] * size)
        bottom = clues.get("bottom", [0] * size)
        left = clues.get("left", [0] * size)
        right = clues.get("right", [0] * size)

        lines = []
        # Top clue line
        top_str = "       " + " ".join(str(v) if v > 0 else " " for v in top)
        lines.append(top_str)

        sep = "     +" + "---+" * size
        lines.append(sep)

        for r in range(size):
            l_char = str(left[r]) if left[r] > 0 else " "
            r_char = str(right[r]) if right[r] > 0 else " "
            row_str = f"   {l_char} |"
            for c in range(size):
                row_str += "   |"
            row_str += f" {r_char}"
            lines.append(row_str)
            lines.append(sep)

        # Bottom clue line
        bot_str = "       " + " ".join(str(v) if v > 0 else " " for v in bottom)
        lines.append(bot_str)

        return "\n".join(lines)

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

        clues = puzzle_data.get("clues", {})
        top = clues.get("top", [0] * size)
        bottom = clues.get("bottom", [0] * size)
        left = clues.get("left", [0] * size)
        right = clues.get("right", [0] * size)

        # Top exterior clues (scale 2: 10x14px glyph, 12px char width)
        for c in range(size):
            if top[c] > 0:
                cx = grid_x + c * cell_size + (cell_size - 12) // 2
                cy = grid_y - 20
                tb.draw_text(cx, cy, str(top[c]), scale=2)

        # Bottom exterior clues
        for c in range(size):
            if bottom[c] > 0:
                cx = grid_x + c * cell_size + (cell_size - 12) // 2
                cy = grid_y + grid_w + 6
                tb.draw_text(cx, cy, str(bottom[c]), scale=2)

        # Left exterior clues
        for r in range(size):
            if left[r] > 0:
                cx = grid_x - 18
                cy = grid_y + r * cell_size + (cell_size - 14) // 2
                tb.draw_text(cx, cy, str(left[r]), scale=2)

        # Right exterior clues
        for r in range(size):
            if right[r] > 0:
                cx = grid_x + grid_w + 6
                cy = grid_y + r * cell_size + (cell_size - 14) // 2
                tb.draw_text(cx, cy, str(right[r]), scale=2)

        return tb.to_escpos()

    def verify_accuracy(
        self,
        puzzle_data: Union[BasePuzzleResult, Dict[str, Any]],
    ) -> Tuple[bool, str]:
        size = puzzle_data.get("size", 5)
        sol = puzzle_data.get("solution", [])
        clues = puzzle_data.get("clues", {})

        if len(sol) != size:
            return False, f"Expected {size} rows, found {len(sol)}"

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

        def count_vis(seq: List[int]) -> int:
            m = 0
            cnt = 0
            for x in seq:
                if x > m:
                    cnt += 1
                    m = x
            return cnt

        top = clues.get("top", [0] * size)
        bottom = clues.get("bottom", [0] * size)
        left = clues.get("left", [0] * size)
        right = clues.get("right", [0] * size)

        for c in range(size):
            if top[c] > 0:
                col_seq = [sol[r][c] for r in range(size)]
                v = count_vis(col_seq)
                if v != top[c]:
                    return False, f"Top clue mismatch at col {c}: expected {top[c]}, got {v}"
            if bottom[c] > 0:
                col_seq = [sol[r][c] for r in reversed(range(size))]
                v = count_vis(col_seq)
                if v != bottom[c]:
                    return False, f"Bottom clue mismatch at col {c}: expected {bottom[c]}, got {v}"

        for r in range(size):
            if left[r] > 0:
                v = count_vis(sol[r])
                if v != left[r]:
                    return False, f"Left clue mismatch at row {r}: expected {left[r]}, got {v}"
            if right[r] > 0:
                v = count_vis(list(reversed(sol[r])))
                if v != right[r]:
                    return False, f"Right clue mismatch at row {r}: expected {right[r]}, got {v}"

        diff = puzzle_data.get("difficulty", "medium").lower()
        if diff in ("easy", "medium"):
            all_clues = top + bottom + left + right
            if (1 not in all_clues) and (size not in all_clues):
                return False, f"No opening anchor clue (1 or {size}) found on {diff}"

        return True, "All rules satisfied"
