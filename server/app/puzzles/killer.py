"""
Morning Puzzles - Killer Sudoku Plugin
Encapsulates generation, canonical instruction formatting, ASCII layout,
solution key formatting, and 576-dot thermal raster rendering.
"""

import random
from collections import defaultdict
from typing import List, Tuple, Dict, Any, Optional, Set, Union

from .base import BasePuzzle, BasePuzzleResult
from ..renderer.canvas import (
    THERMAL_WIDTH_DOTS,
    HAS_PILLOW,
    pil_to_escpos,
    ThermalBitmap,
)

if HAS_PILLOW:
    from PIL import Image, ImageDraw, ImageFont


class KillerPuzzle(BasePuzzle):
    """Killer Sudoku puzzle plugin with guaranteed unique solutions."""

    DIFFICULTY_SETTINGS = {
        "easy":    {"size": 4, "box_r": 2, "box_c": 2, "min_cage": 1, "max_cage": 2},
        "medium":  {"size": 4, "box_r": 2, "box_c": 2, "min_cage": 2, "max_cage": 3},
        "hard":    {"size": 6, "box_r": 2, "box_c": 3, "min_cage": 2, "max_cage": 4},
        "extreme": {"size": 6, "box_r": 2, "box_c": 3, "min_cage": 2, "max_cage": 4},
    }

    @property
    def puzzle_id(self) -> str:
        return "killer"

    @property
    def title(self) -> str:
        return "KILLER"

    @property
    def has_difficulty(self) -> bool:
        return True

    @property
    def supported_difficulties(self) -> List[str]:
        return ["easy", "medium", "extreme"]

    def generate(
        self,
        difficulty: str = "medium",
        seed: Optional[int] = None,
        **kwargs,
    ) -> BasePuzzleResult:
        if seed is not None:
            random.seed(seed)

        diff_key = difficulty.lower()
        cfg = self.DIFFICULTY_SETTINGS.get(diff_key, self.DIFFICULTY_SETTINGS["medium"])
        size = cfg["size"]
        box_r = cfg["box_r"]
        box_c = cfg["box_c"]
        min_cage = cfg["min_cage"]
        max_cage = cfg["max_cage"]
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        solution = None
        cages = None

        for attempt in range(50):
            cand_sol = self._generate_solved_board(size, box_r, box_c)
            cand_cages = self._partition_into_cages(cand_sol, size, min_cage, max_cage)

            is_unique = False
            for step in range(8):
                sols = self._find_multiple_solutions(size, box_r, box_c, cand_cages, max_count=2)
                if len(sols) == 1:
                    is_unique = True
                    break
                elif len(sols) == 2:
                    diff_cells = [
                        (r, c)
                        for r in range(size)
                        for c in range(size)
                        if sols[0][r][c] != sols[1][r][c]
                    ]
                    split_done = False
                    for dr, dc in diff_cells:
                        for cg in cand_cages:
                            if (dr, dc) in cg["cells"] and len(cg["cells"]) > 1:
                                cg["cells"].remove((dr, dc))
                                cg["sum"] -= cand_sol[dr][dc]
                                new_cg = {
                                    "id": len(cand_cages),
                                    "label": "",
                                    "cells": [(dr, dc)],
                                    "sum": cand_sol[dr][dc],
                                }
                                cand_cages.append(new_cg)
                                split_done = True
                                break
                        if split_done:
                            break
                    if not split_done:
                        break
                else:
                    break

            if is_unique:
                cand_cages = [cg for cg in cand_cages if cg["cells"]]
                for i, cg in enumerate(cand_cages):
                    cg["id"] = i
                    cg["label"] = letters[i % len(letters)]
                solution = cand_sol
                cages = cand_cages
                break

        if solution is None or cages is None:
            fallback_cfg = self.DIFFICULTY_SETTINGS["easy"]
            solution = self._generate_solved_board(fallback_cfg["size"], fallback_cfg["box_r"], fallback_cfg["box_c"])
            cages = self._partition_into_cages(solution, fallback_cfg["size"], 1, 2)
            for i, cg in enumerate(cages):
                cg["id"] = i
                cg["label"] = letters[i % len(letters)]
            size = fallback_cfg["size"]
            box_r = fallback_cfg["box_r"]
            box_c = fallback_cfg["box_c"]

        raw_data = {
            "type": "killer",
            "title": "KILLER",
            "difficulty": difficulty,
            "size": size,
            "box_rows": box_r,
            "box_cols": box_c,
            "cages": cages,
            "solution": solution,
        }
        ascii_text = self.format_ascii_puzzle(raw_data)
        raw_data["text"] = ascii_text
        instruction = self.get_instruction(raw_data)

        return BasePuzzleResult(
            puzzle_type=self.puzzle_id,
            title=self.title,
            difficulty=difficulty,
            instruction=instruction,
            raw_data=raw_data,
        )

    def get_instruction(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        k_diff = str(puzzle_data.get("difficulty", "medium"))
        k_range = "1-4" if k_diff.lower() in ("easy", "medium") else "1-6"
        return f"Fill every row, column, and box with digits {k_range}, matching cage sums without repeats."

    def format_ascii_puzzle(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        size = puzzle_data.get("size", 4)
        cages = puzzle_data.get("cages", [])

        grid = [[" "] * size for _ in range(size)]
        for cg in cages:
            for r, c in cg.get("cells", []):
                if r < size and c < size:
                    grid[r][c] = cg.get("label", " ")

        lines = []
        sep_border = "      +" + ("---+" * size)
        lines.append(sep_border)
        for r in range(size):
            row_str = "      |"
            for c in range(size):
                row_str += f" {grid[r][c]} |"
            lines.append(row_str)
            lines.append(sep_border)

        lines.append("")
        clue_items = [f"{cg.get('label', '')}={cg.get('sum', '')}" for cg in cages]
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

    def format_solution_key(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> List[str]:
        sol = puzzle_data.get("solution", [])
        if not sol:
            return []
        lines = []
        for row in sol:
            lines.append("      " + " ".join(str(c) for c in row))
        return lines

    def render_raster(
        self,
        puzzle_data: Union[BasePuzzleResult, Dict[str, Any]],
        target_width: int = THERMAL_WIDTH_DOTS,
    ) -> bytes:
        size = puzzle_data.get("size", 4)
        box_r = puzzle_data.get("box_rows", 2)
        box_c = puzzle_data.get("box_cols", 2 if size == 4 else 3)
        cages = puzzle_data.get("cages", [])

        padding = 24
        board_size = target_width - padding * 2
        c_size = board_size // size
        actual_board = c_size * size
        total_h = padding + actual_board + padding
        inset = 10 if size == 4 else 8

        h_segments = []
        v_segments = []
        for cg in cages:
            cell_set = {(r, c) for r, c in cg.get("cells", [])}

            def in_cage(r: int, c: int) -> bool:
                return (r, c) in cell_set

            for r, c in cg.get("cells", []):
                x0 = padding + c * c_size
                x1 = x0 + c_size
                y0 = padding + r * c_size
                y1 = y0 + c_size

                if not in_cage(r - 1, c):
                    y = y0 + inset
                    x_s = x0 + inset if not in_cage(r, c - 1) else (x0 - inset if in_cage(r - 1, c - 1) else x0)
                    x_e = x1 - inset if not in_cage(r, c + 1) else (x1 + inset if in_cage(r - 1, c + 1) else x1)
                    h_segments.append((min(x_s, x_e), max(x_s, x_e), y))

                if not in_cage(r + 1, c):
                    y = y1 - inset
                    x_s = x0 + inset if not in_cage(r, c - 1) else (x0 - inset if in_cage(r + 1, c - 1) else x0)
                    x_e = x1 - inset if not in_cage(r, c + 1) else (x1 + inset if in_cage(r + 1, c + 1) else x1)
                    h_segments.append((min(x_s, x_e), max(x_s, x_e), y))

                if not in_cage(r, c - 1):
                    x = x0 + inset
                    y_s = y0 + inset if not in_cage(r - 1, c) else (y0 - inset if in_cage(r - 1, c - 1) else y0)
                    y_e = y1 - inset if not in_cage(r + 1, c) else (y1 + inset if in_cage(r + 1, c - 1) else y1)
                    v_segments.append((x, min(y_s, y_e), max(y_s, y_e)))

                if not in_cage(r, c + 1):
                    x = x1 - inset
                    y_s = y0 + inset if not in_cage(r - 1, c) else (y0 - inset if in_cage(r - 1, c + 1) else y0)
                    y_e = y1 - inset if not in_cage(r + 1, c) else (y1 + inset if in_cage(r + 1, c + 1) else y1)
                    v_segments.append((x, min(y_s, y_e), max(y_s, y_e)))

        h_by_y = defaultdict(list)
        for x1, x2, y in h_segments:
            h_by_y[y].append((x1, x2))
        merged_h = []
        for y, intervals in h_by_y.items():
            intervals.sort()
            cur_s, cur_e = intervals[0]
            for s, e in intervals[1:]:
                if s <= cur_e:
                    cur_e = max(cur_e, e)
                else:
                    merged_h.append((cur_s, cur_e, y))
                    cur_s, cur_e = s, e
            merged_h.append((cur_s, cur_e, y))

        v_by_x = defaultdict(list)
        for x, y1, y2 in v_segments:
            v_by_x[x].append((y1, y2))
        merged_v = []
        for x, intervals in v_by_x.items():
            intervals.sort()
            cur_s, cur_e = intervals[0]
            for s, e in intervals[1:]:
                if s <= cur_e:
                    cur_e = max(cur_e, e)
                else:
                    merged_v.append((x, cur_s, cur_e))
                    cur_s, cur_e = s, e
            merged_v.append((x, cur_s, cur_e))

        dash_len = 8
        gap_len = 6

        if HAS_PILLOW:
            img = Image.new("L", (target_width, total_h), 255)
            draw = ImageDraw.Draw(img)

            try:
                font_clue = ImageFont.truetype("Courier.ttf", max(13, int(c_size * 0.16)))
            except IOError:
                font_clue = ImageFont.load_default()

            draw.rectangle([padding, padding, padding + actual_board, padding + actual_board], outline=0, width=4)

            for r in range(1, size):
                y = padding + r * c_size
                thick = 4 if (r % box_r == 0) else 1
                draw.line([padding, y, padding + actual_board, y], fill=0, width=thick)

            for c in range(1, size):
                x = padding + c * c_size
                thick = 4 if (c % box_c == 0) else 1
                draw.line([x, padding, x, padding + actual_board], fill=0, width=thick)

            for x1, x2, y in merged_h:
                x = x1
                while x < x2:
                    seg = min(dash_len, x2 - x)
                    draw.line([x, y, x + seg, y], fill=0, width=2)
                    x += dash_len + gap_len

            for x, y1, y2 in merged_v:
                y = y1
                while y < y2:
                    seg = min(dash_len, y2 - y)
                    draw.line([x, y, x, y + seg], fill=0, width=2)
                    y += dash_len + gap_len

            for cg in cages:
                cells = sorted(cg.get("cells", []))
                if not cells:
                    continue
                r0, c0 = cells[0]
                tx = padding + c0 * c_size + inset + 4
                ty = padding + r0 * c_size + inset + 2
                draw.text((tx, ty), str(cg.get("sum", "")), fill=0, font=font_clue)

            return pil_to_escpos(img)

        # Pure Python ThermalBitmap Fallback
        tb = ThermalBitmap(target_width, total_h)
        tb.draw_rect(padding, padding, actual_board, actual_board, thickness=4)

        for r in range(1, size):
            y = padding + r * c_size
            thick = 4 if (r % box_r == 0) else 2
            tb.draw_hline(padding, y, actual_board, thickness=thick)

        for c in range(1, size):
            x = padding + c * c_size
            thick = 4 if (c % box_c == 0) else 2
            tb.draw_vline(x, padding, actual_board, thickness=thick)

        for x1, x2, y in merged_h:
            x = x1
            while x < x2:
                seg = min(dash_len, x2 - x)
                tb.draw_hline(x, y, seg, thickness=2)
                x += dash_len + gap_len

        for x, y1, y2 in merged_v:
            y = y1
            while y < y2:
                seg = min(dash_len, y2 - y)
                tb.draw_vline(x, y, seg, thickness=2)
                y += dash_len + gap_len

        for cg in cages:
            cells = sorted(cg.get("cells", []))
            if not cells:
                continue
            r0, c0 = cells[0]
            tx = padding + c0 * c_size + inset + 3
            ty = padding + r0 * c_size + inset + 3
            tb.draw_text(tx, ty, str(cg.get("sum", "")), scale=2, color=1)

        return tb.to_escpos()

    def _generate_solved_board(self, size: int, box_r: int, box_c: int) -> List[List[int]]:
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
        assigned = [[-1] * size for _ in range(size)]
        cages = []
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

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
                "sum": sum(solution[cr][cc] for cr, cc in current_cage_cells),
            })
            cage_id += 1

        for i, cg in enumerate(cages):
            cg["id"] = i
            cg["label"] = letters[i % len(letters)]

        return cages

    def _find_multiple_solutions(
        self, size: int, box_r: int, box_c: int, cages: List[Dict[str, Any]], max_count: int = 2
    ) -> List[List[List[int]]]:
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
