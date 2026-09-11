"""
ESC/POS 80mm Raster Image Renderer (576 Dots Width)
Converts 1-bit monochrome images, graphical grids, and dithered territory puzzles
into ESC/POS GS v 0 format.
"""

from typing import Tuple, Dict, Any, List

def image_to_escpos_raster(image_bytes: bytes, width: int, height: int) -> bytes:
    """
    Wraps 1-bit bitmap bytes into the ESC/POS GS v 0 (raster bit image) command.
    Standard 80mm receipt printable width = 576 dots (72 bytes wide).
    
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


def pil_to_escpos(image) -> bytes:
    """
    Converts a PIL.Image instance into ESC/POS raster bytes.
    Automatically handles resizing to 576px width and 1-bit thresholding.
    """
    try:
        from PIL import Image
    except ImportError:
        raise RuntimeError("Pillow is required for graphical rendering. Install via: pip install Pillow")

    target_width = 576
    if image.width != target_width:
        ratio = target_width / float(image.width)
        new_height = int(float(image.height) * ratio)
        image = image.resize((target_width, new_height), Image.Resampling.LANCZOS)

    # Convert to 1-bit monochrome using Floyd-Steinberg dithering
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
                    # In PIL '1' mode: 0 is black, 255 is white.
                    # In ESC/POS thermal printer: 1 is black (burn dot), 0 is white (no burn).
                    if pixels[x, y] == 0:
                        byte_val |= (1 << (7 - bit))
            raw_data.append(byte_val)

    return image_to_escpos_raster(bytes(raw_data), width, height)


def render_queens_dithered_raster(queens_data: Dict[str, Any], target_width: int = 576) -> bytes:
    """
    Renders a Queens / Star Battle puzzle as a crisp 1-bit dithered graphic.
    Each territory is filled with a distinct shade of gray and dithered for thermal printing.
    Region borders are drawn with heavy solid black lines.
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        raise RuntimeError("Pillow is required for Queens graphical rendering. Install via: pip install Pillow")

    size = queens_data["grid_size"]
    regions = queens_data["regions"]

    padding = 36  # margin for row/column coordinates
    board_size = target_width - padding * 2
    cell_size = board_size / float(size)

    # Base image: 8-bit grayscale ('L')
    img = Image.new("L", (target_width, target_width), 255)
    draw = ImageDraw.Draw(img)

    # Distinct grayscale tones for regions
    tones = [255, 225, 195, 165, 135, 105, 75, 45, 15]

    # 1. Fill cells with region tones
    for r in range(size):
        for c in range(size):
            reg = regions[r][c]
            tone = tones[reg % len(tones)]
            x0 = int(padding + c * cell_size)
            y0 = int(padding + r * cell_size)
            x1 = int(padding + (c + 1) * cell_size)
            y1 = int(padding + (r + 1) * cell_size)
            draw.rectangle([x0, y0, x1, y1], fill=tone)

    # 2. Draw interior grid lines and territory boundaries
    for r in range(size):
        for c in range(size):
            reg = regions[r][c]
            x0 = int(padding + c * cell_size)
            y0 = int(padding + r * cell_size)
            x1 = int(padding + (c + 1) * cell_size)
            y1 = int(padding + (r + 1) * cell_size)

            # Bottom edge
            is_bottom_boundary = (r == size - 1) or (regions[r + 1][c] != reg)
            w = 5 if is_bottom_boundary else 1
            color = 0 if is_bottom_boundary else 180
            draw.line([x0, y1, x1, y1], fill=color, width=w)

            # Right edge
            is_right_boundary = (c == size - 1) or (regions[r][c + 1] != reg)
            w = 5 if is_right_boundary else 1
            color = 0 if is_right_boundary else 180
            draw.line([x1, y0, x1, y1], fill=color, width=w)

    # 3. Outer border (thick black)
    draw.rectangle([padding, padding, padding + board_size, padding + board_size], outline=0, width=5)

    # Convert grayscale image to 1-bit monochrome using Floyd-Steinberg dithering
    return pil_to_escpos(img)


def render_jumble_raster(jumble_data: Dict[str, Any], target_width: int = 576) -> bytes:
    """
    Renders a syndicated newspaper-style Jumble puzzle as an ESC/POS 1-bit raster graphic.
    - Clue box containing scrambled letters directly stacked above answer squares
    - Circles inscribed in designated answer squares
    - 4 word combos stacked vertically
    - Riddle question
    - Blank ruled scratchpad lines for handwriting discovered circled letters
    - Answer letter squares with inscribed circles grouped by word
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        raise RuntimeError("Pillow is required for Jumble graphical rendering. Install via: pip install Pillow")

    padding = 24
    inner_width = target_width - padding * 2

    # Attempt to load clean fonts or fallback
    try:
        font_banner = ImageFont.truetype("Arial.ttf", 32)
        font_sub = ImageFont.truetype("Arial.ttf", 16)
        font_box = ImageFont.truetype("Courier.ttf", 24)
        font_riddle = ImageFont.truetype("Arial.ttf", 20)
    except IOError:
        font_banner = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_box = ImageFont.load_default()
        font_riddle = ImageFont.load_default()

    total_height = 1100
    img = Image.new("L", (target_width, total_height), 255)
    draw = ImageDraw.Draw(img)

    # 1. Header Banner
    draw.text((padding, padding), "J U M B L E", fill=0, font=font_banner)
    draw.text((padding + 220, padding + 4), "THAT SCRAMBLED WORD GAME", fill=0, font=font_sub)
    draw.text((padding + 220, padding + 22), "Syndicated Newspaper Format", fill=100, font=font_sub)

    cur_y = padding + 54
    draw.text((padding, cur_y), "Unscramble these four Jumbles, one letter to each square,", fill=50, font=font_sub)
    cur_y += 22
    draw.text((padding, cur_y), "to form four ordinary words.", fill=50, font=font_sub)
    cur_y += 32

    # 2. 4 Word Combos (Stacked Vertically, Full Width of Receipt)
    clue_height = 46
    cell_height = 68
    word_gap = 20

    words = jumble_data.get("words", [])
    scrambled = jumble_data.get("scrambled", words)
    circles = jumble_data.get("circles", [])

    for i in range(min(4, len(scrambled))):
        scram = scrambled[i]
        length = len(scram)
        circ = circles[i] if i < len(circles) else []

        col_pos = [padding + int(round(c * inner_width / float(length))) for c in range(length + 1)]

        # Clue Box (Scrambled Letters) - spans entire inner_width
        draw.rectangle([padding, cur_y, padding + inner_width, cur_y + clue_height], outline=0, width=4)
        for c in range(length):
            cx0 = col_pos[c]
            cx1 = col_pos[c + 1]
            col_w = cx1 - cx0
            char_cx = cx0 + col_w // 2 - 8

            if c > 0:
                draw.line([cx0, cur_y, cx0, cur_y + clue_height], fill=160, width=2)

            draw.text((char_cx, cur_y + 10), scram[c], fill=0, font=font_box)

        ans_y = cur_y + clue_height

        # Answer Squares (directly connected underneath, full width)
        for c in range(length):
            cx0 = col_pos[c]
            cx1 = col_pos[c + 1]
            col_w = cx1 - cx0
            draw.rectangle([cx0, ans_y, cx1, ans_y + cell_height], outline=0, width=4)
            if c in circ:
                radius = min(col_w, cell_height) // 2 - 6
                circ_cx = cx0 + col_w // 2
                circ_cy = ans_y + cell_height // 2
                draw.ellipse([circ_cx - radius, circ_cy - radius, circ_cx + radius, circ_cy + radius], outline=0, width=4)

        cur_y = ans_y + cell_height + word_gap

    # 3. Divider Line
    draw.line([padding, cur_y, padding + inner_width, cur_y], fill=120, width=2)
    cur_y += 18

    # 4. Riddle Clue Section
    draw.text((padding, cur_y), "RIDDLE CLUE:", fill=0, font=font_sub)
    cur_y += 24
    riddle_text = f'"{jumble_data.get("riddle", "")}"'
    draw.text((padding + 8, cur_y), riddle_text, fill=0, font=font_riddle)
    cur_y += 32

    # 5. Scratchpad Ruled Lines
    draw.text((padding, cur_y), "Discovered letters scratchpad (write letters here):", fill=80, font=font_sub)
    cur_y += 26
    for _ in range(2):
        draw.line([padding, cur_y, padding + inner_width, cur_y], fill=160, width=2)
        cur_y += 32

    # 6. Final Answer Circles (Centered & Large)
    cur_y += 10
    draw.text((padding, cur_y), "Answer here:", fill=0, font=font_sub)
    cur_y += 28

    answer_words = jumble_data.get("answer", "").split(" ")
    ans_box = cell_height  # Exactly matches clue answer squares height (68 dots)
    word_spacing = 20
    max_boxes = max(1, inner_width // ans_box)

    word_tokens = []
    for w in answer_words:
        if len(w) > max_boxes:
            for i in range(0, len(w), max_boxes):
                word_tokens.append(w[i:i + max_boxes])
        else:
            word_tokens.append(w)

    # Group words into lines
    lines = []
    cur_line = []
    cur_w = 0
    for w in word_tokens:
        w_w = len(w) * ans_box
        add_w = word_spacing + w_w if cur_line else w_w
        if cur_w + add_w > inner_width and cur_line:
            lines.append(cur_line)
            cur_line = [w]
            cur_w = w_w
        else:
            cur_line.append(w)
            cur_w += add_w
    if cur_line:
        lines.append(cur_line)

    for line in lines:
        line_w = sum(len(w) * ans_box for w in line) + (len(line) - 1) * word_spacing
        cur_x = padding + max(0, (inner_width - line_w) // 2)

        for w_str in line:
            for c in range(len(w_str)):
                bx = cur_x + c * ans_box
                draw.rectangle([bx, cur_y, bx + ans_box, cur_y + ans_box], outline=0, width=4)
                radius = ans_box // 2 - 6
                circ_cx = bx + ans_box // 2
                circ_cy = cur_y + ans_box // 2
                draw.ellipse([circ_cx - radius, circ_cy - radius, circ_cx + radius, circ_cy + radius], outline=0, width=4)
            cur_x += len(w_str) * ans_box + word_spacing

        cur_y += ans_box + 16

    cur_y += 16

    # Crop to actual content height
    final_img = img.crop((0, 0, target_width, min(cur_y, total_height)))
    return pil_to_escpos(final_img)


def render_nonogram_raster(nonogram_data: Dict[str, Any], target_width: int = 576, show_solution: bool = False) -> bytes:
    """
    Renders a high-contrast 1-bit thermal Nonogram (Picross) grid as ESC/POS GS v 0 raster bytes.
    Supports any difficulty size (5x5, 8x8, 10x10, 15x15) and stretches across the full 576-dot width.
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        raise RuntimeError("Pillow is required for Nonogram graphical rendering. Install via: pip install Pillow")

    size = nonogram_data.get("rows", nonogram_data.get("size", 5))
    row_clues = nonogram_data.get("row_clues", [])
    col_clues = nonogram_data.get("col_clues", [])
    solution = nonogram_data.get("solution", nonogram_data.get("grid", []))

    padding = 24
    inner_width = target_width - padding * 2  # 528 dots

    if size <= 5:
        cell_size = 76
        major_interval = 5
        font_size = 24
        label_size = 20
    elif size <= 8:
        cell_size = 50
        major_interval = 4
        font_size = 20
        label_size = 18
    elif size <= 10:
        cell_size = 40
        major_interval = 5
        font_size = 18
        label_size = 16
    else:
        cell_size = 26
        major_interval = 5
        font_size = 14
        label_size = 14

    grid_size = cell_size * size
    row_clue_width = inner_width - grid_size

    max_col_clues = max((len(c) for c in col_clues), default=1)
    col_clue_item_h = max(24, int(cell_size * 0.55))
    col_clue_height = max(50, max_col_clues * col_clue_item_h + 16)

    total_height = padding + col_clue_height + grid_size + padding
    img = Image.new("L", (target_width, total_height), 255)
    draw = ImageDraw.Draw(img)

    try:
        font_clue = ImageFont.truetype("Courier.ttf", font_size)
        font_label = ImageFont.truetype("Arial.ttf", label_size)
    except IOError:
        font_clue = ImageFont.load_default()
        font_label = ImageFont.load_default()

    grid_x = padding + row_clue_width
    grid_y = padding + col_clue_height

    # 1. Top-Left Corner Tile
    draw.rectangle([padding, padding, grid_x, grid_y], fill=240, outline=0, width=3)
    draw.text((padding + row_clue_width // 2 - 20, padding + col_clue_height // 2 - 12), f"{size}x{size}", fill=0, font=font_label)

    # 2. Column Clues (Top Area)
    draw.rectangle([grid_x, padding, grid_x + grid_size, grid_y], outline=0, width=3)
    for c in range(size):
        col_cx = grid_x + c * cell_size + cell_size // 2
        clues = col_clues[c] if c < len(col_clues) else [0]
        for k, val in enumerate(clues):
            dist_from_bottom = (len(clues) - 1 - k) * col_clue_item_h
            val_y = grid_y - 12 - dist_from_bottom
            draw.text((col_cx - 6, val_y), str(val), fill=0, font=font_clue)

        if c > 0:
            is_major = (c % major_interval == 0)
            draw.line([grid_x + c * cell_size, padding, grid_x + c * cell_size, grid_y], fill=0 if is_major else 180, width=3 if is_major else 1)

    # 3. Row Clues (Left Area)
    draw.rectangle([padding, grid_y, grid_x, grid_y + grid_size], outline=0, width=3)
    row_clue_char_w = max(18, int(cell_size * 0.45))
    for r in range(size):
        row_cy = grid_y + r * cell_size + cell_size // 2 - font_size // 2
        clues = row_clues[r] if r < len(row_clues) else [0]
        for k, val in enumerate(clues):
            dist_from_right = (len(clues) - 1 - k) * row_clue_char_w
            val_x = grid_x - 14 - dist_from_right
            draw.text((val_x, row_cy), str(val), fill=0, font=font_clue)

        if r > 0:
            is_major = (r % major_interval == 0)
            draw.line([padding, grid_y + r * cell_size, grid_x, grid_y + r * cell_size], fill=0 if is_major else 180, width=3 if is_major else 1)

    # 4. Grid Cells
    for r in range(size):
        for c in range(size):
            cx = grid_x + c * cell_size
            cy = grid_y + r * cell_size
            if show_solution and solution and r < len(solution) and c < len(solution[r]) and solution[r][c] == 1:
                draw.rectangle([cx, cy, cx + cell_size, cy + cell_size], fill=0)
            else:
                # Tactile center dot guide
                dot_r = 2
                draw.ellipse([cx + cell_size // 2 - dot_r, cy + cell_size // 2 - dot_r, cx + cell_size // 2 + dot_r, cy + cell_size // 2 + dot_r], fill=160)

    # 5. Grid Lines (Major & Minor)
    for i in range(size + 1):
        is_major = (i % major_interval == 0) or (i == size)
        w = 4 if is_major else 1
        color = 0 if is_major else 160
        # Horizontal
        draw.line([grid_x, grid_y + i * cell_size, grid_x + grid_size, grid_y + i * cell_size], fill=color, width=w)
        # Vertical
        draw.line([grid_x + i * cell_size, grid_y, grid_x + i * cell_size, grid_y + grid_size], fill=color, width=w)

    # Outer border
    draw.rectangle([padding, padding, padding + inner_width, grid_y + grid_size], outline=0, width=5)
    return pil_to_escpos(img)


