"""
Tents (Tents and Trees) Generator and Solver
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
from typing import List, Tuple, Optional, Dict, Any, Set


class TentsGenerator:
    """
    Procedural generator and solver for Tents & Trees (Simon Tatham tents.c).
    Guarantees unique solution with 1:1 tree-tent matching and non-touching tents.
    """

    DIFFICULTY_SETTINGS = {
        "easy": {"size": 6, "tents": 4},
        "medium": {"size": 8, "tents": 8},
        "hard": {"size": 8, "tents": 11},
    }

    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)

    def _ortho_neighbors(self, r: int, c: int, size: int) -> List[Tuple[int, int]]:
        res = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < size and 0 <= nc < size:
                res.append((nr, nc))
        return res

    def _all_neighbors(self, r: int, c: int, size: int) -> List[Tuple[int, int]]:
        res = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < size and 0 <= nc < size:
                    res.append((nr, nc))
        return res

    def count_solutions(
        self,
        size: int,
        trees: List[Tuple[int, int]],
        row_counts: List[int],
        col_counts: List[int],
        max_count: int = 2
    ) -> int:
        """
        Backtracking solver to count solutions. Stops when solutions >= max_count.
        Enforces:
        - Tents in row r == row_counts[r]
        - Tents in col c == col_counts[c]
        - No two tents touch orthogonally or diagonally
        - Tents are a subset of cells orthogonally adjacent to at least one tree
        - There exists a valid 1:1 matching between placed tents and trees
        """
        tree_set = set(trees)
        num_trees = len(trees)

        # Potential tent cells must be adjacent to at least one tree and not be a tree itself
        tent_candidates: Set[Tuple[int, int]] = set()
        tree_adj: Dict[Tuple[int, int], List[Tuple[int, int]]] = {}
        for tr, tc in trees:
            adj = [p for p in self._ortho_neighbors(tr, tc, size) if p not in tree_set]
            tree_adj[(tr, tc)] = adj
            tent_candidates.update(adj)

        cand_list = sorted(list(tent_candidates))
        row_rem = list(row_counts)
        col_rem = list(col_counts)

        # Quick check: row sum == col sum == num_trees
        if sum(row_counts) != num_trees or sum(col_counts) != num_trees:
            return 0

        # Backtracking placement
        placed_tents: Set[Tuple[int, int]] = set()
        solutions_found = 0

        def can_place(r: int, c: int) -> bool:
            if row_rem[r] <= 0 or col_rem[c] <= 0:
                return False
            for nr, nc in self._all_neighbors(r, c, size):
                if (nr, nc) in placed_tents:
                    return False
            return True

        # Bipartite matching helper (Hopcroft-Karp / DFS)
        def has_valid_matching(tent_set: Set[Tuple[int, int]]) -> bool:
            if len(tent_set) != num_trees:
                return False
            tent_l = list(tent_set)
            t_adj: List[List[int]] = []
            for tr, tc in trees:
                t_adj.append([i for i, tp in enumerate(tent_l) if tp in tree_adj[(tr, tc)]])

            match: Dict[int, int] = {}
            for u in range(num_trees):
                vis: Set[int] = set()

                def dfs(node: int) -> bool:
                    for v in t_adj[node]:
                        if v not in vis:
                            vis.add(v)
                            if v not in match or dfs(match[v]):
                                match[v] = node
                                return True
                    return False

                if not dfs(u):
                    return False
            return len(match) == num_trees

        def search(idx: int, needed: int):
            nonlocal solutions_found
            if solutions_found >= max_count:
                return

            if needed == 0:
                if all(rem == 0 for rem in row_rem) and all(rem == 0 for rem in col_rem):
                    if has_valid_matching(placed_tents):
                        solutions_found += 1
                return

            if idx >= len(cand_list):
                return

            # Prune if remaining candidate cells in any row/col cannot fulfill remaining counts
            rem_cands = len(cand_list) - idx
            if rem_cands < needed:
                return

            r, c = cand_list[idx]

            # Try placing a tent at (r, c)
            if can_place(r, c):
                placed_tents.add((r, c))
                row_rem[r] -= 1
                col_rem[c] -= 1

                search(idx + 1, needed - 1)

                placed_tents.remove((r, c))
                row_rem[r] += 1
                col_rem[c] += 1

            # Try not placing a tent at (r, c)
            search(idx + 1, needed)

        search(0, num_trees)
        return solutions_found

    def generate(self, difficulty: str = "medium") -> Dict[str, Any]:
        diff_key = difficulty.lower()
        if diff_key not in self.DIFFICULTY_SETTINGS:
            diff_key = "medium"

        settings = self.DIFFICULTY_SETTINGS[diff_key]
        size = settings["size"]
        target_tents = settings["tents"]

        max_attempts = 150
        for _ in range(max_attempts):
            # 1. Place target_tents non-touching tents
            all_cells = [(r, c) for r in range(size) for c in range(size)]
            random.shuffle(all_cells)

            tent_positions: List[Tuple[int, int]] = []
            occupied_tent_influence: Set[Tuple[int, int]] = set()

            for r, c in all_cells:
                if len(tent_positions) >= target_tents:
                    break
                if (r, c) not in occupied_tent_influence:
                    tent_positions.append((r, c))
                    occupied_tent_influence.add((r, c))
                    for nr, nc in self._all_neighbors(r, c, size):
                        occupied_tent_influence.add((nr, nc))

            if len(tent_positions) < target_tents:
                continue

            # 2. For each tent, pick an orthogonal neighbor for its tree
            tree_positions: List[Tuple[int, int]] = []
            used_cells = set(tent_positions)
            success = True

            tent_set = set(tent_positions)
            for tr, tc in tent_positions:
                adj = [p for p in self._ortho_neighbors(tr, tc, size) if p not in used_cells and p not in tent_set]
                if not adj:
                    success = False
                    break
                tree_choice = random.choice(adj)
                tree_positions.append(tree_choice)
                used_cells.add(tree_choice)

            if not success or len(tree_positions) != target_tents:
                continue

            # 3. Compute row and column clue numbers
            row_counts = [0] * size
            col_counts = [0] * size
            for tr, tc in tent_positions:
                row_counts[tr] += 1
                col_counts[tc] += 1

            # 4. Verify uniqueness
            sol_count = self.count_solutions(size, tree_positions, row_counts, col_counts, max_count=2)
            if sol_count == 1:
                # Format output
                puzzle_grid = [[0] * size for _ in range(size)]
                for tr, tc in tree_positions:
                    puzzle_grid[tr][tc] = 1  # 1 = Tree

                solution_grid = [[0] * size for _ in range(size)]
                for tr, tc in tree_positions:
                    solution_grid[tr][tc] = 1  # 1 = Tree
                for tr, tc in tent_positions:
                    solution_grid[tr][tc] = 2  # 2 = Tent

                return {
                    "title": "TENTS",
                    "difficulty": diff_key.upper(),
                    "size": size,
                    "rows": size,
                    "cols": size,
                    "row_clues": row_counts,
                    "col_clues": col_counts,
                    "trees": [list(p) for p in sorted(tree_positions)],
                    "tents": [list(p) for p in sorted(tent_positions)],
                    "tree_count": len(tree_positions),
                    "puzzle": puzzle_grid,
                    "solution": solution_grid,
                    "text": self.format_ascii({
                        "size": size,
                        "row_clues": row_counts,
                        "col_clues": col_counts,
                        "puzzle": puzzle_grid
                    })
                }

        raise RuntimeError(f"Failed to generate unique Tents puzzle for {difficulty} in {max_attempts} attempts")

    def format_ascii(self, puzzle_data: Dict[str, Any]) -> str:
        size = puzzle_data["size"]
        row_clues = puzzle_data["row_clues"]
        col_clues = puzzle_data["col_clues"]
        grid = puzzle_data["puzzle"]

        lines = []
        # Column clues header
        col_header = "       " + " ".join(str(c) for c in col_clues)
        lines.append(col_header)
        sep = "     +" + "--" * size + "+"
        lines.append(sep)

        for r in range(size):
            row_str = f"   {row_clues[r]} |"
            for c in range(size):
                cell = grid[r][c]
                if cell == 1:
                    row_str += " T"
                else:
                    row_str += " ."
            row_str += " |"
            lines.append(row_str)

        lines.append(sep)
        return "\n".join(lines)
