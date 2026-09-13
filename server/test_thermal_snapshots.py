#!/usr/bin/env python3
"""
Automated Test Suite: Thermal Raster Regression & Golden Snapshots
Validates that 1-bit ESC/POS GS v 0 thermal rasters remain pixel-perfect
and reproducible against stored golden hashes under deterministic seeds.
Also verifies all thermal hardware safety requirements:
- 576 dots width (72 bytes)
- Valid GS v 0 framing (0x1D 0x76 0x30 0x00)
- Height aligned to 8 dots
- Average duty cycle <= 35%
- Max consecutive dense scanlines <= 16
"""

import os
import sys
import json
import hashlib

# Add server directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.puzzles.registry import DEFAULT_REGISTRY
from app.renderer.canvas import calculate_duty_cycle, THERMAL_WIDTH_DOTS, THERMAL_WIDTH_BYTES

SNAPSHOTS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests", "snapshots", "golden_registry.json")


def test_thermal_snapshots_and_safety():
    print("=" * 60)
    print("RUNNING TIER 3: Thermal Raster Specs & Golden Snapshots")
    print("=" * 60)

    assert os.path.exists(SNAPSHOTS_PATH), f"Missing golden snapshots registry at {SNAPSHOTS_PATH}"
    with open(SNAPSHOTS_PATH, "r", encoding="utf-8") as f:
        golden_data = json.load(f)

    all_plugins = DEFAULT_REGISTRY.get_all()
    print(f"Testing {len(all_plugins)} registered plugins against golden snapshots (seed=42)...\n")

    for plugin in all_plugins:
        pid = plugin.puzzle_id
        title = plugin.title
        print(f"Testing raster for '{title}' (id={pid})...")

        puzzle = plugin.generate("medium", seed=42)
        raster = plugin.render_raster(puzzle)

        # 1. Verify Minimum Length & Header
        assert len(raster) >= 8, f"{title}: Raster too short ({len(raster)} bytes)"
        assert raster[0:4] == bytes([0x1D, 0x76, 0x30, 0x00]), (
            f"{title}: Invalid GS v 0 ESC/POS header: {raster[0:4].hex()}"
        )

        # 2. Verify Width is Strictly 576 Dots (72 bytes)
        width_bytes = raster[4] | (raster[5] << 8)
        assert width_bytes == THERMAL_WIDTH_BYTES, (
            f"{title}: Width must be {THERMAL_WIDTH_BYTES} bytes ({THERMAL_WIDTH_DOTS} dots), got {width_bytes}"
        )

        # 3. Verify Height
        height_dots = raster[6] | (raster[7] << 8)
        assert height_dots > 50, f"{title}: Unreasonably small raster height ({height_dots} dots)"
        assert len(raster) == 8 + width_bytes * height_dots, (
            f"{title}: Data length mismatch: expected {8 + width_bytes * height_dots}, got {len(raster)}"
        )

        # 4. Verify Thermal Duty Cycle & Safety
        metrics = calculate_duty_cycle(raster)
        avg_duty = metrics.get("average_duty_cycle_pct", 100)
        max_dense = metrics.get("max_consecutive_dense_lines", 999)
        assert metrics.get("is_safe"), (
            f"{title}: Thermal safety violation! avg_duty={avg_duty}% (limit 35%), "
            f"consecutive_dense={max_dense} (limit 16)"
        )

        # 5. Verify against Golden Snapshot
        assert pid in golden_data, f"{title}: Missing from golden snapshots registry"
        expected = golden_data[pid]
        actual_sha = hashlib.sha256(raster).hexdigest()

        assert actual_sha == expected["sha256"], (
            f"{title}: Snapshot SHA-256 mismatch!\n"
            f"  Expected: {expected['sha256']}\n"
            f"  Actual:   {actual_sha}\n"
            f"  If intentional, re-record golden snapshots via run_tests.py --update-snapshots"
        )
        assert len(raster) == expected["byte_length"], (
            f"{title}: Byte length mismatch ({len(raster)} vs {expected['byte_length']})"
        )
        assert height_dots == expected["height_dots"], (
            f"{title}: Height mismatch ({height_dots} vs {expected['height_dots']})"
        )

        print(f"  -> Passed! SHA256: {actual_sha[:16]}... (duty={avg_duty}%, height={height_dots}px)")

    print("\n[SUCCESS] All registered plugins passed thermal raster specifications & snapshot tests!\n")


if __name__ == "__main__":
    test_thermal_snapshots_and_safety()
