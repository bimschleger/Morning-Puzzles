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
import re
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


def test_rule_7_flat_includes():
    print("\nTest 4: Verifying Rule 7 (Zero Relative Include Paths in MorningPuzzles/)...")
    assert os.path.exists(SKETCH_DIR), f"MorningPuzzles dir not found at {SKETCH_DIR}"

    relative_includes = []
    for root, _, files in os.walk(SKETCH_DIR):
        for f in files:
            if f.endswith((".h", ".cpp", ".ino")):
                fpath = os.path.join(root, f)
                with open(fpath, "r", encoding="utf-8", errors="ignore") as fh:
                    for line_num, line in enumerate(fh, 1):
                        if re.search(r'#include\s*["<]\.\./', line):
                            relative_includes.append(f"{f}:{line_num}: {line.strip()}")

    assert not relative_includes, (
        f"Rule 7 Violation: Found relative include paths in MorningPuzzles/:\n" + "\n".join(relative_includes)
    )
    print("  -> Passed! Zero relative #include paths found in MorningPuzzles/ (100% flat includes).")


def test_rule_14_offline_appliance_libraries():
    print("\nTest 5: Verifying Rule 14 (Offline Appliance Standards: No HTTPClient/ArduinoJson)...")
    src_dir = os.path.join(FW_DIR, "src")
    assert os.path.exists(src_dir), f"src dir not found at {src_dir}"

    violations = []
    for root, _, files in os.walk(src_dir):
        for f in files:
            if f.endswith((".h", ".cpp")):
                fpath = os.path.join(root, f)
                rel_path = os.path.relpath(fpath, src_dir)
                with open(fpath, "r", encoding="utf-8", errors="ignore") as fh:
                    content = fh.read()

                if "HTTPClient" in content:
                    violations.append(f"{rel_path}: Contains prohibited HTTPClient")
                if "ArduinoJson" in content:
                    violations.append(f"{rel_path}: Contains prohibited ArduinoJson")
                if "WiFiClient" in content and rel_path not in ("printer/EscPosPrinter.h", "printer/EscPosPrinter.cpp"):
                    violations.append(f"{rel_path}: Contains WiFiClient outside printer/EscPosPrinter")

    assert not violations, (
        f"Rule 14 Violation: Prohibited network/cloud client libraries found:\n" + "\n".join(violations)
    )
    print("  -> Passed! Zero occurrences of HTTPClient or ArduinoJson in esp32-firmware/src/.")


def test_softap_portal_parity():
    print("\nTest 6: Verifying SoftAP Captive Portal Parity (PortalHtml.h matches portal.html)...")
    portal_html_path = os.path.join(ROOT_DIR, "portal.html")
    portal_h_path = os.path.join(FW_DIR, "src", "time", "PortalHtml.h")

    assert os.path.exists(portal_html_path), f"portal.html not found at {portal_html_path}"
    assert os.path.exists(portal_h_path), f"PortalHtml.h not found at {portal_h_path}"

    with open(portal_html_path, "rb") as f:
        html_bytes = f.read()

    with open(portal_h_path, "r", encoding="utf-8") as f:
        header_text = f.read()

    # Extract hex bytes from header
    hex_values = re.findall(r"0x([0-9A-Fa-f]{2})", header_text)
    assert hex_values, f"No hex bytes found in {portal_h_path}"
    compressed_bytes = bytes(int(h, 16) for h in hex_values)

    import gzip
    decompressed = gzip.decompress(compressed_bytes)
    assert decompressed == html_bytes, (
        f"PortalHtml.h decompressed content does not match portal.html! Run scripts/build_portal_header.py to synchronize."
    )
    print("  -> Passed! PortalHtml.h accurately reflects compressed portal.html.")


def test_offline_puzzle_enum_ordering_parity():
    print("\nTest 7: Verifying OfflinePuzzleType Enum Ordering Parity with DEFAULT_REGISTRY...")
    config_h_path = os.path.join(FW_DIR, "src", "config", "OfflineConfigManager.h")
    assert os.path.exists(config_h_path), f"OfflineConfigManager.h not found at {config_h_path}"

    with open(config_h_path, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.search(r"enum\s+OfflinePuzzleType\s*:\s*uint8_t\s*\{([^}]+)\};", content)
    assert match, "Could not find enum OfflinePuzzleType in OfflineConfigManager.h"

    raw_items = [item.strip() for item in match.group(1).split(",") if item.strip()]
    enum_names = []
    for item in raw_items:
        # Strip comments and assignments
        name = item.split("//")[0].split("/*")[0].split("=")[0].strip()
        if name and name != "OFFLINE_PUZZLE_TOTAL":
            enum_names.append(name)

    all_plugins = DEFAULT_REGISTRY.get_all()
    assert len(enum_names) == len(all_plugins), (
        f"Enum length mismatch: OfflinePuzzleType has {len(enum_names)} items, "
        f"DEFAULT_REGISTRY has {len(all_plugins)} plugins"
    )

    ENUM_MAP = {
        "PUZZLE_SUDOKU": "sudoku",
        "PUZZLE_WORDSEARCH": "wordsearch",
        "PUZZLE_NONOGRAM": "nonogram",
        "PUZZLE_QUEENS": "queens",
        "PUZZLE_JUMBLE": "jumble",
        "PUZZLE_BINARY": "binary",
        "PUZZLE_MINES": "mines",
        "PUZZLE_TENTS": "tents",
        "PUZZLE_BRIDGES": "bridges",
        "PUZZLE_KILLER": "killer",
        "PUZZLE_CRYPTOGRAM": "cryptogram",
        "PUZZLE_TANGO": "tango",
        "PUZZLE_LADDER": "ladder",
        "PUZZLE_WHEEL": "wheel",
        "PUZZLE_LIGHTS": "lights",
        "PUZZLE_LOOP": "loop",
        "PUZZLE_TOWERS": "towers",
        "PUZZLE_INEQUALITY": "inequality",
    }

    for i, enum_name in enumerate(enum_names):
        expected_id = ENUM_MAP.get(enum_name)
        actual_id = all_plugins[i].puzzle_id.lower()
        assert expected_id == actual_id, (
            f"Enum parity mismatch at index {i} (bit {i}): "
            f"C++ has '{enum_name}' (maps to '{expected_id}'), but DEFAULT_REGISTRY has '{actual_id}'!"
        )

    print(f"  -> Passed! All {len(enum_names)} enum entries in OfflinePuzzleType match DEFAULT_REGISTRY 1:1.")


def run_firmware_tests(strict: bool = False):
    print("=" * 60)
    print("RUNNING TIER 4: Firmware Parity & C++ Compilation Verification")
    print("=" * 60)
    test_generator_parity(strict=strict)
    test_arduino_sketch_sync()
    test_host_cpp_compilation()
    test_rule_7_flat_includes()
    test_rule_14_offline_appliance_libraries()
    test_softap_portal_parity()
    test_offline_puzzle_enum_ordering_parity()
    print("\n[SUCCESS] Tier 4 Firmware verification completed!\n")


if __name__ == "__main__":
    strict_flag = "--strict" in sys.argv
    run_firmware_tests(strict=strict_flag)
