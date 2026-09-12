"""
ESC/POS 80mm Raster Image Renderer (576 Dots Width)
Converts 1-bit monochrome images, graphical grids, and dithered territory puzzles
into ESC/POS GS v 0 format. Strictly conforms to:
  - 80mm thermal hardware standards (576 dots width / 72 bytes per row)
  - docs/THERMAL_80MM_PRINT_GUIDE.md
  - docs/THERMAL_DRAWING_SPEC.md
  - docs/PUZZLE_HEADER_SPEC.md

Supports both Pillow (when available for high-res typography) and a built-in
Pure-Python ThermalBitmap engine (zero external dependencies).
"""

from typing import Tuple, Dict, Any, List, Optional

# Standard 80mm thermal receipt constants
THERMAL_WIDTH_DOTS = 576
THERMAL_WIDTH_BYTES = 72  # 576 // 8

# Check Pillow availability
try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False


def image_to_escpos_raster(image_bytes: bytes, width: int, height: int) -> bytes:
    """
    Wraps 1-bit bitmap bytes into the ESC/POS GS v 0 (raster bit image) command.
    Standard 80mm receipt printable width = 576 dots (72 bytes wide).

    ESC/POS GS v 0 format:
      0x1D 0x76 0x30 0x00 xL xH yL yH [data...]
      xL, xH = width in bytes
      yL, yH = height in dots
    """
    width_bytes = (width + 7) // 8
    xl = width_bytes & 0xFF
    xh = (width_bytes >> 8) & 0xFF
    yl = height & 0xFF
    yh = (height >> 8) & 0xFF

    header = bytes([0x1D, 0x76, 0x30, 0x00, xl, xh, yl, yh])
    return header + image_bytes


def calculate_duty_cycle(raster_bytes: bytes) -> Dict[str, Any]:
    """
    Analyzes an ESC/POS GS v 0 byte stream to evaluate thermal printhead stress:
    - Average black pixel density (duty cycle) across the entire graphic
    - Peak black pixel density across any single horizontal scanline
    - Compliance with the 35% safe thermal duty cycle guideline
    """
    if len(raster_bytes) < 8:
        return {"error": "Invalid raster byte stream (too short)"}

    # Verify GS v 0 header: 0x1D, 0x76, 0x30, m
    if raster_bytes[0] != 0x1D or raster_bytes[1] != 0x76 or raster_bytes[2] != 0x30:
        return {"error": "Not a GS v 0 raster command"}

    width_bytes = raster_bytes[4] | (raster_bytes[5] << 8)
    height_dots = raster_bytes[6] | (raster_bytes[7] << 8)
    data = raster_bytes[8:]

    expected_len = width_bytes * height_dots
    if len(data) < expected_len:
        return {"error": f"Truncated data: expected {expected_len} bytes, got {len(data)}"}

    total_bits = width_bytes * 8 * height_dots
    total_black_dots = 0
    max_line_black_dots = 0
    consec_dense = 0
    max_consec_dense = 0

    bit_counts = [bin(b).count("1") for b in range(256)]

    for y in range(height_dots):
        line_start = y * width_bytes
        line_bytes = data[line_start:line_start + width_bytes]
        line_black = sum(bit_counts[b] for b in line_bytes)
        total_black_dots += line_black
        if line_black > max_line_black_dots:
            max_line_black_dots = line_black

        # Check for consecutive scanlines with >75% black dots
        if line_black / float(width_bytes * 8) > 0.75:
            consec_dense += 1
            if consec_dense > max_consec_dense:
                max_consec_dense = consec_dense
        else:
            consec_dense = 0

    line_total_dots = width_bytes * 8
    avg_density = (total_black_dots / float(total_bits)) * 100.0 if total_bits > 0 else 0.0
    peak_line_density = (max_line_black_dots / float(line_total_dots)) * 100.0 if line_total_dots > 0 else 0.0

    return {
        "width_dots": line_total_dots,
        "width_bytes": width_bytes,
        "height_dots": height_dots,
        "total_black_pixels": total_black_dots,
        "total_pixels": total_bits,
        "average_duty_cycle_pct": round(avg_density, 2),
        "peak_scanline_duty_cycle_pct": round(peak_line_density, 2),
        "max_consecutive_dense_lines": max_consec_dense,
        "is_safe": avg_density <= 35.0 and max_consec_dense <= 16
    }


# ==============================================================================
# Pure-Python 1-Bit Thermal Bitmap Engine (Zero Dependencies)
# ==============================================================================
# Compact 5x7 bitmap font for rendering numbers, uppercase letters, and symbols
FONT_5X7 = {
    '0': [0x1E, 0x21, 0x21, 0x21, 0x21, 0x21, 0x1E],
    '1': [0x08, 0x18, 0x28, 0x08, 0x08, 0x08, 0x3E],
    '2': [0x1E, 0x21, 0x01, 0x0E, 0x18, 0x20, 0x3F],
    '3': [0x1E, 0x21, 0x01, 0x0E, 0x01, 0x21, 0x1E],
    '4': [0x02, 0x06, 0x0A, 0x12, 0x3F, 0x02, 0x02],
    '5': [0x3F, 0x20, 0x3E, 0x01, 0x01, 0x21, 0x1E],
    '6': [0x1E, 0x21, 0x20, 0x3E, 0x21, 0x21, 0x1E],
    '7': [0x3F, 0x01, 0x02, 0x04, 0x08, 0x10, 0x10],
    '8': [0x1E, 0x21, 0x21, 0x1E, 0x21, 0x21, 0x1E],
    '9': [0x1E, 0x21, 0x21, 0x1F, 0x01, 0x21, 0x1E],
    'A': [0x0C, 0x12, 0x21, 0x3F, 0x21, 0x21, 0x21],
    'B': [0x3E, 0x21, 0x21, 0x3E, 0x21, 0x21, 0x3E],
    'C': [0x1E, 0x21, 0x20, 0x20, 0x20, 0x21, 0x1E],
    'D': [0x3C, 0x22, 0x21, 0x21, 0x21, 0x22, 0x3C],
    'E': [0x3F, 0x20, 0x20, 0x3E, 0x20, 0x20, 0x3F],
    'F': [0x3F, 0x20, 0x20, 0x3E, 0x20, 0x20, 0x20],
    'G': [0x1E, 0x21, 0x20, 0x27, 0x21, 0x21, 0x1E],
    'H': [0x21, 0x21, 0x21, 0x3F, 0x21, 0x21, 0x21],
    'I': [0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x1F],
    'J': [0x07, 0x02, 0x02, 0x02, 0x22, 0x22, 0x1C],
    'K': [0x21, 0x22, 0x24, 0x38, 0x24, 0x22, 0x21],
    'L': [0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x3F],
    'M': [0x21, 0x33, 0x2D, 0x21, 0x21, 0x21, 0x21],
    'N': [0x21, 0x31, 0x29, 0x25, 0x23, 0x21, 0x21],
    'O': [0x1E, 0x21, 0x21, 0x21, 0x21, 0x21, 0x1E],
    'P': [0x3E, 0x21, 0x21, 0x3E, 0x20, 0x20, 0x20],
    'Q': [0x1E, 0x21, 0x21, 0x21, 0x25, 0x22, 0x1D],
    'R': [0x3E, 0x21, 0x21, 0x3E, 0x24, 0x22, 0x21],
    'S': [0x1E, 0x21, 0x20, 0x1E, 0x01, 0x21, 0x1E],
    'T': [0x3F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04],
    'U': [0x21, 0x21, 0x21, 0x21, 0x21, 0x21, 0x1E],
    'V': [0x21, 0x21, 0x21, 0x12, 0x12, 0x0C, 0x0C],
    'W': [0x21, 0x21, 0x21, 0x21, 0x2D, 0x33, 0x21],
    'X': [0x21, 0x12, 0x0C, 0x0C, 0x12, 0x21, 0x21],
    'Y': [0x21, 0x12, 0x0C, 0x04, 0x04, 0x04, 0x04],
    'Z': [0x3F, 0x02, 0x04, 0x08, 0x10, 0x20, 0x3F],
    ' ': [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    '.': [0x00, 0x00, 0x00, 0x00, 0x00, 0x0C, 0x0C],
    ':': [0x00, 0x0C, 0x0C, 0x00, 0x0C, 0x0C, 0x00],
    '-': [0x00, 0x00, 0x00, 0x3E, 0x00, 0x00, 0x00],
    '?': [0x1E, 0x21, 0x02, 0x04, 0x04, 0x00, 0x04],
    '!': [0x04, 0x04, 0x04, 0x04, 0x04, 0x00, 0x04],
    '[': [0x1E, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1E],
    ']': [0x1E, 0x02, 0x02, 0x02, 0x02, 0x02, 0x1E],
}


class ThermalBitmap:
    """
    Pure Python 1-bit raster canvas for 80mm thermal receipt printers.
    Enforces strict 576-dot width (72 bytes/row), MSB-first packing,
    and 1=burn (black) polarity.
    """
    def __init__(self, width: int = THERMAL_WIDTH_DOTS, height: int = 100):
        self.width = width
        self.height = height
        self.width_bytes = (width + 7) // 8
        self.buffer = bytearray(self.width_bytes * height)

    def set_pixel(self, x: int, y: int, color: int = 1):
        if 0 <= x < self.width and 0 <= y < self.height:
            byte_idx = y * self.width_bytes + (x // 8)
            bit_mask = 1 << (7 - (x % 8))
            if color:
                self.buffer[byte_idx] |= bit_mask
            else:
                self.buffer[byte_idx] &= ~bit_mask

    def draw_hline(self, x: int, y: int, w: int, thickness: int = 1, color: int = 1):
        for t in range(thickness):
            py = y + t
            if 0 <= py < self.height:
                for px in range(max(0, x), min(x + w, self.width)):
                    self.set_pixel(px, py, color)

    def draw_vline(self, x: int, y: int, h: int, thickness: int = 1, color: int = 1):
        for t in range(thickness):
            px = x + t
            if 0 <= px < self.width:
                for py in range(max(0, y), min(y + h, self.height)):
                    self.set_pixel(px, py, color)

    def draw_rect(self, x: int, y: int, w: int, h: int, thickness: int = 1, color: int = 1):
        self.draw_hline(x, y, w, thickness, color)
        self.draw_hline(x, y + h - thickness, w, thickness, color)
        self.draw_vline(x, y, h, thickness, color)
        self.draw_vline(x + w - thickness, y, h, thickness, color)

    def fill_rect(self, x: int, y: int, w: int, h: int, color: int = 1):
        for py in range(max(0, y), min(y + h, self.height)):
            for px in range(max(0, x), min(x + w, self.width)):
                self.set_pixel(px, py, color)

    def fill_hatch(self, x: int, y: int, w: int, h: int, pattern_id: int):
        """Fills area using standard geometric hatching patterns from THERMAL_DRAWING_SPEC."""
        pat = pattern_id % 8
        for py in range(max(0, y), min(y + h, self.height)):
            for px in range(max(0, x), min(x + w, self.width)):
                is_burn = False
                if pat == 0:
                    is_burn = False
                elif pat == 1:
                    is_burn = ((px + py) % 6 == 0)
                elif pat == 2:
                    is_burn = ((px - py + 1000) % 6 == 0)
                elif pat == 3:
                    is_burn = (px % 4 == 0 or py % 4 == 0)
                elif pat == 4:
                    is_burn = ((px + py) % 4 == 0)
                elif pat == 5:
                    is_burn = (px % 3 == 0 and py % 3 == 0)
                elif pat == 6:
                    is_burn = ((px + py) % 3 == 0 or (px - py + 1000) % 3 == 0)
                elif pat == 7:
                    is_burn = (py % 3 == 0)

                if is_burn:
                    self.set_pixel(px, py, 1)

    def draw_char(self, x: int, y: int, char: str, scale: int = 2, color: int = 1):
        glyph = FONT_5X7.get(char.upper(), FONT_5X7.get(' ', [0]*7))
        for row_idx, row_byte in enumerate(glyph):
            for col_idx in range(6):
                if (row_byte >> (5 - col_idx)) & 1:
                    for sy in range(scale):
                        for sx in range(scale):
                            self.set_pixel(x + col_idx * scale + sx, y + row_idx * scale + sy, color)

    def draw_text(self, x: int, y: int, text: str, scale: int = 2, color: int = 1):
        cur_x = x
        char_w = 6 * scale + max(1, scale // 2)
        for ch in text:
            self.draw_char(cur_x, y, ch, scale=scale, color=color)
            cur_x += char_w

    def draw_circle(self, cx: int, cy: int, radius: int, thickness: int = 2, color: int = 1):
        r_inner_sq = (radius - thickness) ** 2
        r_outer_sq = radius ** 2
        for py in range(max(0, cy - radius), min(cy + radius + 1, self.height)):
            for px in range(max(0, cx - radius), min(cx + radius + 1, self.width)):
                dist_sq = (px - cx) ** 2 + (py - cy) ** 2
                if r_inner_sq <= dist_sq <= r_outer_sq:
                    self.set_pixel(px, py, color)

    def to_escpos(self) -> bytes:
        return image_to_escpos_raster(bytes(self.buffer), self.width, self.height)


# ==============================================================================
# Helper for PIL Conversion
# ==============================================================================
def pil_to_escpos(image) -> bytes:
    """
    Converts a PIL.Image instance into ESC/POS GS v 0 raster bytes.
    Strictly forces width to 576 dots and ensures 1-bit MSB-first packing.
    """
    if not HAS_PILLOW:
        raise RuntimeError("Pillow is required for graphical rendering. Install via: pip install Pillow")

    target_width = THERMAL_WIDTH_DOTS
    if image.width != target_width:
        ratio = target_width / float(image.width)
        new_height = int(float(image.height) * ratio)
        image = image.resize((target_width, new_height), Image.Resampling.LANCZOS)

    mono = image.convert("1", dither=Image.Dither.FLOYDSTEINBERG)
    width, height = mono.size
    width_bytes = (width + 7) // 8

    raw_data = bytearray()
    pixels = mono.load()

    for y in range(height):
        for x_byte in range(width_bytes):
            byte_val = 0
            for bit in range(8):
                x = x_byte * 8 + bit
                if x < width:
                    if pixels[x, y] == 0:  # 0 is black in PIL
                        byte_val |= (1 << (7 - bit))
            raw_data.append(byte_val)

    return image_to_escpos_raster(bytes(raw_data), width, height)


# ==============================================================================
# 1. STARS / QUEENS RASTERIZER (576 Dots Width)
# ==============================================================================
def render_queens_dithered_raster(queens_data: Dict[str, Any], target_width: int = THERMAL_WIDTH_DOTS) -> bytes:
    """Renders a Stars / Queens puzzle as a crisp 1-bit dithered graphic."""
    size = queens_data.get("grid_size", queens_data.get("size", 8))
    regions = queens_data.get("regions", [])

    if HAS_PILLOW:
        padding = 24
        board_size = target_width - padding * 2
        cell_size = board_size / float(size)

        img = Image.new("L", (target_width, target_width), 255)
        draw = ImageDraw.Draw(img)
        tones = [255, 225, 195, 165, 135, 105, 75, 45, 15]

        for r in range(size):
            for c in range(size):
                reg = regions[r][c] if r < len(regions) and c < len(regions[r]) else 0
                tone = tones[reg % len(tones)]
                x0 = int(padding + c * cell_size)
                y0 = int(padding + r * cell_size)
                x1 = int(padding + (c + 1) * cell_size)
                y1 = int(padding + (r + 1) * cell_size)
                draw.rectangle([x0, y0, x1, y1], fill=tone)

        for r in range(size):
            for c in range(size):
                reg = regions[r][c] if r < len(regions) and c < len(regions[r]) else 0
                x0 = int(padding + c * cell_size)
                y0 = int(padding + r * cell_size)
                x1 = int(padding + (c + 1) * cell_size)
                y1 = int(padding + (r + 1) * cell_size)

                is_bottom_boundary = (r == size - 1) or (r + 1 < len(regions) and regions[r + 1][c] != reg)
                w = 5 if is_bottom_boundary else 1
                color = 0 if is_bottom_boundary else 180
                draw.line([x0, y1, x1, y1], fill=color, width=w)

                is_right_boundary = (c == size - 1) or (c + 1 < len(regions[r]) and regions[r][c + 1] != reg)
                w = 5 if is_right_boundary else 1
                color = 0 if is_right_boundary else 180
                draw.line([x1, y0, x1, y1], fill=color, width=w)

        draw.rectangle([padding, padding, padding + board_size, padding + board_size], outline=0, width=5)
        return pil_to_escpos(img)

    # Pure Python ThermalBitmap Fallback
    padding = 24
    board_size = target_width - padding * 2
    cell_size = board_size // size
    tb = ThermalBitmap(target_width, target_width)

    # Fill regions with geometric hatching
    for r in range(size):
        for c in range(size):
            reg = regions[r][c] if r < len(regions) and c < len(regions[r]) else 0
            x0 = padding + c * cell_size
            y0 = padding + r * cell_size
            tb.fill_hatch(x0, y0, cell_size, cell_size, reg)

    # Internal lines and borders
    for r in range(size):
        for c in range(size):
            reg = regions[r][c] if r < len(regions) and c < len(regions[r]) else 0
            x0 = padding + c * cell_size
            y0 = padding + r * cell_size
            is_bottom = (r == size - 1) or (r + 1 < len(regions) and regions[r + 1][c] != reg)
            tb.draw_hline(x0, y0 + cell_size, cell_size, thickness=4 if is_bottom else 1)
            is_right = (c == size - 1) or (c + 1 < len(regions[r]) and regions[r][c + 1] != reg)
            tb.draw_vline(x0 + cell_size, y0, cell_size, thickness=4 if is_right else 1)

    tb.draw_rect(padding, padding, cell_size * size, cell_size * size, thickness=5)
    return tb.to_escpos()


# ==============================================================================
# 2. SUDOKU RASTERIZER (576 Dots Width)
# ==============================================================================
def render_sudoku_raster(sudoku_data: Dict[str, Any], target_width: int = THERMAL_WIDTH_DOTS) -> bytes:
    """Renders a crisp, 576-dot wide Sudoku 9x9 grid with bold 3x3 block dividers."""
    board = sudoku_data.get("grid", [])
    padding = 24
    board_size = target_width - padding * 2
    cell_size = board_size / 9.0

    if HAS_PILLOW:
        total_height = int(padding + board_size + padding)
        img = Image.new("L", (target_width, total_height), 255)
        draw = ImageDraw.Draw(img)

        try:
            font_digit = ImageFont.truetype("Courier.ttf", int(cell_size * 0.6))
        except IOError:
            font_digit = ImageFont.load_default()

        for i in range(10):
            pos = padding + i * cell_size
            is_major = (i % 3 == 0)
            w = 4 if is_major else 1
            color = 0 if is_major else 180
            draw.line([padding, pos, padding + board_size, pos], fill=color, width=w)
            draw.line([pos, padding, pos, padding + board_size], fill=color, width=w)

        for r in range(9):
            for c in range(9):
                val = board[r][c] if r < len(board) and c < len(board[r]) else 0
                if val != 0:
                    cx = padding + c * cell_size + cell_size // 2 - int(cell_size * 0.16)
                    cy = padding + r * cell_size + cell_size // 2 - int(cell_size * 0.32)
                    draw.text((cx, cy), str(val), fill=0, font=font_digit)

        return pil_to_escpos(img)

    # Pure Python ThermalBitmap Fallback
    c_size = board_size // 9
    total_h = padding + c_size * 9 + padding
    tb = ThermalBitmap(target_width, total_h)

    for i in range(10):
        pos = padding + i * c_size
        is_major = (i % 3 == 0)
        tb.draw_hline(padding, pos, c_size * 9, thickness=4 if is_major else 1)
        tb.draw_vline(pos, padding, c_size * 9, thickness=4 if is_major else 1)

    for r in range(9):
        for c in range(9):
            val = board[r][c] if r < len(board) and c < len(board[r]) else 0
            if val != 0:
                cx = padding + c * c_size + (c_size - 18) // 2
                cy = padding + r * c_size + (c_size - 21) // 2
                tb.draw_char(cx, cy, str(val), scale=3)

    return tb.to_escpos()


# ==============================================================================
# 3. NONOGRAM RASTERIZER (576 Dots Width)
# ==============================================================================
def render_nonogram_raster(nonogram_data: Dict[str, Any], target_width: int = THERMAL_WIDTH_DOTS, show_solution: bool = False) -> bytes:
    """Renders a high-contrast 1-bit thermal Nonogram grid."""
    size = nonogram_data.get("rows", nonogram_data.get("size", 5))
    row_clues = nonogram_data.get("row_clues", [])
    col_clues = nonogram_data.get("col_clues", [])
    solution = nonogram_data.get("solution", nonogram_data.get("grid", []))

    padding = 24
    inner_width = target_width - padding * 2

    cell_size = 76 if size <= 5 else (50 if size <= 8 else (40 if size <= 10 else 26))
    major_interval = 4 if size == 8 else 5
    grid_size = cell_size * size
    row_clue_width = inner_width - grid_size

    max_col_clues = max((len(c) for c in col_clues), default=1)
    col_clue_item_h = max(24, int(cell_size * 0.55))
    col_clue_height = max(50, max_col_clues * col_clue_item_h + 16)
    total_height = 12 + col_clue_height + grid_size + 12

    if HAS_PILLOW:
        img = Image.new("L", (target_width, total_height), 255)
        draw = ImageDraw.Draw(img)

        try:
            font_clue = ImageFont.truetype("Courier.ttf", int(cell_size * 0.45))
        except IOError:
            font_clue = ImageFont.load_default()

        grid_x = padding + row_clue_width
        grid_y = 12 + col_clue_height

        draw.rectangle([padding, 12, grid_x, grid_y], fill=240, outline=0, width=3)
        draw.rectangle([grid_x, 12, grid_x + grid_size, grid_y], outline=0, width=3)

        for c in range(size):
            col_cx = grid_x + c * cell_size + cell_size // 2
            clues = col_clues[c] if c < len(col_clues) else [0]
            for k, val in enumerate(clues):
                dist_from_bottom = (len(clues) - 1 - k) * col_clue_item_h
                val_y = grid_y - 12 - dist_from_bottom
                draw.text((col_cx - 6, val_y), str(val), fill=0, font=font_clue)
            if c > 0:
                is_major = (c % major_interval == 0)
                draw.line([grid_x + c * cell_size, 12, grid_x + c * cell_size, grid_y], fill=0 if is_major else 180, width=3 if is_major else 1)

        draw.rectangle([padding, grid_y, grid_x, grid_y + grid_size], outline=0, width=3)
        row_clue_char_w = max(18, int(cell_size * 0.45))
        for r in range(size):
            row_cy = grid_y + r * cell_size + cell_size // 2 - int(cell_size * 0.22)
            clues = row_clues[r] if r < len(row_clues) else [0]
            for k, val in enumerate(clues):
                dist_from_right = (len(clues) - 1 - k) * row_clue_char_w
                val_x = grid_x - 14 - dist_from_right
                draw.text((val_x, row_cy), str(val), fill=0, font=font_clue)
            if r > 0:
                is_major = (r % major_interval == 0)
                draw.line([padding, grid_y + r * cell_size, grid_x, grid_y + r * cell_size], fill=0 if is_major else 180, width=3 if is_major else 1)

        for r in range(size):
            for c in range(size):
                cx = grid_x + c * cell_size
                cy = grid_y + r * cell_size
                if show_solution and solution and r < len(solution) and c < len(solution[r]) and solution[r][c] == 1:
                    draw.rectangle([cx, cy, cx + cell_size, cy + cell_size], fill=0)
                else:
                    dot_r = 2
                    draw.ellipse([cx + cell_size // 2 - dot_r, cy + cell_size // 2 - dot_r, cx + cell_size // 2 + dot_r, cy + cell_size // 2 + dot_r], fill=160)

        for i in range(size + 1):
            is_major = (i % major_interval == 0) or (i == size)
            w = 4 if is_major else 1
            color = 0 if is_major else 160
            draw.line([grid_x, grid_y + i * cell_size, grid_x + grid_size, grid_y + i * cell_size], fill=color, width=w)
            draw.line([grid_x + i * cell_size, grid_y, grid_x + i * cell_size, grid_y + grid_size], fill=color, width=w)

        draw.rectangle([padding, 12, padding + inner_width, grid_y + grid_size], outline=0, width=5)
        return pil_to_escpos(img)

    # Pure Python Fallback
    tb = ThermalBitmap(target_width, total_height)
    grid_x = padding + row_clue_width
    grid_y = 12 + col_clue_height

    tb.draw_rect(padding, 12, row_clue_width, col_clue_height, thickness=3)
    tb.draw_rect(grid_x, 12, grid_size, col_clue_height, thickness=3)
    tb.draw_rect(padding, grid_y, row_clue_width, grid_size, thickness=3)
    tb.draw_rect(grid_x, grid_y, grid_size, grid_size, thickness=4)

    # Clues
    for c in range(size):
        clues = col_clues[c] if c < len(col_clues) else [0]
        col_cx = grid_x + c * cell_size + cell_size // 2 - 6
        for k, val in enumerate(clues):
            dist = (len(clues) - 1 - k) * col_clue_item_h
            tb.draw_char(col_cx, grid_y - 18 - dist, str(val), scale=2)

    for r in range(size):
        clues = row_clues[r] if r < len(row_clues) else [0]
        row_cy = grid_y + r * cell_size + cell_size // 2 - 7
        for k, val in enumerate(clues):
            dist = (len(clues) - 1 - k) * 16
            tb.draw_char(grid_x - 18 - dist, row_cy, str(val), scale=2)

    for i in range(size + 1):
        is_maj = (i % major_interval == 0)
        tb.draw_hline(grid_x, grid_y + i * cell_size, grid_size, thickness=3 if is_maj else 1)
        tb.draw_vline(grid_x + i * cell_size, grid_y, grid_size, thickness=3 if is_maj else 1)

    return tb.to_escpos()


# ==============================================================================
# 4. JUMBLE RASTERIZER (576 Dots Width)
# ==============================================================================
def render_jumble_raster(jumble_data: Dict[str, Any], target_width: int = THERMAL_WIDTH_DOTS) -> bytes:
    """Renders newspaper-style Jumble puzzle graphics (boxes, circles, scratchpad)."""
    padding = 24
    inner_width = target_width - padding * 2

    words = jumble_data.get("words", [])
    scrambled = jumble_data.get("scrambled", words)
    circles = jumble_data.get("circles", [])

    clue_height = 44
    cell_height = 58
    word_gap = 16

    if HAS_PILLOW:
        try:
            font_box = ImageFont.truetype("Courier.ttf", 26)
            font_riddle = ImageFont.truetype("Arial.ttf", 20)
            font_label = ImageFont.truetype("Arial.ttf", 16)
        except IOError:
            font_box = ImageFont.load_default()
            font_riddle = ImageFont.load_default()
            font_label = ImageFont.load_default()

        total_height = 900
        img = Image.new("L", (target_width, total_height), 255)
        draw = ImageDraw.Draw(img)
        cur_y = 12

        for i in range(min(4, len(scrambled))):
            scram = scrambled[i]
            scram_text = scram.get("scrambled", "") if isinstance(scram, dict) else str(scram)
            circ = scram.get("circles", []) if isinstance(scram, dict) else (circles[i] if i < len(circles) else [])
            length = max(1, len(scram_text))
            col_pos = [padding + int(round(c * inner_width / float(length))) for c in range(length + 1)]

            draw.rectangle([padding, cur_y, padding + inner_width, cur_y + clue_height], outline=0, width=3)
            for c in range(length):
                cx0 = col_pos[c]
                cx1 = col_pos[c + 1]
                col_w = cx1 - cx0
                if c > 0:
                    draw.line([cx0, cur_y, cx0, cur_y + clue_height], fill=160, width=2)
                draw.text((cx0 + col_w // 2 - 8, cur_y + 8), scram_text[c], fill=0, font=font_box)

            ans_y = cur_y + clue_height
            for c in range(length):
                cx0 = col_pos[c]
                cx1 = col_pos[c + 1]
                col_w = cx1 - cx0
                draw.rectangle([cx0, ans_y, cx1, ans_y + cell_height], outline=0, width=3)
                if c in circ:
                    radius = min(col_w, cell_height) // 2 - 5
                    draw.ellipse([cx0 + col_w // 2 - radius, ans_y + cell_height // 2 - radius,
                                  cx0 + col_w // 2 + radius, ans_y + cell_height // 2 + radius], outline=0, width=3)

            cur_y = ans_y + cell_height + word_gap

        draw.line([padding, cur_y, padding + inner_width, cur_y], fill=140, width=2)
        cur_y += 16
        draw.text((padding, cur_y), "RIDDLE CLUE:", fill=0, font=font_label)
        cur_y += 24
        riddle_text = f'"{jumble_data.get("riddle", jumble_data.get("clue", ""))}"'
        draw.text((padding + 8, cur_y), riddle_text, fill=0, font=font_riddle)
        cur_y += 32

        draw.text((padding, cur_y), "Discovered letters scratchpad:", fill=80, font=font_label)
        cur_y += 24
        for _ in range(2):
            draw.line([padding, cur_y, padding + inner_width, cur_y], fill=160, width=2)
            cur_y += 30

        cur_y += 6
        draw.text((padding, cur_y), "Answer:", fill=0, font=font_label)
        cur_y += 24

        ans_box = cell_height
        answer_words = str(jumble_data.get("answer", "")).split(" ")
        for w in answer_words:
            start_x = padding + 10
            for c in range(len(w)):
                bx = start_x + c * (ans_box + 4)
                draw.rectangle([bx, cur_y, bx + ans_box, cur_y + ans_box], outline=0, width=3)
                radius = ans_box // 2 - 5
                draw.ellipse([bx + ans_box // 2 - radius, cur_y + ans_box // 2 - radius,
                              bx + ans_box // 2 + radius, cur_y + ans_box // 2 + radius], outline=0, width=3)
            cur_y += ans_box + 14

        return pil_to_escpos(img.crop((0, 0, target_width, min(cur_y + 10, total_height))))

    # Pure Python Fallback
    total_h = 750
    tb = ThermalBitmap(target_width, total_h)
    cur_y = 12

    for i in range(min(4, len(scrambled))):
        scram = scrambled[i]
        scram_text = scram.get("scrambled", "") if isinstance(scram, dict) else str(scram)
        circ = scram.get("circles", []) if isinstance(scram, dict) else (circles[i] if i < len(circles) else [])
        length = max(1, len(scram_text))
        col_pos = [padding + int(round(c * inner_width / float(length))) for c in range(length + 1)]

        tb.draw_rect(padding, cur_y, inner_width, clue_height, thickness=3)
        for c in range(length):
            cx0 = col_pos[c]
            cx1 = col_pos[c + 1]
            col_w = cx1 - cx0
            if c > 0:
                tb.draw_vline(cx0, cur_y, clue_height, thickness=2)
            tb.draw_char(cx0 + col_w // 2 - 9, cur_y + 8, scram_text[c], scale=3)

        ans_y = cur_y + clue_height
        for c in range(length):
            cx0 = col_pos[c]
            cx1 = col_pos[c + 1]
            col_w = cx1 - cx0
            tb.draw_rect(cx0, ans_y, col_w, cell_height, thickness=3)
            if c in circ:
                radius = min(col_w, cell_height) // 2 - 5
                tb.draw_circle(cx0 + col_w // 2, ans_y + cell_height // 2, radius, thickness=3)

        cur_y = ans_y + cell_height + word_gap

    # Scratchpad lines
    tb.draw_hline(padding, cur_y, inner_width, thickness=2)
    cur_y += 24
    tb.draw_text(padding, cur_y, "SCRATCHPAD:", scale=2)
    cur_y += 24
    for _ in range(2):
        tb.draw_hline(padding, cur_y, inner_width, thickness=2)
        cur_y += 30

    return tb.to_escpos()


# ==============================================================================
# 5. WORD SEARCH RASTERIZER (576 Dots Width)
# ==============================================================================
def render_wordsearch_raster(wordsearch_data: Dict[str, Any], target_width: int = THERMAL_WIDTH_DOTS) -> bytes:
    """Renders a crisp 1-bit letter matrix and checkbox list."""
    grid = wordsearch_data.get("grid", [])
    words = wordsearch_data.get("words", [])
    theme = wordsearch_data.get("theme", "General")

    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 12

    padding = 24
    inner_width = target_width - padding * 2
    cell_size = inner_width // cols
    grid_h = cell_size * rows

    checklist_rows = (len(words) + 1) // 2
    checklist_h = 40 + checklist_rows * 28
    total_h = 12 + grid_h + 20 + checklist_h + 12

    tb = ThermalBitmap(target_width, total_h)
    grid_y = 12

    tb.draw_rect(padding, grid_y, cell_size * cols, grid_h, thickness=4)
    for r in range(rows):
        for c in range(cols):
            letter = grid[r][c] if r < len(grid) and c < len(grid[r]) else " "
            cx = padding + c * cell_size + (cell_size - 18) // 2
            cy = grid_y + r * cell_size + (cell_size - 21) // 2
            tb.draw_char(cx, cy, letter, scale=3)
            if c > 0:
                tb.draw_vline(padding + c * cell_size, grid_y, grid_h, thickness=1)
        if r > 0:
            tb.draw_hline(padding, grid_y + r * cell_size, cell_size * cols, thickness=1)

    cur_y = grid_y + grid_h + 16
    tb.draw_hline(padding, cur_y, inner_width, thickness=2)
    cur_y += 18
    tb.draw_text(padding, cur_y, f"THEME: {theme.upper()}", scale=2)
    cur_y += 28

    col_w = inner_width // 2
    for i, word in enumerate(words):
        col_idx = i % 2
        row_idx = i // 2
        ix = padding + col_idx * col_w
        iy = cur_y + row_idx * 28
        tb.draw_rect(ix, iy + 2, 16, 16, thickness=2)
        tb.draw_text(ix + 24, iy + 2, word.upper(), scale=2)

    return tb.to_escpos()


# ==============================================================================
# 6. BINARY RASTERIZER (576 Dots Width)
# ==============================================================================
def render_binary_raster(binary_data: Dict[str, Any], target_width: int = THERMAL_WIDTH_DOTS) -> bytes:
    """Renders a crisp 576-dot wide Binary (Takuzu) grid."""
    size = binary_data.get("size", 8)
    puzzle = binary_data.get("puzzle", [])

    padding = 24
    board_size = target_width - padding * 2
    cell_size = board_size // size
    total_h = padding + cell_size * size + padding

    tb = ThermalBitmap(target_width, total_h)
    tb.draw_rect(padding, padding, cell_size * size, cell_size * size, thickness=4)

    for i in range(1, size):
        pos = padding + i * cell_size
        tb.draw_hline(padding, pos, cell_size * size, thickness=2)
        tb.draw_vline(pos, padding, cell_size * size, thickness=2)

    for r in range(size):
        for c in range(size):
            val = puzzle[r][c] if r < len(puzzle) and c < len(puzzle[r]) else -1
            if val in (0, 1):
                cx = padding + c * cell_size + (cell_size - 18) // 2
                cy = padding + r * cell_size + (cell_size - 21) // 2
                tb.draw_char(cx, cy, str(val), scale=3)

    return tb.to_escpos()


# ==============================================================================
# 7. MINES RASTERIZER (576 Dots Width)
# ==============================================================================
def render_mines_raster(mines_data: Dict[str, Any], target_width: int = THERMAL_WIDTH_DOTS) -> bytes:
    """Renders a crisp 576-dot wide Mines deduction grid."""
    rows = mines_data.get("rows", 8)
    cols = mines_data.get("cols", 8)
    puzzle = mines_data.get("puzzle", [])
    total_mines = mines_data.get("total_mines", 10)

    padding = 24
    inner_width = target_width - padding * 2
    cell_size = inner_width // cols
    board_h = cell_size * rows

    badge_h = 36
    total_h = 12 + badge_h + 12 + board_h + 12
    tb = ThermalBitmap(target_width, total_h)

    # Badge
    tb.draw_rect(padding, 12, inner_width, badge_h, thickness=3)
    tb.draw_text(padding + 16, 20, f"TOTAL MINES: {total_mines}", scale=2)

    grid_y = 12 + badge_h + 12
    tb.draw_rect(padding, grid_y, cell_size * cols, board_h, thickness=4)

    for c in range(1, cols):
        tb.draw_vline(padding + c * cell_size, grid_y, board_h, thickness=2)
    for r in range(1, rows):
        tb.draw_hline(padding, grid_y + r * cell_size, cell_size * cols, thickness=2)

    for r in range(rows):
        for c in range(cols):
            val = puzzle[r][c] if r < len(puzzle) and c < len(puzzle[r]) else -1
            if val >= 0:
                cx = padding + c * cell_size + (cell_size - 18) // 2
                cy = grid_y + r * cell_size + (cell_size - 21) // 2
                tb.draw_char(cx, cy, str(val), scale=3)
            else:
                tb.draw_circle(padding + c * cell_size + cell_size // 2,
                               grid_y + r * cell_size + cell_size // 2, 2, thickness=2)

    return tb.to_escpos()


# ==============================================================================
# 8. TENTS RASTERIZER (576 Dots Width)
# ==============================================================================
def render_tents_raster(tents_data: Dict[str, Any], target_width: int = THERMAL_WIDTH_DOTS) -> bytes:
    """
    Renders a crisp 576-dot wide Tents & Trees grid.
    Features 1-bit pine tree icons, row/column margin clues, and Tier 1 borders.
    """
    size = tents_data.get("size", 8)
    row_clues = tents_data.get("row_clues", [0] * size)
    col_clues = tents_data.get("col_clues", [0] * size)
    puzzle = tents_data.get("puzzle", [])

    padding = 24
    inner_width = target_width - padding * 2
    # 1 column for row clues, size columns for grid
    total_cols = size + 1
    cell_size = inner_width // total_cols
    board_w = cell_size * total_cols
    board_h = cell_size * (size + 1)
    total_h = padding + board_h + padding

    tb = ThermalBitmap(target_width, total_h)

    # Grid origin
    gx = padding
    gy = padding

    # Draw outer perimeter around actual puzzle grid (excluding header clues)
    puzzle_x = gx + cell_size
    puzzle_y = gy + cell_size
    puzzle_w = cell_size * size
    puzzle_h = cell_size * size
    tb.draw_rect(puzzle_x, puzzle_y, puzzle_w, puzzle_h, thickness=4)

    # Internal grid lines
    for i in range(1, size):
        tb.draw_vline(puzzle_x + i * cell_size, puzzle_y, puzzle_h, thickness=2)
        tb.draw_hline(puzzle_x, puzzle_y + i * cell_size, puzzle_w, thickness=2)

    # Column clues (top margin)
    for c in range(size):
        clue = col_clues[c]
        cx = puzzle_x + c * cell_size + (cell_size - 18) // 2
        cy = gy + (cell_size - 21) // 2
        tb.draw_char(cx, cy, str(clue), scale=3)

    # Row clues (left margin)
    for r in range(size):
        clue = row_clues[r]
        cx = gx + (cell_size - 18) // 2
        cy = puzzle_y + r * cell_size + (cell_size - 21) // 2
        tb.draw_char(cx, cy, str(clue), scale=3)

    # Draw cells: pine trees in tree cells
    for r in range(size):
        for c in range(size):
            is_tree = (r < len(puzzle) and c < len(puzzle[r]) and puzzle[r][c] == 1)
            cx = puzzle_x + c * cell_size + cell_size // 2
            cy = puzzle_y + r * cell_size + cell_size // 2

            if is_tree:
                # Draw geometric 1-bit pine tree
                # Trunk
                trunk_w = max(4, cell_size // 10)
                trunk_h = max(6, cell_size // 6)
                tb.fill_rect(cx - trunk_w // 2, cy + cell_size // 4 - trunk_h, trunk_w, trunk_h, color=1)

                # Tiered foliage (3 stacked triangles)
                for tier in range(3):
                    tier_top = cy - cell_size // 3 + tier * (cell_size // 6)
                    tier_base = tier_top + cell_size // 4
                    half_w = (tier + 1) * (cell_size // 7)
                    for y in range(tier_top, tier_base):
                        prog = (y - tier_top) / float(max(1, tier_base - tier_top))
                        cur_w = int(half_w * prog)
                        tb.draw_hline(cx - cur_w, y, cur_w * 2 + 1, thickness=1, color=1)

    return tb.to_escpos()


# ==============================================================================
# 9. BRIDGES RASTERIZER (576 Dots Width)
# ==============================================================================
def render_bridges_raster(bridges_data: Dict[str, Any], target_width: int = THERMAL_WIDTH_DOTS) -> bytes:
    """
    Renders a crisp 576-dot wide Bridges (Hashiwokakero) network.
    Features circular island badges with centered digits and clean whitespace corridors.
    """
    size = bridges_data.get("size", 8)
    islands = bridges_data.get("islands", [])

    padding = 32
    board_size = target_width - padding * 2
    step = board_size // (size - 1) if size > 1 else board_size
    total_h = padding + board_size + padding

    tb = ThermalBitmap(target_width, total_h)

    # Subtle outer boundary markers
    corner_len = 16
    # Top-left
    tb.draw_hline(padding, padding, corner_len, thickness=2)
    tb.draw_vline(padding, padding, corner_len, thickness=2)
    # Top-right
    tb.draw_hline(padding + board_size - corner_len, padding, corner_len, thickness=2)
    tb.draw_vline(padding + board_size, padding, corner_len, thickness=2)
    # Bottom-left
    tb.draw_hline(padding, padding + board_size, corner_len, thickness=2)
    tb.draw_vline(padding, padding + board_size - corner_len, corner_len, thickness=2)
    # Bottom-right
    tb.draw_hline(padding + board_size - corner_len, padding + board_size, corner_len, thickness=2)
    tb.draw_vline(padding + board_size, padding + board_size - corner_len, corner_len, thickness=2)

    # Draw Islands
    island_radius = max(18, min(24, step // 3))
    for isl in islands:
        r, c = isl.get("r", 0), isl.get("c", 0)
        count = isl.get("count", 1)

        cx = padding + c * step
        cy = padding + r * step

        # Clear background inside island circle
        tb.fill_circle = getattr(tb, 'fill_circle', None)
        # Clear square under circle
        tb.fill_rect(cx - island_radius, cy - island_radius, island_radius * 2, island_radius * 2, color=0)

        # Draw circle outline
        tb.draw_circle(cx, cy, island_radius, thickness=3, color=1)

        # Draw centered clue digit
        char_scale = 3 if island_radius >= 20 else 2
        char_w = 6 * char_scale
        char_h = 7 * char_scale
        tb.draw_char(cx - char_w // 2, cy - char_h // 2, str(count), scale=char_scale, color=1)

    return tb.to_escpos()


# ==============================================================================
# 10. KILLER SUDOKU RASTERIZER (576 Dots Width)
# ==============================================================================
def render_killer_raster(killer_data: Dict[str, Any], target_width: int = THERMAL_WIDTH_DOTS) -> bytes:
    """
    Renders a 576-dot wide Killer Sudoku grid (4x4 or 6x6) for 80mm thermal receipts:
    - Thick solid lines (4px) for outer frame and 2x2 / 2x3 box boundaries.
    - Thin solid lines (2px) between all individual cells.
    - Inset dashed lines tracing the inner perimeter of each cage (~8-10 dots inset).
    - Top-left cage sum numbers tucked neatly inside the inset dashed border.
    """
    size = killer_data.get("size", 4)
    box_r = killer_data.get("box_rows", 2)
    box_c = killer_data.get("box_cols", 2 if size == 4 else 3)
    cages = killer_data.get("cages", [])

    padding = 24
    board_size = target_width - padding * 2
    c_size = board_size // size
    actual_board = c_size * size
    total_h = padding + actual_board + padding
    inset = 10 if size == 4 else 8

    # Collect inset cage boundary segments
    h_segments = []
    v_segments = []
    for cg in cages:
        cell_set = {(r, c) for r, c in cg.get("cells", [])}

        def in_cage(r: int, c: int) -> bool:
            return (r, c) in cell_set

        for r, c in cg.get("cells", []):
            x0 = padding + c * c_size
            x1 = x0 + c_size
            y0 = padding + r * c_size
            y1 = y0 + c_size

            # Top edge
            if not in_cage(r - 1, c):
                y = y0 + inset
                x_s = x0 + inset if not in_cage(r, c - 1) else (x0 - inset if in_cage(r - 1, c - 1) else x0)
                x_e = x1 - inset if not in_cage(r, c + 1) else (x1 + inset if in_cage(r - 1, c + 1) else x1)
                h_segments.append((min(x_s, x_e), max(x_s, x_e), y))

            # Bottom edge
            if not in_cage(r + 1, c):
                y = y1 - inset
                x_s = x0 + inset if not in_cage(r, c - 1) else (x0 - inset if in_cage(r + 1, c - 1) else x0)
                x_e = x1 - inset if not in_cage(r, c + 1) else (x1 + inset if in_cage(r + 1, c + 1) else x1)
                h_segments.append((min(x_s, x_e), max(x_s, x_e), y))

            # Left edge
            if not in_cage(r, c - 1):
                x = x0 + inset
                y_s = y0 + inset if not in_cage(r - 1, c) else (y0 - inset if in_cage(r - 1, c - 1) else y0)
                y_e = y1 - inset if not in_cage(r + 1, c) else (y1 + inset if in_cage(r + 1, c - 1) else y1)
                v_segments.append((x, min(y_s, y_e), max(y_s, y_e)))

            # Right edge
            if not in_cage(r, c + 1):
                x = x1 - inset
                y_s = y0 + inset if not in_cage(r - 1, c) else (y0 - inset if in_cage(r - 1, c + 1) else y0)
                y_e = y1 - inset if not in_cage(r + 1, c) else (y1 + inset if in_cage(r + 1, c + 1) else y1)
                v_segments.append((x, min(y_s, y_e), max(y_s, y_e)))

    # Merge collinear segments
    from collections import defaultdict
    h_by_y = defaultdict(list)
    for x1, x2, y in h_segments:
        h_by_y[y].append((x1, x2))
    merged_h = []
    for y, intervals in h_by_y.items():
        intervals.sort()
        cur_s, cur_e = intervals[0]
        for s, e in intervals[1:]:
            if s <= cur_e:
                cur_e = max(cur_e, e)
            else:
                merged_h.append((cur_s, cur_e, y))
                cur_s, cur_e = s, e
        merged_h.append((cur_s, cur_e, y))

    v_by_x = defaultdict(list)
    for x, y1, y2 in v_segments:
        v_by_x[x].append((y1, y2))
    merged_v = []
    for x, intervals in v_by_x.items():
        intervals.sort()
        cur_s, cur_e = intervals[0]
        for s, e in intervals[1:]:
            if s <= cur_e:
                cur_e = max(cur_e, e)
            else:
                merged_v.append((x, cur_s, cur_e))
                cur_s, cur_e = s, e
        merged_v.append((x, cur_s, cur_e))

    dash_len = 8
    gap_len = 6

    if HAS_PILLOW:
        img = Image.new("L", (target_width, total_h), 255)
        draw = ImageDraw.Draw(img)

        try:
            font_clue = ImageFont.truetype("Courier.ttf", max(13, int(c_size * 0.16)))
        except IOError:
            font_clue = ImageFont.load_default()

        # 1. Outer Frame (4px)
        draw.rectangle([padding, padding, padding + actual_board, padding + actual_board], outline=0, width=4)

        # 2. Grid lines
        for r in range(1, size):
            y = padding + r * c_size
            thick = 4 if (r % box_r == 0) else 1
            draw.line([padding, y, padding + actual_board, y], fill=0, width=thick)

        for c in range(1, size):
            x = padding + c * c_size
            thick = 4 if (c % box_c == 0) else 1
            draw.line([x, padding, x, padding + actual_board], fill=0, width=thick)

        # 3. Inset Dashed Cage Outlines
        for x1, x2, y in merged_h:
            x = x1
            while x < x2:
                seg = min(dash_len, x2 - x)
                draw.line([x, y, x + seg, y], fill=0, width=2)
                x += dash_len + gap_len

        for x, y1, y2 in merged_v:
            y = y1
            while y < y2:
                seg = min(dash_len, y2 - y)
                draw.line([x, y, x, y + seg], fill=0, width=2)
                y += dash_len + gap_len

        # 4. Cage Sum Clues
        for cg in cages:
            cells = sorted(cg.get("cells", []))
            if not cells:
                continue
            r0, c0 = cells[0]
            tx = padding + c0 * c_size + inset + 4
            ty = padding + r0 * c_size + inset + 2
            draw.text((tx, ty), str(cg.get("sum", "")), fill=0, font=font_clue)

        return pil_to_escpos(img)

    # Pure Python ThermalBitmap Fallback
    tb = ThermalBitmap(target_width, total_h)

    # 1. Outer Frame (4px)
    tb.draw_rect(padding, padding, actual_board, actual_board, thickness=4)

    # 2. Grid lines
    for r in range(1, size):
        y = padding + r * c_size
        thick = 4 if (r % box_r == 0) else 2
        tb.draw_hline(padding, y, actual_board, thickness=thick)

    for c in range(1, size):
        x = padding + c * c_size
        thick = 4 if (c % box_c == 0) else 2
        tb.draw_vline(x, padding, actual_board, thickness=thick)

    # 3. Inset Dashed Cage Outlines
    for x1, x2, y in merged_h:
        x = x1
        while x < x2:
            seg = min(dash_len, x2 - x)
            tb.draw_hline(x, y, seg, thickness=2)
            x += dash_len + gap_len

    for x, y1, y2 in merged_v:
        y = y1
        while y < y2:
            seg = min(dash_len, y2 - y)
            tb.draw_vline(x, y, seg, thickness=2)
            y += dash_len + gap_len

    # 4. Cage Sum Clues
    for cg in cages:
        cells = sorted(cg.get("cells", []))
        if not cells:
            continue
        r0, c0 = cells[0]
        tx = padding + c0 * c_size + inset + 3
        ty = padding + r0 * c_size + inset + 3
        tb.draw_text(tx, ty, str(cg.get("sum", "")), scale=2, color=1)

    return tb.to_escpos()
