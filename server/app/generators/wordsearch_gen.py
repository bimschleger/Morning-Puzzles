"""
Word Search Puzzle Generator
Inspired by craigk5n/wordsearch (Apache-2.0).
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
import string
from typing import List, Tuple, Dict, Any, Optional

from app.generators.wordsearch_dataset import (
    WORDSEARCH_THEMES_EASY,
    WORDSEARCH_THEMES_MEDIUM,
    WORDSEARCH_THEMES_HARD,
    THEMES_BY_DIFFICULTY,
    get_random_theme,
    get_theme_words,
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

# Backward compatibility mapping
THEMES = {
    **WORDSEARCH_THEMES_MEDIUM,
    "Morning": ["COFFEE", "SUNRISE", "BAGEL", "ALARM", "TOAST", "PAPER", "SHOWER", "ROOSTER"],
    "Nature":  ["FOREST", "RIVER", "MEADOW", "CANYON", "SUMMIT", "BREEZE", "VALLEY", "STREAM"],
    "Tech":    ["PYTHON", "SERVER", "SOCKET", "ROUTER", "BUFFER", "SERIAL", "BINARY", "KERNEL"],
}

class WordSearchGenerator:
    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)

    def generate(self, 
                 words: Optional[List[str]] = None, 
                 theme: Optional[str] = None,
                 grid_size: Optional[int] = None, 
                 difficulty: str = "medium") -> Dict[str, Any]:
        """
        Generates a Word Search grid.
        Difficulty tiers:
          - easy:   Left-to-Right only (E), 10x10 grid, 6 words
          - medium: Left-to-Right, Right-to-Left, Top-to-Bottom (E, W, S), 12x12 grid, 8 words
          - hard:   All 8 directions including backwards, 12x12 grid, 10 words
        """
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

        # Filter and sanitize words
        raw_words = [w.strip().upper() for w in words if len(w.strip()) <= grid_size]

        best_grid = None
        best_placed = []
        best_placements = {}

        # Attempt generation with up to 5 restarts
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
                placed = False
                attempts = 0
                while not placed and attempts < 150:
                    attempts += 1
                    direction_name = random.choice(allowed_dirs)
                    dr, dc = DIRECTIONS[direction_name]

                    # Compute valid start coordinates
                    r_start = random.randint(0, grid_size - 1)
                    c_start = random.randint(0, grid_size - 1)

                    r_end = r_start + dr * (len(word) - 1)
                    c_end = c_start + dc * (len(word) - 1)

                    if 0 <= r_end < grid_size and 0 <= c_end < grid_size:
                        # Check overlap collision
                        can_place = True
                        for i in range(len(word)):
                            curr_r = r_start + dr * i
                            curr_c = c_start + dc * i
                            if grid[curr_r][curr_c] not in (" ", word[i]):
                                can_place = False
                                break
                        
                        if can_place:
                            for i in range(len(word)):
                                grid[r_start + dr * i][c_start + dc * i] = word[i]
                            placed_words.append(word)
                            placements[word] = {
                                "start": (r_start, c_start),
                                "direction": direction_name
                            }
                            placed = True

            if len(placed_words) > len(best_placed):
                best_grid = grid
                best_placed = placed_words
                best_placements = placements

            if len(best_placed) >= target_words:
                break

        grid = best_grid or [[" " for _ in range(grid_size)] for _ in range(grid_size)]
        placed_words = best_placed
        placements = best_placements

        # Fill blanks with random letters
        solution_mask = [row[:] for row in grid]
        for r in range(grid_size):
            for c in range(grid_size):
                if grid[r][c] == " ":
                    grid[r][c] = random.choice(string.ascii_uppercase)

        return {
            "type": "wordsearch",
            "difficulty": difficulty,
            "theme": theme_name,
            "grid_size": grid_size,
            "words": sorted(placed_words),
            "grid": grid,
            "solution_mask": solution_mask,
            "placements": placements,
            "text": self.format_text(grid, sorted(placed_words))
        }

    @staticmethod
    def format_text(grid: List[List[str]], words: List[str]) -> str:
        lines = []
        for row in grid:
            lines.append(" ".join(row))
        lines.append("")
        lines.append("Words to find:")
        # 2 words per line
        for i in range(0, len(words), 2):
            w1 = f"[ ] {words[i]}"
            w2 = f"[ ] {words[i+1]}" if i + 1 < len(words) else ""
            lines.append(f"{w1:<20} {w2}")
        return "\n".join(lines)


if __name__ == "__main__":
    gen = WordSearchGenerator()
    res = gen.generate(difficulty="medium", grid_size=12)
    print("Word Search Puzzle:")
    print(res["text"])
