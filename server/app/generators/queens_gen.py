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
from collections import deque
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
        "hard":   {"size": 9, "stars": 2},
        "master": {"size": 10, "stars": 2}
    }

    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)

    def generate(self, difficulty: str = "medium") -> Dict[str, Any]:
        difficulty = difficulty.lower()
        cfg = self.DIFFICULTY_CONFIGS.get(difficulty, self.DIFFICULTY_CONFIGS["medium"])
        n = cfg["size"]
        k_stars = cfg["stars"]

        for _ in range(50):
            # 1. Place valid non-touching star positions on the N x N board
            stars = self._place_stars(n, k_stars)
            if not stars:
                continue

            # 2. Partition grid into N contiguous regions
            regions = self._generate_regions(n, stars, k_stars)

            # 3. Validate correctness: exactly k_stars per region, 4-connected, no 0-star shapes
            if self._validate_puzzle(regions, stars, n, k_stars):
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

        raise RuntimeError(f"Failed to generate valid Queens puzzle ({difficulty}) after 50 attempts")

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
        Grows contiguous regions ensuring every single shape contains exactly k_stars.
        In 1-star mode: uses multi-source BFS frontier growth seeded by each star.
        In 2-star mode: pairs the 2N stars using shortest non-intersecting BFS corridors,
        then expands the N paired seeds via multi-source BFS frontier growth.
        """
        grid = [[-1] * n for _ in range(n)]
        frontiers: List[List[Tuple[int, int]]] = [[] for _ in range(n)]
        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        if k_stars == 1:
            for idx, (r, c) in enumerate(stars):
                grid[r][c] = idx
                frontiers[idx].append((r, c))
        else:
            # 2-Star mode: Pair the 2*n stars and connect each pair with a corridor
            paired_grid = None
            star_set = set(stars)

            for _ in range(50):
                temp_grid = [[-1] * n for _ in range(n)]
                unpaired = list(stars)
                random.shuffle(unpaired)
                pairs = []
                all_paired = True

                while unpaired:
                    s1 = unpaired.pop(0)
                    unpaired.sort(key=lambda s: abs(s[0] - s1[0]) + abs(s[1] - s1[1]))

                    found_corridor = None
                    target_idx = -1
                    for idx, s2 in enumerate(unpaired):
                        q = deque([(s1[0], s1[1], [(s1[0], s1[1])])])
                        visited = {s1}
                        while q:
                            cr, cc, path = q.popleft()
                            if (cr, cc) == s2:
                                found_corridor = path
                                break
                            for dr, dc in dirs:
                                nr, nc = cr + dr, cc + dc
                                if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in visited:
                                    if (nr, nc) == s2 or ((nr, nc) not in star_set and temp_grid[nr][nc] == -1):
                                        visited.add((nr, nc))
                                        q.append((nr, nc, path + [(nr, nc)]))
                        if found_corridor:
                            target_idx = idx
                            break

                    if found_corridor:
                        s2 = unpaired.pop(target_idx)
                        reg_id = len(pairs)
                        for pr, pc in found_corridor:
                            temp_grid[pr][pc] = reg_id
                        pairs.append(reg_id)
                    else:
                        all_paired = False
                        break

                if all_paired and len(pairs) == n:
                    paired_grid = temp_grid
                    break

            if paired_grid:
                for r in range(n):
                    for c in range(n):
                        grid[r][c] = paired_grid[r][c]
                        if grid[r][c] != -1:
                            frontiers[grid[r][c]].append((r, c))
            else:
                for idx, (r, c) in enumerate(stars):
                    reg = idx % n
                    grid[r][c] = reg
                    frontiers[reg].append((r, c))

        # Multi-source randomized BFS expansion until 100% of cells are partitioned
        unassigned = sum(row.count(-1) for row in grid)
        active_regions = list(range(n))

        while unassigned > 0 and active_regions:
            reg = random.choice(active_regions)
            candidates = []
            for fr, fc in frontiers[reg]:
                for dr, dc in dirs:
                    nr, nc = fr + dr, fc + dc
                    if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == -1:
                        candidates.append((nr, nc))

            if not candidates:
                active_regions.remove(reg)
                continue

            nr, nc = random.choice(candidates)
            grid[nr][nc] = reg
            frontiers[reg].append((nr, nc))
            unassigned -= 1

        # Fallback: strictly attach any remaining unassigned cells to adjacent regions
        if unassigned > 0:
            progress = True
            while unassigned > 0 and progress:
                progress = False
                for r in range(n):
                    for c in range(n):
                        if grid[r][c] == -1:
                            for dr, dc in dirs:
                                nr, nc = r + dr, c + dc
                                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] != -1:
                                    grid[r][c] = grid[nr][nc]
                                    unassigned -= 1
                                    progress = True
                                    break

        return grid

    def _validate_puzzle(self, regions: List[List[int]], stars: Set[Tuple[int, int]], n: int, k_stars: int) -> bool:
        """
        Validation test: verifies that:
        1. All cells belong to a region in [0, n-1].
        2. Total star count equals n * k_stars.
        3. Exactly k_stars in every row.
        4. Exactly k_stars in every column.
        5. Exactly k_stars in every shape/region.
        6. No two stars touch orthogonally or diagonally.
        7. Every region is a single 4-connected component (no disconnected islands).
        """
        for r in range(n):
            for c in range(n):
                if regions[r][c] < 0 or regions[r][c] >= n:
                    return False

        if len(stars) != n * k_stars:
            return False

        row_counts = [0] * n
        col_counts = [0] * n
        reg_counts = [0] * n
        star_list = list(stars)

        for sr, sc in star_list:
            if not (0 <= sr < n and 0 <= sc < n):
                return False
            row_counts[sr] += 1
            col_counts[sc] += 1
            reg_counts[regions[sr][sc]] += 1

        for i in range(n):
            if row_counts[i] != k_stars or col_counts[i] != k_stars or reg_counts[i] != k_stars:
                return False

        for i in range(len(star_list)):
            for j in range(i + 1, len(star_list)):
                if abs(star_list[i][0] - star_list[j][0]) <= 1 and abs(star_list[i][1] - star_list[j][1]) <= 1:
                    return False

        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for reg in range(n):
            cells = [(r, c) for r in range(n) for c in range(n) if regions[r][c] == reg]
            if not cells:
                return False
            visited = {cells[0]}
            q = deque([cells[0]])
            cell_set = set(cells)
            while q:
                cr, cc = q.popleft()
                for dr, dc in dirs:
                    nr, nc = cr + dr, cc + dc
                    if (nr, nc) in cell_set and (nr, nc) not in visited:
                        visited.add((nr, nc))
                        q.append((nr, nc))
            if len(visited) != len(cells):
                return False

        return True

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
