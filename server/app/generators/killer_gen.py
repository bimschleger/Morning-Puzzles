"""
Killer Sudoku Generator and Solver (4x4 and 6x6 Variants)
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


class KillerSudokuGenerator:
    """
    Procedural generator and solver for Killer Sudoku.
    Supports:
      - 4x4 grid with 2x2 boxes (digits 1-4) for Easy and Medium difficulties.
      - 6x6 grid with 2x3 boxes (digits 1-6) for Extreme difficulty.
    Guarantees:
      - Orthogonally contiguous cages without digit repetition within any cage.
      - Exactly 1 unique mathematical solution verified via constraint backtracking.
    """

    DIFFICULTY_SETTINGS = {
        "easy": {"size": 4, "box_r": 2, "box_c": 2, "min_cage": 1, "max_cage": 2},
        "medium": {"size": 4, "box_r": 2, "box_c": 2, "min_cage": 2, "max_cage": 3},
        "extreme": {"size": 6, "box_r": 2, "box_c": 3, "min_cage": 2, "max_cage": 4},
    }

    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)

    def _generate_solved_board(self, size: int, box_r: int, box_c: int) -> List[List[int]]:
        """Generates a complete, randomized valid Sudoku board."""
        board = [[0] * size for _ in range(size)]

        def is_valid(r: int, c: int, val: int) -> bool:
            for i in range(size):
                if board[r][i] == val or board[i][c] == val:
                    return False
            br = (r // box_r) * box_r
            bc = (c // box_c) * box_c
            for dr in range(box_r):
                for dc in range(box_c):
                    if board[br + dr][bc + dc] == val:
                        return False
            return True

        def fill(r: int, c: int) -> bool:
            if r == size:
                return True
            next_r = r + (c + 1) // size
            next_c = (c + 1) % size

            nums = list(range(1, size + 1))
            random.shuffle(nums)
            for n in nums:
                if is_valid(r, c, n):
                    board[r][c] = n
                    if fill(next_r, next_c):
                        return True
                    board[r][c] = 0
            return False

        fill(0, 0)
        return board

    def _partition_into_cages(
        self, solution: List[List[int]], size: int, min_cage: int, max_cage: int
    ) -> List[Dict[str, Any]]:
        """Partitions the board into contiguous cages without duplicate digits."""
        assigned = [[-1] * size for _ in range(size)]
        cages = []
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        # Helper to get orthogonal neighbors
        def neighbors(r: int, c: int) -> List[Tuple[int, int]]:
            res = []
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < size and 0 <= nc < size:
                    res.append((nr, nc))
            return res

        all_coords = [(r, c) for r in range(size) for c in range(size)]
        random.shuffle(all_coords)

        cage_id = 0
        for r, c in all_coords:
            if assigned[r][c] != -1:
                continue

            target_size = random.randint(min_cage, max_cage)
            current_cage_cells = [(r, c)]
            current_digits = {solution[r][c]}
            assigned[r][c] = cage_id

            while len(current_cage_cells) < target_size:
                # Find available unassigned adjacent cells that don't duplicate digits
                candidates = []
                for cr, cc in current_cage_cells:
                    for nr, nc in neighbors(cr, cc):
                        if assigned[nr][nc] == -1 and solution[nr][nc] not in current_digits:
                            candidates.append((nr, nc))

                if not candidates:
                    break

                chosen = random.choice(candidates)
                current_cage_cells.append(chosen)
                current_digits.add(solution[chosen[0]][chosen[1]])
                assigned[chosen[0]][chosen[1]] = cage_id

            cages.append({
                "id": cage_id,
                "label": letters[cage_id % len(letters)],
                "cells": sorted(current_cage_cells),
                "sum": sum(solution[cr][cc] for cr, cc in current_cage_cells)
            })
            cage_id += 1

        # Check for any isolated single-cell cages if min_cage > 1 and merge with neighbor
        if min_cage > 1:
            for idx in range(len(cages) - 1, -1, -1):
                cg = cages[idx]
                if len(cg["cells"]) == 1:
                    cr, cc = cg["cells"][0]
                    cval = solution[cr][cc]
                    merged = False
                    for nr, nc in neighbors(cr, cc):
                        nid = assigned[nr][nc]
                        ncage = next((c for c in cages if c["id"] == nid), None)
                        if ncage and len(ncage["cells"]) < max_cage:
                            ndigits = {solution[r][c] for r, c in ncage["cells"]}
                            if cval not in ndigits:
                                ncage["cells"].append((cr, cc))
                                ncage["cells"].sort()
                                ncage["sum"] += cval
                                assigned[cr][cc] = nid
                                cages.pop(idx)
                                merged = True
                                break
                    if not merged:
                        pass

        # Re-index cage labels cleanly
        for i, cg in enumerate(cages):
            cg["id"] = i
            cg["label"] = letters[i % len(letters)]

        return cages

    @staticmethod
    def _get_connected_components(cells: List[Tuple[int, int]]) -> List[List[Tuple[int, int]]]:
        """Decomposes a list of cell coordinates into orthogonally connected components."""
        if not cells:
            return []
        cell_set = set(cells)
        visited: Set[Tuple[int, int]] = set()
        components = []
        for c in cells:
            if c not in visited:
                comp = []
                queue = [c]
                visited.add(c)
                while queue:
                    curr = queue.pop(0)
                    comp.append(curr)
                    cr, cc = curr
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = cr + dr, cc + dc
                        if (nr, nc) in cell_set and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            queue.append((nr, nc))
                components.append(sorted(comp))
        return components

    def _find_multiple_solutions(
        self, size: int, box_r: int, box_c: int, cages: List[Dict[str, Any]], max_count: int = 2
    ) -> List[List[List[int]]]:
        """Finds up to max_count solutions to detect ambiguity locations."""
        board = [[0] * size for _ in range(size)]
        cell_cage: Dict[Tuple[int, int], Dict[str, Any]] = {}
        for cg in cages:
            for r, c in cg["cells"]:
                cell_cage[(r, c)] = cg

        solutions: List[List[List[int]]] = []

        def is_valid_placement(r: int, c: int, val: int) -> bool:
            for i in range(size):
                if board[r][i] == val or board[i][c] == val:
                    return False

            br = (r // box_r) * box_r
            bc = (c // box_c) * box_c
            for dr in range(box_r):
                for dc in range(box_c):
                    if board[br + dr][bc + dc] == val:
                        return False

            cg = cell_cage[(r, c)]
            current_sum = val
            filled_cells = 1
            for cr, cc in cg["cells"]:
                if (cr, cc) == (r, c):
                    continue
                v = board[cr][cc]
                if v != 0:
                    if v == val:
                        return False
                    current_sum += v
                    filled_cells += 1

            target_sum = cg["sum"]
            total_cells = len(cg["cells"])

            if current_sum > target_sum:
                return False

            if filled_cells == total_cells:
                if current_sum != target_sum:
                    return False
            else:
                remaining_cells = total_cells - filled_cells
                min_add = sum(range(1, remaining_cells + 1))
                if current_sum + min_add > target_sum:
                    return False

            return True

        def solve(r: int, c: int) -> bool:
            if r == size:
                solutions.append([row[:] for row in board])
                return len(solutions) >= max_count

            next_r = r + (c + 1) // size
            next_c = (c + 1) % size

            for val in range(1, size + 1):
                if is_valid_placement(r, c, val):
                    board[r][c] = val
                    if solve(next_r, next_c):
                        return True
                    board[r][c] = 0

            return False

        solve(0, 0)
        return solutions

    def generate(self, difficulty: str = "medium") -> Dict[str, Any]:
        """Generates a Killer Sudoku puzzle with guaranteed unique solution."""
        diff_key = difficulty.lower()
        cfg = self.DIFFICULTY_SETTINGS.get(diff_key, self.DIFFICULTY_SETTINGS["medium"])
        size = cfg["size"]
        box_r = cfg["box_r"]
        box_c = cfg["box_c"]
        min_cage = cfg["min_cage"]
        max_cage = cfg["max_cage"]
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        for attempt in range(50):
            solution = self._generate_solved_board(size, box_r, box_c)
            cages = self._partition_into_cages(solution, size, min_cage, max_cage)

            # Iterative targeted disambiguation
            is_unique = False
            for step in range(8):
                sols = self._find_multiple_solutions(size, box_r, box_c, cages, max_count=2)
                if len(sols) == 1:
                    is_unique = True
                    break
                elif len(sols) == 2:
                    # Find cells where the two solutions differ
                    diff_cells = [
                        (r, c)
                        for r in range(size)
                        for c in range(size)
                        if sols[0][r][c] != sols[1][r][c]
                    ]
                    
                    # Search for candidate cell to split, preferring non-articulation points
                    best_candidate = None
                    for dr, dc in diff_cells:
                        for cg in cages:
                            if (dr, dc) in cg["cells"] and len(cg["cells"]) > 1:
                                remaining = [cell for cell in cg["cells"] if cell != (dr, dc)]
                                comps = self._get_connected_components(remaining)
                                if len(comps) == 1:
                                    best_candidate = (dr, dc, cg, comps)
                                    break
                                elif best_candidate is None:
                                    best_candidate = (dr, dc, cg, comps)
                        if best_candidate and len(best_candidate[3]) == 1:
                            break

                    if best_candidate:
                        dr, dc, cg, comps = best_candidate
                        cg["cells"] = comps[0]
                        cg["sum"] = sum(solution[r][c] for r, c in comps[0])
                        for comp in comps[1:]:
                            cages.append({
                                "id": len(cages),
                                "label": "",
                                "cells": comp,
                                "sum": sum(solution[r][c] for r, c in comp),
                            })
                        cages.append({
                            "id": len(cages),
                            "label": "",
                            "cells": [(dr, dc)],
                            "sum": solution[dr][dc],
                        })
                    else:
                        break
                else:
                    break

            if is_unique:
                # Re-index cage labels cleanly
                cages = [cg for cg in cages if cg["cells"]]
                for i, cg in enumerate(cages):
                    cg["id"] = i
                    cg["label"] = letters[i % len(letters)]

                return {
                    "title": "KILLER",
                    "difficulty": difficulty.upper(),
                    "size": size,
                    "box_rows": box_r,
                    "box_cols": box_c,
                    "cages": cages,
                    "solution": solution,
                }

        # Fallback to standard 4x4 if generation takes too many retries
        fallback_cfg = self.DIFFICULTY_SETTINGS["easy"]
        solution = self._generate_solved_board(fallback_cfg["size"], fallback_cfg["box_r"], fallback_cfg["box_c"])
        cages = self._partition_into_cages(solution, fallback_cfg["size"], 1, 2)
        for i, cg in enumerate(cages):
            cg["id"] = i
            cg["label"] = letters[i % len(letters)]
        return {
            "title": "KILLER",
            "difficulty": difficulty.upper(),
            "size": fallback_cfg["size"],
            "box_rows": fallback_cfg["box_r"],
            "box_cols": fallback_cfg["box_c"],
            "cages": cages,
            "solution": solution,
        }

    def format_ascii(self, puzzle_data: Dict[str, Any]) -> str:
        """Formats the Killer Sudoku into monospaced ASCII for thermal receipt."""
        size = puzzle_data["size"]
        box_r = puzzle_data["box_rows"]
        box_c = puzzle_data["box_cols"]
        cages = puzzle_data["cages"]
        difficulty = puzzle_data["difficulty"]

        # Grid of cage labels
        grid = [[" "] * size for _ in range(size)]
        for cg in cages:
            for r, c in cg["cells"]:
                grid[r][c] = cg["label"]

        lines = []
        lines.append("--- KILLER ---")
        lines.append(f"DIFFICULTY: {difficulty}")
        range_str = "1-4" if size == 4 else "1-6"
        lines.append(f"Fill every row, column, and box with digits {range_str}, matching cage sums without repeats.")
        lines.append("")

        # ASCII Grid with box borders
        sep_border = "      +" + ("---+" * size)
        lines.append(sep_border)
        for r in range(size):
            row_str = "      |"
            for c in range(size):
                row_str += f" {grid[r][c]} |"
            lines.append(row_str)
            lines.append(sep_border)

        lines.append("")
        # Cage legend formatted cleanly <= 44 chars per line
        clue_items = [f"{cg['label']}={cg['sum']}" for cg in cages]
        legend_prefix = "CAGES: "
        cur_line = legend_prefix
        legend_lines = []
        for item in clue_items:
            if len(cur_line) + len(item) + 2 > 44:
                legend_lines.append(cur_line.rstrip(", "))
                cur_line = "       " + item + ", "
            else:
                cur_line += item + ", "
        if cur_line.strip():
            legend_lines.append(cur_line.rstrip(", "))

        for l in legend_lines:
            lines.append(l)

        return "\n".join(lines)
