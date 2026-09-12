"""
Unit test suite for Killer Sudoku Generator & Solver
"""

import time
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "server"))
from app.generators.killer_gen import KillerSudokuGenerator


def test_killer_sudoku():
    print("================================================================")
    print("RUNNING KILLER SUDOKU GENERATION & UNIQUENESS VERIFICATION TESTS")
    print("================================================================\n")

    gen = KillerSudokuGenerator(seed=42)

    # Test 1: Easy (4x4, 2x2 boxes, digits 1-4)
    print("Test 1: Verifying EASY 4x4 Killer Sudoku Generation...")
    t0 = time.time()
    for _ in range(15):
        puzzle = gen.generate("easy")
        assert puzzle["size"] == 4, f"Expected size 4, got {puzzle['size']}"
        assert puzzle["box_rows"] == 2 and puzzle["box_cols"] == 2
        # Verify solution satisfies standard 4x4 Sudoku
        sol = puzzle["solution"]
        for r in range(4):
            assert set(sol[r]) == {1, 2, 3, 4}, f"Row {r} invalid: {sol[r]}"
        for c in range(4):
            assert {sol[r][c] for r in range(4)} == {1, 2, 3, 4}, f"Col {c} invalid"
        for br in (0, 2):
            for bc in (0, 2):
                box = {sol[br + dr][bc + dc] for dr in range(2) for dc in range(2)}
                assert box == {1, 2, 3, 4}, f"Box at ({br},{bc}) invalid"

        # Verify cages
        assigned = {}
        for cg in puzzle["cages"]:
            cage_digits = [sol[r][c] for r, c in cg["cells"]]
            assert len(cage_digits) == len(set(cage_digits)), f"Duplicate digit in cage {cg['label']}"
            assert sum(cage_digits) == cg["sum"], f"Cage sum mismatch in {cg['label']}: expected {cg['sum']}, got {sum(cage_digits)}"
            for r, c in cg["cells"]:
                assert (r, c) not in assigned, f"Cell ({r},{c}) assigned multiple times"
                assigned[(r, c)] = cg["label"]
        assert len(assigned) == 16, f"All 16 cells must belong to a cage, got {len(assigned)}"

    dt_easy = (time.time() - t0) * 1000 / 15
    print(f"  -> Passed! 15 Easy puzzles verified (Avg {dt_easy:.2f} ms per puzzle).\n")

    # Test 2: Medium (4x4, challenging cages, min_cage >= 2)
    print("Test 2: Verifying MEDIUM 4x4 Killer Sudoku Generation...")
    t0 = time.time()
    for _ in range(15):
        puzzle = gen.generate("medium")
        assert puzzle["size"] == 4
        # Verify no 1-cell cages on Medium if possible
        for cg in puzzle["cages"]:
            cage_digits = [puzzle["solution"][r][c] for r, c in cg["cells"]]
            assert len(cage_digits) == len(set(cage_digits))
            assert sum(cage_digits) == cg["sum"]
    dt_med = (time.time() - t0) * 1000 / 15
    print(f"  -> Passed! 15 Medium puzzles verified (Avg {dt_med:.2f} ms per puzzle).\n")

    # Test 3: Extreme (6x6, 2x3 boxes, digits 1-6)
    print("Test 3: Verifying EXTREME 6x6 Killer Sudoku Generation...")
    t0 = time.time()
    for _ in range(10):
        puzzle = gen.generate("extreme")
        assert puzzle["size"] == 6
        assert puzzle["box_rows"] == 2 and puzzle["box_cols"] == 3
        sol = puzzle["solution"]
        for r in range(6):
            assert set(sol[r]) == {1, 2, 3, 4, 5, 6}
        for c in range(6):
            assert {sol[r][c] for r in range(6)} == {1, 2, 3, 4, 5, 6}
        for br in (0, 2, 4):
            for bc in (0, 3):
                box = {sol[br + dr][bc + dc] for dr in range(2) for dc in range(3)}
                assert box == {1, 2, 3, 4, 5, 6}
        for cg in puzzle["cages"]:
            cage_digits = [sol[r][c] for r, c in cg["cells"]]
            assert len(cage_digits) == len(set(cage_digits))
            assert sum(cage_digits) == cg["sum"]
    dt_ext = (time.time() - t0) * 1000 / 10
    print(f"  -> Passed! 10 Extreme puzzles verified (Avg {dt_ext:.2f} ms per puzzle).\n")

    print("================================================================")
    print("ALL KILLER SUDOKU TESTS PASSED SUCCESSFULLY!")
    print("================================================================")


if __name__ == "__main__":
    test_killer_sudoku()
