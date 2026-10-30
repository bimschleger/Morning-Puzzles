#!/usr/bin/env python3
"""
Automated Test Suite: Game Onboarding, Setup Portal, Documentation & Parity (Rule 18)

Validates that any new game added to the Morning Puzzles inventory:
1. Has full details on how to play the game (canonical rules, guides, ASCII & 1-bit raster, C++ header, docs).
2. Is fully integrated on the SoftAP Setup Portal (eligible games toggle, bitmask, guide modal, PortalHtml.h).
3. Is documented in README.md with updated game counts.
4. Ensures the game description on the setup portal matches the game description on the README page.
5. Ensures every game has an explicit name in OfflineConfigManager::getPuzzleName() so initial setup receipts never display 'Unknown Puzzle'.
"""

import gzip
import json
import os
import re
import sys
from pathlib import Path

# Add server directory to sys.path
SERVER_DIR = Path(__file__).resolve().parent
ROOT_DIR = SERVER_DIR.parent
sys.path.insert(0, str(SERVER_DIR))

from app.puzzles.registry import DEFAULT_REGISTRY
from app.puzzles.rules import load_game_rules, get_game_rule

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


def extract_portal_games(portal_html_text: str):
    """Parses the const GAMES = [...] array from portal.html."""
    match = re.search(r"const\s+GAMES\s*=\s*(\[\s*\{.*?\}\s*\]);", portal_html_text, re.DOTALL)
    assert match, "Could not find 'const GAMES = [...]' array in portal.html"
    raw_json = match.group(1)
    # Convert JS object keys to valid JSON if needed
    raw_json = re.sub(r"([{,]\s*)([a-zA-Z0-9_]+)\s*:", r'\1"\2":', raw_json)
    # Remove trailing commas
    raw_json = re.sub(r",\s*([}\]])", r"\1", raw_json)
    return json.loads(raw_json)


def extract_readme_featured_games(readme_text: str):
    """
    Parses the Featured Games list from README.md.
    Returns (declared_count, list_of_games) where each game is:
    {"index": int, "title": str, "aliases": str, "description": str}
    """
    section_match = re.search(r"## 🧩 Featured Games \(All (\d+) Included\)(.*?)(?:\n---|(?=\n## ))", readme_text, re.DOTALL)
    assert section_match, "README.md is missing '## 🧩 Featured Games (All N Included)' section"
    declared_count = int(section_match.group(1))
    section_text = section_match.group(2)

    # Match each numbered list item: N. **Title** *(Aliases)*: Description
    item_pattern = re.compile(
        r"^\s*(\d+)\.\s+\*\*([^*]+)\*\*(?:\s+\*([^*]+)\*)?:\s*(.+)$",
        re.MULTILINE,
    )
    games = []
    for m in item_pattern.finditer(section_text):
        idx = int(m.group(1))
        title = m.group(2).strip()
        aliases = m.group(3).strip() if m.group(3) else ""
        desc = m.group(4).strip()
        games.append({
            "index": idx,
            "title": title,
            "aliases": aliases,
            "description": desc,
        })

    return declared_count, games


def normalize_desc(text: str) -> str:
    """Normalizes descriptions for comparison (stripping markdown backticks and normalizing spaces)."""
    t = text.replace("`", "").strip()
    return re.sub(r"\s+", " ", t)


def test_game_inventory_parity():
    print("Test 1: Verifying game inventory parity across backend, firmware, simulator, portal, and README...")
    plugins = DEFAULT_REGISTRY.get_all()
    total_plugins = len(plugins)

    # 1. ESP32 firmware OFFLINE_PUZZLE_TOTAL
    config_header = (ROOT_DIR / "esp32-firmware" / "src" / "config" / "OfflineConfigManager.h").read_text(encoding="utf-8")
    enum_match = re.search(r"enum\s+OfflinePuzzleType\s*:\s*uint8_t\s*\{(.*?)\};", config_header, re.DOTALL)
    assert enum_match, "Could not find OfflinePuzzleType enum in OfflineConfigManager.h"
    enum_entries = [line.strip().rstrip(",") for line in enum_match.group(1).split("\n") if line.strip() and not line.strip().startswith("//")]
    assert "OFFLINE_PUZZLE_TOTAL" in enum_entries, "OFFLINE_PUZZLE_TOTAL missing in OfflinePuzzleType enum"
    puzzle_enum_items = [e for e in enum_entries if e != "OFFLINE_PUZZLE_TOTAL"]
    assert len(puzzle_enum_items) == total_plugins, (
        f"OfflinePuzzleType has {len(puzzle_enum_items)} puzzles, expected {total_plugins}"
    )

    # 2. Canonical game_rules.json
    rules_data = load_game_rules()
    canonical_games = rules_data.get("games", [])
    assert len(canonical_games) == total_plugins, (
        f"server/data/game_rules.json has {len(canonical_games)} games, expected {total_plugins}"
    )

    # 3. Setup Portal GAMES list
    portal_text = (ROOT_DIR / "portal.html").read_text(encoding="utf-8")
    portal_games = extract_portal_games(portal_text)
    assert len(portal_games) == total_plugins, (
        f"portal.html GAMES list has {len(portal_games)} games, expected {total_plugins}"
    )

    # 4. Web Simulator ALL_GAMES list
    sim_text = (ROOT_DIR / "simulator" / "receipt_simulator.html").read_text(encoding="utf-8")
    sim_match = re.search(r"const\s+ALL_GAMES\s*=\s*\[(.*?)\];", sim_text, re.DOTALL)
    assert sim_match, "Could not find const ALL_GAMES in simulator/receipt_simulator.html"
    sim_games = [g.strip().strip("'\"") for g in sim_match.group(1).split(",") if g.strip()]
    assert len(sim_games) == total_plugins, (
        f"receipt_simulator.html ALL_GAMES has {len(sim_games)} games, expected {total_plugins}"
    )

    # 5. README.md declared count
    readme_text = (ROOT_DIR / "README.md").read_text(encoding="utf-8")
    declared_count, readme_games = extract_readme_featured_games(readme_text)
    assert declared_count == total_plugins, (
        f"README.md declares 'All {declared_count} Included', expected 'All {total_plugins} Included'"
    )
    assert len(readme_games) == total_plugins, (
        f"README.md lists {len(readme_games)} games, expected {total_plugins}"
    )

    print(f"  -> All {total_plugins} inventory games matched across Python, C++, simulator, setup portal, and README.\n")


def test_how_to_play_details_present():
    print("Test 2: Verifying complete how-to-play rules and guide rendering for all games...")
    plugins = DEFAULT_REGISTRY.get_all()
    rules_data = load_game_rules()
    games_by_id = {g["id"]: g for g in rules_data.get("games", [])}
    games_by_key = {g["key"].lower(): g for g in rules_data.get("games", [])}

    for idx, plugin in enumerate(plugins):
        pid = plugin.puzzle_id.lower()
        title = plugin.title.upper()

        # Check canonical rules entry
        rule = games_by_id.get(idx) or games_by_key.get(pid)
        assert rule is not None, f"Game {title} ({pid}) missing from server/data/game_rules.json"

        # Check required how-to-play fields
        for field in ["instruction", "objective", "rules", "valid_move", "invalid_move", "opening_anchors", "faq"]:
            assert field in rule and rule[field], f"Game {title} missing '{field}' in game_rules.json"

        # Instruction standards (Rule 3)
        inst = rule["instruction"]
        assert len(inst) <= 100, f"Instruction for {title} exceeds 100 chars: '{inst}'"
        assert inst.split()[0] in APPROVED_VERBS, f"Instruction for {title} doesn't start with approved verb: '{inst}'"

        # Rules of play count (3-4 rules)
        assert 3 <= len(rule["rules"]) <= 4, f"Game {title} must have 3-4 rules, found {len(rule['rules'])}"

        # Valid / Invalid move captions
        assert rule["valid_move"].get("caption"), f"Valid move caption empty in {title}"
        assert rule["invalid_move"].get("caption"), f"Invalid move caption empty in {title}"

        # Opening deduction anchors & FAQ
        assert 1 <= len(rule["opening_anchors"]) <= 2, f"Game {title} must have 1-2 opening anchors"
        assert 1 <= len(rule["faq"]) <= 2, f"Game {title} must have 1-2 FAQs"

        # BasePuzzle Guide Rendering: ASCII
        ascii_lines = plugin.format_guide_ascii()
        assert len(ascii_lines) >= 8, f"ASCII guide for {title} too short ({len(ascii_lines)} lines)"
        assert f"--- {title} ---" in ascii_lines[0], f"ASCII guide for {title} header mismatch: '{ascii_lines[0]}'"

        # BasePuzzle Guide Rendering: 1-Bit Thermal Raster
        raster_bytes = plugin.render_guide_raster(target_width=576)
        assert len(raster_bytes) > 0, f"Raster guide for {title} is empty"
        assert raster_bytes.startswith(b"\x1dv0\x00"), f"Raster guide for {title} missing ESC/POS GS v 0 header"

    # Compiled artifacts check
    cpp_header = (ROOT_DIR / "esp32-firmware" / "src" / "generators" / "GameRulesDataset.h").read_text(encoding="utf-8")
    assert f"TOTAL_GAME_RULES = {len(plugins)};" in cpp_header, "GameRulesDataset.h TOTAL_GAME_RULES mismatch"

    docs_faq = (ROOT_DIR / "docs" / "GAME_RULES_FAQ.md").read_text(encoding="utf-8")
    for plugin in plugins:
        assert f"## --- {plugin.title.upper()} ---" in docs_faq, f"docs/GAME_RULES_FAQ.md missing section for {plugin.title}"

    print(f"  -> All {len(plugins)} games have complete how-to-play guides, ASCII/raster renderers, and compiled docs.\n")


def test_setup_portal_inclusion():
    print("Test 3: Verifying setup portal inclusion, dynamic bitmasks, and compiled header...")
    plugins = DEFAULT_REGISTRY.get_all()
    total_games = len(plugins)
    portal_text = (ROOT_DIR / "portal.html").read_text(encoding="utf-8")
    portal_games = extract_portal_games(portal_text)

    # 1. Check all games present in GAMES array with id, name, and desc
    seen_ids = set()
    for idx, g in enumerate(portal_games):
        gid = g["id"]
        name = g["name"]
        desc = g.get("desc", "")

        assert gid == idx, f"portal.html GAMES entry at position {idx} has mismatched id {gid}"
        assert gid not in seen_ids, f"Duplicate game id {gid} in portal.html"
        seen_ids.add(gid)

        assert name, f"Game at id {gid} has empty name in portal.html"
        assert desc, f"Game '{name}' (id {gid}) has empty description in portal.html"

    # 2. Check dynamic bitmask usage (no hardcoded old bitmasks)
    assert "ALL_GAMES_MASK" in portal_text or "GAMES.length" in portal_text, (
        "portal.html must use dynamic bitmask based on GAMES.length"
    )

    # 3. Check drawThermalGuideCanvas covers all game IDs
    for gid in range(total_games):
        assert f"case {gid}:" in portal_text, (
            f"portal.html drawThermalGuideCanvas missing case {gid} for '{portal_games[gid]['name']}'"
        )

    # 4. Verify compiled PortalHtml.h matches portal.html
    header_path = ROOT_DIR / "esp32-firmware" / "src" / "time" / "PortalHtml.h"
    assert header_path.exists(), "PortalHtml.h does not exist"
    portal_bytes = (ROOT_DIR / "portal.html").read_bytes()
    expected_gz = gzip.compress(portal_bytes, compresslevel=9, mtime=0)

    header_text = header_path.read_text(encoding="utf-8")
    assert f"Original size: {len(portal_bytes)} bytes" in header_text, (
        "PortalHtml.h is out of sync with portal.html! Run 'python3 tools/datasets/build_game_rules.py' or 'scripts/build_portal_header.py'."
    )
    assert f"Compressed size: {len(expected_gz)} bytes" in header_text, (
        "PortalHtml.h compressed size does not match portal.html gzip output!"
    )

    print(f"  -> Setup portal correctly includes all {total_games} games, dynamic controls, and synchronized PortalHtml.h.\n")


def test_readme_inclusion_and_description_parity():
    print("Test 4: Verifying README inclusion and bit-for-bit description parity with setup portal...")
    readme_text = (ROOT_DIR / "README.md").read_text(encoding="utf-8")
    declared_count, readme_games = extract_readme_featured_games(readme_text)

    portal_text = (ROOT_DIR / "portal.html").read_text(encoding="utf-8")
    portal_games = extract_portal_games(portal_text)

    assert len(readme_games) == len(portal_games), (
        f"README games count ({len(readme_games)}) does not match portal GAMES count ({len(portal_games)})"
    )

    for idx, (rg, pg) in enumerate(zip(readme_games, portal_games), start=1):
        assert rg["index"] == idx, f"README item out of order: expected #{idx}, got #{rg['index']}"

        # Match title
        r_title = rg["title"].lower()
        p_name = pg["name"].lower()
        assert r_title == p_name or r_title in p_name or p_name in r_title, (
            f"Game #{idx} title mismatch: README has '{rg['title']}', setup portal has '{pg['name']}'"
        )

        # Match description
        r_desc = normalize_desc(rg["description"])
        p_desc = normalize_desc(pg.get("desc", ""))
        assert r_desc == p_desc, (
            f"Description mismatch for game #{idx} ({pg['name']}):\n"
            f"  README:       '{r_desc}'\n"
            f"  Setup Portal: '{p_desc}'"
        )

    print(f"  -> All {len(portal_games)} game descriptions on the setup portal perfectly match README.md.\n")


def extract_puzzle_names_from_cpp(cpp_text: str) -> dict:
    match = re.search(
        r"const\s+char\*\s+OfflineConfigManager::getPuzzleName\s*\([^)]*\)\s*const\s*\{(.*?)\}",
        cpp_text,
        re.DOTALL,
    )
    assert match, "Could not find OfflineConfigManager::getPuzzleName definition in C++ source"
    body = match.group(1)
    case_matches = re.findall(r"case\s+([A-Za-z0-9_]+)\s*:\s*return\s*\"([^\"]+)\"\s*;", body)
    return dict(case_matches)


def test_setup_receipt_name_parity():
    print("Test 5: Verifying Initial Setup Receipt & Offline Config name parity across firmware targets...")
    plugins = DEFAULT_REGISTRY.get_all()
    total_games = len(plugins)

    # 1. Read OfflinePuzzleType enum from OfflineConfigManager.h
    config_header = (ROOT_DIR / "esp32-firmware" / "src" / "config" / "OfflineConfigManager.h").read_text(encoding="utf-8")
    enum_match = re.search(r"enum\s+OfflinePuzzleType\s*:\s*uint8_t\s*\{(.*?)\};", config_header, re.DOTALL)
    assert enum_match, "Could not find OfflinePuzzleType enum in OfflineConfigManager.h"
    enum_entries = [
        line.split("=")[0].strip().rstrip(",")
        for line in enum_match.group(1).split("\n")
        if line.strip() and not line.strip().startswith("//")
    ]
    enum_entries = [e for e in enum_entries if e != "OFFLINE_PUZZLE_TOTAL"]
    assert len(enum_entries) == total_games, (
        f"OfflinePuzzleType has {len(enum_entries)} enum entries, expected {total_games}"
    )

    # 2. Check esp32-firmware and PenAndPaperPuzzles implementations
    fw_cpp_path = ROOT_DIR / "esp32-firmware" / "src" / "config" / "OfflineConfigManager.cpp"
    arduino_cpp_path = ROOT_DIR / "PenAndPaperPuzzles" / "OfflineConfigManager.cpp"

    for cpp_path in [fw_cpp_path, arduino_cpp_path]:
        assert cpp_path.exists(), f"Source file does not exist: {cpp_path}"
        cpp_text = cpp_path.read_text(encoding="utf-8")
        name_map = extract_puzzle_names_from_cpp(cpp_text)

        # Check every enum entry has an explicit case
        for idx, (plugin, enum_entry) in enumerate(zip(plugins, enum_entries)):
            assert enum_entry in name_map, (
                f"{cpp_path.name}: OfflineConfigManager::getPuzzleName() is missing case for '{enum_entry}'! "
                f"This causes the initial setup receipt to print 'Unknown Puzzle'."
            )
            returned_name = name_map[enum_entry]
            assert returned_name != "Unknown Puzzle", (
                f"{cpp_path.name}: '{enum_entry}' returned 'Unknown Puzzle'!"
            )
            # Expect strict match to plugin.title.capitalize() (e.g. Sudoku, Maze, Stars, Search)
            expected_name = plugin.title.capitalize()
            assert returned_name == expected_name, (
                f"{cpp_path.name}: Name mismatch for '{enum_entry}': "
                f"got '{returned_name}', expected '{expected_name}'"
            )

        assert len(name_map) == total_games, (
            f"{cpp_path.name}: getPuzzleName has {len(name_map)} cases, expected {total_games}"
        )

    print(f"  -> All {total_games} games have explicit, non-unknown names in OfflineConfigManager::getPuzzleName() for setup receipts.\n")


def run_all_onboarding_checks() -> bool:
    print("=" * 70)
    print(">>> RUNNING GAME ONBOARDING, SETUP PORTAL & README VERIFICATION <<<")
    print("=" * 70)
    try:
        test_game_inventory_parity()
        test_how_to_play_details_present()
        test_setup_portal_inclusion()
        test_readme_inclusion_and_description_parity()
        test_setup_receipt_name_parity()
        print("=" * 70)
        print(">>> ALL GAME ONBOARDING & PARITY VERIFICATION CHECKS PASSED! <<<")
        print("=" * 70)
        return True
    except Exception as e:
        print(f"\n[ONBOARDING VERIFICATION FAILED] {e}\n")
        return False


if __name__ == "__main__":
    success = run_all_onboarding_checks()
    sys.exit(0 if success else 1)
