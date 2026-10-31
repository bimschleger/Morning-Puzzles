"""
Morning Puzzles - Search (Word Search) Plugin
Procedural multi-directional word search puzzle generator conforming to docs/PUZZLE_HEADER_SPEC.md.
Provides difficulty-scaled grids, orientations, and letter intersections.
"""

import random
import string
import textwrap
from typing import List, Tuple, Dict, Any, Optional, Union

from .base import BasePuzzle, BasePuzzleResult, load_curated_dataset
from ..renderer.canvas import (
    THERMAL_WIDTH_DOTS,
    ThermalBitmap,
)


def _get_wordsearch_dataset() -> Dict[str, List[str]]:
    return load_curated_dataset("wordsearch_dataset.json") or {}


def get_random_words(difficulty: str = "medium", count: int = 8) -> List[str]:
    data = _get_wordsearch_dataset()
    diff_key = difficulty.lower()
    pool = data.get(diff_key, data.get("medium", []))
    if isinstance(pool, dict):
        # Fallback if old format dictionary
        words = []
        for wlist in pool.values():
            words.extend(wlist)
        pool = words
    if not pool:
        pool = ["SEARCH", "PUZZLE", "FIND", "WORD", "LETTER", "HIDDEN", "DISCOVER", "SOLVE"]
    return random.sample(pool, min(len(pool), count))


DIRECTIONS = {
    "E":  (0, 1),    # Horizontal forward
    "W":  (0, -1),   # Horizontal backwards
    "S":  (1, 0),    # Vertical downward
    "N":  (-1, 0),   # Vertical upward
    "SE": (1, 1),    # Diagonal downward right
    "NE": (-1, 1),   # Diagonal upward right
    "SW": (1, -1),   # Diagonal downward left
    "NW": (-1, -1),  # Diagonal upward left
}


class WordSearchPuzzle(BasePuzzle):
    """Word Search puzzle plugin."""

    @property
    def puzzle_id(self) -> str:
        return "wordsearch"

    @property
    def title(self) -> str:
        return "SEARCH"

    @property
    def has_difficulty(self) -> bool:
        return True

    def generate(
        self,
        difficulty: str = "medium",
        words: Optional[List[str]] = None,
        theme: Optional[str] = None,
        grid_size: Optional[int] = None,
        seed: Optional[int] = None,
        **kwargs,
    ) -> BasePuzzleResult:
        if seed is not None:
            random.seed(seed)

        difficulty = difficulty.lower()
        if difficulty == "easy":
            target_words = 6
            if grid_size is None:
                grid_size = 10
            min_intersections = 0
        elif difficulty == "hard" or difficulty == "extreme":
            target_words = 8
            if grid_size is None:
                grid_size = 12
            min_intersections = 3
        else:
            target_words = 8
            if grid_size is None:
                grid_size = 12
            min_intersections = 2

        dataset = _get_wordsearch_dataset()
        pool = dataset.get(difficulty, dataset.get("medium", []))
        if isinstance(pool, dict):
            flattened = []
            for wlist in pool.values():
                flattened.extend(wlist)
            pool = flattened

        best_grid = None
        best_placed = []
        best_placements = {}
        best_intersections = -1

        for restart in range(8):
            if words:
                raw_words = [w.strip().upper() for w in words if len(w.strip()) <= grid_size]
            else:
                sample_count = min(len(pool), target_words + 8)
                raw_words = [w.strip().upper() for w in random.sample(pool, sample_count) if len(w.strip()) <= grid_size]

            raw_words.sort(key=len, reverse=True)

            if difficulty in ("hard", "extreme"):
                dir_assignment = list(DIRECTIONS.keys())
                random.shuffle(dir_assignment)
            elif difficulty == "easy":
                dir_assignment = ["E", "S"]
            else:
                dir_assignment = list(DIRECTIONS.keys())

            grid = [[" " for _ in range(grid_size)] for _ in range(grid_size)]
            placed_words = []
            placements = {}

            for word in raw_words:
                if len(placed_words) >= target_words:
                    break

                if difficulty in ("hard", "extreme"):
                    d_name = dir_assignment[len(placed_words)]
                    allowed = [d_name]
                elif difficulty == "easy":
                    allowed = ["E", "S"]
                    random.shuffle(allowed)
                else:
                    allowed = list(DIRECTIONS.keys())
                    random.shuffle(allowed)

                placed = False
                for d in allowed:
                    dr, dc = DIRECTIONS[d]
                    L = len(word)
                    candidates = []

                    for r in range(grid_size):
                        for c in range(grid_size):
                            end_r = r + dr * (L - 1)
                            end_c = c + dc * (L - 1)
                            if not (0 <= end_r < grid_size and 0 <= end_c < grid_size):
                                continue

                            can_place = True
                            overlaps = 0
                            for i in range(L):
                                cr = r + dr * i
                                cc = c + dc * i
                                ch = grid[cr][cc]
                                if ch != " ":
                                    if ch == word[i]:
                                        overlaps += 1
                                    else:
                                        can_place = False
                                        break
                            if can_place:
                                if len(placed_words) == 0:
                                    mid_r = r + dr * (L // 2)
                                    mid_c = c + dc * (L // 2)
                                    dist = abs(mid_r - grid_size // 2) + abs(mid_c - grid_size // 2)
                                    score = 20 - dist
                                else:
                                    score = overlaps * 10
                                candidates.append((score, r, c, d))

                    if candidates:
                        candidates.sort(key=lambda x: x[0], reverse=True)
                        top_score = candidates[0][0]
                        top_tier = [c_cand for c_cand in candidates if c_cand[0] == top_score]
                        score, r, c, d = random.choice(top_tier)

                        for i, ch in enumerate(word):
                            grid[r + dr * i][c + dc * i] = ch
                        placed_words.append(word)
                        placements[word] = {"row": r, "col": c, "dir": d}
                        placed = True
                        break

            # Count cell intersections (shared letters)
            cell_usage = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
            for w, p in placements.items():
                r, c, d = p["row"], p["col"], p["dir"]
                dr, dc = DIRECTIONS[d]
                for i in range(len(w)):
                    cell_usage[r + dr * i][c + dc * i] += 1
            intersections = sum(1 for r in range(grid_size) for c in range(grid_size) if cell_usage[r][c] >= 2)

            if len(placed_words) == target_words:
                if intersections > best_intersections:
                    best_intersections = intersections
                    best_grid = [row[:] for row in grid]
                    best_placed = list(placed_words)
                    best_placements = dict(placements)
                if intersections >= min_intersections:
                    break

        grid = best_grid or [[" " for _ in range(grid_size)] for _ in range(grid_size)]
        placed_words = best_placed
        placements = best_placements

        # Solution snapshot before filling empty cells
        solution_grid = [row[:] for row in grid]

        # Fill empty cells with random uppercase letters
        for r in range(grid_size):
            for c in range(grid_size):
                if grid[r][c] == " ":
                    grid[r][c] = random.choice(string.ascii_uppercase)

        raw_data = {
            "type": "wordsearch",
            "grid": grid,
            "solution": solution_grid,
            "words": placed_words,
            "placed_words": placed_words,
            "placements": placements,
            "grid_size": grid_size,
            "difficulty": difficulty,
            "intersections": best_intersections,
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
        words_count = len(puzzle_data.get("placed_words", [])) or len(puzzle_data.get("words", []))
        if words_count:
            return f"Find all {words_count} hidden words listed below."
        return "Find all listed words hidden across the grid."

    def format_ascii_puzzle(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        grid = puzzle_data.get("grid", [])
        words = puzzle_data.get("words", [])

        lines = []
        for row in grid:
            lines.append("   " + " ".join(row))
        lines.append("")
        lines.append("Words to find:")
        for i in range(0, len(words), 2):
            w1 = f"[ ] {words[i]}"
            w2 = f"[ ] {words[i+1]}" if i + 1 < len(words) else ""
            lines.append(f"  {w1:<20} {w2}")
        return "\n".join(lines)

    def format_solution_key(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> List[str]:
        words = puzzle_data.get("words", [])
        words_str = "Words: " + ", ".join(words)
        lines = []
        for line in textwrap.wrap(words_str, 46):
            lines.append(line)
        return lines

    def render_raster(
        self,
        puzzle_data: Union[BasePuzzleResult, Dict[str, Any]],
        target_width: int = THERMAL_WIDTH_DOTS,
    ) -> bytes:
        grid = puzzle_data.get("grid", [])
        words = puzzle_data.get("words", [])

        rows = len(grid)
        cols = len(grid[0]) if rows > 0 else 12

        cell_size = (target_width - 48) // cols
        inner_width = cell_size * cols
        padding = (target_width - inner_width) // 2
        grid_h = cell_size * rows

        checklist_rows = (len(words) + 1) // 2
        checklist_h = 40 + checklist_rows * 28
        total_h = 12 + grid_h + 20 + checklist_h + 12

        tb = ThermalBitmap(target_width, total_h)
        grid_y = 12

        tb.draw_rect(padding, grid_y, cell_size * cols, grid_h, thickness=4)
        for r in range(rows):
            for c in range(cols):
                letter = grid[r][c] if r < len(grid) and c < len(grid[r]) else " "
                cx = padding + c * cell_size + (cell_size - 18) // 2
                cy = grid_y + r * cell_size + (cell_size - 21) // 2
                tb.draw_char(cx, cy, letter, scale=3)
                if c > 0:
                    tb.draw_vline(padding + c * cell_size, grid_y, grid_h, thickness=1)
            if r > 0:
                tb.draw_hline(padding, grid_y + r * cell_size, cell_size * cols, thickness=1)

        cur_y = grid_y + grid_h + 16
        tb.draw_hline(padding, cur_y, inner_width, thickness=2)
        cur_y += 18
        tb.draw_text(padding, cur_y, "WORDS TO FIND:", scale=2)
        cur_y += 28

        col_w = inner_width // 2
        for i, word in enumerate(words):
            col_idx = i % 2
            row_idx = i // 2
            ix = padding + col_idx * col_w
            iy = cur_y + row_idx * 28
            tb.draw_rect(ix, iy + 2, 16, 16, thickness=2)
            tb.draw_text(ix + 24, iy + 2, word.upper(), scale=2)

        return tb.to_escpos()

    def verify_accuracy(
        self,
        puzzle_data: Union[BasePuzzleResult, Dict[str, Any]],
    ) -> Tuple[bool, str]:
        grid = puzzle_data.get("grid")
        if not grid or not isinstance(grid, list):
            return False, "WordSearch grid missing or invalid"
        rows = len(grid)
        cols = len(grid[0]) if rows > 0 else 0
        if rows < 8 or cols < 8:
            return False, f"WordSearch grid too small: {rows}x{cols}"
        for r in range(rows):
            for c in range(cols):
                if not grid[r][c] or grid[r][c] == " ":
                    return False, f"WordSearch grid contains empty cell at ({r},{c})"

        placed_words = puzzle_data.get("placed_words") or puzzle_data.get("words") or []
        if len(placed_words) < 4:
            return False, f"WordSearch has too few placed words: {len(placed_words)}"

        placements = puzzle_data.get("placements") or {}
        for word in placed_words:
            if word in placements:
                info = placements[word]
                r, c, d_name = info["row"], info["col"], info["dir"]
                if d_name not in DIRECTIONS:
                    return False, f"WordSearch word '{word}' has invalid direction '{d_name}'"
                dr, dc = DIRECTIONS[d_name]
                for i, char in enumerate(word):
                    cr, cc = r + dr * i, c + dc * i
                    if not (0 <= cr < rows and 0 <= cc < cols):
                        return False, f"WordSearch word '{word}' exceeds grid boundaries at index {i}"
                    if grid[cr][cc] != char:
                        return False, f"WordSearch word '{word}' character mismatch at ({cr},{cc}): expected '{char}', got '{grid[cr][cc]}'"

        return True, "All rules satisfied"
