#!/usr/bin/env python3
"""
Morning Puzzles - Unified Automated Test Suite & Verification Harness
Run with:
    python3 run_tests.py                     # Runs all standard tiers (standards, logic, raster, firmware)
    python3 run_tests.py --tier standards    # Presentation, naming, <=100 char instructions, solution key
    python3 run_tests.py --tier logic        # Mathematical accuracy, rule checking, unique solvability
    python3 run_tests.py --tier raster       # 576-dot thermal specs, <=35% duty cycle, golden snapshots
    python3 run_tests.py --tier firmware     # C++ inventory parity, Arduino sync, host compilation
    python3 run_tests.py --tier stress       # Monte Carlo combinatorial stress loop (zero crashes, 100% convergence)
    python3 run_tests.py --puzzle sudoku     # Filter by specific puzzle ID
    python3 run_tests.py --update-snapshots  # Regenerate golden raster snapshots
"""

import os
import sys
import argparse
import hashlib
import json
import time

# Ensure server package is on sys.path
SERVER_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "server")
if SERVER_DIR not in sys.path:
    sys.path.insert(0, SERVER_DIR)

from app.puzzles.registry import DEFAULT_REGISTRY
from app.renderer.canvas import calculate_duty_cycle


def run_standards_tier(puzzle_filter: str = None) -> bool:
    print("\n" + "=" * 70)
    print(">>> TIER 1: PRESENTATION, NAMING & CONTRACT STANDARDS <<<")
    print("=" * 70)
    try:
        import test_puzzle_standards
        test_puzzle_standards.test_titles_and_forbidden_terms()
        test_puzzle_standards.test_difficulty_presentation_and_theme_rules()
        test_puzzle_standards.test_description_length_and_canonical_formula()
        test_puzzle_standards.test_solution_key_spec()
        test_puzzle_standards.test_simulator_consistency()
        test_puzzle_standards.test_plugin_contract_compliance()
        print("[TIER 1 PASSED] All presentation and authoring standards verified.\n")
        return True
    except Exception as e:
        print(f"[TIER 1 FAILED] {e}\n")
        return False


def run_logic_tier(puzzle_filter: str = None) -> bool:
    print("\n" + "=" * 70)
    print(">>> TIER 2: GAME LOGIC, MATHEMATICAL RULES & SOLVABILITY ACCURACY <<<")
    print("=" * 70)

    plugins = DEFAULT_REGISTRY.get_all()
    if puzzle_filter:
        plugins = [p for p in plugins if p.puzzle_id == puzzle_filter or p.title.lower() == puzzle_filter.lower()]
        if not plugins:
            print(f"No registered puzzle matches filter '{puzzle_filter}'")
            return False

    all_passed = True
    total_checks = 0

    for plugin in plugins:
        pid = plugin.puzzle_id
        title = plugin.title
        difficulties = plugin.supported_difficulties if plugin.has_difficulty else ["medium"]

        print(f"Verifying {title} ({pid}):")
        for diff in difficulties:
            total_checks += 1
            start_t = time.time()
            try:
                puzzle_data = plugin.generate(difficulty=diff, seed=100 + hash(diff) % 1000)
                elapsed_gen = time.time() - start_t

                valid, msg = plugin.verify_accuracy(puzzle_data)
                elapsed_total = time.time() - start_t

                if valid:
                    print(f"  [{diff.upper():<7}] -> PASS ({msg}) [gen={elapsed_gen*1000:.1f}ms, total={elapsed_total*1000:.1f}ms]")
                else:
                    print(f"  [{diff.upper():<7}] -> FAIL: {msg}")
                    all_passed = False
            except Exception as e:
                print(f"  [{diff.upper():<7}] -> CRASH: {e}")
                all_passed = False

    if all_passed:
        print(f"\n[TIER 2 PASSED] All {total_checks} logic & accuracy checks succeeded.\n")
    else:
        print(f"\n[TIER 2 FAILED] One or more puzzle accuracy verifications failed.\n")
    return all_passed


def run_raster_tier(puzzle_filter: str = None) -> bool:
    print("\n" + "=" * 70)
    print(">>> TIER 3: THERMAL RASTER SPECS, SAFETY & GOLDEN SNAPSHOTS <<<")
    print("=" * 70)
    try:
        import test_thermal_format
        import test_thermal_snapshots

        test_thermal_snapshots.test_thermal_snapshots_and_safety()
        bundle = test_thermal_format.test_bundle_completeness()
        test_thermal_format.test_raster_specifications(bundle)
        test_thermal_format.test_text_receipt_format(bundle)
        test_thermal_format.test_hybrid_receipt_format(bundle)
        test_thermal_format.test_solution_key_spec(bundle)

        print("[TIER 3 PASSED] All thermal raster specs, duty cycles, and snapshots verified.\n")
        return True
    except Exception as e:
        print(f"[TIER 3 FAILED] {e}\n")
        return False


def run_firmware_tier(strict: bool = False) -> bool:
    print("\n" + "=" * 70)
    print(">>> TIER 4: FIRMWARE PARITY & C++ HOST COMPILATION <<<")
    print("=" * 70)
    try:
        import test_firmware_parity
        test_firmware_parity.run_firmware_tests(strict=strict)
        print("[TIER 4 PASSED] Firmware synchronization and host compilation verified.\n")
        return True
    except Exception as e:
        print(f"[TIER 4 FAILED] {e}\n")
        return False


def run_stress_tier(iterations: int = 5, puzzle_filter: str = None) -> bool:
    print("\n" + "=" * 70)
    print(f">>> TIER 5: MONTE CARLO COMBINATORIAL STRESS LOOP ({iterations} ITERATIONS) <<<")
    print("=" * 70)

    plugins = DEFAULT_REGISTRY.get_all()
    if puzzle_filter:
        plugins = [p for p in plugins if p.puzzle_id == puzzle_filter or p.title.lower() == puzzle_filter.lower()]
        if not plugins:
            print(f"No registered puzzle matches filter '{puzzle_filter}'")
            return False

    all_passed = True
    total_runs = 0
    total_start = time.time()

    for plugin in plugins:
        pid = plugin.puzzle_id
        title = plugin.title
        difficulties = plugin.supported_difficulties if plugin.has_difficulty else ["medium"]

        print(f"Stress testing {title} ({pid}) over {iterations} randomized iterations per difficulty:")

        for diff in difficulties:
            diff_start = time.time()
            failures = 0
            for i in range(iterations):
                total_runs += 1
                seed = int(time.time() * 1000 + i * 997 + hash(diff)) % 10000000
                try:
                    p = plugin.generate(difficulty=diff, seed=seed)
                    valid, msg = plugin.verify_accuracy(p)
                    if not valid:
                        failures += 1
                        print(f"    FAIL at iter #{i+1} (seed={seed}): {msg}")
                        all_passed = False
                    # Also test raster generation and duty cycle
                    raster = plugin.render_raster(p)
                    metrics = calculate_duty_cycle(raster)
                    if not metrics.get("is_safe"):
                        failures += 1
                        print(f"    THERMAL HAZARD at iter #{i+1} (seed={seed}): avg_duty={metrics.get('average_duty_cycle_pct')}%")
                        all_passed = False
                except Exception as e:
                    failures += 1
                    print(f"    CRASH at iter #{i+1} (seed={seed}): {e}")
                    all_passed = False

            elapsed = time.time() - diff_start
            status = "PASS" if failures == 0 else f"FAIL ({failures}/{iterations} failed)"
            print(f"  [{diff.upper():<7}] -> {status} ({iterations} runs in {elapsed:.2f}s, avg {elapsed*1000/iterations:.1f}ms/run)")

    total_time = time.time() - total_start
    if all_passed:
        print(f"\n[TIER 5 PASSED] Completed {total_runs} stress iterations with 100% success rate in {total_time:.2f}s.\n")
    else:
        print(f"\n[TIER 5 FAILED] Stress testing encountered one or more failures.\n")
    return all_passed


def update_golden_snapshots():
    print("\nRecording new golden snapshots for all plugins...")
    snapshots_dir = os.path.join(SERVER_DIR, "tests", "snapshots")
    os.makedirs(snapshots_dir, exist_ok=True)
    snapshots_file = os.path.join(snapshots_dir, "golden_registry.json")

    snapshots = {}
    for plugin in DEFAULT_REGISTRY.get_all():
        p = plugin.generate("medium", seed=42)
        raster = plugin.render_raster(p)
        sha256 = hashlib.sha256(raster).hexdigest()
        metrics = calculate_duty_cycle(raster)
        snapshots[plugin.puzzle_id] = {
            "title": plugin.title,
            "sha256": sha256,
            "byte_length": len(raster),
            "width_dots": metrics.get("width_dots"),
            "height_dots": metrics.get("height_dots"),
            "average_duty_cycle_pct": metrics.get("average_duty_cycle_pct"),
            "max_consecutive_dense_lines": metrics.get("max_consecutive_dense_lines"),
            "is_safe": metrics.get("is_safe"),
        }
        print(f"  {plugin.title:<12} -> SHA: {sha256[:16]}... len={len(raster)}")

    with open(snapshots_file, "w", encoding="utf-8") as f:
        json.dump(snapshots, f, indent=2)
    print(f"Updated {snapshots_file} with {len(snapshots)} golden snapshots.\n")


def main():
    parser = argparse.ArgumentParser(description="Morning Puzzles Unified Automated Test Suite")
    parser.add_argument(
        "--tier",
        choices=["all", "standards", "logic", "raster", "firmware", "stress"],
        default="all",
        help="Test tier to run (default: all fast tiers: standards, logic, raster, firmware)",
    )
    parser.add_argument("--puzzle", "-p", help="Filter tests to a specific puzzle ID (e.g. sudoku, binary)")
    parser.add_argument("--iterations", "-n", type=int, default=5, help="Number of iterations for stress testing")
    parser.add_argument("--strict-firmware", action="store_true", help="Enforce 100% C++ parity (fail on missing generators)")
    parser.add_argument("--update-snapshots", action="store_true", help="Regenerate golden raster snapshots")
    args = parser.parse_args()

    if args.update_snapshots:
        update_golden_snapshots()
        return

    success = True
    tier = args.tier

    if tier in ("all", "standards"):
        if not run_standards_tier(args.puzzle):
            success = False

    if tier in ("all", "logic"):
        if not run_logic_tier(args.puzzle):
            success = False

    if tier in ("all", "raster"):
        if not run_raster_tier(args.puzzle):
            success = False

    if tier in ("all", "firmware"):
        if not run_firmware_tier(strict=args.strict_firmware):
            success = False

    if tier == "stress":
        if not run_stress_tier(iterations=args.iterations, puzzle_filter=args.puzzle):
            success = False

    print("=" * 70)
    if success:
        print("[SUMMARY] ALL REQUESTED TEST TIERS COMPLETED SUCCESSFULLY (EXIT 0)")
        print("=" * 70)
        sys.exit(0)
    else:
        print("[SUMMARY] TEST SUITE FAILED (EXIT 1)")
        print("=" * 70)
        sys.exit(1)


if __name__ == "__main__":
    main()
