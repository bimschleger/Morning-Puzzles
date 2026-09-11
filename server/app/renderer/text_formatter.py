"""
80mm Receipt ESC/POS Text Formatter
Formats daily puzzle receipts directly into standard ESC/POS command sequences.
Compatible with all commercial 80mm receipt printers (Epson, Star, Munbyn, etc.).
No external dependencies required (Pure Python).
"""

from typing import Dict, Any, List

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

    def section_title(self, title: str, subtitle: str = ""):
        self.bold(True)
        self.println(f"[{title.upper()}]")
        self.bold(False)
        if subtitle:
            self.println(subtitle)
        self.println()

    def key_value(self, key: str, val: str):
        spaces = max(1, COLS_80MM - len(key) - len(val))
        self.println(key + (" " * spaces) + val)

    def feed(self, lines: int = 3):
        for _ in range(lines):
            self.buffer.extend(LF)

    def cut(self):
        self.buffer.extend(CMD_CUT_PARTIAL)

    def get_bytes(self) -> bytes:
        return bytes(self.buffer)


def build_daily_receipt_bytes(daily_data: Dict[str, Any]) -> bytes:
    """Combines generated puzzles into an 80mm ESC/POS byte stream."""
    r = EscPosTextReceipt()

    # Header
    title = daily_data.get("title", "MORNING PUZZLES")
    date_str = daily_data.get("date", "Daily Edition")
    r.header(title, date_str)

    # 1. Sudoku
    if "sudoku" in daily_data:
        s = daily_data["sudoku"]
        r.section_title("Sudoku", f"Difficulty: {s.get('difficulty', 'Medium').capitalize()}")
        for line in s.get("text", "").split("\n"):
            r.println("  " + line)
        r.println()
        r.horizontal_rule("-")

    # 2. Word Search
    if "wordsearch" in daily_data:
        ws = daily_data["wordsearch"]
        r.section_title("Word Search", f"Theme: {ws.get('theme', 'General')} | Diff: {ws.get('difficulty', 'Medium').capitalize()}")
        for line in ws.get("text", "").split("\n"):
            r.println(line)
        r.println()
        r.horizontal_rule("-")

    # 3. Nonogram
    if "nonogram" in daily_data:
        n = daily_data["nonogram"]
        r.section_title("Nonogram / Picross", f"Size: {n.get('rows')}x{n.get('cols')} | Diff: {n.get('difficulty', 'Easy').capitalize()}")
        for line in n.get("text", "").split("\n"):
            r.println(line)
        r.println()
        r.horizontal_rule("-")

    # 4. Queens / Star Battle
    if "queens" in daily_data:
        q = daily_data["queens"]
        r.section_title(f"{q.get('style', 'Queens')} Puzzle", f"Grid: {q.get('grid_size')}x{q.get('grid_size')} (1 per row, col, region)")
        for line in q.get("text", "").split("\n"):
            r.println("  " + line)
        r.println()
        r.horizontal_rule("-")

    # 5. Jumble
    if "jumble" in daily_data:
        j = daily_data["jumble"]
        r.section_title("Daily Jumble", "Unscramble words, then solve riddle:")
        for line in j.get("text", "").split("\n"):
            r.println(line)
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
