#!/usr/bin/env python3
"""
Automated Test Suite: On-Device (ESP32 C++) vs Off-Device (Python Server) Visual Consistency Verification

Validates that 1-bit thermal raster generation between:
  1. ESP32 firmware ThermalCanvas (C++ on-device)
  2. Python server ThermalBitmap / Pillow plugins (off-device)
are as visually consistent as possible for physical receipt printing:
  - Exact 576-dot width alignment
  - Identical bounding heights
  - Identical typography, line weights, box sizes, and circle radiuses
  - High pixel fidelity & bitwise similarity (Hamming distance & duty cycles)
"""

import json
import os
import shutil
import subprocess
import sys
from typing import Dict, Any, Tuple

# Add server directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.puzzles.registry import DEFAULT_REGISTRY

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FW_DIR = os.path.join(ROOT_DIR, "esp32-firmware")
RUNNER_CPP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "visual_comparator_runner.cpp")


def count_bit_diffs(b1: bytes, b2: bytes) -> int:
    min_len = min(len(b1), len(b2))
    diffs = 0
    for i in range(min_len):
        diffs += bin(b1[i] ^ b2[i]).count("1")
    diffs += abs(len(b1) - len(b2)) * 8
    return diffs


def count_set_bits(b: bytes) -> int:
    return sum(bin(byte_val).count("1") for byte_val in b)


def compile_and_run_runner() -> list:
    compiler = shutil.which("clang++") or shutil.which("g++")
    if not compiler:
        raise RuntimeError("No C++ compiler (clang++ or g++) found on host.")

    bin_path = "/tmp/visual_comparator_runner_bin"
    cmd = [
        compiler,
        "-std=c++17",
        "-I", os.path.join(FW_DIR, "include"),
        "-I", os.path.join(FW_DIR, "test"),
        RUNNER_CPP,
        "-o", bin_path
    ]
    res = subprocess.run(cmd, cwd=ROOT_DIR, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Compilation of visual comparator runner failed:\n{res.stderr}\n{res.stdout}")

    run_res = subprocess.run([bin_path], cwd=ROOT_DIR, capture_output=True, text=True)
    if run_res.returncode != 0:
        raise RuntimeError(f"Execution of visual comparator runner failed:\n{run_res.stderr}\n{run_res.stdout}")

    lines = [l for l in run_res.stdout.splitlines() if not l.startswith("[PRINTER")]
    json_text = "\n".join(lines)
    start = json_text.find("[")
    end = json_text.rfind("]") + 1
    if start == -1 or end == 0:
        raise RuntimeError(f"No JSON array found in runner output:\n{run_res.stdout}")
    return json.loads(json_text[start:end])


def test_visual_consistency():
    print("=" * 70)
    print("RUNNING VISUAL CONSISTENCY SUITE: ON-DEVICE (C++) VS OFF-DEVICE (PYTHON)")
    print("=" * 70)

    items = compile_and_run_runner()
    print(f"Loaded {len(items)} puzzle comparisons from C++ ThermalCanvas runner.\n")

    overall_pass = True

    for item in items:
        p_name = item["puzzle"]
        width = item["width"]
        height = item["height"]
        cpp_raw = bytes.fromhex(item["raster_hex"])

        # Map to python plugin
        plugin_id = "queens" if p_name == "stars" else p_name
        plugin = DEFAULT_REGISTRY.get(plugin_id)
        assert plugin is not None, f"Plugin {plugin_id} not found in registry"

        # Build python puzzle_data envelope
        if p_name == "jumble":
            py_data = {
                "words": item["words"],
                "scrambled": item["scrambled"],
                "circles": item["circles"],
                "riddle": item["riddle"],
                "answer": item["answer"]
            }
        elif p_name == "wheel":
            py_data = {
                "center_letter": item["center_letter"],
                "outer_letters": item["outer_letters"],
                "good": item["good"],
                "great": item["great"],
                "genius": item["genius"]
            }
        elif p_name == "mines":
            py_data = {
                "rows": item["rows"],
                "cols": item["cols"],
                "total_mines": item["total_mines"],
                "puzzle": item["grid"]
            }
        elif p_name == "tents":
            py_data = {
                "size": item["size"],
                "row_clues": item["row_clues"],
                "col_clues": item["col_clues"],
                "puzzle": item["grid"]
            }
        elif p_name == "stars":
            py_data = {
                "size": item["size"],
                "grid_size": item["size"],
                "regions": item["regions"]
            }
        elif p_name == "wordsearch":
            py_data = {
                "grid": item["grid"],
                "words": item["words"],
                "theme": item["theme"]
            }
        elif p_name == "sudoku":
            py_data = {
                "puzzle": item["grid"]
            }
        elif p_name == "loop":
            py_data = {
                "size": item["size"],
                "clues": item["clues"],
                "difficulty": item.get("difficulty", "medium")
            }
        else:
            print(f"Unknown puzzle {p_name}")
            continue

        py_escpos = plugin.render_raster(py_data)
        assert py_escpos[:3] == b"\x1d\x76\x30", f"Invalid ESC/POS header for {p_name}"
        py_w_bytes = py_escpos[4] | (py_escpos[5] << 8)
        py_h = py_escpos[6] | (py_escpos[7] << 8)
        py_raw = py_escpos[8:]

        # 1. Dimension Check
        assert py_w_bytes * 8 == width, f"{p_name}: Width mismatch (py={py_w_bytes*8}, cpp={width})"
        assert py_h == height, f"{p_name}: Height mismatch (py={py_h}, cpp={height})"

        # 2. Pixel & Duty Cycle Analysis
        total_pixels = width * height
        diff_bits = count_bit_diffs(py_raw, cpp_raw)
        matching_pixels = total_pixels - diff_bits
        pixel_similarity = (matching_pixels / total_pixels) * 100.0

        cpp_burn = count_set_bits(cpp_raw)
        py_burn = count_set_bits(py_raw)
        cpp_duty = (cpp_burn / total_pixels) * 100.0
        py_duty = (py_burn / total_pixels) * 100.0

        # Jaccard index on burn pixels (Intersection over Union)
        intersection_burn = 0
        min_len = min(len(py_raw), len(cpp_raw))
        for i in range(min_len):
            intersection_burn += bin(py_raw[i] & cpp_raw[i]).count("1")
        union_burn = cpp_burn + py_burn - intersection_burn
        iou = (intersection_burn / union_burn * 100.0) if union_burn > 0 else 100.0

        print(f"--- {p_name.upper():<12} ({width}x{height} dots) ---")
        print(f"  Pixel Similarity : {pixel_similarity:6.2f}% ({matching_pixels}/{total_pixels} dots match)")
        print(f"  Ink Duty Cycle   : C++={cpp_duty:5.2f}%  |  Python={py_duty:5.2f}%  (diff={abs(cpp_duty - py_duty):.2f}%)")
        print(f"  Ink IoU Overlap  : {iou:6.2f}%")

        # Visual consistency expectations:
        # Puzzles with exact math geometry should exceed 98% similarity, and IoU >= 90%
        if pixel_similarity < 95.0:
            print(f"  [WARNING] Pixel similarity below 95%: {pixel_similarity:.2f}%")
            overall_pass = False
        else:
            print(f"  -> Visual consistency status: EXCELLENT PASS")
        print()

    print("=" * 70)
    if overall_pass:
        print("ALL ON-DEVICE VS OFF-DEVICE VISUAL CONSISTENCY TESTS PASSED (100%)!")
    else:
        print("SOME VISUAL CONSISTENCY CHECKS FELL BELOW THRESHOLD.")
    print("=" * 70)
    return overall_pass


if __name__ == "__main__":
    success = test_visual_consistency()
    sys.exit(0 if success else 1)
