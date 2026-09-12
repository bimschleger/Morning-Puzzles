"""
Morning Puzzles - Daily Receipt Composer
Provides unified polymorphic generation of 80mm thermal receipt streams
in pure ESC/POS text or hybrid 1-bit raster graphics.
Strictly conforms to:
  - docs/THERMAL_80MM_PRINT_GUIDE.md
  - docs/PUZZLE_HEADER_SPEC.md
  - docs/PUZZLE_SOLUTION_KEY_SPEC.md
  - docs/THERMAL_DRAWING_SPEC.md
"""

from typing import Dict, Any, List, Optional
from ..puzzles.registry import PuzzleRegistry, DEFAULT_REGISTRY
from ..renderer.canvas import HAS_PILLOW

# ESC/POS Hardware Constants
ESC = b"\x1b"
GS  = b"\x1d"
LF  = b"\x0a"

CMD_INIT         = ESC + b"@"
CMD_ALIGN_LEFT   = ESC + b"a\x00"
CMD_ALIGN_CENTER = ESC + b"a\x01"
CMD_ALIGN_RIGHT  = ESC + b"a\x02"
CMD_BOLD_ON      = ESC + b"E\x01"
CMD_BOLD_OFF     = ESC + b"E\x00"
CMD_DOUBLE_SIZE  = GS  + b"!\x11"
CMD_NORMAL_SIZE  = GS  + b"!\x00"
CMD_CUT_PARTIAL  = GS  + b"V\x42\x03"

COLS_80MM = 48  # Standard 80mm Font A characters per line


class EscPosTextReceipt:
    """Bytearray-based builder for standard ESC/POS printer byte streams."""

    def __init__(self):
        self.buffer = bytearray()
        self.buffer.extend(CMD_INIT)

    def text(self, s: str):
        self.buffer.extend(s.encode("latin-1", errors="replace"))

    def println(self, s: str = ""):
        self.text(s)
        self.buffer.extend(LF)

    def align(self, mode: str):
        if mode == "center":
            self.buffer.extend(CMD_ALIGN_CENTER)
        elif mode == "right":
            self.buffer.extend(CMD_ALIGN_RIGHT)
        else:
            self.buffer.extend(CMD_ALIGN_LEFT)

    def bold(self, enable: bool):
        self.buffer.extend(CMD_BOLD_ON if enable else CMD_BOLD_OFF)

    def double_size(self, enable: bool):
        self.buffer.extend(CMD_DOUBLE_SIZE if enable else CMD_NORMAL_SIZE)

    def horizontal_rule(self, char: str = "-"):
        self.println(char * COLS_80MM)

    def header(self, title: str, date_str: str):
        self.align("center")
        self.horizontal_rule("=")
        self.bold(True)
        self.double_size(True)
        self.println(title)
        self.double_size(False)
        self.bold(False)
        self.println(date_str)
        self.horizontal_rule("=")
        self.align("left")
        self.println()

    def puzzle_header(self, title: str, difficulty: Optional[str] = None, instruction: str = ""):
        """Standardized puzzle header matching docs/PUZZLE_HEADER_SPEC.md"""
        self.align("center")
        self.bold(True)
        self.println(f"--- {title.upper()} ---")
        self.bold(False)
        if difficulty:
            self.println(f"DIFFICULTY: {difficulty.upper()}")
        if instruction:
            import textwrap
            for line in textwrap.wrap(instruction, width=44):
                self.println(line)
        self.println()
        self.align("left")

    def key_value(self, key: str, val: str):
        spaces = max(1, COLS_80MM - len(key) - len(val))
        self.println(key + (" " * spaces) + val)

    def write_raw(self, raw_bytes: bytes):
        self.buffer.extend(raw_bytes)

    def feed(self, lines: int = 4):
        for _ in range(lines):
            self.buffer.extend(LF)

    def cut(self):
        self.buffer.extend(CMD_CUT_PARTIAL)

    def get_bytes(self) -> bytes:
        return bytes(self.buffer)


class DailyReceiptComposer:
    """
    Polymorphic receipt composer that renders registered puzzles into
    ESC/POS byte streams conforming to hardware receipt specifications.
    """

    def __init__(self, registry: Optional[PuzzleRegistry] = None):
        self.registry = registry or DEFAULT_REGISTRY

    def build_receipt(
        self,
        daily_data: Dict[str, Any],
        style: str = "hybrid",
        show_solutions: Optional[bool] = None,
    ) -> bytes:
        """
        Builds complete daily receipt bytes.
        - style: 'hybrid' (text headers + 1-bit raster graphics) or 'text' (monospaced ASCII).
        - show_solutions: whether to append the formatted Solution Key.
        """
        use_raster = (style == "hybrid")
        r = EscPosTextReceipt()

        # 1. Master Receipt Header
        title = daily_data.get("title", "MORNING PUZZLES")
        date_str = daily_data.get("date", "Daily Edition")
        r.header(title, date_str)

        # 2. Render each puzzle in canonical sequence
        plugins = [p for p in self.registry.get_all() if p.puzzle_id in daily_data]

        for idx, plugin in enumerate(plugins):
            p_data = daily_data[plugin.puzzle_id]

            # Header & Instruction
            diff_str = str(p_data.get("difficulty", "")).upper() if plugin.has_difficulty else None
            instruction = plugin.get_instruction(p_data)
            r.puzzle_header(plugin.title, diff_str, instruction)

            # Puzzle Body: Raster or ASCII Fallback
            rendered_graphical = False
            if use_raster:
                try:
                    raster_bytes = plugin.render_raster(p_data)
                    if raster_bytes:
                        r.write_raw(raster_bytes)
                        rendered_graphical = True
                except Exception:
                    rendered_graphical = False

            if not rendered_graphical:
                ascii_text = p_data.get("text") or plugin.format_ascii_puzzle(p_data)
                for line in ascii_text.split("\n"):
                    # Maintain standard indentation for clean ASCII layout
                    if plugin.puzzle_id in ("sudoku", "binary", "tango") and not line.startswith("   "):
                        r.println("   " + line)
                    else:
                        r.println(line)

            r.println()
            if idx < len(plugins) - 1:
                r.horizontal_rule("-")

        # 3. Optional Solution Key
        include_solutions = show_solutions if show_solutions is not None else daily_data.get("show_solutions", False)
        if include_solutions:
            self._append_solution_key(r, daily_data)

        # 4. Master Receipt Footer
        r.align("center")
        r.horizontal_rule("=")
        r.println("Good luck! Solutions tomorrow morning.")
        r.println("Printed on ESP32 80mm Commercial Thermal Receipt")
        r.horizontal_rule("=")

        # Mandatory 4-line feed before cutter offset
        r.feed(4)
        r.cut()

        return r.get_bytes()

    def _append_solution_key(self, r: EscPosTextReceipt, daily_data: Dict[str, Any]):
        """Appends the formatted Solution Key block matching docs/PUZZLE_SOLUTION_KEY_SPEC.md."""
        r.horizontal_rule("-")
        r.align("center")
        r.bold(True)
        r.println("[ SOLUTION KEY ]")
        r.bold(False)
        r.horizontal_rule("-")
        r.align("left")
        r.println()

        for plugin in self.registry.get_all():
            if plugin.puzzle_id in daily_data:
                p_data = daily_data[plugin.puzzle_id]
                solution_lines = plugin.format_solution_key(p_data)
                if solution_lines:
                    r.bold(True)
                    r.println(plugin.title)
                    r.bold(False)
                    for line in solution_lines:
                        r.println(line)
                    r.println()
