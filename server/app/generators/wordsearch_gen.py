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

THEMES = {
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
                 theme: str = "Morning",
                 grid_size: int = 12, 
                 difficulty: str = "medium") -> Dict[str, Any]:
        """
        Generates a Word Search grid.
        Difficulty tiers:
          - easy:   Horizontal & Vertical forward only (E, S)
          - medium: Forward directions (E, S, SE, NE)
          - hard:   All 8 directions including backwards (E, S, SE, NE, W, N, SW, NW)
        """
        difficulty = difficulty.lower()
        if difficulty == "easy":
            allowed_dirs = ["E", "S"]
        elif difficulty == "hard":
            allowed_dirs = list(DIRECTIONS.keys())
        else:
            allowed_dirs = ["E", "S", "SE", "NE"]

        if not words:
            words = THEMES.get(theme, THEMES["Morning"])

        # Filter and sanitize words
        clean_words = [w.strip().upper() for w in words if len(w.strip()) <= grid_size]
        random.shuffle(clean_words)

        grid = [[" " for _ in range(grid_size)] for _ in range(grid_size)]
        placed_words = []
        placements = {}

        for word in clean_words:
            placed = False
            attempts = 0
            while not placed and attempts < 100:
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

        # Fill blanks with random letters
        solution_mask = [row[:] for row in grid]
        for r in range(grid_size):
            for c in range(grid_size):
                if grid[r][c] == " ":
                    grid[r][c] = random.choice(string.ascii_uppercase)

        return {
            "type": "wordsearch",
            "difficulty": difficulty,
            "theme": theme,
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
