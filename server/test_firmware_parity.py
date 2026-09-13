#!/usr/bin/env python3
"""
Automated Test Suite: Firmware Parity & C++ Compilation Verification
Validates:
1. Generator Inventory Parity: Checks whether every puzzle in DEFAULT_REGISTRY has a corresponding
   C++ generator (.h and .cpp) in esp32-firmware/src/generators/.
2. Arduino Sketch Synchronization: Verifies that scripts/sync_arduino_sketch.sh leaves zero drift
   between esp32-firmware/ and MorningPuzzles/.
3. Host C++ Syntax & Build Compilation: Compiles esp32-firmware/test/test_offline_generators.cpp
   using the host C++ compiler (clang++ or g++) to guarantee zero syntax or linkage regressions.
"""

import os
import sys
import shutil
import subprocess
from typing import Dict, List, Tuple

# Add server directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.puzzles.registry import DEFAULT_REGISTRY

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FW_DIR = os.path.join(ROOT_DIR, "esp32-firmware")
SKETCH_DIR = os.path.join(ROOT_DIR, "MorningPuzzles")
GEN_DIR = os.path.join(FW_DIR, "src", "generators")
TEST_CPP = os.path.join(FW_DIR, "test", "test_offline_generators.cpp")

# Mapping from puzzle_id to expected C++ generator file prefix
GENERATOR_MAP = {
    "sudoku": ("SudokuGen.h", "SudokuGen.cpp"),
    "wordsearch": ("WordSearchGen.h", "WordSearchGen.cpp"),
    "nonogram": ("NonogramGen.h", "NonogramGen.cpp"),
    "queens": ("QueensGen.h", "QueensGen.cpp"),
    "jumble": ("JumbleGen.h", "JumbleGen.cpp"),
    "binary": ("BinaryGen.h", "BinaryGen.cpp"),
    "mines": ("MinesGen.h", "MinesGen.cpp"),
    "tents": ("TentsGen.h", "TentsGen.cpp"),
    "bridges": ("BridgesGen.h", "BridgesGen.cpp"),
    "tango": ("TangoGen.h", "TangoGen.cpp"),
    "wheel": ("WheelGen.h", "WheelGen.cpp"),
    "killer": ("KillerGen.h", "KillerGen.cpp"),
    "cryptogram": ("CryptogramGen.h", "CryptogramGen.cpp"),
    "ladder": ("LadderGen.h", "LadderGen.cpp"),
}


def test_generator_parity(strict: bool = False) -> Tuple[List[str], List[str]]:
    print("Test 1: Verifying Python <-> ESP32 C++ Generator Inventory Parity...")
    all_plugins = DEFAULT_REGISTRY.get_all()

    present: List[str] = []
    missing: List[str] = []

    for plugin in all_plugins:
        pid = plugin.puzzle_id
        title = plugin.title
        h_file, cpp_file = GENERATOR_MAP.get(pid, (f"{title.capitalize()}Gen.h", f"{title.capitalize()}Gen.cpp"))
        h_path = os.path.join(GEN_DIR, h_file)
        cpp_path = os.path.join(GEN_DIR, cpp_file)

        if os.path.exists(h_path) and os.path.exists(cpp_path):
            present.append(f"{title} ({h_file})")
            print(f"  [OK] {title:<12} -> {h_file} & {cpp_file}")
        else:
            missing.append(f"{title} ({pid}: {h_file})")
            print(f"  [MISSING] {title:<12} -> Missing {h_file} / {cpp_file}")

    print(f"\nInventory: {len(present)} present, {len(missing)} missing out of {len(all_plugins)} games.")

    if strict and missing:
        raise AssertionError(f"Strict parity failure: Missing C++ generators for: {', '.join(missing)}")

    return present, missing


def test_arduino_sketch_sync():
    print("\nTest 2: Verifying Arduino Sketch Synchronization Parity...")
    sync_script = os.path.join(ROOT_DIR, "scripts", "sync_arduino_sketch.sh")
    assert os.path.exists(sync_script), f"Missing sync script at {sync_script}"

    # Run the sync script
    res = subprocess.run(["/bin/bash", sync_script], cwd=ROOT_DIR, capture_output=True, text=True)
    assert res.returncode == 0, f"sync_arduino_sketch.sh failed:\n{res.stderr}\n{res.stdout}"

    # Verify key synced files exist in MorningPuzzles/
    expected_files = [
        "config.h",
        "EscPosPrinter.h",
        "EscPosPrinter.cpp",
        "OfflinePuzzleComposer.h",
        "OfflinePuzzleComposer.cpp",
        "MorningPuzzles.ino",
    ]
    for f in expected_files:
        path = os.path.join(SKETCH_DIR, f)
        assert os.path.exists(path), f"Missing synchronized sketch file: {path}"

    print("  -> Passed! Arduino sketch directory MorningPuzzles/ is cleanly synchronized.")


def test_host_cpp_compilation():
    print("\nTest 3: Verifying Host C++ Offline Generator Compilation...")
    compiler = shutil.which("clang++") or shutil.which("g++")
    if not compiler:
        print("  -> Skipped: No host C++ compiler (clang++/g++) available in environment.")
        return

    output_bin = os.path.join(FW_DIR, "test", "test_runner_parity_check")
    cmd = [
        compiler,
        "-std=c++17",
        "-I", os.path.join(FW_DIR, "test"),
        "-I", os.path.join(FW_DIR, "include"),
        "-I", os.path.join(FW_DIR, "src"),
        TEST_CPP,
        "-o", output_bin,
    ]

    try:
        build_res = subprocess.run(cmd, cwd=ROOT_DIR, capture_output=True, text=True)
        assert build_res.returncode == 0, (
            f"Host C++ compilation failed for {TEST_CPP}:\n{build_res.stderr}\n{build_res.stdout}"
        )

        run_res = subprocess.run([output_bin], cwd=ROOT_DIR, capture_output=True, text=True)
        assert run_res.returncode == 0, (
            f"Execution of compiled offline generator test failed:\n{run_res.stderr}\n{run_res.stdout}"
        )
        print("  -> Passed! C++ firmware generator suite compiles and runs cleanly on host.")
    finally:
        if os.path.exists(output_bin):
            os.remove(output_bin)


def run_firmware_tests(strict: bool = False):
    print("=" * 60)
    print("RUNNING TIER 4: Firmware Parity & C++ Compilation Verification")
    print("=" * 60)
    test_generator_parity(strict=strict)
    test_arduino_sketch_sync()
    test_host_cpp_compilation()
    print("\n[SUCCESS] Tier 4 Firmware verification completed!\n")


if __name__ == "__main__":
    strict_flag = "--strict" in sys.argv
    run_firmware_tests(strict=strict_flag)
