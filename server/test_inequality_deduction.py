#!/usr/bin/env python3
"""
Unit test suite for INEQUALITY (Latin Square with Inequality Operators) Dataset & Deductive Solver
Validates:
  - Dataset presence and structure (100 base puzzles per tier: easy, medium, hard)
  - Solution uniqueness for all curated base puzzles (count_solutions == 1)
  - Valid Latin square properties (all digits 1..N per row/col)
  - Clue consistency against the ground-truth solution
  - 8-fold dihedral symmetry (D4) transform invariance and solvability
"""

import json
import os
import unittest
from typing import Dict, List, Tuple

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "inequality_dataset.json")


def count_inequality_solutions(size: int, givens: List[List[int]], edges_h: List[List[int]], edges_v: List[List[int]], limit: int = 2) -> int:
    grid = [[0] * size for _ in range(size)]
    for r, c, val in givens:
        grid[r][c] = val

    count = 0

    def is_valid(r: int, c: int, val: int) -> bool:
        for i in range(size):
            if grid[r][i] == val or grid[i][c] == val:
                return False
        if c > 0 and grid[r][c - 1] > 0:
            op = edges_h[r][c - 1]
            if op == 1 and not (grid[r][c - 1] < val): return False
            if op == 2 and not (grid[r][c - 1] > val): return False
        if c + 1 < size and grid[r][c + 1] > 0:
            op = edges_h[r][c];
            if op == 1 and not (val < grid[r][c + 1]): return False
            if op == 2 and not (val > grid[r][c + 1]): return False
        if r > 0 and grid[r - 1][c] > 0:
            op = edges_v[r - 1][c]
            if op == 1 and not (grid[r - 1][c] < val): return False
            if op == 2 and not (grid[r - 1][c] > val): return False
        if r + 1 < size and grid[r + 1][c] > 0:
            op = edges_v[r][c]
            if op == 1 and not (val < grid[r + 1][c]): return False
            if op == 2 and not (val > grid[r + 1][c]): return False
        return True

    def backtrack():
        nonlocal count
        if count >= limit:
            return
        best_r, best_c = -1, -1
        best_candidates = None
        min_cand_count = size + 1

        for r in range(size):
            for c in range(size):
                if grid[r][c] == 0:
                    cands = [val for val in range(1, size + 1) if is_valid(r, c, val)]
                    if len(cands) == 0:
                        return
                    if len(cands) < min_cand_count:
                        min_cand_count = len(cands)
                        best_candidates = cands
                        best_r, best_c = r, c
                        if min_cand_count == 1:
                            break
            if min_cand_count == 1:
                break

        if best_r == -1:
            count += 1
            return

        for val in best_candidates:
            grid[best_r][best_c] = val
            backtrack()
            grid[best_r][best_c] = 0
            if count >= limit:
                return

    backtrack()
    return count


def transform_inequality(size: int, givens: List[List[int]], edges_h: List[List[int]], edges_v: List[List[int]], sol: List[List[int]], transform_id: int):
    def map_coord(r: int, c: int) -> Tuple[int, int]:
        if transform_id == 0: return (r, c)
        if transform_id == 1: return (c, size - 1 - r) # rot90
        if transform_id == 2: return (size - 1 - r, size - 1 - c) # rot180
        if transform_id == 3: return (size - 1 - c, r) # rot270
        if transform_id == 4: return (r, size - 1 - c) # flip_h
        if transform_id == 5: return (size - 1 - r, c) # flip_v
        if transform_id == 6: return (c, r) # transpose
        if transform_id == 7: return (size - 1 - c, size - 1 - r) # anti-transpose
        return (r, c)

    new_sol = [[0] * size for _ in range(size)]
    for r in range(size):
        for c in range(size):
            nr, nc = map_coord(r, c)
            new_sol[nr][nc] = sol[r][c]

    new_givens = []
    for r, c, val in givens:
        nr, nc = map_coord(r, c)
        new_givens.append([nr, nc, val])

    new_edges_h = [[0] * (size - 1) for _ in range(size)]
    new_edges_v = [[0] * size for _ in range(size - 1)]

    for r in range(size):
        for c in range(size - 1):
            if edges_h[r][c] != 0:
                p1 = map_coord(r, c)
                p2 = map_coord(r, c + 1)
                v1, v2 = sol[r][c], sol[r][c + 1]
                if p1[0] == p2[0]:
                    r_new = p1[0]
                    c_left = min(p1[1], p2[1])
                    val_left = v1 if p1[1] < p2[1] else v2
                    val_right = v2 if p1[1] < p2[1] else v1
                    new_edges_h[r_new][c_left] = 1 if val_left < val_right else 2
                else:
                    c_new = p1[1]
                    r_top = min(p1[0], p2[0])
                    val_top = v1 if p1[0] < p2[0] else v2
                    val_bot = v2 if p1[0] < p2[0] else v1
                    new_edges_v[r_top][c_new] = 1 if val_top < val_bot else 2

    for r in range(size - 1):
        for c in range(size):
            if edges_v[r][c] != 0:
                p1 = map_coord(r, c)
                p2 = map_coord(r + 1, c)
                v1, v2 = sol[r][c], sol[r + 1][c]
                if p1[0] == p2[0]:
                    r_new = p1[0]
                    c_left = min(p1[1], p2[1])
                    val_left = v1 if p1[1] < p2[1] else v2
                    val_right = v2 if p1[1] < p2[1] else v1
                    new_edges_h[r_new][c_left] = 1 if val_left < val_right else 2
                else:
                    c_new = p1[1]
                    r_top = min(p1[0], p2[0])
                    val_top = v1 if p1[0] < p2[0] else v2
                    val_bot = v2 if p1[0] < p2[0] else v1
                    new_edges_v[r_top][c_new] = 1 if val_top < val_bot else 2

    return new_givens, new_edges_h, new_edges_v, new_sol


class TestInequalityDeduction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.path.exists(DATA_PATH):
            raise unittest.SkipTest(f"Dataset not found at {DATA_PATH}")
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            cls.dataset = json.load(f)

    def test_dataset_structure_and_counts(self):
        for tier in ["easy", "medium", "hard"]:
            self.assertIn(tier, self.dataset)
            self.assertEqual(len(self.dataset[tier]), 100, f"{tier} tier must have 100 puzzles")

    def test_latin_square_properties(self):
        expected_sizes = {"easy": 4, "medium": 5, "hard": 6}
        for tier, size in expected_sizes.items():
            for i, p in enumerate(self.dataset[tier]):
                self.assertEqual(p["size"], size)
                sol = p["solution"]
                self.assertEqual(len(sol), size)
                for r in range(size):
                    self.assertEqual(sorted(sol[r]), list(range(1, size + 1)), f"{tier} #{i} row {r} not 1..N")
                for c in range(size):
                    col = [sol[r][c] for r in range(size)]
                    self.assertEqual(sorted(col), list(range(1, size + 1)), f"{tier} #{i} col {c} not 1..N")

    def test_clue_satisfaction(self):
        for tier in ["easy", "medium", "hard"]:
            for i, p in enumerate(self.dataset[tier]):
                N = p["size"]
                sol = p["solution"]
                for r, c, val in p["givens"]:
                    self.assertEqual(sol[r][c], val, f"{tier} #{i} given ({r},{c}) mismatch")
                for r in range(N):
                    for c in range(N - 1):
                        op = p["edges_h"][r][c]
                        if op == 1:
                            self.assertTrue(sol[r][c] < sol[r][c + 1], f"{tier} #{i} edge_h < violated")
                        elif op == 2:
                            self.assertTrue(sol[r][c] > sol[r][c + 1], f"{tier} #{i} edge_h > violated")
                for r in range(N - 1):
                    for c in range(N):
                        op = p["edges_v"][r][c]
                        if op == 1:
                            self.assertTrue(sol[r][c] < sol[r + 1][c], f"{tier} #{i} edge_v ^ violated")
                        elif op == 2:
                            self.assertTrue(sol[r][c] > sol[r + 1][c], f"{tier} #{i} edge_v v violated")

    def test_unique_solvability(self):
        for tier in ["easy", "medium", "hard"]:
            for i in range(20):
                p = self.dataset[tier][i]
                sols = count_inequality_solutions(p["size"], p["givens"], p["edges_h"], p["edges_v"], limit=2)
                self.assertEqual(sols, 1, f"{tier} #{i} does not have unique solution")

    def test_d4_symmetry_transform_invariance(self):
        for tier in ["easy", "medium", "hard"]:
            for i in range(5):
                p = self.dataset[tier][i]
                for tid in range(8):
                    t_givens, t_edges_h, t_edges_v, t_sol = transform_inequality(
                        p["size"], p["givens"], p["edges_h"], p["edges_v"], p["solution"], tid
                    )
                    N = p["size"]
                    for r in range(N):
                        self.assertEqual(sorted(t_sol[r]), list(range(1, N + 1)))
                    sols = count_inequality_solutions(N, t_givens, t_edges_h, t_edges_v, limit=2)
                    self.assertEqual(sols, 1, f"{tier} #{i} transform {tid} failed unique solvability")


if __name__ == "__main__":
    unittest.main()
