#!/usr/bin/env python3
"""
Automated Test Suite: Game Rules, Step-by-Step Guides & FAQs
Validates:
  - Canonical data integrity in server/data/game_rules.json
  - Compliance with Rule 1 (Strict 1-Word Titles) and Rule 3 (Instructions <= 100 chars, approved verb)
  - Python lookup API (server/app/puzzles/rules.py)
  - BasePuzzle guide rendering (format_guide_ascii and render_guide_raster)
  - Tri-target dataset synchronization (docs/GAME_RULES_FAQ.md, GameRulesDataset.h)
"""

import json
import os
import sys
from pathlib import Path

# Add server directory to sys.path
SERVER_DIR = Path(__file__).resolve().parent
ROOT_DIR = SERVER_DIR.parent
sys.path.insert(0, str(SERVER_DIR))

from app.puzzles.rules import get_game_rule, get_all_game_rules, load_game_rules
from app.puzzles.registry import DEFAULT_REGISTRY

APPROVED_TITLES = [
    "SUDOKU",
    "SEARCH",
    "NONOGRAM",
    "STARS",
    "JUMBLE",
    "BINARY",
    "MINES",
    "TENTS",
    "BRIDGES",
    "KILLER",
    "CRYPTOGRAM",
    "TANGO",
    "LADDER",
    "WHEEL",
    "LIGHTS",
    "LOOP",
    "TOWERS",
    "INEQUALITY",
]

APPROVED_VERBS = [
    "Place",
    "Fill",
    "Find",
    "Shade",
    "Unscramble",
    "Deduce",
    "Pitch",
    "Connect",
    "Draw",
]


def test_canonical_json():
    print("Test 1: Validating server/data/game_rules.json schema and rules...")
    data = load_game_rules()
    assert "games" in data, "game_rules.json missing 'games' array"
    games = data["games"]
    assert len(games) == 18, f"Expected 18 games, found {len(games)}"

    seen_ids = set()
    seen_keys = set()
    seen_titles = set()

    for g in games:
        # Check required fields
        for field in ["id", "key", "title", "instruction", "objective", "rules", "valid_move", "invalid_move", "opening_anchors", "faq"]:
            assert field in g, f"Game {g.get('key', 'unknown')} missing required field '{field}'"

        # Unique ID (0-indexed to match ESP32 enum/index)
        gid = g["id"]
        assert 0 <= gid < 18, f"Game ID {gid} out of range [0, 17]"
        assert gid not in seen_ids, f"Duplicate game ID: {gid}"
        seen_ids.add(gid)

        # Unique Key & Title
        key = g["key"]
        title = g["title"]
        assert key not in seen_keys, f"Duplicate game key: {key}"
        assert title not in seen_titles, f"Duplicate game title: {title}"
        seen_keys.add(key)
        seen_titles.add(title)

        # Rule 1: Title must be in APPROVED_TITLES and strictly 1 uppercase word
        assert title in APPROVED_TITLES, f"Title '{title}' not in APPROVED_TITLES list"
        assert len(title.split()) == 1, f"Title '{title}' must be a single word"
        assert title.isupper(), f"Title '{title}' must be uppercase"

        # Rule 3: Instruction length <= 100 characters and starts with approved verb
        inst = g["instruction"]
        assert len(inst) <= 100, f"Instruction for {title} exceeds 100 characters ({len(inst)} chars): '{inst}'"
        first_word = inst.split()[0]
        assert first_word in APPROVED_VERBS, f"Instruction for {title} starts with '{first_word}', which is not an approved verb ({APPROVED_VERBS})"

        # Content completeness
        assert len(g["objective"].strip()) > 0, f"Objective for {title} is empty"
        assert 3 <= len(g["rules"]) <= 4, f"Game {title} must have 3-4 rules, has {len(g['rules'])}"
        for r in g["rules"]:
            assert len(r.strip()) > 0, f"Empty rule string in {title}"

        # Valid / Invalid moves
        vm = g["valid_move"]
        ivm = g["invalid_move"]
        assert "caption" in vm and len(vm["caption"].strip()) > 0, f"Valid move caption empty in {title}"
        assert "caption" in ivm and len(ivm["caption"].strip()) > 0, f"Invalid move caption empty in {title}"

        # Anchors and FAQ
        anchors = g["opening_anchors"]
        assert 1 <= len(anchors) <= 2, f"Game {title} must have 1-2 opening anchors, has {len(anchors)}"
        faq = g["faq"]
        assert 1 <= len(faq) <= 2, f"Game {title} must have 1-2 FAQs, has {len(faq)}"
        for item in faq:
            assert len(item.get("q", "").strip()) > 0, f"Empty FAQ question in {title}"
            assert len(item.get("a", "").strip()) > 0, f"Empty FAQ answer in {title}"

    print(f"  -> All {len(games)} games passed schema, title, instruction, and content checks.")


def test_python_api():
    print("Test 2: Validating rules lookup API (server/app/puzzles/rules.py)...")
    all_rules = get_all_game_rules()
    assert len(all_rules) == 18, f"get_all_game_rules() returned {len(all_rules)} items, expected 18"

    for g in all_rules:
        by_id = get_game_rule(g["id"])
        assert by_id is not None, f"Failed lookup for ID {g['id']}"
        assert by_id["key"] == g["key"], f"ID lookup mismatch for {g['id']}"

        by_key = get_game_rule(g["key"])
        assert by_key is not None, f"Failed lookup for key '{g['key']}'"
        assert by_key["id"] == g["id"], f"Key lookup mismatch for '{g['key']}'"

        by_title = get_game_rule(g["title"])
        assert by_title is not None, f"Failed lookup for title '{g['title']}'"
        assert by_title["id"] == g["id"], f"Title lookup mismatch for '{g['title']}'"

    # Test aliases
    assert get_game_rule("wordsearch") is not None
    assert get_game_rule("queens") is not None

    # Test unknown lookup
    assert get_game_rule("nonexistent_puzzle_xyz") is None
    assert get_game_rule(999) is None
    print("  -> Lookup API functions correctly.")


def test_puzzle_plugin_guide_generation():
    print("Test 3: Validating BasePuzzle guide rendering (ASCII & Raster)...")
    plugins = DEFAULT_REGISTRY.get_all()
    assert len(plugins) == 18, f"Expected 18 registered plugins, got {len(plugins)}"
    for plugin in plugins:
        puzzle_id = plugin.puzzle_id
        # 1. ASCII guide
        ascii_lines = plugin.format_guide_ascii()
        assert len(ascii_lines) >= 8, f"ASCII guide for {puzzle_id} too short ({len(ascii_lines)} lines)"
        header_line = ascii_lines[0]
        assert header_line.startswith("--- ") and header_line.endswith(" ---"), f"Malformed header in guide ASCII: '{header_line}'"

        # 2. Raster guide
        raster_bytes = plugin.render_guide_raster(target_width=576)
        assert len(raster_bytes) > 0, f"Empty raster output for {puzzle_id}"
        # Standard ESC/POS raster header is b'\x1dv0\x00' (GS v 0 0)
        assert raster_bytes.startswith(b"\x1dv0\x00"), f"Invalid ESC/POS header for {puzzle_id}: {raster_bytes[:8]}"
        # Ensure dimensions match 576 dots width (576 / 8 = 72 bytes per row)
        x_bytes = raster_bytes[4] | (raster_bytes[5] << 8)
        assert x_bytes == 72, f"Expected 72 bytes per row (576 dots), got {x_bytes}"

    print(f"  -> All {len(plugins)} registered plugins successfully generated ASCII & 1-bit raster guides.")


def test_compiled_artifacts():
    print("Test 4: Validating compiled artifacts and docs...")
    cpp_header = ROOT_DIR / "esp32-firmware" / "src" / "generators" / "GameRulesDataset.h"
    assert cpp_header.exists(), f"GameRulesDataset.h missing at {cpp_header}"
    cpp_text = cpp_header.read_text(encoding="utf-8")
    assert "TOTAL_GAME_RULES = 18;" in cpp_text
    for title in APPROVED_TITLES:
        assert f'"{title}"' in cpp_text, f"Missing title {title} in GameRulesDataset.h"

    docs_md = ROOT_DIR / "docs" / "GAME_RULES_FAQ.md"
    assert docs_md.exists(), f"docs/GAME_RULES_FAQ.md missing at {docs_md}"
    docs_text = docs_md.read_text(encoding="utf-8")
    for title in APPROVED_TITLES:
        assert f"## --- {title} ---" in docs_text, f"Missing section for {title} in docs/GAME_RULES_FAQ.md"

    portal_html = ROOT_DIR / "portal.html"
    assert portal_html.exists(), "portal.html missing"
    portal_text = portal_html.read_text(encoding="utf-8")
    assert "/* [[START_GAME_RULES_DATA]] */" in portal_text, "portal.html missing rules data marker"

    sim_html = ROOT_DIR / "simulator" / "receipt_simulator.html"
    assert sim_html.exists(), "simulator/receipt_simulator.html missing"
    sim_text = sim_html.read_text(encoding="utf-8")
    assert "/* [[START_GAME_RULES_DATA]] */" in sim_text, "receipt_simulator.html missing rules data marker"

    print("  -> All compiled artifacts and documentation verified.")


def main():
    print("==================================================================")
    print("STARTING AUTOMATED GAME RULES & GUIDE VALIDATION SUITE")
    print("==================================================================")
    test_canonical_json()
    test_python_api()
    test_puzzle_plugin_guide_generation()
    test_compiled_artifacts()
    print("==================================================================")
    print("ALL GAME RULES & GUIDE VALIDATION CHECKS PASSED!")
    print("==================================================================")


if __name__ == "__main__":
    main()
