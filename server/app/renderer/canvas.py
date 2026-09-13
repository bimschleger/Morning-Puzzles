"""
Morning Puzzles - Thermal Drawing Canvas Engine
Provides unified 1-bit thermal raster primitives and GS v 0 byte packing
conforming strictly to:
  - 80mm thermal hardware standards (576 dots width / 72 bytes per row)
  - docs/THERMAL_80MM_PRINT_GUIDE.md
  - docs/THERMAL_DRAWING_SPEC.md

Supports both high-resolution Pillow rendering and Pure-Python ThermalBitmap fallback.
"""

from typing import Tuple, Dict, Any, List, Optional
import os

THERMAL_WIDTH_DOTS = 576
THERMAL_WIDTH_BYTES = 72  # 576 // 8

try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False


def image_to_escpos_raster(image_bytes: bytes, width: int, height: int) -> bytes:
    """
    Wraps 1-bit bitmap bytes into the ESC/POS GS v 0 (raster bit image) command.
    ESC/POS GS v 0 format:
      0x1D 0x76 0x30 0x00 xL xH yL yH [data...]
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
    - Average black pixel density (duty cycle) across the graphic
    - Peak black pixel density across any single horizontal scanline
    - Compliance with the 35% safe thermal duty cycle guideline
    """
    if len(raster_bytes) < 8:
        return {"error": "Invalid raster byte stream (too short)"}

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


def pil_to_escpos(image) -> bytes:
    """
    Converts a PIL.Image instance into ESC/POS GS v 0 raster bytes.
    Strictly forces width to 576 dots and ensures 1-bit MSB-first packing.
    """
    if not HAS_PILLOW:
        raise RuntimeError("Pillow is required for graphical rendering.")

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
    '+': [0x00, 0x08, 0x08, 0x3E, 0x08, 0x08, 0x00],
    '=': [0x00, 0x3E, 0x00, 0x3E, 0x00, 0x00, 0x00],
    '*': [0x00, 0x2A, 0x1C, 0x3E, 0x1C, 0x2A, 0x00],
    '/': [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x00],
    '(': [0x04, 0x08, 0x10, 0x10, 0x10, 0x08, 0x04],
    ')': [0x10, 0x08, 0x04, 0x04, 0x04, 0x08, 0x10],
    '_': [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3F],
    ',': [0x00, 0x00, 0x00, 0x00, 0x0C, 0x04, 0x08],
    '"': [0x14, 0x14, 0x14, 0x00, 0x00, 0x00, 0x00],
    "'": [0x08, 0x08, 0x10, 0x00, 0x00, 0x00, 0x00],
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

    def draw_line(self, x0: int, y0: int, x1: int, y1: int, thickness: int = 1, color: int = 1):
        dx = abs(x1 - x0)
        sx = 1 if x0 < x1 else -1
        dy = -abs(y1 - y0)
        sy = 1 if y0 < y1 else -1
        err = dx + dy

        while True:
            if thickness <= 1:
                self.set_pixel(x0, y0, color)
            else:
                half_t = thickness // 2
                for ty in range(-half_t, half_t + (thickness % 2)):
                    for tx in range(-half_t, half_t + (thickness % 2)):
                        self.set_pixel(x0 + tx, y0 + ty, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def draw_dashed_hline(self, x: int, y: int, w: int, dash_len: int = 4, gap_len: int = 4, thickness: int = 1, color: int = 1):
        if w <= 0 or dash_len == 0:
            return
        cur_x = x
        end_x = x + w
        while cur_x < end_x:
            seg_w = min(dash_len, end_x - cur_x)
            self.draw_hline(cur_x, y, seg_w, thickness=thickness, color=color)
            cur_x += dash_len + gap_len

    def draw_polygon(self, points: List[Tuple[int, int]], thickness: int = 1, color: int = 1):
        if len(points) < 2:
            return
        for i in range(len(points)):
            p1 = points[i]
            p2 = points[(i + 1) % len(points)]
            self.draw_line(int(round(p1[0])), int(round(p1[1])), int(round(p2[0])), int(round(p2[1])), thickness=thickness, color=color)

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
        pat = pattern_id % 10
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
                    is_burn = (py % 6 == 0)
                elif pat == 4:
                    is_burn = (px % 6 == 0)
                elif pat == 5:
                    is_burn = (px % 3 == 0 and py % 3 == 0)
                elif pat == 6:
                    is_burn = ((px + py) % 8 == 0 or (px - py + 1000) % 8 == 0)
                elif pat == 7:
                    is_burn = (px % 8 == 0 or py % 8 == 0)
                elif pat == 8:
                    rx = px % 6
                    ry = py % 6
                    is_burn = ((rx == 3 and abs(ry - 3) <= 1) or (ry == 3 and abs(rx - 3) <= 1))
                elif pat == 9:
                    is_burn = ((px + py) % 6 == 0 and (px % 4 < 2))

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

    def get_text_width(self, text: str, scale: int = 2) -> int:
        if not text or scale == 0:
            return 0
        char_w = 6 * scale + max(1, scale // 2)
        return len(text) * char_w

    def draw_centered_text(self, y: int, text: str, scale: int = 2, color: int = 1):
        w = self.get_text_width(text, scale=scale)
        x = (self.width - w) // 2
        self.draw_text(x, y, text, scale=scale, color=color)

    def draw_circle(self, cx: int, cy: int, radius: int, thickness: int = 2, color: int = 1):
        r_inner_sq = (radius - thickness) ** 2
        r_outer_sq = radius ** 2
        for py in range(max(0, cy - radius), min(cy + radius + 1, self.height)):
            for px in range(max(0, cx - radius), min(cx + radius + 1, self.width)):
                dist_sq = (px - cx) ** 2 + (py - cy) ** 2
                if r_inner_sq <= dist_sq <= r_outer_sq:
                    self.set_pixel(px, py, color)

    def fill_circle(self, cx: int, cy: int, radius: int, color: int = 1):
        if radius <= 0:
            return
        r_sq = radius * radius
        for py in range(max(0, cy - radius), min(cy + radius + 1, self.height)):
            dy_sq = (py - cy) ** 2
            for px in range(max(0, cx - radius), min(cx + radius + 1, self.width)):
                if (px - cx) ** 2 + dy_sq <= r_sq:
                    self.set_pixel(px, py, color)

    def to_escpos(self) -> bytes:
        return image_to_escpos_raster(bytes(self.buffer), self.width, self.height)
