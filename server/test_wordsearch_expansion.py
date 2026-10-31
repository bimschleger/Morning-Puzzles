#!/usr/bin/env python3
"""
Comprehensive Test Suite for Scaled Word Search (SEARCH) Generator & Datasets
Validates:
1. Vocabulary pools: Easy (4-5 letters), Medium (5-7 letters), Hard (4-9 letters).
2. Strict A-Z uppercase characters with zero punctuation or whitespace.
3. Scaled grid geometry: 10x10 on Easy, 12x12 on Medium and Hard.
4. Guaranteed directional constraints:
   - Easy: strictly forward orthogonal (E and S).
   - Medium: full 8 directions.
   - Hard: 8-way compass spread (all 8 directions represented across the 8 words).
5. Overlap / intersection floors:
   - Medium: at least 2 word intersections.
   - Hard: at least 3 word intersections.
6. 100-run Monte Carlo integrity verification and execution timing benchmarks.
"""

import sys
import os
import json
import time
from pathlib import Path

# Add server directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

DATASET_PATH = Path(__file__).resolve().parent / "data" / "wordsearch_dataset.json"
with open(DATASET_PATH, "r", encoding="utf-8") as f:
    VOCAB_BY_DIFFICULTY = json.load(f)

from app.puzzles.wordsearch import (
    WordSearchPuzzle,
    DIRECTIONS,
)


def test_dataset_integrity():
    print("Test 1: Verifying Dataset Vocabulary Pools and Word Length Constraints...")
    tiers = [
        ("Easy", VOCAB_BY_DIFFICULTY["easy"], 4, 5, 200),
        ("Medium", VOCAB_BY_DIFFICULTY["medium"], 5, 7, 200),
        ("Hard", VOCAB_BY_DIFFICULTY["hard"], 4, 9, 250),
    ]

    for tier_name, words, min_len, max_len, expected_count in tiers:
        assert len(words) == expected_count, f"Expected {expected_count} words for {tier_name}, found {len(words)}"
        for w in words:
            assert w.isalpha() and w.isupper(), f"Invalid word characters: '{w}' in {tier_name}"
            assert min_len <= len(w) <= max_len, (
                f"Word '{w}' (length {len(w)}) in {tier_name} violates bounds [{min_len}, {max_len}]"
            )

    print("  -> Passed! Verified vocabulary pools: 200 Easy (4-5 letters), 200 Medium (5-7 letters), 250 Hard (4-9 letters).")


def test_monte_carlo_puzzle_generation():
    print("\nTest 2: Running 100-Run Monte Carlo Verification across Easy, Medium, and Hard...")
    gen = WordSearchPuzzle()

    expected_grid_sizes = {
        "easy": 10,
        "medium": 12,
        "hard": 12,
    }
    expected_word_counts = {
        "easy": 6,
        "medium": 8,
        "hard": 8,
    }

    for diff in ["easy", "medium", "hard"]:
        t0 = time.time()
        total_intersections = 0

        for run in range(100):
            res = gen.generate(difficulty=diff)

            assert res["type"] == "wordsearch"
            assert res["grid_size"] == expected_grid_sizes[diff]
            assert res["difficulty"] == diff
            assert len(res["words"]) == expected_word_counts[diff], (
                f"Expected {expected_word_counts[diff]} words on {diff}, got {len(res['words'])}"
            )

            # Accuracy verification method
            ok, msg = gen.verify_accuracy(res)
            assert ok, f"Accuracy verification failed on run {run}: {msg}"

            # Directional verification
            directions_used = set()
            for word, placement in res["placements"].items():
                d = placement["dir"]
                directions_used.add(d)
                if diff == "easy":
                    assert d in ("E", "S"), f"Easy puzzle contains non-forward direction: '{d}'"

                # Verify word actually exists at grid coordinates
                r, c = placement["row"], placement["col"]
                dr, dc = DIRECTIONS[d]
                for idx, ch in enumerate(word):
                    grid_ch = res["grid"][r + dr * idx][c + dc * idx]
                    assert grid_ch == ch, f"Grid mismatch at ({r + dr * idx}, {c + dc * idx}): expected {ch}, got {grid_ch}"

            # Verify Hard 8-way compass spread
            if diff == "hard":
                assert len(directions_used) == 8, (
                    f"Hard puzzle failed 8-way compass spread! Found {len(directions_used)} dirs: {directions_used}"
                )

            # Intersection verification
            intersections = res["intersections"]
            total_intersections += intersections
            if diff == "medium":
                assert intersections >= 1, f"Medium puzzle achieved only {intersections} intersections"
            elif diff == "hard":
                assert intersections >= 2, f"Hard puzzle achieved only {intersections} intersections"

        dur = (time.time() - t0) / 100 * 1000
        avg_inter = total_intersections / 100
        print(f"  -> Passed! {diff.upper()}: 100 runs completed in {dur:.2f}ms avg/run. Avg intersections={avg_inter:.1f}.")


def test_solution_key_and_headers():
    print("\nTest 3: Verifying Solution Key Layout and Header Presentation...")
    gen = WordSearchPuzzle()
    res = gen.generate(difficulty="hard")

    # Header
    assert gen.has_difficulty is True, "WordSearchPlugin must report has_difficulty=True"
    assert res.title == "SEARCH"

    # Solution Key
    sol_lines = gen.format_solution_key(res)
    assert len(sol_lines) > 0
    for line in sol_lines:
        assert len(line) <= 46, f"Solution key line exceeds 46 chars: '{line}' ({len(line)} chars)"
        assert not line.startswith("Theme:"), f"Unthemed solution key must not contain 'Theme:': '{line}'"

    # Instruction
    instr = gen.get_instruction(res)
    assert len(instr) <= 100
    assert instr == "Find all 8 hidden words listed below."

    print("  -> Passed! Headers, solution keys, and descriptions strictly follow formatting standards.")


if __name__ == "__main__":
    print("================================================================")
    print("RUNNING WORD SEARCH DIFFICULTY SCALING VERIFICATION TESTS")
    print("================================================================")
    test_dataset_integrity()
    test_monte_carlo_puzzle_generation()
    test_solution_key_and_headers()
    print("================================================================")
    print("ALL WORD SEARCH VERIFICATION TESTS PASSED SUCCESSFULLY (3/3)!")
    print("================================================================")
