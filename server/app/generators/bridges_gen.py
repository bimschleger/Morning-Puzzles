"""
Bridges (Hashiwokakero) Generator and Solver
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


class BridgesGenerator:
    """
    Procedural generator and solver for Bridges / Hashiwokakero (Simon Tatham bridges.c).
    Guarantees a fully connected network, no crossing bridges, and exactly one unique solution.
    """

    DIFFICULTY_SETTINGS = {
        "easy": {"size": 6, "islands": 6, "max_degree": 4},
        "medium": {"size": 8, "islands": 10, "max_degree": 6},
        "hard": {"size": 8, "islands": 14, "max_degree": 8},
    }

    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)

    def _find_potential_edges(self, islands: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        Finds all pairs of islands (i, j) that are aligned horizontally or vertically
        with no other island between them.
        """
        edges = []
        n = len(islands)
        for i in range(n):
            r1, c1 = islands[i]
            for j in range(i + 1, n):
                r2, c2 = islands[j]
                if r1 == r2:
                    # Horizontal alignment: check no island between
                    c_min, c_max = min(c1, c2), max(c1, c2)
                    blocked = False
                    for k in range(n):
                        if k != i and k != j:
                            rk, ck = islands[k]
                            if rk == r1 and c_min < ck < c_max:
                                blocked = True
                                break
                    if not blocked:
                        edges.append((i, j))
                elif c1 == c2:
                    # Vertical alignment: check no island between
                    r_min, r_max = min(r1, r2), max(r1, r2)
                    blocked = False
                    for k in range(n):
                        if k != i and k != j:
                            rk, ck = islands[k]
                            if ck == c1 and r_min < rk < r_max:
                                blocked = True
                                break
                    if not blocked:
                        edges.append((i, j))
        return edges

    def _edges_cross(
        self,
        e1: Tuple[int, int],
        e2: Tuple[int, int],
        islands: List[Tuple[int, int]]
    ) -> bool:
        """Determines if two edges strictly cross each other."""
        i1, j1 = e1
        i2, j2 = e2
        r1a, c1a = islands[i1]
        r1b, c1b = islands[j1]
        r2a, c2a = islands[i2]
        r2b, c2b = islands[j2]

        is_e1_horiz = (r1a == r1b)
        is_e2_horiz = (r2a == r2b)

        if is_e1_horiz == is_e2_horiz:
            return False  # Parallel lines cannot cross if unobstructed

        if is_e1_horiz:
            h_r = r1a
            h_c_min, h_c_max = min(c1a, c1b), max(c1a, c1b)
            v_c = c2a
            v_r_min, v_r_max = min(r2a, r2b), max(r2a, r2b)
        else:
            h_r = r2a
            h_c_min, h_c_max = min(c2a, c2b), max(c2a, c2b)
            v_c = c1a
            v_r_min, v_r_max = min(r1a, r1b), max(r1a, r1b)

        # Cross if horizontal row is strictly between vertical bounds AND
        # vertical col is strictly between horizontal bounds
        return (v_r_min < h_r < v_r_max) and (h_c_min < v_c < h_c_max)

    def count_solutions(
        self,
        islands: List[Tuple[int, int]],
        degrees: List[int],
        potential_edges: List[Tuple[int, int]],
        max_solutions: int = 2
    ) -> int:
        """
        Backtracking solver to count valid bridge assignments (0, 1, or 2 per edge).
        Enforces:
        - Sum of incident bridges == degrees[i]
        - No crossing bridges with count > 0
        - Full connectivity of all islands
        """
        num_islands = len(islands)
        num_edges = len(potential_edges)

        # Precompute crossing conflicts
        conflicts = [[] for _ in range(num_edges)]
        for e_idx1 in range(num_edges):
            for e_idx2 in range(e_idx1 + 1, num_edges):
                if self._edges_cross(potential_edges[e_idx1], potential_edges[e_idx2], islands):
                    conflicts[e_idx1].append(e_idx2)
                    conflicts[e_idx2].append(e_idx1)

        # Map islands to incident edges
        island_edges = [[] for _ in range(num_islands)]
        for e_idx, (u, v) in enumerate(potential_edges):
            island_edges[u].append((e_idx, v))
            island_edges[v].append((e_idx, u))

        edge_val = [0] * num_edges
        island_rem = list(degrees)
        solutions_count = 0

        # Quick check: total degree must be even
        if sum(degrees) % 2 != 0:
            return 0

        def check_connectivity() -> bool:
            adj = [[] for _ in range(num_islands)]
            for e_idx, (u, v) in enumerate(potential_edges):
                if edge_val[e_idx] > 0:
                    adj[u].append(v)
                    adj[v].append(u)

            vis = [False] * num_islands
            q = [0]
            vis[0] = True
            head = 0
            while head < len(q):
                curr = q[head]
                head += 1
                for nxt in adj[curr]:
                    if not vis[nxt]:
                        vis[nxt] = True
                        q.append(nxt)
            return len(q) == num_islands

        def search(e_idx: int):
            nonlocal solutions_count
            if solutions_count >= max_solutions:
                return

            if e_idx == num_edges:
                if all(rem == 0 for rem in island_rem):
                    if check_connectivity():
                        solutions_count += 1
                return

            u, v = potential_edges[e_idx]

            # Try values 0, 1, 2
            max_allowed = min(2, island_rem[u], island_rem[v])

            # Check crossing conflicts
            has_conflict = False
            for c_edge in conflicts[e_idx]:
                if c_edge < e_idx and edge_val[c_edge] > 0:
                    has_conflict = True
                    break

            if has_conflict:
                max_allowed = 0

            # Prune if remaining capacity of any island is too large to be satisfied by remaining edges
            for val in range(max_allowed, -1, -1):
                edge_val[e_idx] = val
                island_rem[u] -= val
                island_rem[v] -= val

                # Check feasibility of u and v if this is their last edge
                feasible = True
                # Quick check: remaining capacity cannot be negative
                if island_rem[u] < 0 or island_rem[v] < 0:
                    feasible = False

                if feasible:
                    search(e_idx + 1)

                island_rem[u] += val
                island_rem[v] += val
                edge_val[e_idx] = 0

        search(0)
        return solutions_count

    def generate(self, difficulty: str = "medium") -> Dict[str, Any]:
        diff_key = difficulty.lower()
        if diff_key not in self.DIFFICULTY_SETTINGS:
            diff_key = "medium"

        settings = self.DIFFICULTY_SETTINGS[diff_key]
        size = settings["size"]
        target_islands = settings["islands"]
        max_degree = settings["max_degree"]

        max_attempts = 120
        for _ in range(max_attempts):
            # 1. Place target_islands on the grid with at least 1 empty space between them
            all_cells = [(r, c) for r in range(size) for c in range(size)]
            random.shuffle(all_cells)

            islands: List[Tuple[int, int]] = []
            for r, c in all_cells:
                if len(islands) >= target_islands:
                    break
                # Keep islands at least 1 cell apart
                too_close = False
                for ir, ic in islands:
                    if abs(ir - r) <= 0 and abs(ic - c) <= 0:
                        too_close = True
                        break
                if not too_close:
                    islands.append((r, c))

            if len(islands) < target_islands:
                continue

            islands.sort()

            # 2. Find potential unobstructed orthogonal edges
            edges = self._find_potential_edges(islands)
            if len(edges) < target_islands - 1:
                continue

            # 3. Build a spanning tree to guarantee connectivity
            random.shuffle(edges)
            tree_edges: List[Tuple[int, int]] = []
            parent = list(range(len(islands)))

            def find(p):
                if parent[p] != p:
                    parent[p] = find(parent[p])
                return parent[p]

            def union(p1, p2):
                r1, r2 = find(p1), find(p2)
                if r1 != r2:
                    parent[r1] = r2
                    return True
                return False

            edge_bridge_count: Dict[Tuple[int, int], int] = {}
            # Try to form a spanning tree without crossings
            for e in edges:
                u, v = e
                # Check if e crosses any chosen tree edge
                crosses = False
                for te in tree_edges:
                    if self._edges_cross(e, te, islands):
                        crosses = True
                        break
                if not crosses and union(u, v):
                    tree_edges.append(e)
                    edge_bridge_count[e] = 1

            # Check if all islands are connected
            root = find(0)
            if any(find(i) != root for i in range(len(islands))):
                continue

            # 4. Add extra bridges (single or double) to non-crossing edges
            island_degrees = [0] * len(islands)
            for (u, v), cnt in edge_bridge_count.items():
                island_degrees[u] += cnt
                island_degrees[v] += cnt

            # Randomly double some tree edges
            for e in tree_edges:
                u, v = e
                if island_degrees[u] < max_degree and island_degrees[v] < max_degree:
                    if random.random() < 0.4:
                        edge_bridge_count[e] += 1
                        island_degrees[u] += 1
                        island_degrees[v] += 1

            # Randomly add non-tree edges if they don't cross
            for e in edges:
                if e not in edge_bridge_count:
                    u, v = e
                    crosses = any(self._edges_cross(e, te, islands) for te in edge_bridge_count)
                    if not crosses:
                        if island_degrees[u] + 1 <= max_degree and island_degrees[v] + 1 <= max_degree:
                            if random.random() < 0.35:
                                added = 2 if (random.random() < 0.3 and island_degrees[u] + 2 <= max_degree and island_degrees[v] + 2 <= max_degree) else 1
                                edge_bridge_count[e] = added
                                island_degrees[u] += added
                                island_degrees[v] += added

            # Final degree array
            degrees = [0] * len(islands)
            for (u, v), cnt in edge_bridge_count.items():
                degrees[u] += cnt
                degrees[v] += cnt

            # Ensure every island has at least 1 bridge and at most max_degree
            if any(d == 0 or d > max_degree for d in degrees):
                continue

            # 5. Verify uniqueness
            active_potential_edges = self._find_potential_edges(islands)
            sol_count = self.count_solutions(islands, degrees, active_potential_edges, max_solutions=2)

            if sol_count == 1:
                # Build formatted solution and puzzle data
                islands_data = []
                for idx, (r, c) in enumerate(islands):
                    islands_data.append({"r": r, "c": c, "count": degrees[idx]})

                solution_bridges = []
                for (u, v), cnt in edge_bridge_count.items():
                    r1, c1 = islands[u]
                    r2, c2 = islands[v]
                    solution_bridges.append({
                        "r1": r1, "c1": c1,
                        "r2": r2, "c2": c2,
                        "count": cnt
                    })

                puzzle_dict = {
                    "title": "BRIDGES",
                    "difficulty": diff_key.upper(),
                    "size": size,
                    "rows": size,
                    "cols": size,
                    "islands": islands_data,
                    "island_count": len(islands_data),
                    "solution_bridges": solution_bridges,
                    "text": self.format_ascii(size, islands_data, solution_bridges, show_solution=False),
                    "solution_text": self.format_ascii(size, islands_data, solution_bridges, show_solution=True)
                }
                return puzzle_dict

        raise RuntimeError(f"Failed to generate unique Bridges puzzle for {difficulty} in {max_attempts} attempts")

    def format_ascii(
        self,
        size: int,
        islands: List[Dict[str, int]],
        bridges: List[Dict[str, int]],
        show_solution: bool = False
    ) -> str:
        # Build an expanded character grid for ASCII representation
        # Each cell in original grid maps to row 2*r, col 2*c
        grid_h = 2 * size - 1
        grid_w = 2 * size - 1
        char_grid = [[" " for _ in range(grid_w)] for _ in range(grid_h)]

        # Place islands
        for isl in islands:
            r, c = isl["r"], isl["c"]
            char_grid[2 * r][2 * c] = str(isl["count"])

        if show_solution:
            for b in bridges:
                r1, c1 = b["r1"], b["c1"]
                r2, c2 = b["r2"], b["c2"]
                cnt = b["count"]

                if r1 == r2:
                    # Horizontal bridge
                    row = 2 * r1
                    start_c = min(2 * c1, 2 * c2) + 1
                    end_c = max(2 * c1, 2 * c2)
                    sym = "=" if cnt == 2 else "-"
                    for col in range(start_c, end_c):
                        char_grid[row][col] = sym
                elif c1 == c2:
                    # Vertical bridge
                    col = 2 * c1
                    start_r = min(2 * r1, 2 * r2) + 1
                    end_r = max(2 * r1, 2 * r2)
                    sym = '"' if cnt == 2 else "|"
                    for row in range(start_r, end_r):
                        char_grid[row][col] = sym

        lines = []
        for row in range(grid_h):
            row_str = "      " + " ".join(char_grid[row])
            lines.append(row_str)

        return "\n".join(lines)
