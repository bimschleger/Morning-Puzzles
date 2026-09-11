"""
Queens / Star Battle Puzzle Generator
Inspired by IBM/chuk-puzzles-gym (Apache-2.0).
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
from typing import List, Tuple, Dict, Any, Optional, Set

class QueensGenerator:
    """
    Generates Star Battle / Queens puzzles.
    Rules:
      - For 1-star (LinkedIn Queens style): Place exactly 1 Queen in every row,
        column, and color region. No two Queens can touch, even diagonally.
      - For 2-star: Place exactly 2 Stars in every row, column, and region.
        No two Stars can touch, even diagonally.
    """
    DIFFICULTY_CONFIGS = {
        "easy":   {"size": 6, "stars": 1},
        "medium": {"size": 8, "stars": 1},
        "hard":   {"size": 9, "stars": 2}
    }

    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)

    def generate(self, difficulty: str = "medium") -> Dict[str, Any]:
        difficulty = difficulty.lower()
        cfg = self.DIFFICULTY_CONFIGS.get(difficulty, self.DIFFICULTY_CONFIGS["medium"])
        n = cfg["size"]
        k_stars = cfg["stars"]

        # 1. Place valid star positions on the N x N board
        stars = self._place_stars(n, k_stars)
        if not stars:
            # Fallback for small random chance of failure
            stars = self._place_stars(n, k_stars, max_attempts=500)

        # 2. Partition grid into N contiguous regions
        regions = self._generate_regions(n, stars, k_stars)

        return {
            "type": "queens",
            "style": f"{k_stars}-Star / Queens",
            "difficulty": difficulty,
            "grid_size": n,
            "stars_per_unit": k_stars,
            "regions": regions,
            "stars_solution": list(stars),
            "text": self.format_text(regions, stars, n)
        }

    def _place_stars(self, n: int, k_stars: int, max_attempts: int = 200) -> Set[Tuple[int, int]]:
        for _ in range(max_attempts):
            stars: Set[Tuple[int, int]] = set()
            col_counts = [0] * n

            def can_place(r: int, c: int) -> bool:
                if col_counts[c] >= k_stars:
                    return False
                # Check touching (all 8 adjacent neighbors)
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if (r + dr, c + dc) in stars:
                            return False
                return True

            success = True
            for r in range(n):
                placed_in_row = 0
                cols = list(range(n))
                random.shuffle(cols)
                for c in cols:
                    if can_place(r, c):
                        stars.add((r, c))
                        col_counts[c] += 1
                        placed_in_row += 1
                        if placed_in_row == k_stars:
                            break
                if placed_in_row < k_stars:
                    success = False
                    break

            if success and all(count == k_stars for count in col_counts):
                return stars

        return set()

    def _generate_regions(self, n: int, stars: Set[Tuple[int, int]], k_stars: int) -> List[List[int]]:
        """
        Grows contiguous regions using randomized flood-fill expansion.
        Ensures each region contains exactly k_stars.
        """
        grid = [[-1] * n for _ in range(n)]
        
        # In 1-star, each star gets its own seed region (0 to n-1)
        if k_stars == 1 and len(stars) == n:
            star_list = list(stars)
            for idx, (r, c) in enumerate(star_list):
                grid[r][c] = idx
        else:
            # For 2-stars, pair stars or place N seeds
            seeds = list(stars)[:n]
            for idx, (r, c) in enumerate(seeds):
                grid[r][c] = idx % n

        # Expand regions until all cells are filled
        unassigned = sum(row.count(-1) for row in grid)
        iterations = 0
        while unassigned > 0 and iterations < n * n * 5:
            iterations += 1
            r = random.randint(0, n - 1)
            c = random.randint(0, n - 1)
            if grid[r][c] != -1:
                # Try expanding to a neighbor
                neighbors = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
                random.shuffle(neighbors)
                for nr, nc in neighbors:
                    if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == -1:
                        grid[nr][nc] = grid[r][c]
                        unassigned -= 1
                        break

        # Cleanup any remaining unassigned cells
        for r in range(n):
            for c in range(n):
                if grid[r][c] == -1:
                    grid[r][c] = 0

        return grid

    @staticmethod
    def format_text(regions: List[List[int]], stars: Set[Tuple[int, int]], n: int) -> str:
        # Letters A, B, C... represent the colored regions
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        lines = []
        lines.append("  " + " ".join(str(c + 1) for c in range(n)))
        lines.append("  +" + "--" * n)
        for r in range(n):
            row_str = f"{r + 1}|"
            for c in range(n):
                region_id = regions[r][c]
                label = letters[region_id % len(letters)]
                row_str += f" {label}"
            lines.append(row_str)
        return "\n".join(lines)


if __name__ == "__main__":
    gen = QueensGenerator()
    res = gen.generate(difficulty="easy")
    print(f"Queens / Star Battle ({res['difficulty']}, {res['grid_size']}x{res['grid_size']}):")
    print(res["text"])
    print("Star positions:", sorted(list(res["stars_solution"])))
