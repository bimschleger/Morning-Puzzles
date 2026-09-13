"""
Morning Puzzles - Lights Plugin (Akari / Light Up)
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


class LightsPuzzle(BasePuzzle):
    """
    Lights (Akari) line-of-sight deduction puzzle.
    Solvers place bulbs to illuminate all white cells without mutual line of sight,
    while matching orthogonal count clues on numbered barrier walls.
    """

    DIFFICULTY_SETTINGS = {
        "easy":    {"size": 6,  "wall_prob": 0.20, "retain_target": 0.85},
        "medium":  {"size": 8,  "wall_prob": 0.20, "retain_target": 0.65},
        "hard":    {"size": 10, "wall_prob": 0.22, "retain_target": 0.45},
        "extreme": {"size": 12, "wall_prob": 0.22, "retain_target": 0.35},
    }

    @property
    def puzzle_id(self) -> str:
        return "lights"

    @property
    def title(self) -> str:
        return "LIGHTS"

    @property
    def has_difficulty(self) -> bool:
        return True

    @property
    def default_difficulty(self) -> str:
        return "medium"

    @property
    def supported_difficulties(self) -> List[str]:
        return ["easy", "medium", "hard", "extreme"]

    def _get_visibility(self, rows: int, cols: int, walls: List[List[int]], r: int, c: int) -> List[Tuple[int, int]]:
        """Returns list of white cells visible from (r, c) including (r, c) itself."""
        if walls[r][c] != -1:
            return []
        vis = [(r, c)]
        for dr in range(r - 1, -1, -1):
            if walls[dr][c] != -1:
                break
            vis.append((dr, c))
        for dr in range(r + 1, rows):
            if walls[dr][c] != -1:
                break
            vis.append((dr, c))
        for dc in range(c - 1, -1, -1):
            if walls[r][dc] != -1:
                break
            vis.append((r, dc))
        for dc in range(c + 1, cols):
            if walls[r][dc] != -1:
                break
            vis.append((r, dc))
        return vis

    def _get_adj_cells(self, rows: int, cols: int, r: int, c: int) -> List[Tuple[int, int]]:
        adj = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                adj.append((nr, nc))
        return adj

    def _solve_deductive(self, rows: int, cols: int, walls: List[List[int]]) -> Tuple[bool, Optional[List[List[int]]]]:
        """
        Pure deductive logic solver for Akari / Lights.
        Returns (is_solved, bulb_grid).
        Only forced logical moves are made; zero guessing/branching.
        """
        white_cells = [(r, c) for r in range(rows) for c in range(cols) if walls[r][c] == -1]
        vis_map = {cell: set(self._get_visibility(rows, cols, walls, cell[0], cell[1])) for cell in white_cells}

        is_bulb: Dict[Tuple[int, int], bool] = {cell: False for cell in white_cells}
        can_be_bulb: Dict[Tuple[int, int], bool] = {cell: True for cell in white_cells}
        is_lit: Dict[Tuple[int, int], bool] = {cell: False for cell in white_cells}

        changed = True

        def place_bulb(br: int, bc: int):
            nonlocal changed
            if is_bulb[(br, bc)]:
                return
            is_bulb[(br, bc)] = True
            is_lit[(br, bc)] = True
            for vr, vc in vis_map[(br, bc)]:
                is_lit[(vr, vc)] = True
                if (vr, vc) != (br, bc) and can_be_bulb[(vr, vc)]:
                    can_be_bulb[(vr, vc)] = False
                    changed = True

        def forbid_bulb(fr: int, fc: int):
            nonlocal changed
            if can_be_bulb[(fr, fc)]:
                can_be_bulb[(fr, fc)] = False
                changed = True

        iterations = 0
        max_iterations = 200

        while changed and iterations < max_iterations:
            changed = False
            iterations += 1

            # Rule 1: Numbered walls
            for r in range(rows):
                for c in range(cols):
                    clue = walls[r][c]
                    if clue < 0:
                        continue
                    adj_white = [cell for cell in self._get_adj_cells(rows, cols, r, c) if walls[cell[0]][cell[1]] == -1]
                    confirmed = [cell for cell in adj_white if is_bulb[cell]]
                    candidates = [cell for cell in adj_white if can_be_bulb[cell] and not is_bulb[cell]]

                    if len(confirmed) > clue or len(confirmed) + len(candidates) < clue:
                        return False, None

                    if len(confirmed) == clue and candidates:
                        for cell in candidates:
                            forbid_bulb(cell[0], cell[1])
                    elif len(confirmed) + len(candidates) == clue and candidates:
                        for cell in candidates:
                            place_bulb(cell[0], cell[1])

            # Rule 2: Unlit white cells with only 1 possible placer
            for r, c in white_cells:
                if not is_lit[(r, c)]:
                    cand_placers = [cell for cell in vis_map[(r, c)] if can_be_bulb[cell]]
                    if len(cand_placers) == 0:
                        return False, None
                    elif len(cand_placers) == 1:
                        br, bc = cand_placers[0]
                        place_bulb(br, bc)

            # Rule 3: Contradiction probe on candidates
            for r, c in white_cells:
                if can_be_bulb[(r, c)] and not is_bulb[(r, c)]:
                    adj_walls = [w for w in self._get_adj_cells(rows, cols, r, c) if walls[w[0]][w[1]] >= 0]
                    for wr, wc in adj_walls:
                        clue = walls[wr][wc]
                        adj_white = [cell for cell in self._get_adj_cells(rows, cols, wr, wc) if walls[cell[0]][cell[1]] == -1]
                        confirmed_cnt = sum(1 for cell in adj_white if is_bulb[cell])
                        if confirmed_cnt + 1 > clue:
                            forbid_bulb(r, c)
                            break

        # Verification of complete logical solution
        for r in range(rows):
            for c in range(cols):
                clue = walls[r][c]
                if clue >= 0:
                    adj_white = [cell for cell in self._get_adj_cells(rows, cols, r, c) if walls[cell[0]][cell[1]] == -1]
                    if sum(1 for cell in adj_white if is_bulb[cell]) != clue:
                        return False, None

        for cell in white_cells:
            if not is_lit[cell]:
                return False, None

        bulb_grid = [[1 if is_bulb.get((r, c), False) else 0 for c in range(cols)] for r in range(rows)]
        return True, bulb_grid

    def generate(
        self,
        difficulty: str = "medium",
        seed: Optional[int] = None,
        **kwargs,
    ) -> BasePuzzleResult:
        if seed is not None:
            random.seed(seed)

        diff_key = difficulty.lower() if difficulty else "medium"
        cfg = self.DIFFICULTY_SETTINGS.get(diff_key, self.DIFFICULTY_SETTINGS["medium"])
        size = cfg["size"]
        rows = cols = size
        wall_prob = cfg["wall_prob"]
        retain_target = cfg["retain_target"]

        for _ in range(80):
            walls = [[-1] * cols for _ in range(rows)]
            num_wall_pairs = int((rows * cols * wall_prob) / 2)
            cells = [(r, c) for r in range(rows) for c in range(cols)]
            random.shuffle(cells)

            placed = 0
            for r, c in cells:
                sr, sc = rows - 1 - r, cols - 1 - c
                if walls[r][c] == -1 and walls[sr][sc] == -1:
                    walls[r][c] = -2
                    walls[sr][sc] = -2
                    placed += 1
                    if placed >= num_wall_pairs:
                        break

            white_cells = [(r, c) for r in range(rows) for c in range(cols) if walls[r][c] == -1]
            if len(white_cells) < size * size * 0.65:
                continue

            vis_map = {cell: self._get_visibility(rows, cols, walls, cell[0], cell[1]) for cell in white_cells}
            if any(len(vis_map[c]) <= 1 for c in white_cells):
                continue

            # Independent dominating set search
            bulbs = set()
            success = False
            for _ in range(25):
                bulbs.clear()
                unlit = set(white_cells)
                forbidden = set()

                while unlit:
                    target = min(unlit, key=lambda c: sum(1 for v in vis_map[c] if v not in forbidden))
                    placers = [v for v in vis_map[target] if v not in forbidden]
                    if not placers:
                        break
                    b = max(placers, key=lambda p: len(set(vis_map[p]) & unlit))
                    bulbs.add(b)
                    for v in vis_map[b]:
                        unlit.discard(v)
                        forbidden.add(v)

                if not unlit and all(b1 == b2 or b2 not in vis_map[b1] for b1 in bulbs for b2 in bulbs):
                    success = True
                    break

            if not success:
                continue

            # Assign initial wall clues
            for r in range(rows):
                for c in range(cols):
                    if walls[r][c] == -2:
                        adj = self._get_adj_cells(rows, cols, r, c)
                        walls[r][c] = sum(1 for ar, ac in adj if (ar, ac) in bulbs)

            # Check deductive solvability
            can_solve, bulb_grid = self._solve_deductive(rows, cols, walls)
            if not can_solve:
                continue

            # Clue thinning to match difficulty
            all_walls = [(r, c) for r in range(rows) for c in range(cols) if walls[r][c] >= 0]
            random.shuffle(all_walls)

            for wr, wc in all_walls:
                old_clue = walls[wr][wc]
                walls[wr][wc] = -2  # unnumbered wall

                can_solve, _ = self._solve_deductive(rows, cols, walls)
                if can_solve:
                    current_numbered = sum(1 for r in range(rows) for c in range(cols) if walls[r][c] >= 0)
                    if current_numbered <= len(all_walls) * retain_target:
                        pass
                else:
                    walls[wr][wc] = old_clue

            # Final deductive pass
            can_solve, final_grid = self._solve_deductive(rows, cols, walls)
            if can_solve and final_grid is not None:
                bulb_list = [[r, c] for r, c in bulbs]
                total_bulbs = len(bulbs)

                raw_data = {
                    "rows": rows,
                    "cols": cols,
                    "size": size,
                    "puzzle": walls,
                    "solution": final_grid,
                    "bulbs": bulb_list,
                    "total_bulbs": total_bulbs,
                    "difficulty": diff_key,
                }

                instruction = self.get_instruction(raw_data)
                return BasePuzzleResult(
                    puzzle_type=self.puzzle_id,
                    title=self.title,
                    difficulty=diff_key,
                    instruction=instruction,
                    raw_data=raw_data,
                )

        raise RuntimeError(f"Failed to generate valid LIGHTS puzzle for difficulty '{diff_key}'")

    def get_instruction(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        total_bulbs = puzzle_data.get("total_bulbs", 10)
        return f"Place {total_bulbs} bulbs to light all corridors without bulbs shining on each other or exceeding numbers."

    def format_ascii_puzzle(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        rows = puzzle_data.get("rows", 8)
        cols = puzzle_data.get("cols", 8)
        puzzle = puzzle_data.get("puzzle", [])
        total_bulbs = puzzle_data.get("total_bulbs", 10)

        lines = [f"TOTAL BULBS: {total_bulbs}", ""]
        sep = "   +" + "---+" * cols
        lines.append(sep)

        for r in range(rows):
            line = "   |"
            for c in range(cols):
                val = puzzle[r][c] if r < len(puzzle) and c < len(puzzle[r]) else -1
                if val >= 0:
                    line += f" {val} |"
                elif val == -2:
                    line += " # |"
                else:
                    line += "   |"
            lines.append(line)
            lines.append(sep)

        return "\n".join(lines)

    def format_solution_key(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> List[str]:
        rows = puzzle_data.get("rows", 8)
        cols = puzzle_data.get("cols", 8)
        puzzle = puzzle_data.get("puzzle", [])
        sol = puzzle_data.get("solution", [])
        if not sol:
            return []

        lines = []
        for r in range(rows):
            row_str = "      "
            for c in range(cols):
                p_val = puzzle[r][c] if r < len(puzzle) and c < len(puzzle[r]) else -1
                if p_val >= 0:
                    row_str += f"{p_val} "
                elif p_val == -2:
                    row_str += "# "
                elif r < len(sol) and c < len(sol[r]) and sol[r][c] == 1:
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
        size = puzzle_data.get("size", puzzle_data.get("rows", 8))
        rows = cols = size
        puzzle = puzzle_data.get("puzzle", [])

        padding = 24
        board_size = target_width - padding * 2
        cell_size = board_size // size
        actual_board = cell_size * size
        total_h = padding + actual_board + padding

        # Pillow rendering
        if HAS_PILLOW:
            img = Image.new("L", (target_width, total_h), 255)
            draw = ImageDraw.Draw(img)

            # Heavy outer boundary (Tier 1: 4px)
            draw.rectangle(
                [padding, padding, padding + actual_board, padding + actual_board],
                outline=0,
                width=4,
            )

            # Internal grid dividers (Tier 4: 1px)
            for r in range(1, size):
                y = padding + r * cell_size
                draw.line([padding, y, padding + actual_board, y], fill=0, width=1)
            for c in range(1, size):
                x = padding + c * cell_size
                draw.line([x, padding, x, padding + actual_board], fill=0, width=1)

            # Clue font
            font_size = max(16, int(cell_size * 0.52))
            try:
                font_clue = ImageFont.truetype("Courier.ttf", font_size)
            except IOError:
                font_clue = ImageFont.load_default()

            # Render barrier cells
            margin = max(2, int(cell_size * 0.06))
            for r in range(rows):
                for c in range(cols):
                    val = puzzle[r][c] if r < len(puzzle) and c < len(puzzle[r]) else -1
                    if val != -1:
                        x0 = padding + c * cell_size + margin
                        y0 = padding + r * cell_size + margin
                        x1 = padding + (c + 1) * cell_size - margin
                        y1 = padding + (r + 1) * cell_size - margin

                        draw.rectangle([x0, y0, x1, y1], fill=0)

                        if val >= 0:
                            digit_str = str(val)
                            try:
                                bbox = font_clue.getbbox(digit_str)
                                tw = bbox[2] - bbox[0]
                                th = bbox[3] - bbox[1]
                            except AttributeError:
                                tw, th = draw.textsize(digit_str, font=font_clue)

                            tx = padding + c * cell_size + (cell_size - tw) // 2
                            ty = padding + r * cell_size + (cell_size - th) // 2
                            draw.text((tx, ty), digit_str, fill=255, font=font_clue)
                        else:
                            draw.line([x0 + 4, y0 + 4, x1 - 4, y1 - 4], fill=255, width=1)
                            draw.line([x0 + 4, y1 - 4, x1 - 4, y0 + 4], fill=255, width=1)

            # Convert 1-bit ESC/POS GS v 0
            img_1bit = img.convert("1")
            raw_bytes = img_1bit.tobytes()
            return image_to_escpos_raster(raw_bytes, target_width, total_h)

        # Fallback pure-Python ThermalBitmap
        tb = ThermalBitmap(target_width, total_h)
        tb.draw_rect(padding, padding, actual_board, actual_board, thickness=4)

        for r in range(1, size):
            tb.draw_hline(padding, padding + r * cell_size, actual_board, thickness=1)
        for c in range(1, size):
            tb.draw_vline(padding + c * cell_size, padding, actual_board, thickness=1)

        for r in range(rows):
            for c in range(cols):
                val = puzzle[r][c] if r < len(puzzle) and c < len(puzzle[r]) else -1
                if val != -1:
                    cx = padding + c * cell_size
                    cy = padding + r * cell_size
                    tb.draw_rect(cx + 2, cy + 2, cell_size - 4, cell_size - 4, thickness=2)
                    if val >= 0:
                        tb.draw_char(cx + (cell_size - 18) // 2, cy + (cell_size - 21) // 2, str(val), scale=2)

        return tb.to_escpos()

    def verify_accuracy(
        self,
        puzzle_data: Union[BasePuzzleResult, Dict[str, Any]],
    ) -> Tuple[bool, str]:
        puzzle = puzzle_data.get("puzzle")
        solution = puzzle_data.get("solution")
        bulbs = puzzle_data.get("bulbs")

        if not puzzle or not isinstance(puzzle, list):
            return False, "Lights puzzle grid missing or invalid"
        if not solution or not isinstance(solution, list):
            return False, "Lights solution grid missing or invalid"

        rows = len(puzzle)
        cols = len(puzzle[0]) if rows > 0 else 0
        if rows != cols:
            return False, f"Lights grid must be square, got {rows}x{cols}"

        # 1. Check bulb placements
        bulb_coords = set()
        for r in range(rows):
            for c in range(cols):
                if solution[r][c] == 1:
                    if puzzle[r][c] != -1:
                        return False, f"Bulb placed in wall cell ({r}, {c})"
                    bulb_coords.add((r, c))

        if bulbs is not None and len(bulb_coords) != len(bulbs):
            return False, f"Bulbs count mismatch: solution has {len(bulb_coords)}, data has {len(bulbs)}"

        # 2. No two bulbs can illuminate each other
        vis_map = {cell: set(self._get_visibility(rows, cols, puzzle, cell[0], cell[1]))
                   for r in range(rows) for c in range(cols) if puzzle[r][c] == -1 for cell in [(r, c)]}

        for b1 in bulb_coords:
            for b2 in bulb_coords:
                if b1 != b2 and b2 in vis_map.get(b1, set()):
                    return False, f"Bulbs at {b1} and {b2} shine on each other"

        # 3. All white cells must be lit
        lit_cells = set()
        for b in bulb_coords:
            lit_cells.update(vis_map.get(b, set()))

        for r in range(rows):
            for c in range(cols):
                if puzzle[r][c] == -1 and (r, c) not in lit_cells:
                    return False, f"White cell ({r}, {c}) is not illuminated"

        # 4. Numbered wall clues must be strictly satisfied
        for r in range(rows):
            for c in range(cols):
                clue = puzzle[r][c]
                if clue >= 0:
                    adj = self._get_adj_cells(rows, cols, r, c)
                    adj_bulbs = sum(1 for ar, ac in adj if (ar, ac) in bulb_coords)
                    if adj_bulbs != clue:
                        return False, f"Wall at ({r}, {c}) has clue {clue} but has {adj_bulbs} adjacent bulbs"

        # 5. Logical solvability check
        can_solve, deduced_solution = self._solve_deductive(rows, cols, puzzle)
        if not can_solve:
            return False, "Lights puzzle cannot be solved by pure deductive logic"
        if deduced_solution != solution:
            return False, "Deduced solution does not match generated solution"

        return True, "All rules satisfied"
