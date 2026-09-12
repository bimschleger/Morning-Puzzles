"""
Morning Puzzles - Bridges (Hashiwokakero) Plugin
Encapsulates generation, canonical instruction formatting, ASCII layout,
solution key formatting, and 576-dot thermal raster rendering.
"""

import random
import textwrap
from typing import List, Tuple, Optional, Dict, Any, Set, Union

from .base import BasePuzzle, BasePuzzleResult
from ..renderer.canvas import (
    THERMAL_WIDTH_DOTS,
    ThermalBitmap,
)


class BridgesPuzzle(BasePuzzle):
    """Bridges (Hashiwokakero) network puzzle plugin."""

    DIFFICULTY_SETTINGS = {
        "easy":   {"size": 6, "islands": 8,  "max_degree": 4},
        "medium": {"size": 8, "islands": 10, "max_degree": 6},
        "hard":   {"size": 8, "islands": 14, "max_degree": 8},
    }

    @property
    def puzzle_id(self) -> str:
        return "bridges"

    @property
    def title(self) -> str:
        return "BRIDGES"

    @property
    def has_difficulty(self) -> bool:
        return True

    @property
    def supported_difficulties(self) -> List[str]:
        return ["easy", "medium", "hard"]

    def generate(
        self,
        difficulty: str = "medium",
        seed: Optional[int] = None,
        **kwargs,
    ) -> BasePuzzleResult:
        if seed is not None:
            random.seed(seed)

        diff_key = difficulty.lower()
        if diff_key not in self.DIFFICULTY_SETTINGS:
            diff_key = "medium"

        settings = self.DIFFICULTY_SETTINGS[diff_key]
        size = settings["size"]
        target_islands = settings["islands"]
        max_degree = settings["max_degree"]

        max_attempts = 120
        for _ in range(max_attempts):
            all_cells = [(r, c) for r in range(size) for c in range(size)]
            random.shuffle(all_cells)

            islands: List[Tuple[int, int]] = []
            for r, c in all_cells:
                if len(islands) >= target_islands:
                    break
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

            edges = self._find_potential_edges(islands)
            if len(edges) < target_islands - 1:
                continue

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
            for e in edges:
                u, v = e
                crosses = False
                for te in tree_edges:
                    if self._edges_cross(e, te, islands):
                        crosses = True
                        break
                if not crosses and union(u, v):
                    tree_edges.append(e)
                    edge_bridge_count[e] = 1

            root = find(0)
            if any(find(i) != root for i in range(len(islands))):
                continue

            island_degrees = [0] * len(islands)
            for (u, v), cnt in edge_bridge_count.items():
                island_degrees[u] += cnt
                island_degrees[v] += cnt

            for e in tree_edges:
                u, v = e
                if island_degrees[u] < max_degree and island_degrees[v] < max_degree:
                    if random.random() < 0.4:
                        edge_bridge_count[e] += 1
                        island_degrees[u] += 1
                        island_degrees[v] += 1

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

            degrees = [0] * len(islands)
            for (u, v), cnt in edge_bridge_count.items():
                degrees[u] += cnt
                degrees[v] += cnt

            if any(d == 0 or d > max_degree for d in degrees):
                continue

            active_potential_edges = self._find_potential_edges(islands)
            sol_count = self._count_solutions(islands, degrees, active_potential_edges, max_solutions=2)

            if sol_count == 1:
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
                        "count": cnt,
                    })

                ascii_text = self._format_grid_ascii(size, islands_data, solution_bridges, show_solution=False)
                solution_text = self._format_grid_ascii(size, islands_data, solution_bridges, show_solution=True)

                raw_data = {
                    "type": "bridges",
                    "title": "BRIDGES",
                    "difficulty": diff_key,
                    "size": size,
                    "rows": size,
                    "cols": size,
                    "islands": islands_data,
                    "island_count": len(islands_data),
                    "solution_bridges": solution_bridges,
                    "text": ascii_text,
                    "solution_text": solution_text,
                }
                instruction = self.get_instruction(raw_data)

                return BasePuzzleResult(
                    puzzle_type=self.puzzle_id,
                    title=self.title,
                    difficulty=diff_key,
                    instruction=instruction,
                    raw_data=raw_data,
                )

        raise RuntimeError(f"Failed to generate unique Bridges puzzle for {difficulty} in {max_attempts} attempts")

    def get_instruction(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        return "Connect all islands into one network using 1 or 2 lines matching each island's number."

    def format_ascii_puzzle(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        size = puzzle_data.get("size", 8)
        islands = puzzle_data.get("islands", [])
        return self._format_grid_ascii(size, islands, [], show_solution=False)

    def format_solution_key(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> List[str]:
        sol_text = puzzle_data.get("solution_text", "")
        bridges = puzzle_data.get("solution_bridges", [])
        lines = []
        if sol_text:
            for line in sol_text.split("\n"):
                lines.append(line)
        if bridges:
            b_str = "Bridges: " + ", ".join(f"({x['r1']+1},{x['c1']+1})-({x['r2']+1},{x['c2']+1})[{x['count']}]" for x in bridges)
            for line in textwrap.wrap(b_str, 46):
                lines.append(line)
        return lines

    def render_raster(
        self,
        puzzle_data: Union[BasePuzzleResult, Dict[str, Any]],
        target_width: int = THERMAL_WIDTH_DOTS,
    ) -> bytes:
        size = puzzle_data.get("size", 8)
        islands = puzzle_data.get("islands", [])

        padding = 32
        board_size = target_width - padding * 2
        step = board_size // (size - 1) if size > 1 else board_size
        total_h = padding + board_size + padding

        tb = ThermalBitmap(target_width, total_h)

        corner_len = 16
        tb.draw_hline(padding, padding, corner_len, thickness=2)
        tb.draw_vline(padding, padding, corner_len, thickness=2)
        tb.draw_hline(padding + board_size - corner_len, padding, corner_len, thickness=2)
        tb.draw_vline(padding + board_size, padding, corner_len, thickness=2)
        tb.draw_hline(padding, padding + board_size, corner_len, thickness=2)
        tb.draw_vline(padding, padding + board_size - corner_len, corner_len, thickness=2)
        tb.draw_hline(padding + board_size - corner_len, padding + board_size, corner_len, thickness=2)
        tb.draw_vline(padding + board_size, padding + board_size - corner_len, corner_len, thickness=2)

        island_radius = max(18, min(24, step // 3))
        for isl in islands:
            r, c = isl.get("r", 0), isl.get("c", 0)
            count = isl.get("count", 1)

            cx = padding + c * step
            cy = padding + r * step

            tb.fill_rect(cx - island_radius, cy - island_radius, island_radius * 2, island_radius * 2, color=0)
            tb.draw_circle(cx, cy, island_radius, thickness=3, color=1)

            char_scale = 3 if island_radius >= 20 else 2
            char_w = 6 * char_scale
            char_h = 7 * char_scale
            tb.draw_char(cx - char_w // 2, cy - char_h // 2, str(count), scale=char_scale, color=1)

        return tb.to_escpos()

    def _format_grid_ascii(
        self,
        size: int,
        islands: List[Dict[str, int]],
        bridges: List[Dict[str, int]],
        show_solution: bool = False,
    ) -> str:
        grid_h = 2 * size - 1
        grid_w = 2 * size - 1
        char_grid = [[" " for _ in range(grid_w)] for _ in range(grid_h)]

        for isl in islands:
            r, c = isl["r"], isl["c"]
            char_grid[2 * r][2 * c] = str(isl["count"])

        if show_solution:
            for b in bridges:
                r1, c1 = b["r1"], b["c1"]
                r2, c2 = b["r2"], b["c2"]
                cnt = b["count"]

                if r1 == r2:
                    row = 2 * r1
                    start_c = min(2 * c1, 2 * c2) + 1
                    end_c = max(2 * c1, 2 * c2)
                    sym = "=" if cnt == 2 else "-"
                    for col in range(start_c, end_c):
                        char_grid[row][col] = sym
                elif c1 == c2:
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

    def _find_potential_edges(self, islands: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        edges = []
        n = len(islands)
        for i in range(n):
            r1, c1 = islands[i]
            for j in range(i + 1, n):
                r2, c2 = islands[j]
                if r1 == r2:
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
        islands: List[Tuple[int, int]],
    ) -> bool:
        i1, j1 = e1
        i2, j2 = e2
        r1a, c1a = islands[i1]
        r1b, c1b = islands[j1]
        r2a, c2a = islands[i2]
        r2b, c2b = islands[j2]

        is_e1_horiz = (r1a == r1b)
        is_e2_horiz = (r2a == r2b)

        if is_e1_horiz == is_e2_horiz:
            return False

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

        return (v_r_min < h_r < v_r_max) and (h_c_min < v_c < h_c_max)

    def _count_solutions(
        self,
        islands: List[Tuple[int, int]],
        degrees: List[int],
        edges: List[Tuple[int, int]],
        max_solutions: int = 2,
    ) -> int:
        num_islands = len(islands)
        num_edges = len(edges)
        edge_val = [0] * num_edges
        island_rem = list(degrees)
        solutions_count = 0

        crossing_pairs = []
        for i in range(num_edges):
            for j in range(i + 1, num_edges):
                if self._edges_cross(edges[i], edges[j], islands):
                    crossing_pairs.append((i, j))

        crossing_lookup: Dict[int, List[int]] = {i: [] for i in range(num_edges)}
        for i, j in crossing_pairs:
            crossing_lookup[i].append(j)
            crossing_lookup[j].append(i)

        def is_connected() -> bool:
            adj = [[] for _ in range(num_islands)]
            for e_idx, val in enumerate(edge_val):
                if val > 0:
                    u, v = edges[e_idx]
                    adj[u].append(v)
                    adj[v].append(u)

            visited = [False] * num_islands
            q = [0]
            visited[0] = True
            count = 1
            while q:
                curr = q.pop()
                for neighbor in adj[curr]:
                    if not visited[neighbor]:
                        visited[neighbor] = True
                        count += 1
                        q.append(neighbor)
            return count == num_islands

        def search(e_idx: int):
            nonlocal solutions_count
            if solutions_count >= max_solutions:
                return

            if e_idx == num_edges:
                if all(rem == 0 for rem in island_rem):
                    if is_connected():
                        solutions_count += 1
                return

            u, v = edges[e_idx]
            has_crossing_active = any(edge_val[other] > 0 for other in crossing_lookup[e_idx])
            allowed_values = [0] if has_crossing_active else [0, 1, 2]

            for val in allowed_values:
                if val > island_rem[u] or val > island_rem[v]:
                    continue

                edge_val[e_idx] = val
                island_rem[u] -= val
                island_rem[v] -= val

                feasible = True
                if island_rem[u] < 0 or island_rem[v] < 0:
                    feasible = False

                if feasible:
                    search(e_idx + 1)

                island_rem[u] += val
                island_rem[v] += val
                edge_val[e_idx] = 0

        search(0)
        return solutions_count
