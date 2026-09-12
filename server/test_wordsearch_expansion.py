#!/usr/bin/env python3
"""
Comprehensive Test Suite for Expanded Word Search Dataset & Generator
Validates:
1. Exact count of 50 themes per difficulty level (150 unique themes total).
2. Exactly 12 words per theme adhering to strict length constraints:
   - Easy: 4 to 6 letters
   - Medium: 5 to 8 letters
   - Hard: 7 to 11 letters
3. Strict A-Z uppercase characters with no punctuation or whitespace.
4. Generator randomization across themes for easy, medium, and hard.
5. Correct directional constraints per difficulty tier.
6. Successful word placement rates (up to 8 words placed per puzzle).
"""

import sys
import os

# Add server directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "server"))

from app.generators.wordsearch_dataset import (
    WORDSEARCH_THEMES_EASY,
    WORDSEARCH_THEMES_MEDIUM,
    WORDSEARCH_THEMES_HARD,
    THEMES_BY_DIFFICULTY,
    get_random_theme,
    get_theme_words,
)
from app.generators.wordsearch_gen import WordSearchGenerator, DIRECTIONS


def test_dataset_integrity():
    print("Test 1: Verifying Dataset Theme Counts and Word Length Constraints...")
    tiers = [
        ("Easy", WORDSEARCH_THEMES_EASY, 4, 6),
        ("Medium", WORDSEARCH_THEMES_MEDIUM, 5, 8),
        ("Hard", WORDSEARCH_THEMES_HARD, 7, 11),
    ]

    total_themes = 0
    all_theme_names = set()

    for tier_name, dataset, min_len, max_len in tiers:
        assert len(dataset) == 50, f"Expected 50 themes for {tier_name}, found {len(dataset)}"
        total_themes += len(dataset)

        for theme_name, words in dataset.items():
            assert theme_name not in all_theme_names, f"Duplicate theme across tiers: {theme_name}"
            all_theme_names.add(theme_name)

            assert len(words) == 12, f"Theme '{theme_name}' in {tier_name} has {len(words)} words; expected 12"
            for w in words:
                assert w.isalpha() and w.isupper(), f"Invalid word characters: '{w}' in '{theme_name}'"
                assert min_len <= len(w) <= max_len, (
                    f"Word '{w}' (length {len(w)}) in '{theme_name}' violates {tier_name} bounds [{min_len}, {max_len}]"
                )

    print(f"  -> Passed! Verified {total_themes} unique themes (50 Easy, 50 Medium, 50 Hard).")
    print("  -> Passed! All 1,800 words (150 themes x 12 words) strictly satisfy length and character rules.")


def test_theme_retrieval():
    print("\nTest 2: Verifying Helper Theme Retrieval Functions...")
    # Random retrieval
    for diff in ["easy", "medium", "hard"]:
        name, words = get_random_theme(diff)
        assert name in THEMES_BY_DIFFICULTY[diff], f"Theme '{name}' not in {diff} pool"
        assert len(words) == 12, f"Expected 12 words, got {len(words)}"

    # Explicit lookup
    t_name, t_words = get_theme_words("Coffee Culture", "medium")
    assert t_name == "Coffee Culture"
    assert "ESPRESSO" in t_words

    # Unknown theme falls back to random selection without crashing
    f_name, f_words = get_theme_words("NonExistentTheme123", "easy")
    assert f_name in WORDSEARCH_THEMES_EASY
    assert len(f_words) == 12

    print("  -> Passed! get_random_theme and get_theme_words perform accurately with safe fallbacks.")


def test_puzzle_generation():
    print("\nTest 3: Verifying Puzzle Generation & Directional Constraints...")
    gen = WordSearchGenerator(seed=42)

    expected_dirs = {
        "easy": {"E", "S"},
        "medium": {"E", "S", "SE", "NE"},
        "hard": set(DIRECTIONS.keys()),
    }

    for diff in ["easy", "medium", "hard"]:
        selected_themes = set()
        for i in range(30):
            res = gen.generate(difficulty=diff)
            assert res["type"] == "wordsearch"
            assert res["grid_size"] == 12
            assert res["difficulty"] == diff
            assert len(res["words"]) >= 6, f"Too few words placed: {len(res['words'])}"
            assert len(res["words"]) <= 8, f"More than 8 words placed: {len(res['words'])}"
            assert res["theme"] in THEMES_BY_DIFFICULTY[diff], f"Theme '{res['theme']}' not in {diff} pool"
            selected_themes.add(res["theme"])

            # Verify directional validity
            for word, placement in res["placements"].items():
                d = placement["direction"]
                assert d in expected_dirs[diff], f"Direction '{d}' not allowed for {diff}"

                # Verify word actually exists at grid coordinates
                r, c = placement["start"]
                dr, dc = DIRECTIONS[d]
                for idx, ch in enumerate(word):
                    grid_ch = res["grid"][r + dr * idx][c + dc * idx]
                    assert grid_ch == ch, f"Grid mismatch at ({r + dr * idx}, {c + dc * idx}): expected {ch}, got {grid_ch}"

        # Ensure random selection hit multiple themes
        assert len(selected_themes) >= 15, f"Expected variety of themes, but only hit {len(selected_themes)} in 30 runs"
        print(f"  -> Passed! {diff.capitalize()} difficulty: {len(selected_themes)} distinct themes picked across 30 runs, directional rules strictly followed.")


if __name__ == "__main__":
    print("================================================================")
    print("RUNNING WORD SEARCH EXPANSION VERIFICATION TESTS")
    print("================================================================")
    test_dataset_integrity()
    test_theme_retrieval()
    test_puzzle_generation()
    print("================================================================")
    print("ALL WORD SEARCH EXPANSION TESTS PASSED SUCCESSFULLY (3/3)!")
    print("================================================================")
