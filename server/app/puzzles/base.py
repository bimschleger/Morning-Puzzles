"""
Morning Puzzles - Base Puzzle Plugin System
Defines the standard contracts for all puzzle types:
- BasePuzzleResult: Standardized envelope with dual dataclass / dict access.
- BasePuzzle: Abstract base class that all puzzle plugins must implement.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union, Tuple
import collections.abc


class BasePuzzleResult(collections.abc.Mapping):
    """
    Standardized envelope for puzzle generation results.
    Provides typed attributes and transparent dictionary access for 100%
    backwards compatibility with legacy callers and JSON serializers.
    """

    def __init__(
        self,
        puzzle_type: str,
        title: str,
        difficulty: Optional[str] = None,
        instruction: str = "",
        raw_data: Optional[Dict[str, Any]] = None,
    ):
        self.puzzle_type = puzzle_type
        self.title = title
        self.difficulty = difficulty
        self.instruction = instruction
        self._raw_data: Dict[str, Any] = dict(raw_data) if raw_data is not None else {}

        # Ensure canonical metadata is reflected in raw_data
        self._raw_data.setdefault("type", puzzle_type)
        if difficulty is not None:
            self._raw_data.setdefault("difficulty", difficulty)

    def to_dict(self) -> Dict[str, Any]:
        """Returns a standard dictionary representation suitable for JSON serialization."""
        res = dict(self._raw_data)
        res["type"] = self.puzzle_type
        if self.difficulty is not None:
            res["difficulty"] = self.difficulty
        return res

    # --- Mapping ABC implementation for dict compatibility ---
    def __getitem__(self, key: str) -> Any:
        return self._raw_data[key]

    def __setitem__(self, key: str, value: Any):
        self._raw_data[key] = value

    def __contains__(self, key: object) -> bool:
        return key in self._raw_data

    def __iter__(self):
        return iter(self._raw_data)

    def __len__(self) -> int:
        return len(self._raw_data)

    def get(self, key: str, default: Any = None) -> Any:
        return self._raw_data.get(key, default)

    def items(self):
        return self._raw_data.items()

    def keys(self):
        return self._raw_data.keys()

    def values(self):
        return self._raw_data.values()

    def __repr__(self) -> str:
        return f"<BasePuzzleResult type={self.puzzle_type!r} difficulty={self.difficulty!r}>"


class BasePuzzle(ABC):
    """
    Abstract Base Class for all Morning Puzzles games.
    Encapsulates generation, canonical instruction formatting, ASCII layout,
    solution key representation, and 576-dot thermal raster rendering.
    """

    @property
    @abstractmethod
    def puzzle_id(self) -> str:
        """Unique lowercase identifier for the puzzle (e.g. 'sudoku', 'mines')."""
        pass

    @property
    @abstractmethod
    def title(self) -> str:
        """Strict one-word uppercase title (e.g. 'SUDOKU', 'MINES')."""
        pass

    @property
    def has_difficulty(self) -> bool:
        """Whether the puzzle has difficulty levels (True for all except SEARCH)."""
        return True

    @property
    def default_difficulty(self) -> str:
        """Default difficulty level (usually 'medium')."""
        return "medium"

    @property
    def supported_difficulties(self) -> List[str]:
        """List of supported difficulty levels."""
        return ["easy", "medium", "hard"]

    @abstractmethod
    def generate(self, difficulty: str = "medium", **kwargs) -> BasePuzzleResult:
        """Generates a puzzle instance with the given difficulty."""
        pass

    @abstractmethod
    def get_instruction(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        """
        Returns the canonical one-sentence gameplay instruction.
        Must strictly follow:
        - <= 100 characters length
        - Starts with an approved imperative verb
        - Exactly one sentence (ends with single period)
        - Zero forbidden jargon terms
        """
        pass

    @abstractmethod
    def format_ascii_puzzle(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> str:
        """Returns the monospaced ASCII representation of the unsolved puzzle."""
        pass

    @abstractmethod
    def format_solution_key(self, puzzle_data: Union[BasePuzzleResult, Dict[str, Any]]) -> List[str]:
        """
        Returns the monospaced lines for the solution key block.
        - 2D ASCII grids must be pre-indented by exactly 6 spaces ('      ')
        - Coordinate and word lists must wrap to <= 46 characters
        - Standalone subtitle is handled by the composer, do NOT include subtitle here.
        """
        pass

    @abstractmethod
    def render_raster(
        self,
        puzzle_data: Union[BasePuzzleResult, Dict[str, Any]],
        target_width: int = 576,
    ) -> bytes:
        """
        Renders the puzzle to an ESC/POS GS v 0 1-bit raster bitmap (576 dots width).
        Must respect the 35% safe thermal duty cycle guideline.
        """
        pass

    @abstractmethod
    def verify_accuracy(
        self,
        puzzle_data: Union[BasePuzzleResult, Dict[str, Any]],
    ) -> Tuple[bool, str]:
        """
        Verifies that the generated puzzle and solution strictly obey all mathematical
        and game rules (e.g. valid cage sums, no trios, connectivity, uniqueness).
        Returns:
            Tuple[bool, str]: (True, "All rules satisfied") if valid,
                              or (False, "<detailed failure reason>") if invalid.
        """
        pass

    def render_guide_raster(self, target_width: int = 576) -> bytes:
        """
        Renders an authentic 1-bit thermal raster graphic (576 dots wide) demonstrating
        a VALID move versus an INVALID move side-by-side.
        """
        from .rules import get_game_rule
        from ..renderer.canvas import ThermalBitmap

        rule = get_game_rule(self.puzzle_id) or get_game_rule(self.title)
        height = 240
        tb = ThermalBitmap(target_width, height)

        # Outer border & vertical column divider
        tb.draw_rect(10, 8, target_width - 20, height - 16, thickness=2)
        mid_x = target_width // 2
        tb.draw_dashed_hline(mid_x, 8, 1, dash_len=4, gap_len=4, thickness=1)
        for y in range(8, height - 8, 8):
            tb.draw_vline(mid_x, y, 4, thickness=1)

        # Headers
        valid_hdr = "[ VALID MOVE ]"
        invalid_hdr = "[ INVALID MOVE ]"
        tb.draw_text(mid_x // 2 - (len(valid_hdr) * 6), 18, valid_hdr, scale=2)
        tb.draw_text(mid_x + (mid_x // 2) - (len(invalid_hdr) * 6), 18, invalid_hdr, scale=2)

        # Mini grids from rule definition if present
        if rule:
            valid_spec = rule.get("valid_move", {})
            invalid_spec = rule.get("invalid_move", {})

            def _draw_mini_matrix(spec, offset_x):
                grid = spec.get("grid", [])
                if not grid:
                    return
                rows = len(grid)
                cols = max(len(r) for r in grid) if rows > 0 else 0
                if rows == 0 or cols == 0:
                    return
                cell_sz = min(36, 160 // max(rows, cols))
                start_x = offset_x + (mid_x - (cols * cell_sz)) // 2
                start_y = 52

                tb.draw_rect(start_x, start_y, cols * cell_sz, rows * cell_sz, thickness=2)
                for r in range(rows):
                    for c in range(len(grid[r])):
                        cx = start_x + c * cell_sz
                        cy = start_y + r * cell_sz
                        tb.draw_rect(cx, cy, cell_sz, cell_sz, thickness=1)
                        val = str(grid[r][c])
                        if val not in ("·", " ", ""):
                            tb.draw_text(cx + (cell_sz - 12) // 2, cy + (cell_sz - 14) // 2, val[:1], scale=2)

            _draw_mini_matrix(valid_spec, 0)
            _draw_mini_matrix(invalid_spec, mid_x)

        return tb.to_escpos()

    def format_guide_ascii(self) -> List[str]:
        """
        Returns monospaced ASCII lines for the tutorial cheat sheet.
        """
        from .rules import get_game_rule
        rule = get_game_rule(self.puzzle_id) or get_game_rule(self.title)
        if not rule:
            return [f"--- {self.title} ---", self.get_instruction({})]

        lines = [
            f"--- {rule['title']} ---",
            rule["instruction"],
            "",
            "OBJECTIVE:",
            f"  {rule['objective']}",
            "",
            "RULES:"
        ]
        for r in rule.get("rules", []):
            lines.append(f"  * {r}")
        lines.append("")
        lines.append("WHERE TO START:")
        for a in rule.get("opening_anchors", []):
            lines.append(f"  * {a}")
        lines.append("")
        lines.append("COMMON QUESTIONS:")
        for faq in rule.get("faq", []):
            lines.append(f"  Q: {faq['q']}")
            lines.append(f"  A: {faq['a']}")
        return lines

