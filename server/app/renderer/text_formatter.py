"""
80mm Receipt ESC/POS Formatter (Text and Hybrid Raster)
Formats daily puzzle receipts directly into standard ESC/POS command sequences.
Compatible with all commercial 80mm receipt printers (Epson, Star, Munbyn, etc.).
Strictly follows:
  - docs/THERMAL_80MM_PRINT_GUIDE.md
  - docs/PUZZLE_HEADER_SPEC.md
  - docs/THERMAL_DRAWING_SPEC.md
"""

from typing import Dict, Any, List, Optional

# ESC/POS Constants
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
            self.println(instruction)
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


# ==============================================================================
# Pure ASCII Text Mode Receipt Builder
# ==============================================================================
def build_daily_receipt_bytes(daily_data: Dict[str, Any]) -> bytes:
    """Combines generated puzzles into an 80mm ESC/POS text-only byte stream."""
    r = EscPosTextReceipt()

    # Header
    title = daily_data.get("title", "MORNING PUZZLES")
    date_str = daily_data.get("date", "Daily Edition")
    r.header(title, date_str)

    # 1. Sudoku
    if "sudoku" in daily_data:
        s = daily_data["sudoku"]
        r.puzzle_header(
            "SUDOKU",
            s.get("difficulty", "Medium"),
            "Fill the grid so that every row, column, and 3x3 box contains digits 1 through 9 without repeating."
        )
        for line in s.get("text", "").split("\n"):
            r.println("   " + line)
        r.println()
        r.horizontal_rule("-")

    # 2. Word Search
    if "wordsearch" in daily_data:
        ws = daily_data["wordsearch"]
        r.puzzle_header(
            "SEARCH",
            None,
            "Find and circle all of the listed words hidden horizontally, vertically, or diagonally within the letter grid."
        )
        for line in ws.get("text", "").split("\n"):
            r.println(line)
        r.println()
        r.horizontal_rule("-")

    # 3. Nonogram
    if "nonogram" in daily_data:
        n = daily_data["nonogram"]
        r.puzzle_header(
            "NONOGRAM",
            n.get("difficulty", "Easy"),
            "Use the number clues outside the grid to shade the correct cells and reveal the hidden pixel picture."
        )
        for line in n.get("text", "").split("\n"):
            r.println(line)
        r.println()
        r.horizontal_rule("-")

    # 4. Queens / Star Battle
    if "queens" in daily_data:
        q = daily_data["queens"]
        r.puzzle_header(
            "STARS",
            q.get("difficulty", "Medium"),
            "Place stars so each row, column, and shaped region contains the required star count with no two stars touching, even diagonally."
        )
        for line in q.get("text", "").split("\n"):
            r.println("   " + line)
        r.println()
        r.horizontal_rule("-")

    # 5. Jumble
    if "jumble" in daily_data:
        j = daily_data["jumble"]
        r.puzzle_header(
            "JUMBLE",
            j.get("difficulty", "Medium"),
            "Unscramble the clue words, then arrange the circled letters to solve the punchline riddle."
        )
        for line in j.get("text", "").split("\n"):
            r.println(line)
        r.println()
        r.horizontal_rule("-")

    # 6. Binary
    if "binary" in daily_data:
        b = daily_data["binary"]
        r.puzzle_header(
            "BINARY",
            b.get("difficulty", "Medium"),
            "Fill the grid with 0s and 1s so no more than two identical numbers touch and each row and column has equal counts."
        )
        for line in b.get("text", "").split("\n"):
            r.println("   " + line)
        r.println()
        r.horizontal_rule("-")

    # 7. Mines
    if "mines" in daily_data:
        m = daily_data["mines"]
        r.puzzle_header(
            "MINES",
            m.get("difficulty", "Medium"),
            "Use the numbered clues showing adjacent mine counts to deduce and mark every hidden mine across the grid."
        )
        r.println(f"TOTAL MINES: {m.get('total_mines', 10)}")
        r.println()
        for line in m.get("text", "").split("\n"):
            r.println("   " + line)
        r.println()

    # Footer
    r.align("center")
    r.horizontal_rule("=")
    r.println("Good luck! Solutions tomorrow morning.")
    r.println("Printed on ESP32 80mm Commercial Thermal Receipt")
    r.horizontal_rule("=")
    r.feed(4)
    r.cut()

    return r.get_bytes()


# ==============================================================================
# Hybrid Mode Receipt Builder (ESC/POS Text Headers + 1-Bit GS v 0 Raster Graphics)
# ==============================================================================
def build_hybrid_daily_receipt_bytes(daily_data: Dict[str, Any]) -> bytes:
    """
    Combines standardized ESC/POS text headers with crisp 576-dot 1-bit raster bitmaps.
    Strictly conforms to:
      - docs/PUZZLE_HEADER_SPEC.md (standardized text headers/instructions)
      - docs/THERMAL_80MM_PRINT_GUIDE.md (576 dots width, 4-line feed before cut)
      - docs/THERMAL_DRAWING_SPEC.md (geometric hatching and stroke hierarchy)
    Falls back gracefully to text mode if Pillow is not available.
    """
    try:
        from .receipt_rasterizer import (
            render_sudoku_raster,
            render_wordsearch_raster,
            render_nonogram_raster,
            render_queens_dithered_raster,
            render_jumble_raster,
            render_binary_raster,
            render_mines_raster,
        )
        has_pillow = True
    except (ImportError, RuntimeError):
        has_pillow = False

    if not has_pillow:
        return build_daily_receipt_bytes(daily_data)

    r = EscPosTextReceipt()

    # 1. Master Receipt Header
    title = daily_data.get("title", "MORNING PUZZLES")
    date_str = daily_data.get("date", "Daily Edition")
    r.header(title, date_str)

    # 2. Sudoku
    if "sudoku" in daily_data:
        s = daily_data["sudoku"]
        r.puzzle_header(
            "SUDOKU",
            s.get("difficulty", "Medium"),
            "Fill the grid so that every row, column, and 3x3 box contains digits 1 through 9 without repeating."
        )
        try:
            raster = render_sudoku_raster(s)
            r.write_raw(raster)
        except Exception:
            for line in s.get("text", "").split("\n"):
                r.println("   " + line)
        r.println()
        r.horizontal_rule("-")

    # 3. Word Search
    if "wordsearch" in daily_data:
        ws = daily_data["wordsearch"]
        r.puzzle_header(
            "SEARCH",
            None,
            "Find and circle all of the listed words hidden horizontally, vertically, or diagonally within the letter grid."
        )
        try:
            raster = render_wordsearch_raster(ws)
            r.write_raw(raster)
        except Exception:
            for line in ws.get("text", "").split("\n"):
                r.println(line)
        r.println()
        r.horizontal_rule("-")

    # 4. Nonogram
    if "nonogram" in daily_data:
        n = daily_data["nonogram"]
        r.puzzle_header(
            "NONOGRAM",
            n.get("difficulty", "Easy"),
            "Use the number clues outside the grid to shade the correct cells and reveal the hidden pixel picture."
        )
        try:
            raster = render_nonogram_raster(n)
            r.write_raw(raster)
        except Exception:
            for line in n.get("text", "").split("\n"):
                r.println(line)
        r.println()
        r.horizontal_rule("-")

    # 5. Stars / Queens
    if "queens" in daily_data:
        q = daily_data["queens"]
        r.puzzle_header(
            "STARS",
            q.get("difficulty", "Medium"),
            "Place stars so each row, column, and shaped region contains the required star count with no two stars touching, even diagonally."
        )
        try:
            raster = render_queens_dithered_raster(q)
            r.write_raw(raster)
        except Exception:
            for line in q.get("text", "").split("\n"):
                r.println("   " + line)
        r.println()
        r.horizontal_rule("-")

    # 6. Daily Jumble
    if "jumble" in daily_data:
        j = daily_data["jumble"]
        r.puzzle_header(
            "JUMBLE",
            j.get("difficulty", "Medium"),
            "Unscramble the clue words, then arrange the circled letters to solve the punchline riddle."
        )
        try:
            raster = render_jumble_raster(j)
            r.write_raw(raster)
        except Exception:
            for line in j.get("text", "").split("\n"):
                r.println(line)
        r.println()
        r.horizontal_rule("-")

    # 7. Binary
    if "binary" in daily_data:
        b = daily_data["binary"]
        r.puzzle_header(
            "BINARY",
            b.get("difficulty", "Medium"),
            "Fill the grid with 0s and 1s so no more than two identical numbers touch and each row and column has equal counts."
        )
        try:
            raster = render_binary_raster(b)
            r.write_raw(raster)
        except Exception:
            for line in b.get("text", "").split("\n"):
                r.println("   " + line)
        r.println()
        r.horizontal_rule("-")

    # 8. Mines
    if "mines" in daily_data:
        m = daily_data["mines"]
        r.puzzle_header(
            "MINES",
            m.get("difficulty", "Medium"),
            "Use the numbered clues showing adjacent mine counts to deduce and mark every hidden mine across the grid."
        )
        try:
            raster = render_mines_raster(m)
            r.write_raw(raster)
        except Exception:
            r.println(f"TOTAL MINES: {m.get('total_mines', 10)}")
            r.println()
            for line in m.get("text", "").split("\n"):
                r.println("   " + line)
        r.println()

    # 9. Master Footer
    r.align("center")
    r.horizontal_rule("=")
    r.println("Good luck! Solutions tomorrow morning.")
    r.println("Printed on ESP32 80mm Commercial Thermal Receipt")
    r.horizontal_rule("=")

    # Mandatory 4-line feed before cutter offset
    r.feed(4)
    r.cut()

    return r.get_bytes()
