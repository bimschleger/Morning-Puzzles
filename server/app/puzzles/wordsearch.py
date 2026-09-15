"""
Morning Puzzles - Search (Word Search) Plugin
Theme-driven word search puzzle generator conforming to docs/PUZZLE_HEADER_SPEC.md.
Completely omits the difficulty line as it is theme-driven.
"""

import random
import string
import textwrap
from typing import List, Tuple, Dict, Any, Optional, Union

from .base import BasePuzzle, BasePuzzleResult
from ..generators.wordsearch_dataset import (
    get_random_theme,
    get_theme_words,
)
from ..renderer.canvas import (
    THERMAL_WIDTH_DOTS,
    ThermalBitmap,
)

DIRECTIONS = {
    "E":  (0, 1),    # Horizontal forward
    "S":  (1, 0),    # Vertical downward
    "SE": (1, 1),    # Diagonal downward right
    "NE": (-1, 1),   # Diagonal upward right
    "W":  (0, -1),   # Horizontal backwards
    "N":  (-1, 0),   # Vertical upward
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
        # Theme-driven: strictly omits difficulty header line
        return False

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
            allowed_dirs = ["E"]
            target_words = 6
            if grid_size is None:
                grid_size = 10
        elif difficulty == "hard":
            allowed_dirs = list(DIRECTIONS.keys())
            target_words = 10
            if grid_size is None:
                grid_size = 12
        else:
            allowed_dirs = ["E", "W", "S"]
            target_words = 8
            if grid_size is None:
                grid_size = 12

        if not words:
            if theme:
                theme_name, words = get_theme_words(theme, difficulty=difficulty)
            else:
                theme_name, words = get_random_theme(difficulty=difficulty)
        else:
            theme_name = theme or "Custom"

        raw_words = [w.strip().upper() for w in words if len(w.strip()) <= grid_size]
        best_grid = None
        best_placed = []
        best_placements = {}

        for retry in range(5):
            clean_words = list(raw_words)
            random.shuffle(clean_words)
            clean_words.sort(key=len, reverse=True)

            grid = [[" " for _ in range(grid_size)] for _ in range(grid_size)]
            placed_words = []
            placements = {}

            for word in clean_words:
                if len(placed_words) >= target_words:
                    break
                shuffled_dirs = list(allowed_dirs)
                random.shuffle(shuffled_dirs)
                placed = False
                for d_name in shuffled_dirs:
                    dr, dc = DIRECTIONS[d_name]
                    positions = [(r, c) for r in range(grid_size) for c in range(grid_size)]
                    random.shuffle(positions)
                    for r, c in positions:
                        if self._can_place(grid, word, r, c, dr, dc, grid_size):
                            self._place_word(grid, word, r, c, dr, dc)
                            placed_words.append(word)
                            placements[word] = {"row": r, "col": c, "dir": d_name}
                            placed = True
                            break
                    if placed:
                        break

            if len(placed_words) > len(best_placed):
                best_placed = placed_words
                best_grid = [row[:] for row in grid]
                best_placements = placements
                if len(best_placed) >= target_words:
                    break

        grid = best_grid or [[" " for _ in range(grid_size)] for _ in range(grid_size)]
        placed_words = best_placed
        placements = best_placements

        # Solution snapshot before filling empty cells
        solution_grid = [row[:] for row in grid]

        # Fill empty cells with random letters
        for r in range(grid_size):
            for c in range(grid_size):
                if grid[r][c] == " ":
                    grid[r][c] = random.choice(string.ascii_uppercase)

        raw_data = {
            "type": "wordsearch",
            "theme": theme_name,
            "grid": grid,
            "solution": solution_grid,
            "words": placed_words,
            "placed_words": placed_words,
            "placements": placements,
            "grid_size": grid_size,
            "difficulty": difficulty,
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
        theme = puzzle_data.get("theme", "")

        lines = []
        for row in grid:
            lines.append("   " + " ".join(row))
        lines.append("")
        if theme:
            lines.append(f"Theme: {theme}")
        lines.append("Words to find:")
        for i in range(0, len(words), 2):
            w1 = f"[ ] {words[i]}"
            w2 = f"[ ] {words[i+1]}" if i + 1 < len(words) else ""
            lines.append(f"  {w1:<20} {w2}")
        return "\n".join(lines)

    def format_solution_key(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> List[str]:
        words = puzzle_data.get("words", [])
        theme = puzzle_data.get("theme", "")
        lines = []
        if theme:
            lines.append(f"Theme: {theme}")
        words_str = "Words: " + ", ".join(words)
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
        theme = puzzle_data.get("theme", "General")

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
        tb.draw_text(padding, cur_y, f"THEME: {theme.upper()}", scale=2)
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

    def _can_place(self, grid, word, r, c, dr, dc, grid_size):
        end_r = r + dr * (len(word) - 1)
        end_c = c + dc * (len(word) - 1)
        if not (0 <= end_r < grid_size and 0 <= end_c < grid_size):
            return False
        for i, ch in enumerate(word):
            curr_r = r + dr * i
            curr_c = c + dc * i
            if grid[curr_r][curr_c] not in (" ", ch):
                return False
        return True

    def _place_word(self, grid, word, r, c, dr, dc):
        for i, ch in enumerate(word):
            grid[r + dr * i][c + dc * i] = ch

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
        # If placements dict is provided, verify every word's coordinate and spelling
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
