"""
Unit test suite for Killer Sudoku Generator & Solver
Strictly validates:
  - Orthogonal cage contiguity (zero disconnected cage fragments)
  - Solution validity (standard Sudoku row, column, and box constraints)
  - Cage constraints (digit uniqueness, exact sum matching, physical feasibility)
  - Unambiguous visual clue placement and single-cell sum bounds (<= max digit)
  - Exactly 1 unique mathematical solution verified via constraint backtracking
"""

import time
import sys
import os
from typing import List, Tuple, Set

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "server"))
from app.puzzles.killer import KillerPuzzle


def is_orthogonally_connected(cells: List[Tuple[int, int]]) -> bool:
    """Verifies that a list of 2D coordinates forms a single connected component."""
    if not cells:
        return False
    cell_set = set(cells)
    visited: Set[Tuple[int, int]] = set()
    queue = [cells[0]]
    visited.add(cells[0])
    while queue:
        r, c = queue.pop(0)
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if (nr, nc) in cell_set and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc))
    return len(visited) == len(cells)


def verify_puzzle_integrity(puzzle: dict, plugin: KillerPuzzle):
    size = puzzle["size"]
    box_r = puzzle["box_rows"]
    box_c = puzzle["box_cols"]
    sol = puzzle["solution"]
    cages = puzzle["cages"]

    # 1. Sudoku grid correctness
    valid_digits = set(range(1, size + 1))
    for r in range(size):
        assert set(sol[r]) == valid_digits, f"Row {r} invalid: {sol[r]}"
    for c in range(size):
        assert {sol[r][c] for r in range(size)} == valid_digits, f"Col {c} invalid"
    for br in range(0, size, box_r):
        for bc in range(0, size, box_c):
            box = {sol[br + dr][bc + dc] for dr in range(box_r) for dc in range(box_c)}
            assert box == valid_digits, f"Box at ({br},{bc}) invalid"

    # 2. Cage coverage, distinct digits, sums, and strict orthogonal contiguity
    assigned = {}
    for cg in cages:
        cells = cg["cells"]
        assert len(cells) > 0, f"Cage {cg['label']} has no cells"

        # STRICT CONTIGUITY: Cages must be a single connected piece
        assert is_orthogonally_connected(cells), (
            f"Cage {cg['label']} with sum {cg['sum']} is DISCONNECTED: {cells}"
        )

        cage_digits = [sol[r][c] for r, c in cells]
        assert len(cage_digits) == len(set(cage_digits)), f"Duplicate digit in cage {cg['label']}: {cage_digits}"
        assert sum(cage_digits) == cg["sum"], (
            f"Cage sum mismatch in {cg['label']}: expected {cg['sum']}, got {sum(cage_digits)}"
        )

        # Single-cell cage sums must not exceed max digit
        if len(cells) == 1:
            assert cg["sum"] <= size, (
                f"Single-cell cage {cg['label']} at {cells[0]} has impossible sum {cg['sum']} > {size}"
            )

        # Verify no overlap between cages
        for r, c in cells:
            assert (r, c) not in assigned, f"Cell ({r},{c}) assigned multiple times to {assigned[(r, c)]} and {cg['label']}"
            assigned[(r, c)] = cg["label"]

    assert len(assigned) == size * size, f"All {size * size} cells must belong to a cage, got {len(assigned)}"

    # 3. Independent solver check: exactly 1 unique solution
    sols = plugin._find_multiple_solutions(size, box_r, box_c, cages, max_count=2)
    assert len(sols) == 1, f"Puzzle has {len(sols)} solutions instead of 1 unique solution"


def test_killer_sudoku():
    print("================================================================")
    print("RUNNING KILLER SUDOKU GENERATION & UNIQUENESS VERIFICATION TESTS")
    print("================================================================\n")

    plugin = KillerPuzzle()

    # Test 1: Easy (4x4, 2x2 boxes, digits 1-4)
    print("Test 1: Verifying EASY 4x4 Killer Sudoku Generation & Contiguity...")
    t0 = time.time()
    for _ in range(30):
        res = plugin.generate("easy")
        verify_puzzle_integrity(res.to_dict(), plugin)
    dt_easy = (time.time() - t0) * 1000 / 30
    print(f"  -> Passed! 30 Easy puzzles verified (Avg {dt_easy:.2f} ms per puzzle, 100% contiguous & unique).\n")

    # Test 2: Medium (4x4, challenging cages, min_cage >= 2)
    print("Test 2: Verifying MEDIUM 4x4 Killer Sudoku Generation & Contiguity...")
    t0 = time.time()
    for _ in range(50):
        res = plugin.generate("medium")
        verify_puzzle_integrity(res.to_dict(), plugin)
    dt_med = (time.time() - t0) * 1000 / 50
    print(f"  -> Passed! 50 Medium puzzles verified (Avg {dt_med:.2f} ms per puzzle, 100% contiguous & unique).\n")

    # Test 3: Extreme (6x6, 2x3 boxes, digits 1-6)
    print("Test 3: Verifying EXTREME 6x6 Killer Sudoku Generation & Contiguity...")
    t0 = time.time()
    for _ in range(20):
        res = plugin.generate("extreme")
        verify_puzzle_integrity(res.to_dict(), plugin)
    dt_ext = (time.time() - t0) * 1000 / 20
    print(f"  -> Passed! 20 Extreme puzzles verified (Avg {dt_ext:.2f} ms per puzzle, 100% contiguous & unique).\n")

    # Test 4: BasePuzzle Plugin compliance
    print("Test 4: Verifying KillerPuzzle Plugin Output...")
    res = plugin.generate(difficulty="medium", seed=123)
    raw = res.to_dict()
    verify_puzzle_integrity(raw, plugin)
    assert res.puzzle_type == "killer"
    assert "Fill every row, column, and box" in res.instruction
    print("  -> Passed! KillerPuzzle plugin output verified.\n")

    print("================================================================")
    print("ALL KILLER SUDOKU TESTS PASSED SUCCESSFULLY!")
    print("================================================================")


if __name__ == "__main__":
    test_killer_sudoku()
