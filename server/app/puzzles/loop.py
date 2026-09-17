"""
Morning Puzzles - Loop Plugin (Slitherlink / Fences)
Encapsulates procedural generation, canonical instruction formatting,
ASCII layout, solution key formatting, and 576-dot thermal raster rendering.
"""

import random
from typing import List, Tuple, Optional, Dict, Any, Set, Union

from .base import BasePuzzle, BasePuzzleResult
from ..renderer.canvas import (
    THERMAL_WIDTH_DOTS,
    ThermalBitmap,
    HAS_PILLOW,
    image_to_escpos_raster,
)

if HAS_PILLOW:
    from PIL import Image, ImageDraw, ImageFont


class SlitherlinkSolver:
    """
    Backtracking constraint propagation solver for Slitherlink.
    Verifies mathematical uniqueness and deduction depth.
    """
    def __init__(self, n: int, clues: List[List[int]]):
        self.n = n
        self.clues = clues
        # Edge states: 0 = UNKNOWN, 1 = LOOP, -1 = EMPTY
        self.H = [[0]*n for _ in range(n + 1)]
        self.V = [[0]*(n + 1) for _ in range(n)]

    def propagate(self) -> bool:
        n = self.n
        changed = True
        while changed:
            changed = False
            # 1. Cell clues
            for r in range(n):
                for c in range(n):
                    k = self.clues[r][c]
                    if k < 0:
                        continue
                    edges = [
                        ('H', r, c),
                        ('H', r+1, c),
                        ('V', r, c),
                        ('V', r, c+1)
                    ]
                    loop_cnt = sum(1 for typ, er, ec in edges if (self.H[er][ec] if typ=='H' else self.V[er][ec]) == 1)
                    empty_cnt = sum(1 for typ, er, ec in edges if (self.H[er][ec] if typ=='H' else self.V[er][ec]) == -1)
                    unk_cnt = 4 - loop_cnt - empty_cnt

                    if loop_cnt > k or loop_cnt + unk_cnt < k:
                        return False

                    if unk_cnt > 0:
                        if loop_cnt == k:
                            for typ, er, ec in edges:
                                val = self.H[er][ec] if typ=='H' else self.V[er][ec]
                                if val == 0:
                                    if typ == 'H': self.H[er][ec] = -1
                                    else: self.V[er][ec] = -1
                                    changed = True
                        elif loop_cnt + unk_cnt == k:
                            for typ, er, ec in edges:
                                val = self.H[er][ec] if typ=='H' else self.V[er][ec]
                                if val == 0:
                                    if typ == 'H': self.H[er][ec] = 1
                                    else: self.V[er][ec] = 1
                                    changed = True

            # 2. Vertex degrees
            for r in range(n + 1):
                for c in range(n + 1):
                    incident = []
                    if c > 0: incident.append(('H', r, c-1))
                    if c < n: incident.append(('H', r, c))
                    if r > 0: incident.append(('V', r-1, c))
                    if r < n: incident.append(('V', r, c))

                    deg_loop = sum(1 for typ, er, ec in incident if (self.H[er][ec] if typ=='H' else self.V[er][ec]) == 1)
                    deg_empty = sum(1 for typ, er, ec in incident if (self.H[er][ec] if typ=='H' else self.V[er][ec]) == -1)
                    deg_unk = len(incident) - deg_loop - deg_empty

                    if deg_loop > 2 or (deg_loop == 1 and deg_unk == 0):
                        return False

                    if deg_loop == 2 and deg_unk > 0:
                        for typ, er, ec in incident:
                            val = self.H[er][ec] if typ=='H' else self.V[er][ec]
                            if val == 0:
                                if typ == 'H': self.H[er][ec] = -1
                                else: self.V[er][ec] = -1
                                changed = True
                    elif deg_loop == 1 and deg_unk == 1:
                        for typ, er, ec in incident:
                            val = self.H[er][ec] if typ=='H' else self.V[er][ec]
                            if val == 0:
                                if typ == 'H': self.H[er][ec] = 1
                                else: self.V[er][ec] = 1
                                changed = True
                    elif deg_loop == 0 and deg_unk == 1:
                        for typ, er, ec in incident:
                            val = self.H[er][ec] if typ=='H' else self.V[er][ec]
                            if val == 0:
                                if typ == 'H': self.H[er][ec] = -1
                                else: self.V[er][ec] = -1
                                changed = True

            # 3. Prevent premature sub-loop closure
            adj: Dict[Tuple[int, int], Set[Tuple[int, int]]] = {}
            for r in range(n+1):
                for c in range(n):
                    if self.H[r][c] == 1:
                        adj.setdefault((r, c), set()).add((r, c+1))
                        adj.setdefault((r, c+1), set()).add((r, c))
            for r in range(n):
                for c in range(n+1):
                    if self.V[r][c] == 1:
                        adj.setdefault((r, c), set()).add((r+1, c))
                        adj.setdefault((r+1, c), set()).add((r, c))

            visited = set()
            for node in adj:
                if node not in visited:
                    comp = []
                    q = [node]
                    visited.add(node)
                    edge_count = 0
                    while q:
                        curr = q.pop(0)
                        comp.append(curr)
                        for nbr in adj.get(curr, []):
                            edge_count += 1
                            if nbr not in visited:
                                visited.add(nbr)
                                q.append(nbr)
                    edge_count //= 2
                    if edge_count == len(comp):
                        has_other = False
                        for r in range(n):
                            for c in range(n):
                                if self.clues[r][c] > 0:
                                    edges = [('H', r, c), ('H', r+1, c), ('V', r, c), ('V', r, c+1)]
                                    l_cnt = sum(1 for typ, er, ec in edges if (self.H[er][ec] if typ=='H' else self.V[er][ec]) == 1)
                                    if l_cnt < self.clues[r][c]:
                                        has_other = True
                                        break
                            if has_other: break
                        if has_other or sum(row.count(0) for row in self.H) + sum(row.count(0) for row in self.V) > 0:
                            return False
                    else:
                        endpoints = [u for u in comp if len(adj[u]) == 1]
                        if len(endpoints) == 2:
                            u, v = endpoints
                            has_other = any(
                                sum(1 for typ, er, ec in [('H', r, c), ('H', r+1, c), ('V', r, c), ('V', r, c+1)]
                                    if (self.H[er][ec] if typ=='H' else self.V[er][ec]) == 1) < self.clues[r][c]
                                for r in range(n) for c in range(n) if self.clues[r][c] > 0
                            )
                            if has_other:
                                if u[0] == v[0] and abs(u[1] - v[1]) == 1:
                                    er, ec = u[0], min(u[1], v[1])
                                    if self.H[er][ec] == 0:
                                        self.H[er][ec] = -1
                                        changed = True
                                elif u[1] == v[1] and abs(u[0] - v[0]) == 1:
                                    er, ec = min(u[0], v[0]), u[1]
                                    if self.V[er][ec] == 0:
                                        self.V[er][ec] = -1
                                        changed = True
        return True

    def count_solutions(self, max_count: int = 2) -> int:
        if not self.propagate():
            return 0

        n = self.n
        for r in range(n + 1):
            for c in range(n):
                if self.H[r][c] == 0:
                    cnt = 0
                    saved_H = [row[:] for row in self.H]
                    saved_V = [row[:] for row in self.V]
                    self.H[r][c] = 1
                    cnt += self.count_solutions(max_count)
                    if cnt >= max_count:
                        return cnt
                    self.H = [row[:] for row in saved_H]
                    self.V = [row[:] for row in saved_V]
                    self.H[r][c] = -1
                    cnt += self.count_solutions(max_count)
                    self.H = saved_H
                    self.V = saved_V
                    return cnt

        for r in range(n):
            for c in range(n + 1):
                if self.V[r][c] == 0:
                    cnt = 0
                    saved_H = [row[:] for row in self.H]
                    saved_V = [row[:] for row in self.V]
                    self.V[r][c] = 1
                    cnt += self.count_solutions(max_count)
                    if cnt >= max_count:
                        return cnt
                    self.H = [row[:] for row in saved_H]
                    self.V = [row[:] for row in saved_V]
                    self.V[r][c] = -1
                    cnt += self.count_solutions(max_count)
                    self.H = saved_H
                    self.V = saved_V
                    return cnt

        # Verify all clues satisfied and single loop
        for r in range(n):
            for c in range(n):
                k = self.clues[r][c]
                if k >= 0:
                    cnt = (1 if self.H[r][c]==1 else 0) + (1 if self.H[r+1][c]==1 else 0) + \
                          (1 if self.V[r][c]==1 else 0) + (1 if self.V[r][c+1]==1 else 0)
                    if cnt != k:
                        return 0

        adj: Dict[Tuple[int, int], List[Tuple[int, int]]] = {}
        for r in range(n+1):
            for c in range(n):
                if self.H[r][c] == 1:
                    adj.setdefault((r, c), []).append((r, c+1))
                    adj.setdefault((r, c+1), []).append((r, c))
        for r in range(n):
            for c in range(n+1):
                if self.V[r][c] == 1:
                    adj.setdefault((r, c), []).append((r+1, c))
                    adj.setdefault((r+1, c), []).append((r, c))

        if not adj or any(len(nbrs) != 2 for nbrs in adj.values()):
            return 0

        start = next(iter(adj))
        visited = {start}
        curr = adj[start][0]
        prev = start
        while curr != start:
            visited.add(curr)
            nbrs = adj[curr]
            curr, prev = (nbrs[1] if nbrs[0] == prev else nbrs[0]), curr
            if len(visited) > len(adj):
                return 0

        return 1 if len(visited) == len(adj) else 0


class LoopPuzzle(BasePuzzle):
    """
    Loop (Slitherlink / Fences) loop-drawing logic puzzle.
    Solvers connect lattice dots horizontally and vertically to form a single
    continuous closed non-intersecting loop so each numbered cell matches its edge count.
    """

    DIFFICULTY_SETTINGS = {
        "easy":   {"size": 6, "target_density": 0.58, "cell_size": 88, "padding": 24},
        "medium": {"size": 7, "target_density": 0.48, "cell_size": 75, "padding": 25},
        "hard":   {"size": 9, "target_density": 0.38, "cell_size": 58, "padding": 27},
    }

    @property
    def puzzle_id(self) -> str:
        return "loop"

    @property
    def title(self) -> str:
        return "LOOP"

    @property
    def has_difficulty(self) -> bool:
        return True

    @property
    def default_difficulty(self) -> str:
        return "medium"

    @property
    def supported_difficulties(self) -> List[str]:
        return ["easy", "medium", "hard"]

    def _generate_loop_polyomino(self, n: int) -> Tuple[List[List[int]], List[List[int]], List[List[int]]]:
        """
        Generates a ground-truth single closed loop on an (n+1)x(n+1) dot lattice
        by growing a simply connected polyomino without 2x2 diagonal checkerboards.
        """
        total_cells = n * n
        target_count = max(4, int(total_cells * 0.45))

        for _ in range(250):
            grid = [[0]*n for _ in range(n)]
            start_r = random.randint(1, n - 2) if n > 3 else random.randint(0, n - 1)
            start_c = random.randint(1, n - 2) if n > 3 else random.randint(0, n - 1)
            grid[start_r][start_c] = 1
            S = {(start_r, start_c)}

            frontier = set()
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                nr, nc = start_r + dr, start_c + dc
                if 0 <= nr < n and 0 <= nc < n:
                    frontier.add((nr, nc))

            def is_valid_to_add(r, c):
                for r0, c0 in [(r-1, c-1), (r-1, c), (r, c-1), (r, c)]:
                    if 0 <= r0 < n - 1 and 0 <= c0 < n - 1:
                        b = [
                            1 if (r0, c0) == (r, c) else grid[r0][c0],
                            1 if (r0, c0+1) == (r, c) else grid[r0][c0+1],
                            1 if (r0+1, c0) == (r, c) else grid[r0+1][c0],
                            1 if (r0+1, c0+1) == (r, c) else grid[r0+1][c0+1],
                        ]
                        if (b[0] == 1 and b[1] == 0 and b[2] == 0 and b[3] == 1) or \
                           (b[0] == 0 and b[1] == 1 and b[2] == 1 and b[3] == 0):
                            return False
                return True

            def complement_connected():
                visited = [[False]*n for _ in range(n)]
                queue = []
                for r in range(n):
                    for c in range(n):
                        if (r == 0 or r == n - 1 or c == 0 or c == n - 1) and grid[r][c] == 0:
                            visited[r][c] = True
                            queue.append((r, c))
                idx = 0
                while idx < len(queue):
                    cr, cc = queue[idx]
                    idx += 1
                    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc] and grid[nr][nc] == 0:
                            visited[nr][nc] = True
                            queue.append((nr, nc))
                zero_count = sum(1 for r in range(n) for c in range(n) if grid[r][c] == 0)
                return len(queue) == zero_count

            while len(S) < target_count and frontier:
                cand = random.choice(list(frontier))
                frontier.remove(cand)
                cr, cc = cand
                if is_valid_to_add(cr, cc):
                    grid[cr][cc] = 1
                    if complement_connected():
                        S.add((cr, cc))
                        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                            nr, nc = cr + dr, cc + dc
                            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                                frontier.add((nr, nc))
                    else:
                        grid[cr][cc] = 0

            if len(S) >= max(3, target_count // 2):
                H = [[0]*n for _ in range(n + 1)]
                V = [[0]*(n + 1) for _ in range(n)]

                for r in range(n + 1):
                    for c in range(n):
                        top = grid[r-1][c] if r > 0 else 0
                        bot = grid[r][c] if r < n else 0
                        if top != bot:
                            H[r][c] = 1

                for r in range(n):
                    for c in range(n + 1):
                        left = grid[r][c-1] if c > 0 else 0
                        right = grid[r][c] if c < n else 0
                        if left != right:
                            V[r][c] = 1

                clues = [[0]*n for _ in range(n)]
                for r in range(n):
                    for c in range(n):
                        clues[r][c] = H[r][c] + H[r+1][c] + V[r][c] + V[r][c+1]

                # Verify single cycle on lattice
                adj: Dict[Tuple[int, int], List[Tuple[int, int]]] = {}
                for r in range(n+1):
                    for c in range(n):
                        if H[r][c]:
                            adj.setdefault((r, c), []).append((r, c+1))
                            adj.setdefault((r, c+1), []).append((r, c))
                for r in range(n):
                    for c in range(n+1):
                        if V[r][c]:
                            adj.setdefault((r, c), []).append((r+1, c))
                            adj.setdefault((r+1, c), []).append((r, c))

                if not adj or any(len(nbrs) != 2 for nbrs in adj.values()):
                    continue

                start_node = next(iter(adj))
                visited_nodes = {start_node}
                curr = adj[start_node][0]
                prev = start_node
                while curr != start_node:
                    visited_nodes.add(curr)
                    nbrs = adj[curr]
                    curr, prev = (nbrs[1] if nbrs[0] == prev else nbrs[0]), curr
                    if len(visited_nodes) > len(adj):
                        break

                if len(visited_nodes) == len(adj) and len(adj) >= 8:
                    return H, V, clues

        raise RuntimeError(f"Failed to generate loop polyomino of size {n}")

    def generate(self, difficulty: str = "medium", **kwargs) -> BasePuzzleResult:
        diff = difficulty.lower()
        cfg = self.DIFFICULTY_SETTINGS.get(diff, self.DIFFICULTY_SETTINGS["medium"])
        n = cfg["size"]
        target_density = cfg["target_density"]

        for _ in range(20):
            H, V, full_clues = self._generate_loop_polyomino(n)
            solver = SlitherlinkSolver(n, full_clues)
            if solver.count_solutions(max_count=2) != 1:
                continue

            clues = [row[:] for row in full_clues]
            cells = [(r, c) for r in range(n) for c in range(n)]
            random.shuffle(cells)
            min_clues = int(n * n * target_density)

            for r, c in cells:
                if sum(1 for row in clues for val in row if val >= 0) <= min_clues:
                    break
                orig = clues[r][c]
                clues[r][c] = -1
                s = SlitherlinkSolver(n, clues)
                if s.count_solutions(max_count=2) != 1:
                    clues[r][c] = orig

            # Verify uniqueness of pruned puzzle
            final_solver = SlitherlinkSolver(n, clues)
            if final_solver.count_solutions(max_count=2) == 1:
                raw_data = {
                    "type": "loop",
                    "difficulty": diff,
                    "size": n,
                    "clues": clues,
                    "solution_h": H,
                    "solution_v": V,
                }
                instruction = self.get_instruction(raw_data)
                return BasePuzzleResult(
                    puzzle_type="loop",
                    title="LOOP",
                    difficulty=diff,
                    instruction=instruction,
                    raw_data=raw_data,
                )

        raise RuntimeError(f"Could not generate unique {diff} Loop puzzle within attempt limit")

    def get_instruction(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        # Strictly <= 100 chars, imperative formula, plain English
        return "Draw a single continuous closed loop connecting dots so each number matches its edge count."

    def format_ascii_puzzle(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        n = puzzle_data.get("size", 7)
        clues = puzzle_data.get("clues", [])
        indent = "      "

        lines = []
        for r in range(n):
            # Dot row
            dot_line = indent + " ".join([".   "] * n) + "."
            lines.append(dot_line)
            # Clue row
            clue_parts = [indent]
            for c in range(n):
                k = clues[r][c] if r < len(clues) and c < len(clues[r]) else -1
                ch = str(k) if k >= 0 else " "
                clue_parts.append(f"  {ch} ")
            lines.append("".join(clue_parts) + " ")
        # Final dot row
        lines.append(indent + " ".join([".   "] * n) + ".")
        return "\n".join(lines)

    def format_solution_key(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> List[str]:
        n = puzzle_data.get("size", 7)
        clues = puzzle_data.get("clues", [])
        H = puzzle_data.get("solution_h", [])
        V = puzzle_data.get("solution_v", [])

        indent = "      "
        lines = []

        for r in range(n):
            # Vertex and horizontal edge row
            h_parts = []
            for c in range(n):
                edge = H[r][c] if r < len(H) and c < len(H[r]) else 0
                h_parts.append("+" + ("---" if edge else "   "))
            h_parts.append("+")
            lines.append(indent + "".join(h_parts))

            # Vertical edges and cell interior row
            v_parts = []
            for c in range(n):
                v_edge = V[r][c] if r < len(V) and c < len(V[r]) else 0
                k = clues[r][c] if r < len(clues) and c < len(clues[r]) else -1
                digit_char = str(k) if k >= 0 else " "
                v_parts.append(("|" if v_edge else " ") + f" {digit_char} ")
            v_edge_last = V[r][n] if r < len(V) and n < len(V[r]) else 0
            v_parts.append("|" if v_edge_last else " ")
            lines.append(indent + "".join(v_parts))

        # Bottom horizontal row
        bottom_parts = []
        for c in range(n):
            edge = H[n][c] if n < len(H) and c < len(H[n]) else 0
            bottom_parts.append("+" + ("---" if edge else "   "))
        bottom_parts.append("+")
        lines.append(indent + "".join(bottom_parts))

        return lines

    def render_raster(
        self,
        puzzle_data: Union[BasePuzzleResult, Dict[str, Any]],
        target_width: int = THERMAL_WIDTH_DOTS,
    ) -> bytes:
        n = puzzle_data.get("size", 7)
        clues = puzzle_data.get("clues", [])
        diff = puzzle_data.get("difficulty", "medium").lower()

        cfg = self.DIFFICULTY_SETTINGS.get(diff, self.DIFFICULTY_SETTINGS["medium"])
        cell_size = cfg["cell_size"]
        padding = cfg["padding"]

        board_size = cell_size * n
        left_margin = (target_width - board_size) // 2
        total_h = 576

        tb = ThermalBitmap(target_width, total_h)
        dot_radius = 3

        # Draw lattice dots (clean Nikoli style: 3px radius filled circles)
        for r in range(n + 1):
            py = padding + r * cell_size
            for c in range(n + 1):
                px = left_margin + c * cell_size
                tb.fill_circle(px, py, dot_radius, color=1)

        # Draw clue numbers (scale 3 monospaced bitmap digits centered in cells)
        for r in range(n):
            for c in range(n):
                k = clues[r][c] if r < len(clues) and c < len(clues[r]) else -1
                if k >= 0:
                    digit_str = str(k)
                    tx = left_margin + c * cell_size + (cell_size - 18) // 2
                    ty = padding + r * cell_size + (cell_size - 21) // 2
                    tb.draw_char(tx, ty, digit_str, scale=3, color=1)

        return tb.to_escpos()

    def verify_accuracy(
        self,
        puzzle_data: Union[BasePuzzleResult, Dict[str, Any]],
    ) -> Tuple[bool, str]:
        n = puzzle_data.get("size", 7)
        clues = puzzle_data.get("clues", [])
        H = puzzle_data.get("solution_h", [])
        V = puzzle_data.get("solution_v", [])

        if len(H) != n + 1 or any(len(row) != n for row in H):
            return False, f"Invalid H dimension: expected {n+1}x{n}"
        if len(V) != n or any(len(row) != n + 1 for row in V):
            return False, f"Invalid V dimension: expected {n}x{n+1}"

        # 1. Clue satisfaction
        for r in range(n):
            for c in range(n):
                k = clues[r][c]
                if k >= 0:
                    cnt = H[r][c] + H[r+1][c] + V[r][c] + V[r][c+1]
                    if cnt != k:
                        return False, f"Cell ({r}, {c}) clue {k} does not match edge count {cnt}"

        # 2. Vertex degrees: every vertex must have degree 0 or 2
        deg: Dict[Tuple[int, int], int] = {}
        adj: Dict[Tuple[int, int], List[Tuple[int, int]]] = {}
        for r in range(n + 1):
            for c in range(n):
                if H[r][c]:
                    deg[(r, c)] = deg.get((r, c), 0) + 1
                    deg[(r, c+1)] = deg.get((r, c+1), 0) + 1
                    adj.setdefault((r, c), []).append((r, c+1))
                    adj.setdefault((r, c+1), []).append((r, c))
        for r in range(n):
            for c in range(n + 1):
                if V[r][c]:
                    deg[(r, c)] = deg.get((r, c), 0) + 1
                    deg[(r+1, c)] = deg.get((r+1, c), 0) + 1
                    adj.setdefault((r, c), []).append((r+1, c))
                    adj.setdefault((r+1, c), []).append((r, c))

        for v, d in deg.items():
            if d != 2:
                return False, f"Vertex {v} has invalid loop degree {d} (must be 2)"

        # 3. Single continuous closed loop
        if not adj:
            return False, "Empty loop"

        start = next(iter(adj))
        visited = {start}
        curr = adj[start][0]
        prev = start
        while curr != start:
            visited.add(curr)
            nbrs = adj[curr]
            curr, prev = (nbrs[1] if nbrs[0] == prev else nbrs[0]), curr
            if len(visited) > len(adj):
                return False, "Cycle traversal exceeded loop vertex count"

        if len(visited) != len(adj):
            return False, f"Multiple disconnected loops found: visited {len(visited)} of {len(adj)} vertices"

        return True, "All rules satisfied"
