"""
Morning Puzzles - Maze Plugin
Encapsulates procedural maze generation, canonical instruction formatting,
ASCII layout, solution key formatting, and 576-dot thermal raster rendering.
"""

import collections
import random
from typing import List, Tuple, Optional, Dict, Any, Union

from .base import BasePuzzle, BasePuzzleResult
from ..renderer.canvas import (
    THERMAL_WIDTH_DOTS,
    ThermalBitmap,
)


class MazePuzzle(BasePuzzle):
    """
    Modular plugin for the MAZE puzzle.
    Generates square perfect labyrinths with escalating grid density,
    branching bias, and passage widths across difficulty levels.
    """

    DIFFICULTY_SETTINGS = {
        "easy": {
            "size": 10,
            "cell_size": 48,
            "wall_thickness": 4,
            "branch_prob": 0.50,
        },
        "medium": {
            "size": 20,
            "cell_size": 24,
            "wall_thickness": 3,
            "branch_prob": 0.25,
        },
        "hard": {
            "size": 30,
            "cell_size": 16,
            "wall_thickness": 2,
            "branch_prob": 0.05,
        },
        "extreme": {
            "size": 40,
            "cell_size": 12,
            "wall_thickness": 2,
            "branch_prob": 0.00,
        },
    }

    @property
    def puzzle_id(self) -> str:
        return "maze"

    @property
    def title(self) -> str:
        return "MAZE"

    @property
    def default_difficulty(self) -> str:
        return "medium"

    @property
    def supported_difficulties(self) -> List[str]:
        return ["easy", "medium", "hard", "extreme"]

    def get_instruction(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        return "Draw a path from the entrance to the exit without crossing any walls."

    def generate(self, difficulty: str = "medium", **kwargs) -> BasePuzzleResult:
        diff_lower = difficulty.lower()
        if diff_lower not in self.DIFFICULTY_SETTINGS:
            diff_lower = self.default_difficulty

        cfg = self.DIFFICULTY_SETTINGS[diff_lower]
        n = cfg["size"]
        cell_size = cfg["cell_size"]
        wall_t = cfg["wall_thickness"]
        branch_prob = cfg["branch_prob"]

        seed = kwargs.get("seed")
        rng = random.Random(seed) if seed is not None else random.Random()

        # Walls:
        # walls_h[r][c] is wall between (r, c) and (r+1, c) for r in 0..n-2, c in 0..n-1
        walls_h = [[1] * n for _ in range(n - 1)]
        # walls_v[r][c] is wall between (r, c) and (r, c+1) for r in 0..n-1, c in 0..n-2
        walls_v = [[1] * (n - 1) for _ in range(n)]

        # Growing Tree Algorithm (DFS with branching bias)
        visited = [[False] * n for _ in range(n)]
        active: List[Tuple[int, int]] = [(0, 0)]
        visited[0][0] = True

        while active:
            if rng.random() < branch_prob:
                idx = rng.randint(0, len(active) - 1)
            else:
                idx = len(active) - 1

            r, c = active[idx]
            unvisited_neighbors = []
            # North
            if r > 0 and not visited[r - 1][c]:
                unvisited_neighbors.append((r - 1, c, "N"))
            # South
            if r < n - 1 and not visited[r + 1][c]:
                unvisited_neighbors.append((r + 1, c, "S"))
            # West
            if c > 0 and not visited[r][c - 1]:
                unvisited_neighbors.append((r, c - 1, "W"))
            # East
            if c < n - 1 and not visited[r][c + 1]:
                unvisited_neighbors.append((r, c + 1, "E"))

            if unvisited_neighbors:
                nr, nc, direction = rng.choice(unvisited_neighbors)
                if direction == "N":
                    walls_h[r - 1][c] = 0
                elif direction == "S":
                    walls_h[r][c] = 0
                elif direction == "W":
                    walls_v[r][c - 1] = 0
                elif direction == "E":
                    walls_v[r][c] = 0

                visited[nr][nc] = True
                active.append((nr, nc))
            else:
                active.pop(idx)

        # BFS to find the unique path from (0, 0) to (n - 1, n - 1)
        parent: Dict[Tuple[int, int], Tuple[int, int]] = {}
        q = collections.deque([(0, 0)])
        seen = {(0, 0)}

        while q:
            curr = q.popleft()
            if curr == (n - 1, n - 1):
                break
            cr, cc = curr
            # Check open neighbors
            # North
            if cr > 0 and walls_h[cr - 1][cc] == 0 and (cr - 1, cc) not in seen:
                seen.add((cr - 1, cc))
                parent[(cr - 1, cc)] = curr
                q.append((cr - 1, cc))
            # South
            if cr < n - 1 and walls_h[cr][cc] == 0 and (cr + 1, cc) not in seen:
                seen.add((cr + 1, cc))
                parent[(cr + 1, cc)] = curr
                q.append((cr + 1, cc))
            # West
            if cc > 0 and walls_v[cr][cc - 1] == 0 and (cr, cc - 1) not in seen:
                seen.add((cr, cc - 1))
                parent[(cr, cc - 1)] = curr
                q.append((cr, cc - 1))
            # East
            if cc < n - 1 and walls_v[cr][cc] == 0 and (cr, cc + 1) not in seen:
                seen.add((cr, cc + 1))
                parent[(cr, cc + 1)] = curr
                q.append((cr, cc + 1))

        # Reconstruct path
        path: List[Tuple[int, int]] = [(n - 1, n - 1)]
        curr = (n - 1, n - 1)
        while curr != (0, 0):
            curr = parent[curr]
            path.append(curr)
        path.reverse()

        # Convert path to cardinal turn-by-turn steps
        moves: List[Tuple[str, int]] = []
        for (r1, c1), (r2, c2) in zip(path[:-1], path[1:]):
            if r2 == r1 + 1:
                d = "S"
            elif r2 == r1 - 1:
                d = "N"
            elif c2 == c1 + 1:
                d = "E"
            else:
                d = "W"

            if moves and moves[-1][0] == d:
                moves[-1] = (d, moves[-1][1] + 1)
            else:
                moves.append((d, 1))

        solution_moves = [f"{d} {cnt}" for d, cnt in moves]

        raw_data = {
            "size": n,
            "cell_size": cell_size,
            "wall_thickness": wall_t,
            "walls_h": walls_h,
            "walls_v": walls_v,
            "solution_path": path,
            "solution_moves": solution_moves,
            "difficulty": diff_lower,
        }

        return BasePuzzleResult(
            puzzle_type=self.puzzle_id,
            title=self.title,
            difficulty=diff_lower,
            instruction=self.get_instruction(raw_data),
            raw_data=raw_data,
        )

    def format_ascii_puzzle(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        n = puzzle_data.get("size", 10)
        walls_h = puzzle_data.get("walls_h", [])
        walls_v = puzzle_data.get("walls_v", [])
        indent = "      "
        lines = []

        if n <= 12:
            # 3-char cells with "+---"
            top_parts = ["+   "] + ["+---"] * (n - 1) + ["+"]
            lines.append(indent + "".join(top_parts))
            for r in range(n):
                row_parts = ["|"]
                for c in range(n):
                    row_parts.append("   ")
                    if c < n - 1:
                        has_v = walls_v[r][c] if r < len(walls_v) and c < len(walls_v[r]) else 1
                        row_parts.append("|" if has_v else " ")
                    else:
                        row_parts.append("|")
                lines.append(indent + "".join(row_parts))

                if r < n - 1:
                    h_parts = ["+"]
                    for c in range(n):
                        has_h = walls_h[r][c] if r < len(walls_h) and c < len(walls_h[r]) else 1
                        h_parts.append("---" if has_h else "   ")
                        h_parts.append("+")
                    lines.append(indent + "".join(h_parts))
                else:
                    bot_parts = ["+---"] * (n - 1) + ["+   "] + ["+"]
                    lines.append(indent + "".join(bot_parts))
        else:
            # Compact 1-char representation for larger grids (n=20 fits in 47 cols)
            top_parts = ["+ "] + ["+-"] * (n - 1) + ["+"]
            lines.append(indent + "".join(top_parts))
            for r in range(n):
                row_parts = ["|"]
                for c in range(n):
                    row_parts.append(" ")
                    if c < n - 1:
                        has_v = walls_v[r][c] if r < len(walls_v) and c < len(walls_v[r]) else 1
                        row_parts.append("|" if has_v else " ")
                    else:
                        row_parts.append("|")
                lines.append(indent + "".join(row_parts))

                if r < n - 1:
                    h_parts = ["+"]
                    for c in range(n):
                        has_h = walls_h[r][c] if r < len(walls_h) and c < len(walls_h[r]) else 1
                        h_parts.append("-" if has_h else " ")
                        h_parts.append("+")
                    lines.append(indent + "".join(h_parts))
                else:
                    bot_parts = ["+-"] * (n - 1) + ["+ "] + ["+"]
                    lines.append(indent + "".join(bot_parts))

        return "\n".join(lines)

    def format_solution_key(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> List[str]:
        moves = puzzle_data.get("solution_moves", [])
        if not moves:
            return []

        indent = "      "
        tokens = ["START ->"]
        for i, m in enumerate(moves):
            if i == len(moves) - 1:
                tokens.append(m)
                tokens.append("-> EXIT")
            else:
                tokens.append(f"{m},")

        lines = []
        curr_tokens = []
        curr_len = 0
        for t in tokens:
            added_len = len(t) if not curr_tokens else len(t) + 1
            # Wrap to <= 40 content characters so indent + content <= 46 chars
            if curr_tokens and curr_len + added_len > 40:
                lines.append(indent + " ".join(curr_tokens))
                curr_tokens = [t]
                curr_len = len(t)
            else:
                curr_tokens.append(t)
                curr_len += added_len

        if curr_tokens:
            lines.append(indent + " ".join(curr_tokens))

        return lines

    def render_raster(
        self,
        puzzle_data: Union[BasePuzzleResult, Dict[str, Any]],
        target_width: int = THERMAL_WIDTH_DOTS,
    ) -> bytes:
        n = puzzle_data.get("size", 20)
        walls_h = puzzle_data.get("walls_h", [])
        walls_v = puzzle_data.get("walls_v", [])
        diff = puzzle_data.get("difficulty", "medium").lower()

        cfg = self.DIFFICULTY_SETTINGS.get(diff, self.DIFFICULTY_SETTINGS["medium"])
        cell_size = cfg["cell_size"]
        wall_t = cfg["wall_thickness"]
        outer_t = 4

        board_size = 480
        left_margin = (target_width - board_size) // 2  # 48
        top_margin = (576 - board_size) // 2           # 48
        total_h = 576

        tb = ThermalBitmap(target_width, total_h)

        half_t = wall_t // 2

        # 1. Inner Walls (strictly clamped to board boundaries to prevent frame protrusion)
        # Horizontal walls between row r and r+1
        for r in range(n - 1):
            wy = top_margin + (r + 1) * cell_size - half_t
            for c in range(n):
                if r < len(walls_h) and c < len(walls_h[r]) and walls_h[r][c]:
                    wx_start = max(left_margin, left_margin + c * cell_size - half_t)
                    wx_end = min(left_margin + board_size, left_margin + (c + 1) * cell_size + half_t + (wall_t % 2))
                    tb.draw_hline(wx_start, wy, wx_end - wx_start, thickness=wall_t, color=1)

        # Vertical walls between col c and c+1
        for r in range(n):
            wy_start = max(top_margin, top_margin + r * cell_size - half_t)
            wy_end = min(top_margin + board_size, top_margin + (r + 1) * cell_size + half_t + (wall_t % 2))
            for c in range(n - 1):
                if r < len(walls_v) and c < len(walls_v[r]) and walls_v[r][c]:
                    wx = left_margin + (c + 1) * cell_size - half_t
                    tb.draw_vline(wx, wy_start, wy_end - wy_start, thickness=wall_t, color=1)

        # 2. Outer Frame (thickness 4, rendered over inner walls for clean single-frame boundaries)
        # Top wall: open at cell 0 (leaving x=48..48+cell_size open)
        tb.draw_hline(left_margin + cell_size, top_margin, board_size - cell_size, thickness=outer_t, color=1)
        # Left wall: solid
        tb.draw_vline(left_margin, top_margin, board_size, thickness=outer_t, color=1)
        # Right wall: solid
        tb.draw_vline(left_margin + board_size - outer_t, top_margin, board_size, thickness=outer_t, color=1)
        # Bottom wall: open at cell n-1 (leaving x=48+board_size-cell_size..48+board_size open)
        tb.draw_hline(left_margin, top_margin + board_size - outer_t, board_size - cell_size, thickness=outer_t, color=1)

        # 3. Text Badges "IN" and "OUT"
        # "IN" centered above entrance cell
        in_cx = left_margin + cell_size // 2
        in_tx = in_cx - 11
        in_ty = 24
        tb.draw_text(in_tx, in_ty, "IN", scale=2, color=1)

        # "OUT" centered below exit cell
        out_cx = left_margin + board_size - cell_size // 2
        out_tx = out_cx - 17
        out_ty = top_margin + board_size + 10
        tb.draw_text(out_tx, out_ty, "OUT", scale=2, color=1)

        return tb.to_escpos()

    def verify_accuracy(
        self,
        puzzle_data: Union[BasePuzzleResult, Dict[str, Any]],
    ) -> Tuple[bool, str]:
        n = puzzle_data.get("size", 0)
        if n not in (10, 20, 30, 40):
            return False, f"Invalid maze dimension: {n} (expected 10, 20, 30, or 40)"

        walls_h = puzzle_data.get("walls_h", [])
        walls_v = puzzle_data.get("walls_v", [])

        if len(walls_h) != n - 1 or any(len(row) != n for row in walls_h):
            return False, f"Invalid walls_h dimensions: expected {n-1}x{n}"
        if len(walls_v) != n or any(len(row) != n - 1 for row in walls_v):
            return False, f"Invalid walls_v dimensions: expected {n}x{n-1}"

        # 1. Verify spanning tree property (number of passages = n * n - 1)
        total_open_h = sum(row.count(0) for row in walls_h)
        total_open_v = sum(row.count(0) for row in walls_v)
        total_open = total_open_h + total_open_v
        if total_open != n * n - 1:
            return False, f"Invalid passage count: got {total_open}, expected {n * n - 1} for a perfect maze"

        # 2. Verify graph connectivity (all cells reachable from (0, 0))
        visited = [[False] * n for _ in range(n)]
        q = collections.deque([(0, 0)])
        visited[0][0] = True
        visited_count = 1

        while q:
            r, c = q.popleft()
            # North
            if r > 0 and walls_h[r - 1][c] == 0 and not visited[r - 1][c]:
                visited[r - 1][c] = True
                visited_count += 1
                q.append((r - 1, c))
            # South
            if r < n - 1 and walls_h[r][c] == 0 and not visited[r + 1][c]:
                visited[r + 1][c] = True
                visited_count += 1
                q.append((r + 1, c))
            # West
            if c > 0 and walls_v[r][c - 1] == 0 and not visited[r][c - 1]:
                visited[r][c - 1] = True
                visited_count += 1
                q.append((r, c - 1))
            # East
            if c < n - 1 and walls_v[r][c] == 0 and not visited[r][c + 1]:
                visited[r][c + 1] = True
                visited_count += 1
                q.append((r, c + 1))

        if visited_count != n * n:
            return False, f"Maze connectivity failure: only {visited_count} of {n * n} cells reachable"

        # 3. Verify solution path
        solution_path = puzzle_data.get("solution_path", [])
        if not solution_path:
            return False, "Missing solution_path"
        if solution_path[0] != (0, 0) and solution_path[0] != [0, 0]:
            return False, f"Solution path does not start at (0, 0): {solution_path[0]}"
        if solution_path[-1] != (n - 1, n - 1) and solution_path[-1] != [n - 1, n - 1]:
            return False, f"Solution path does not end at ({n-1}, {n-1}): {solution_path[-1]}"

        # Verify steps
        for i in range(len(solution_path) - 1):
            r1, c1 = solution_path[i]
            r2, c2 = solution_path[i + 1]
            dr = r2 - r1
            dc = c2 - c1
            if abs(dr) + abs(dc) != 1:
                return False, f"Invalid step from ({r1},{c1}) to ({r2},{c2})"
            if dr == 1 and walls_h[r1][c1] != 0:
                return False, f"Path crosses wall moving South from ({r1},{c1})"
            if dr == -1 and walls_h[r2][c1] != 0:
                return False, f"Path crosses wall moving North from ({r1},{c1})"
            if dc == 1 and walls_v[r1][c1] != 0:
                return False, f"Path crosses wall moving East from ({r1},{c1})"
            if dc == -1 and walls_v[r1][c2] != 0:
                return False, f"Path crosses wall moving West from ({r1},{c1})"

        return True, "All rules satisfied"
