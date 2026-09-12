"""
Morning Puzzles - 80mm Receipt ESC/POS Formatter (Facade)
Maintains 100% backwards compatibility with legacy callers while delegating
to the unified DailyReceiptComposer and PuzzleRegistry architecture.
"""

from typing import Dict, Any, List, Optional
from .composer import (
    EscPosTextReceipt,
    DailyReceiptComposer,
    CMD_INIT,
    CMD_ALIGN_LEFT,
    CMD_ALIGN_CENTER,
    CMD_ALIGN_RIGHT,
    CMD_BOLD_ON,
    CMD_BOLD_OFF,
    CMD_DOUBLE_SIZE,
    CMD_NORMAL_SIZE,
    CMD_CUT_PARTIAL,
    LF,
    ESC,
    GS,
    COLS_80MM,
)
from ..puzzles.registry import DEFAULT_REGISTRY

_composer = DailyReceiptComposer(DEFAULT_REGISTRY)


def build_daily_receipt_bytes(daily_data: Dict[str, Any]) -> bytes:
    """Builds an 80mm ESC/POS text-only receipt byte stream."""
    return _composer.build_receipt(daily_data, style="text")


def build_hybrid_daily_receipt_bytes(daily_data: Dict[str, Any]) -> bytes:
    """Builds an 80mm ESC/POS hybrid (text headers + 1-bit raster) receipt byte stream."""
    return _composer.build_receipt(daily_data, style="hybrid")
