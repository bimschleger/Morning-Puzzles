"""
Tests for Staggered Difficulty Distribution & Dynamic Bundle Composition
Verifies:
1. get_tier_for_slot mathematical distribution for N=3, 5, 7, etc.
2. generate_bundle slot difficulty assignment (Easy -> Medium -> Medium -> Hard -> Extreme/Hard for N=5)
3. Fallback logic when a puzzle does not support Extreme
4. Dynamic subtitle generation ("DAILY <N>-PUZZLE MIX")
5. Progressive ordering in DailyReceiptComposer (puzzles and solutions print in slot order)
"""

import unittest
from app.puzzles.registry import DEFAULT_REGISTRY, PuzzleRegistry
from app.renderer.composer import DailyReceiptComposer


class TestStaggeredDifficulty(unittest.TestCase):
    def test_tier_distribution_n5(self):
        """Verify N=5 slots: 0=easy, 1=medium, 2=medium, 3=hard, 4=extreme."""
        expected = ["easy", "medium", "medium", "hard", "extreme"]
        actual = [PuzzleRegistry.get_tier_for_slot(i, 5) for i in range(5)]
        self.assertEqual(actual, expected)

    def test_tier_distribution_n3(self):
        """Verify N=3 slots: 0=easy, 1=medium, 2=extreme."""
        expected = ["easy", "medium", "extreme"]
        actual = [PuzzleRegistry.get_tier_for_slot(i, 3) for i in range(3)]
        self.assertEqual(actual, expected)

    def test_tier_distribution_n7(self):
        """Verify N=7 slots."""
        expected = ["easy", "easy", "medium", "medium", "hard", "hard", "extreme"]
        actual = [PuzzleRegistry.get_tier_for_slot(i, 7) for i in range(7)]
        self.assertEqual(actual, expected)

    def test_tier_distribution_single(self):
        self.assertEqual(PuzzleRegistry.get_tier_for_slot(0, 1), "medium")

    def test_generate_bundle_n5_staggered(self):
        """Test bundle generation with count=5 and difficulty='random'."""
        for _ in range(2):  # 2 trials to verify progressive slot distribution
            bundle = DEFAULT_REGISTRY.generate_bundle(difficulty="random", count=5)
            self.assertEqual(bundle["subtitle"], "DAILY 5-PUZZLE MIX")
            self.assertEqual(len(bundle["puzzle_order"]), 5)

            order = bundle["puzzle_order"]

            # Check slot 0: Easy
            p0 = bundle[order[0]]
            self.assertEqual(p0["difficulty"], "easy")

            # Check slot 1: Medium
            p1 = bundle[order[1]]
            self.assertEqual(p1["difficulty"], "medium")

            # Check slot 2: Medium
            p2 = bundle[order[2]]
            self.assertEqual(p2["difficulty"], "medium")

            # Check slot 3: Hard
            p3 = bundle[order[3]]
            self.assertEqual(p3["difficulty"], "hard")

            # Check slot 4: Extreme or Hard (fallback)
            p4 = bundle[order[4]]
            plugin4 = DEFAULT_REGISTRY.get(order[4])
            if "extreme" in plugin4.supported_difficulties:
                self.assertEqual(p4["difficulty"], "extreme")
            else:
                self.assertEqual(p4["difficulty"], "hard")

    def test_generate_bundle_uniform_override(self):
        """Test that explicit difficulty overrides staggered progression."""
        bundle = DEFAULT_REGISTRY.generate_bundle(difficulty="easy", count=5)
        for pid in bundle["puzzle_order"]:
            self.assertEqual(bundle[pid]["difficulty"], "easy")
        self.assertEqual(bundle["subtitle"], "DAILY 5-PUZZLE MIX")

    def test_receipt_composer_progressive_order(self):
        """Test that DailyReceiptComposer renders puzzles and solutions in puzzle_order."""
        bundle = DEFAULT_REGISTRY.generate_bundle(difficulty="random", count=5)
        order = bundle["puzzle_order"]
        composer = DailyReceiptComposer()
        receipt_text = composer.build_receipt(daily_data=bundle, style="text", show_solutions=True).decode("latin-1", errors="replace")

        # Subtitle check
        self.assertIn("DAILY 5-PUZZLE MIX", receipt_text)

        # Verify puzzle body order: each title should appear after the previous one
        last_pos = 0
        for pid in order:
            plugin = DEFAULT_REGISTRY.get(pid)
            title_marker = f"--- {plugin.title.upper()} ---"
            pos = receipt_text.find(title_marker, last_pos)
            self.assertNotEqual(pos, -1, f"Marker {title_marker} not found after pos {last_pos}")
            last_pos = pos

        # Verify solution key order: each subtitle should appear after the previous one in solution section
        sol_marker = "[ SOLUTION KEY ]"
        sol_pos = receipt_text.find(sol_marker)
        self.assertNotEqual(sol_pos, -1, "Solution key header missing")

        last_pos = sol_pos
        for pid in order:
            plugin = DEFAULT_REGISTRY.get(pid)
            sol_title = f"{plugin.title.upper()}\n"
            pos = receipt_text.find(sol_title, last_pos)
            self.assertNotEqual(pos, -1, f"Solution {sol_title.strip()} not found after pos {last_pos}")
            last_pos = pos


if __name__ == "__main__":
    unittest.main()
