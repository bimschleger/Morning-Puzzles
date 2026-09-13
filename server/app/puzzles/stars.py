"""
Morning Puzzles - Stars (Queens / Star Battle) Plugin
Encapsulates generation, canonical instruction formatting, ASCII layout,
solution key formatting, and 576-dot dithered thermal raster rendering.
"""

import random
import textwrap
from collections import deque
from typing import List, Tuple, Dict, Any, Optional, Set, Union

from .base import BasePuzzle, BasePuzzleResult
from ..renderer.canvas import (
    THERMAL_WIDTH_DOTS,
    HAS_PILLOW,
    pil_to_escpos,
    ThermalBitmap,
)

if HAS_PILLOW:
    from PIL import Image, ImageDraw


class StarsPuzzle(BasePuzzle):
    """Stars (Queens / Star Battle) puzzle plugin."""

    DIFFICULTY_CONFIGS = {
        "easy":   {"size": 5, "stars": 1},
        "medium": {"size": 8, "stars": 1},
        "hard":   {"size": 9, "stars": 2},
        "master": {"size": 10, "stars": 2},
    }

    @property
    def puzzle_id(self) -> str:
        # Legacy ID for bundle key and endpoint backwards compatibility
        return "queens"

    @property
    def title(self) -> str:
        return "STARS"

    @property
    def has_difficulty(self) -> bool:
        return True

    @property
    def supported_difficulties(self) -> List[str]:
        return ["easy", "medium", "hard", "master"]

    def generate(
        self,
        difficulty: str = "medium",
        seed: Optional[int] = None,
        **kwargs,
    ) -> BasePuzzleResult:
        if seed is not None:
            random.seed(seed)

        difficulty = difficulty.lower()
        cfg = self.DIFFICULTY_CONFIGS.get(difficulty, self.DIFFICULTY_CONFIGS["medium"])
        n = cfg["size"]
        k_stars = cfg["stars"]

        for _ in range(50):
            stars = self._place_stars(n, k_stars)
            if not stars:
                continue

            regions = self._generate_regions(n, stars, k_stars)

            if self._validate_puzzle(regions, stars, n, k_stars):
                ascii_text = self.format_ascii_puzzle({"regions": regions, "stars_solution": list(stars), "grid_size": n})
                instruction = self.get_instruction({"difficulty": difficulty, "stars_per_unit": k_stars})

                raw_data = {
                    "type": "queens",
                    "style": f"{k_stars}-Star / Queens",
                    "difficulty": difficulty,
                    "grid_size": n,
                    "stars_per_unit": k_stars,
                    "regions": regions,
                    "stars_solution": list(stars),
                    "text": ascii_text,
                }

                return BasePuzzleResult(
                    puzzle_type=self.puzzle_id,
                    title=self.title,
                    difficulty=difficulty,
                    instruction=instruction,
                    raw_data=raw_data,
                )

        raise RuntimeError(f"Failed to generate valid Queens puzzle ({difficulty}) after 50 attempts")

    def get_instruction(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        q_diff = str(puzzle_data.get("difficulty", "medium"))
        stars_num = 2 if q_diff.lower() in ("hard", "master", "extreme") or puzzle_data.get("stars_per_unit", 1) > 1 else 1
        star_str = "2 stars" if stars_num > 1 else "1 star"
        return f"Place {star_str} in each row, column, and region with no stars touching, even diagonally."

    def format_ascii_puzzle(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        regions = puzzle_data.get("regions", [])
        n = puzzle_data.get("grid_size", len(regions))
        lines = []
        lines.append("+" + "---+" * n)
        for r in range(n):
            row_str = "|"
            for c in range(n):
                reg = regions[r][c] if r < len(regions) and c < len(regions[r]) else 0
                reg_char = chr(ord('A') + (reg % 26))
                right_reg = regions[r][c+1] if c + 1 < n else -1
                sep = "|" if right_reg != reg else " "
                row_str += f" {reg_char} {sep}"
            lines.append(row_str)

            bot_str = "+"
            for c in range(n):
                reg = regions[r][c] if r < len(regions) and c < len(regions[r]) else 0
                bot_reg = regions[r+1][c] if r + 1 < n else -1
                sep = "---+" if bot_reg != reg else "   +"
                bot_str += sep
            lines.append(bot_str)
        return "\n".join(lines)

    def format_solution_key(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> List[str]:
        stars = puzzle_data.get("stars_solution") or puzzle_data.get("queens") or puzzle_data.get("stars") or []
        if not stars:
            return []
        size = puzzle_data.get("grid_size") or puzzle_data.get("size")
        if not size:
            regions = puzzle_data.get("regions", [])
            if regions:
                size = len(regions)
            else:
                coords = []
                for s in stars:
                    if isinstance(s, (list, tuple)) and len(s) >= 2:
                        coords.extend([s[0], s[1]])
                    elif isinstance(s, dict) and "r" in s and "c" in s:
                        coords.extend([s["r"], s["c"]])
                size = max(coords) + 1 if coords else 8

        star_set = set()
        for s in stars:
            if isinstance(s, (list, tuple)) and len(s) >= 2:
                star_set.add((s[0], s[1]))
            elif isinstance(s, dict) and "r" in s and "c" in s:
                star_set.add((s["r"], s["c"]))

        lines = []
        for r in range(size):
            row_str = "      "
            for c in range(size):
                if (r, c) in star_set:
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
        size = puzzle_data.get("grid_size", puzzle_data.get("size", 8))
        regions = puzzle_data.get("regions", [])

        padding = 24
        board_size = target_width - padding * 2
        cell_size = board_size // size
        total_h = padding + cell_size * size + padding
        tb = ThermalBitmap(target_width, total_h)

        for r in range(size):
            for c in range(size):
                reg = regions[r][c] if r < len(regions) and c < len(regions[r]) else 0
                x0 = padding + c * cell_size
                y0 = padding + r * cell_size
                tb.fill_hatch(x0, y0, cell_size, cell_size, reg)

        for r in range(size):
            for c in range(size):
                reg = regions[r][c] if r < len(regions) and c < len(regions[r]) else 0
                x0 = padding + c * cell_size
                y0 = padding + r * cell_size
                is_bottom = (r == size - 1) or (r + 1 < len(regions) and regions[r + 1][c] != reg)
                tb.draw_hline(x0, y0 + cell_size, cell_size, thickness=4 if is_bottom else 1)
                is_right = (c == size - 1) or (c + 1 < len(regions[r]) and regions[r][c + 1] != reg)
                tb.draw_vline(x0 + cell_size, y0, cell_size, thickness=4 if is_right else 1)

        tb.draw_rect(padding, padding, cell_size * size, cell_size * size, thickness=5)
        return tb.to_escpos()

    # --- Internal Generation & Validation Helpers ---
    def _place_stars(self, n: int, k_stars: int, max_attempts: int = 200) -> Set[Tuple[int, int]]:
        for _ in range(max_attempts):
            stars: Set[Tuple[int, int]] = set()
            col_counts = [0] * n

            def can_place(r: int, c: int) -> bool:
                if col_counts[c] >= k_stars:
                    return False
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
        grid = [[-1] * n for _ in range(n)]
        frontiers: List[List[Tuple[int, int]]] = [[] for _ in range(n)]
        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        if k_stars == 1:
            for idx, (r, c) in enumerate(stars):
                grid[r][c] = idx
                frontiers[idx].append((r, c))
        else:
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

        unassigned = sum(row.count(-1) for row in grid)
        active_regions = list(range(n))

        while unassigned > 0 and active_regions:
            random.shuffle(active_regions)
            progress = False

            for reg_id in list(active_regions):
                frontier = frontiers[reg_id]
                expanded = False

                shuffled_frontier = list(frontier)
                random.shuffle(shuffled_frontier)

                for r, c in shuffled_frontier:
                    random_dirs = list(dirs)
                    random.shuffle(random_dirs)
                    for dr, dc in random_dirs:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == -1:
                            grid[nr][nc] = reg_id
                            frontier.append((nr, nc))
                            unassigned -= 1
                            expanded = True
                            progress = True
                            break
                    if expanded:
                        break

                frontiers[reg_id] = [
                    (r, c) for r, c in frontier
                    if any(0 <= r + dr < n and 0 <= c + dc < n and grid[r + dr][c + dc] == -1 for dr, dc in dirs)
                ]
                if not frontiers[reg_id]:
                    active_regions.remove(reg_id)

            if not progress:
                break

        if unassigned > 0:
            for r in range(n):
                for c in range(n):
                    if grid[r][c] == -1:
                        for dr, dc in dirs:
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] != -1:
                                grid[r][c] = grid[nr][nc]
                                break

        return grid

    def _validate_puzzle(self, regions: List[List[int]], stars: Set[Tuple[int, int]], n: int, k_stars: int) -> bool:
        region_star_counts = [0] * n
        for r, c in stars:
            reg = regions[r][c]
            if reg < 0 or reg >= n:
                return False
            region_star_counts[reg] += 1

        if any(cnt != k_stars for cnt in region_star_counts):
            return False

        for reg_id in range(n):
            cells = [(r, c) for r in range(n) for c in range(n) if regions[r][c] == reg_id]
            if not cells:
                return False
            visited = set()
            queue = [cells[0]]
            visited.add(cells[0])
            while queue:
                cr, cc = queue.pop(0)
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = cr + dr, cc + dc
                    if (nr, nc) in cells and (nr, nc) not in visited:
                        visited.add((nr, nc))
                        queue.append((nr, nc))
            if len(visited) != len(cells):
                return False

        return True

    def verify_accuracy(
        self,
        puzzle_data: Union[BasePuzzleResult, Dict[str, Any]],
    ) -> Tuple[bool, str]:
        regions = puzzle_data.get("regions")
        stars = puzzle_data.get("stars_solution") or puzzle_data.get("queens") or puzzle_data.get("stars")
        if not regions or not isinstance(regions, list):
            return False, "Stars puzzle missing regions grid"
        n = puzzle_data.get("grid_size", len(regions))
        if len(regions) != n or any(len(row) != n for row in regions):
            return False, f"Stars regions grid dimensions mismatch size {n}x{n}"
        if not stars or not isinstance(stars, (list, set)):
            return False, "Stars puzzle missing stars solution"

        star_set = set(tuple(p) for p in stars)
        k_stars = puzzle_data.get("stars_per_unit", 1)

        # 1. Total star count
        expected_total = n * k_stars
        if len(star_set) != expected_total:
            return False, f"Stars count ({len(star_set)}) does not equal expected {expected_total} ({n}x{k_stars})"

        # 2. Check each row and col has exactly k_stars
        for r in range(n):
            row_count = sum(1 for (sr, sc) in star_set if sr == r)
            if row_count != k_stars:
                return False, f"Stars row {r} has {row_count} stars, expected {k_stars}"
        for c in range(n):
            col_count = sum(1 for (sr, sc) in star_set if sc == c)
            if col_count != k_stars:
                return False, f"Stars col {c} has {col_count} stars, expected {k_stars}"

        # 3. Check no two stars touch (even diagonally)
        star_list = list(star_set)
        for i in range(len(star_list)):
            r1, c1 = star_list[i]
            for j in range(i + 1, len(star_list)):
                r2, c2 = star_list[j]
                if max(abs(r1 - r2), abs(c1 - c2)) <= 1:
                    return False, f"Stars at ({r1},{c1}) and ({r2},{c2}) touch orthogonally or diagonally"

        # 4. Check regions and validate connectivity & region star counts
        if not self._validate_puzzle(regions, star_set, n, k_stars):
            return False, "Stars puzzle regions fail connectivity or region star count validation"

        return True, "All rules satisfied"
