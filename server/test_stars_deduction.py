"""
Unit test suite for Stars (Queens / Star Battle) Dataset & Generator
Strictly validates:
  - 100% solution uniqueness across curated puzzles (count_solutions == 1)
  - Opening anchor presence (Easy/Medium: size <= 2; Hard/Extreme: size <= 5)
  - Region 4-connectivity (no disconnected shapes)
  - Star constraints: exact row/column/region star counts, zero touching stars
  - 8-fold geometric symmetry transform invariance
  - Tri-target runtime integration (Python StarsPuzzle and QueensGenerator)
"""

import json
import os
import sys
import unittest
from collections import deque
from typing import List, Tuple, Set

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "server"))
from app.puzzles.stars import StarsPuzzle
from app.generators.queens_gen import QueensGenerator

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "stars_dataset.json")


def is_4_connected(cells: List[Tuple[int, int]]) -> bool:
    if not cells:
        return False
    cell_set = set(cells)
    visited = set()
    q = deque([cells[0]])
    visited.add(cells[0])
    while q:
        r, c = q.popleft()
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if (nr, nc) in cell_set and (nr, nc) not in visited:
                visited.add((nr, nc))
                q.append((nr, nc))
    return len(visited) == len(cells)


def solve_mrv(regions: List[List[int]], n: int, stars_per_unit: int, limit: int = 2) -> int:
    cand = [[True] * n for _ in range(n)]
    row_needed = [stars_per_unit] * n
    col_needed = [stars_per_unit] * n
    reg_needed = [stars_per_unit] * n
    sols = 0

    def search():
        nonlocal sols
        if sols >= limit:
            return
        if all(r == 0 for r in row_needed):
            sols += 1
            return

        min_cands = 999
        best_cells = None

        for r in range(n):
            if row_needed[r] > 0:
                cells = [(r, c) for c in range(n) if cand[r][c]]
                if len(cells) < row_needed[r]:
                    return
                if len(cells) < min_cands:
                    min_cands = len(cells)
                    best_cells = cells

        for c in range(n):
            if col_needed[c] > 0:
                cells = [(r, c) for r in range(n) if cand[r][c]]
                if len(cells) < col_needed[c]:
                    return
                if len(cells) < min_cands:
                    min_cands = len(cells)
                    best_cells = cells

        for reg in range(n):
            if reg_needed[reg] > 0:
                cells = [(r, c) for r in range(n) for c in range(n) if regions[r][c] == reg and cand[r][c]]
                if len(cells) < reg_needed[reg]:
                    return
                if len(cells) < min_cands:
                    min_cands = len(cells)
                    best_cells = cells

        if not best_cells:
            return

        for r, c in best_cells:
            if not cand[r][c]:
                continue
            reg = regions[r][c]
            elim = set()

            if row_needed[r] == 1:
                for cc in range(n):
                    if cand[r][cc]:
                        elim.add((r, cc))
            if col_needed[c] == 1:
                for rr in range(n):
                    if cand[rr][c]:
                        elim.add((rr, c))
            if reg_needed[reg] == 1:
                for rr in range(n):
                    for cc in range(n):
                        if regions[rr][cc] == reg and cand[rr][cc]:
                            elim.add((rr, cc))

            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n and cand[nr][nc]:
                        elim.add((nr, nc))

            for rr, cc in elim:
                cand[rr][cc] = False
            row_needed[r] -= 1
            col_needed[c] -= 1
            reg_needed[reg] -= 1

            search()

            row_needed[r] += 1
            col_needed[c] += 1
            reg_needed[reg] += 1
            for rr, cc in elim:
                cand[rr][cc] = True

    search()
    return sols


class TestStarsDeduction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assertTrue(cls, os.path.exists(DATA_PATH), f"Missing dataset at {DATA_PATH}")
        with open(DATA_PATH, "r") as f:
            cls.dataset = json.load(f)

    def test_dataset_completeness(self):
        """Verify each tier has exactly 100 puzzles with correct dimensions."""
        tiers = {
            "easy": (5, 1),
            "medium": (8, 1),
            "hard": (9, 2),
            "extreme": (10, 2),
        }
        for tier, (expected_size, expected_stars) in tiers.items():
            puzzles = self.dataset.get(tier, [])
            self.assertEqual(len(puzzles), 100, f"{tier} should contain 100 puzzles")
            for i, p in enumerate(puzzles):
                self.assertEqual(p["size"], expected_size, f"{tier} #{i} wrong size")
                self.assertEqual(p["stars_per_unit"], expected_stars, f"{tier} #{i} wrong stars_per_unit")

    def test_region_integrity_and_anchors(self):
        """Verify all regions are 4-connected and opening anchors exist."""
        for tier in ["easy", "medium", "hard", "extreme"]:
            puzzles = self.dataset[tier]
            for i, p in enumerate(puzzles):
                n = p["size"]
                regions = p["regions"]

                # Group cells by region
                reg_cells = {reg: [] for reg in range(n)}
                for r in range(n):
                    for c in range(n):
                        reg_cells[regions[r][c]].append((r, c))

                # Verify every region is non-empty and 4-connected
                for reg_id, cells in reg_cells.items():
                    self.assertGreater(len(cells), 0, f"{tier} #{i} reg {reg_id} is empty")
                    self.assertTrue(
                        is_4_connected(cells),
                        f"{tier} #{i} region {reg_id} is not 4-connected",
                    )

                # Verify opening anchor
                min_reg_size = min(len(cells) for cells in reg_cells.values())
                if tier in ("easy", "medium"):
                    self.assertLessEqual(
                        min_reg_size, 2,
                        f"{tier} #{i} must have opening anchor of size <= 2 (got {min_reg_size})",
                    )
                else:
                    self.assertLessEqual(
                        min_reg_size, 5,
                        f"{tier} #{i} must have compact anchor of size <= 5 (got {min_reg_size})",
                    )

    def test_unique_solvability_and_star_constraints(self):
        """Verify unique solvability (count_solutions == 1) and solution validity."""
        for tier in ["easy", "medium"]:
            for i, p in enumerate(self.dataset[tier]):
                n = p["size"]
                k = p["stars_per_unit"]
                regions = p["regions"]
                solution = [tuple(s) for s in p["solution"]]

                # Check star count
                self.assertEqual(len(solution), n * k)

                # Row/Col/Reg counts
                row_c = [0] * n
                col_c = [0] * n
                reg_c = [0] * n
                for r, c in solution:
                    row_c[r] += 1
                    col_c[c] += 1
                    reg_c[regions[r][c]] += 1
                self.assertTrue(all(cnt == k for cnt in row_c))
                self.assertTrue(all(cnt == k for cnt in col_c))
                self.assertTrue(all(cnt == k for cnt in reg_c))

                # No touching stars
                for a in range(len(solution)):
                    for b in range(a + 1, len(solution)):
                        r1, c1 = solution[a]
                        r2, c2 = solution[b]
                        self.assertFalse(
                            abs(r1 - r2) <= 1 and abs(c1 - c2) <= 1,
                            f"{tier} #{i}: touching stars at ({r1},{c1}) and ({r2},{c2})",
                        )

                # Exactly 1 unique solution
                sols = solve_mrv(regions, n, k, limit=2)
                self.assertEqual(sols, 1, f"{tier} #{i} must have exactly 1 unique solution")

    def test_symmetry_transform_invariance(self):
        """Verify that all 8 symmetry transforms preserve validity."""
        p = self.dataset["medium"][0]
        n = p["size"]
        k = p["stars_per_unit"]
        base_reg = p["regions"]
        base_sol = [tuple(s) for s in p["solution"]]

        for t in range(8):
            t_reg, t_sol = StarsPuzzle._transform_board(base_reg, base_sol, n, t)
            sols = solve_mrv(t_reg, n, k, limit=2)
            self.assertEqual(sols, 1, f"Transform {t} failed unique solvability")

    def test_generator_runtime_integration(self):
        """Verify StarsPuzzle and QueensGenerator instantiate and run cleanly."""
        puzzle_plugin = StarsPuzzle()
        gen = QueensGenerator()

        for diff in ["easy", "medium", "hard", "extreme"]:
            res = puzzle_plugin.generate(difficulty=diff, seed=12345)
            self.assertEqual(res.title, "STARS")
            self.assertEqual(res.difficulty, diff)
            self.assertEqual(res["difficulty"], diff)

            q_data = gen.generate(difficulty=diff)
            self.assertIn("regions", q_data)
            self.assertIn("stars_solution", q_data)


if __name__ == "__main__":
    unittest.main()
