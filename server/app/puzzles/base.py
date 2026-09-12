"""
Morning Puzzles - Base Puzzle Plugin System
Defines the standard contracts for all puzzle types:
- BasePuzzleResult: Standardized envelope with dual dataclass / dict access.
- BasePuzzle: Abstract base class that all puzzle plugins must implement.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union
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
