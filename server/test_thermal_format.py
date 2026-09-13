#!/usr/bin/env python3
"""
Automated Test Suite: 80mm Thermal Receipt Printer Output & Format Verification
Validates that all generated daily bundles, text streams, and 1-bit raster graphics
strictly adhere to:
  - docs/THERMAL_80MM_PRINT_GUIDE.md
  - docs/PUZZLE_HEADER_SPEC.md
  - docs/THERMAL_DRAWING_SPEC.md
"""

import sys
import os

# Add server directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import generate_daily_bundle
from app.puzzles.registry import DEFAULT_REGISTRY
from app.renderer.receipt_rasterizer import (
    calculate_duty_cycle,
    image_to_escpos_raster,
    render_sudoku_raster,
    render_wordsearch_raster,
    render_nonogram_raster,
    render_queens_dithered_raster,
    render_jumble_raster,
    render_binary_raster,
    render_mines_raster,
    render_tents_raster,
    render_bridges_raster,
    render_killer_raster,
    render_cryptogram_raster,
    render_tango_raster,
    render_ladder_raster,
    render_wheel_raster,
    render_lights_raster,
    render_loop_raster,
    THERMAL_WIDTH_DOTS,
    THERMAL_WIDTH_BYTES,
)
from app.renderer.text_formatter import (
    build_daily_receipt_bytes,
    build_hybrid_daily_receipt_bytes,
    CMD_INIT,
    CMD_CUT_PARTIAL,
    LF,
)


def test_bundle_completeness():
    print("Test 1: Verifying Daily Bundle Completeness (All 16 Puzzles)...")
    bundle = generate_daily_bundle(difficulty="medium")
    required_keys = ["title", "date", "difficulty", "sudoku", "wordsearch", "nonogram", "queens", "jumble", "binary", "mines", "tents", "bridges", "killer", "cryptogram", "tango", "ladder", "wheel", "lights", "loop"]
    for k in required_keys:
        assert k in bundle, f"Missing key '{k}' in generated bundle"
    print("  -> Passed! All 16 puzzles present in daily bundle.\n")
    return bundle


def test_raster_specifications(bundle):
    print("Test 2: Verifying 80mm Thermal Raster Specifications (576 Dots / 72 Bytes)...")
    rasterizers = [
        ("Sudoku", render_sudoku_raster, "sudoku"),
        ("WordSearch", render_wordsearch_raster, "wordsearch"),
        ("Nonogram", render_nonogram_raster, "nonogram"),
        ("Stars (Queens)", render_queens_dithered_raster, "queens"),
        ("Jumble", render_jumble_raster, "jumble"),
        ("Binary", render_binary_raster, "binary"),
        ("Mines", render_mines_raster, "mines"),
        ("Tents", render_tents_raster, "tents"),
        ("Bridges", render_bridges_raster, "bridges"),
        ("Killer", render_killer_raster, "killer"),
        ("Cryptogram", render_cryptogram_raster, "cryptogram"),
        ("Tango", render_tango_raster, "tango"),
        ("Ladder", render_ladder_raster, "ladder"),
        ("Wheel", render_wheel_raster, "wheel"),
        ("Lights", render_lights_raster, "lights"),
        ("Loop", render_loop_raster, "loop"),
    ]

    for name, fn, key in rasterizers:
        puzzle_data = bundle[key]
        raster = fn(puzzle_data)
        plugin = DEFAULT_REGISTRY.get(key)
        assert plugin is not None, f"Missing plugin for '{key}'"
        plugin_raster = plugin.render_raster(puzzle_data)
        assert len(plugin_raster) == len(raster), f"{name}: Plugin raster length mismatch"

        # 1. Verify minimum length
        assert len(raster) >= 8, f"{name}: Raster data too short ({len(raster)} bytes)"

        # 2. Verify ESC/POS GS v 0 Command Header: 0x1D 0x76 0x30 0x00
        assert raster[0:4] == bytes([0x1D, 0x76, 0x30, 0x00]), f"{name}: Invalid GS v 0 header: {raster[0:4]}"

        # 3. Verify width is strictly 72 bytes (576 dots)
        width_bytes = raster[4] | (raster[5] << 8)
        assert width_bytes == THERMAL_WIDTH_BYTES, (
            f"{name}: Width must be {THERMAL_WIDTH_BYTES} bytes (576 dots), got {width_bytes}"
        )

        # 4. Verify height
        height_dots = raster[6] | (raster[7] << 8)
        assert height_dots > 50, f"{name}: Height dots unreasonably small ({height_dots})"

        # 5. Verify byte alignment: total length == 8 + width_bytes * height_dots
        expected_len = 8 + width_bytes * height_dots
        assert len(raster) == expected_len, (
            f"{name}: Length mismatch. Expected {expected_len} bytes, got {len(raster)}"
        )

        # 6. Verify thermal duty cycle & peak current safety
        duty = calculate_duty_cycle(raster)
        assert duty["is_safe"], f"{name}: Exceeded safe thermal limits! {duty}"
        assert duty["average_duty_cycle_pct"] <= 35.0, (
            f"{name}: Average duty cycle too high: {duty['average_duty_cycle_pct']}%"
        )
        assert duty["max_consecutive_dense_lines"] <= 16, (
            f"{name}: Too many consecutive dense lines: {duty['max_consecutive_dense_lines']}"
        )

        print(f"  -> {name:15}: {duty['width_dots']}x{duty['height_dots']} dots | {len(raster)} bytes | Avg Duty: {duty['average_duty_cycle_pct']:5.2f}% | Safe: OK")

    print(f"  -> Passed! All {len(rasterizers)} rasterizers conform strictly to 576-dot thermal standard.\n")


def test_text_receipt_format(bundle):
    print("Test 3: Verifying Monospaced Text ESC/POS Receipt Output...")
    receipt_bytes = build_daily_receipt_bytes(bundle)

    # 1. Begins with ESC @ (Init)
    assert receipt_bytes.startswith(CMD_INIT), "Text receipt must begin with ESC @"

    # 2. Ends with partial cut command
    assert receipt_bytes.endswith(CMD_CUT_PARTIAL), "Text receipt must end with partial cut command"

    # 3. Pre-cut feed check: at least 4 LFs before cut command
    pre_cut_slice = receipt_bytes[-(len(CMD_CUT_PARTIAL) + 4) : -len(CMD_CUT_PARTIAL)]
    assert pre_cut_slice == LF * 4, f"Text receipt must include 4 line feeds before cutter offset. Got: {pre_cut_slice}"

    # 4. PUZZLE_HEADER_SPEC compliance: check strict one-word titles
    receipt_text = receipt_bytes.decode("latin-1")
    for title in ["--- SUDOKU ---", "--- SEARCH ---", "--- NONOGRAM ---", "--- STARS ---", "--- JUMBLE ---", "--- BINARY ---", "--- MINES ---", "--- TENTS ---", "--- BRIDGES ---", "--- KILLER ---", "--- CRYPTOGRAM ---", "--- TANGO ---", "--- LADDER ---", "--- WHEEL ---", "--- LIGHTS ---"]:
        assert title in receipt_text, f"Missing canonical title '{title}' in text receipt"

    print("  -> Passed! Text receipt contains all 15 canonical headers, pre-cut feeds, and cutter commands.\n")


def test_hybrid_receipt_format(bundle):
    print("Test 4: Verifying Hybrid ESC/POS (Text Headers + 1-Bit Raster Graphics)...")
    hybrid_bytes = build_hybrid_daily_receipt_bytes(bundle)

    # 1. Begins with ESC @ (Init)
    assert hybrid_bytes.startswith(CMD_INIT), "Hybrid receipt must begin with ESC @"

    # 2. Ends with partial cut command
    assert hybrid_bytes.endswith(CMD_CUT_PARTIAL), "Hybrid receipt must end with partial cut command"

    # 3. Contains embedded GS v 0 raster commands
    gs_v_0_signature = bytes([0x1D, 0x76, 0x30, 0x00, 72, 0])
    count = hybrid_bytes.count(gs_v_0_signature)
    assert count >= 8, f"Expected multiple embedded GS v 0 raster commands in hybrid receipt, found {count}"

    # 4. Pre-cut feed check
    pre_cut_slice = hybrid_bytes[-(len(CMD_CUT_PARTIAL) + 4) : -len(CMD_CUT_PARTIAL)]
    assert pre_cut_slice == LF * 4, "Hybrid receipt must include 4 line feeds before cutter offset"

    print(f"  -> Passed! Hybrid receipt verified ({len(hybrid_bytes)} total bytes with {count} 576-dot graphics).\n")


def test_solution_key_spec(bundle):
    print("Test 5: Verifying ASCII Solution Key Specification Compliance...")
    bundle_with_sol = dict(bundle)
    bundle_with_sol["show_solutions"] = True

    receipt_bytes = build_daily_receipt_bytes(bundle_with_sol)
    receipt_text = receipt_bytes.decode("latin-1")

    # Check solution key header
    assert "[ SOLUTION KEY ]" in receipt_text, "Missing [ SOLUTION KEY ] header"

    # Check that each game is represented in the solution key
    expected_subtitles = ["SUDOKU", "SEARCH", "NONOGRAM", "STARS", "JUMBLE", "BINARY", "MINES", "TENTS", "BRIDGES", "KILLER", "CRYPTOGRAM", "TANGO", "LADDER"]
    for sub in expected_subtitles:
        assert sub in receipt_text, f"Missing '{sub}' in Solution Key"

    # Verify no line in the solution key section exceeds 48 printable characters
    import re
    lines = receipt_text.split("\n")
    in_solution_key = False
    for line in lines:
        if "[ SOLUTION KEY ]" in line:
            in_solution_key = True
        if in_solution_key:
            # Strip ESC and GS hardware control sequences and unprintable bytes
            printable = re.sub(r'\x1b[a-zA-Z@!][\x00-\xff]?|\x1d[a-zA-Z@!][\x00-\xff]?', '', line)
            printable = re.sub(r'[\x00-\x1f]', '', printable)
            assert len(printable) <= 48, f"Line in solution key exceeds 48 printable characters ({len(printable)} chars): '{printable}'"

    print("  -> Passed! Solution Key strictly conforms to 48-column monospaced specification.\n")


if __name__ == "__main__":
    print("================================================================")
    print("RUNNING 80mm THERMAL RECEIPT FORMAT & SPECIFICATION VERIFICATION")
    print("================================================================\n")

    b = test_bundle_completeness()
    test_raster_specifications(b)
    test_text_receipt_format(b)
    test_hybrid_receipt_format(b)
    test_solution_key_spec(b)

    print("================================================================")
    print("ALL 80mm THERMAL RECEIPT FORMAT VERIFICATION TESTS PASSED (5/5)!")
    print("================================================================")

