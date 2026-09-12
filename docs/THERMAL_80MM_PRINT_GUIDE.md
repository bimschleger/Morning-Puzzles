# 80mm Thermal Receipt Printer: Master Specification & Agentic Guide

This document establishes the official technical specification, hardware constraints, protocol standards, and agentic design guidelines for generating print-ready output for **80mm commercial thermal receipt printers** across the Morning Puzzles ecosystem.

---

## 1. Physical Hardware & Printable Geometry

Standard commercial thermal receipt printers (e.g. Epson TM-T88 series, Star Micronics, Munbyn, Rongta, Xprinter, Bixolon) operate under strict physical and electro-mechanical specifications:

| Hardware Attribute | Specification | Operational Implication |
| :--- | :--- | :--- |
| **Paper Roll Width** | $80.0\text{ mm}$ ($3.15\text{ inches}$) | Outer physical dimension of the paper roll. |
| **Printhead Width** | $72.0\text{ mm}$ ($2.83\text{ inches}$) | Active thermal element width. |
| **Side Margins** | $\approx 4.0\text{ mm}$ on left and right | Physical unprintable paper edges. Paper guidance space. |
| **Printhead Resolution** | $203.2\text{ DPI}$ ($8.0\text{ dots/mm}$) | Fixed dot grid resolution across the line. |
| **Native Line Width** | **$576\text{ dots}$** ($72\text{ mm} \times 8\text{ dots/mm}$) | **Universal standard pixel width for all raster graphics.** |
| **Line Byte Width** | **$72\text{ bytes}$** ($576 \div 8$) | Each horizontal raster scanline must be exactly 72 bytes. |
| **Character Columns (Font A)**| $48\text{ columns}$ ($12 \times 24\text{ dots}$) | Default monospaced text width ($48 \times 12 = 576\text{ dots}$). |
| **Character Columns (Font B)**| $64\text{ columns}$ ($9 \times 17\text{ or }9 \times 24\text{ dots}$)| Condensed monospaced text width ($64 \times 9 = 576\text{ dots}$). |
| **Cutter Distance (Offset)** | $15\text{ mm} - 25\text{ mm}$ ($120 - 200\text{ dots}$) | Distance from thermal burn line to cutting blade. |

> [!IMPORTANT]
> **The 576-Dot Rule**: Any bitmap image generated for an 80mm thermal printer **must have a width of exactly 576 dots**. If an image has an arbitrary width, the printer driver will either wrap the scanlines diagonally (ruining the image) or truncate content.

---

## 2. 1-Bit Monochrome Raster Encoding & Polarity

Thermal printers cannot produce continuous grayscales or color. A thermal printhead dot is binary: either energized (burns black) or unenergized (leaves paper white).

### A. Bit Order and Pixel Polarity
* **ESC/POS Raster Polarity**:
  * **`1` = Burn Dot (Black)**
  * **`0` = Leave Unburnt (White / Paper)**
  *(Caution: Many graphic libraries like PIL mode `'1'` treat `0` as black and `255` or `1` as white. When converting, bits MUST be inverted so that dark pixels map to `1`).*
* **Byte Alignment & Bit Packing**:
  * Scanned horizontally from left to right, top to bottom.
  * Packed **Most Significant Bit (MSB) first**:
    * Bit 7 (0x80) = Pixel $(x + 0)$
    * Bit 6 (0x40) = Pixel $(x + 1)$
    * Bit 5 (0x20) = Pixel $(x + 2)$
    * Bit 4 (0x10) = Pixel $(x + 3)$
    * Bit 3 (0x08) = Pixel $(x + 4)$
    * Bit 2 (0x04) = Pixel $(x + 5)$
    * Bit 1 (0x02) = Pixel $(x + 6)$
    * Bit 0 (0x01) = Pixel $(x + 7)$
  * Every raster line consists of $\frac{576}{8} = \mathbf{72\text{ bytes}}$.

### B. Shading & Halftoning Guidelines
To render shaded regions (such as Star Battle regions, Nonogram guides, or puzzle cell fills) without native grayscales:
1. **Deterministic Geometric Hatching (Recommended for Puzzle Logic)**:
   - Use distinct geometric line patterns (45° diagonal, reverse diagonal, crosshatch, stipple dots, pinstripes) as defined in [`docs/THERMAL_DRAWING_SPEC.md`](file:///Users/brian.bimschleger/Documents/GitHub/MOrning%20Puzzles/docs/THERMAL_DRAWING_SPEC.md).
   - Guarantees 100% sharp rendering without fuzzy anti-aliasing artifacts.
2. **Ordered Dithering (Bayer Matrix)**:
   - Use an $8 \times 8$ Bayer threshold matrix when rendering smooth pictorial illustrations or continuous grayscales.
3. **Error Diffusion (Floyd-Steinberg)**:
   - Suitable for photographic or natural illustrations. Avoid for sharp grid lines, as diffusion can introduce noise along straight borders.

---

## 3. ESC/POS Protocol Reference for 80mm Output

Thermal printers communicate using standard ESC/POS command sequences over TCP Port 9100 (JetDirect / RAW socket) or Serial UART:

### A. Core Control Commands
| Command | Hex Bytes | Description |
| :--- | :--- | :--- |
| `ESC @` | `1B 40` | **Initialize Printer**: Resets buffer, line spacing, margins, and text styles. Always send at the start of a print job. |
| `ESC a n` | `1B 61 n` | **Select Justification**: `n=0` (Left), `n=1` (Center), `n=2` (Right). |
| `ESC E n` | `1B 45 n` | **Bold Mode**: `n=1` (On), `n=0` (Off). |
| `GS ! n` | `1D 21 n` | **Character Size**: `n=0x00` (Normal $1 \times 1$), `n=0x11` (Double Width & Double Height). |
| `ESC d n` | `1B 64 n` | **Print and Feed $n$ Lines**: Advances paper by $n$ lines. |
| `GS V m n` | `1D 56 42 03` | **Feed and Partial Cut**: Advances paper by 3 units and executes a partial cut, leaving a small uncut tab. |
| `GS V m` | `1D 56 01` | **Full Cut**: Immediately cuts paper entirely across. |

### B. Raster Bit Image Command: `GS v 0`
The universal command for rendering 1-bit bitmap graphics supported across virtually all 80mm thermal receipt printers:

$$\text{Command: } \mathtt{1D\ 76\ 30}\ m\ xL\ xH\ yL\ yH\ [d_1 \dots d_k]$$

* `m = 0x00`: Normal density ($203 \times 203\text{ DPI}$, 1:1 aspect ratio).
* `xL, xH`: Width in **BYTES** calculated as $xL = \text{widthBytes} \pmod{256}$, $xH = \lfloor \text{widthBytes} / 256 \rfloor$.
  * For 576 dots: $\text{widthBytes} = 72 \rightarrow \mathbf{xL = 0x48 (72)}, \mathbf{xH = 0x00}$.
* `yL, yH`: Height in **DOTS** (lines) calculated as $yL = \text{height} \pmod{256}$, $yH = \lfloor \text{height} / 256 \rfloor$.
* Data size $k = \text{widthBytes} \times \text{heightDots} = 72 \times \text{heightDots}$.

```python
# Standard ESC/POS GS v 0 Header for 576-dot raster image
def make_escpos_raster_header(height_dots: int) -> bytes:
    width_bytes = 72  # 576 dots // 8
    xl = width_bytes & 0xFF
    xh = (width_bytes >> 8) & 0xFF
    yl = height_dots & 0xFF
    yh = (height_dots >> 8) & 0xFF
    return bytes([0x1D, 0x76, 0x30, 0x00, xl, xh, yl, yh])
```

---

## 4. Thermal Physics, Power Management & Duty Cycle

Thermal receipt printers are thermal impulse devices. Ignoring the physical limitations of the thermal printhead can cause print failures, blurred output, or equipment damage:

### A. Peak Current & Power Supply Brownouts
- Each energized dot pulls approximately $15\text{ mA} - 25\text{ mA}$ at $24\text{V}$.
- Firing all 576 dots simultaneously on a solid black horizontal line demands **$\approx 8.6\text{ Amps}$ to $14\text{ Amps}$ peak current**.
- Most receipt printer power supplies are rated for **$2.0\text{ A} - 2.5\text{ A}$ continuous (peak $4.0\text{ A}$)**.
- **Symptom of Over-Current**: Microcontroller brownout / reboot, dropped TCP connections, or horizontal white streaks where voltage sags.

### B. Thermal Accumulation & Bleed
- When consecutive scanlines contain heavy black areas, the thermal elements retain residual heat.
- **Symptom of Thermal Accumulation**: Smearing, fuzzy edges, paper sticking to the platen roller, and high-pitched squealing.

### C. The 35% Duty Cycle Rule
- **Average Black Pixel Density per Scanline**: Keep total burned dots below **$35\%$** ($\le 200$ black dots out of 576).
- **Rule**: NEVER use solid black full-width banners ($100\%$ black lines).
- **Inverted Blocks**: Inverted text boxes (white text on black fill) must be limited to short badges with generous whitespace padding, or bordered boxes with normal text.
- **Grid Dividers**: Use $1.0\text{px} - 3.5\text{px}$ strokes instead of solid blocks.

---

## 5. Buffer Management & Network Flow Control

Thermal printers have minimal on-board RAM (typically $4\text{ KB} - 64\text{ KB}$ input buffer):

* **The Problem**: A high-resolution daily puzzle raster receipt may span $1,200\text{ scanlines} \times 72\text{ bytes} \approx \mathbf{86.4\text{ KB}}$. Dumping this entire stream over Port 9100 in a single network burst will overflow the printer's receive buffer, leading to dropped scanlines, corrupt ESC/POS commands, or printed garbage characters.
* **Flow Control Best Practices**:
  1. **Chunked Streaming**: Send bitmap data in chunks of $512\text{ bytes} - 1024\text{ bytes}$.
  2. **Inter-Chunk Pacing**: Introduce a small pacing delay ($2\text{ ms} - 5\text{ ms}$) between chunks when streaming from microcontrollers (ESP32) or serial links.
  3. **Multi-Slice Rasterization**: For very tall prints, divide the graphic into smaller vertical slices (e.g. $200 - 300\text{ dots}$ height per `GS v 0` block) rather than one massive bitmap block.

---

## 6. Paper Handling: Feed & Cutter Offset

A standard receipt printer features two separate mechanical components positioned along the paper feed path:
1. **Thermal Printhead Line** (upstream)
2. **Auto-Cutter Blade** (downstream)

```
[Paper Roll] ---> [Thermal Printhead] === (15-25mm gap) ===> [Cutter Blade] ---> [Ejected Paper]
```

### The Cutter Offset Rule
Because the cutter blade is located $15\text{ mm} - 25\text{ mm}$ past the printhead:
* If you issue a cut command (`GS V`) immediately after printing, **the blade will slice through the last $4 - 6$ lines of your receipt**.
* **Mandatory Pre-Cut Feed**:
  * ALWAYS send at least **$4\text{ to }5\text{ line feeds}$ (`\n\n\n\n\n` or `ESC d 4`)** before executing the cut command.
* **Partial Cut (`GS V 66 3`) vs Full Cut (`GS V 65`)**:
  * Prefer **Partial Cut** (`\x1d\x56\x42\x03`): Leaves a small paper bridge tab so the receipt remains attached to the printer mouth and does not fall onto the floor.

---

## 7. Hybrid Receipt Architecture (Text + 1-Bit Raster)

For daily puzzle receipts, the optimal architecture is a **Hybrid ESC/POS Pipeline**:

```
┌────────────────────────────────────────────────────────┐
│  [ESC @] Initialize Printer                            │
│  [ESC a 1] Center                                      │
│  ================================================      │ <-- ESC/POS Monospace Text Header
│               DAILY MORNING PUZZLES                    │
│             Monday, September 14, 2026                 │
│  ================================================      │
│                                                        │
│  --- SUDOKU ---                                        │ <-- Standard Text Title (PUZZLE_HEADER_SPEC)
│  DIFFICULTY: MEDIUM                                    │ <-- Standard Text Difficulty
│  Fill the grid so every row, col, and box has 1-9.     │ <-- Canonical One-Sentence Instruction
│                                                        │
│  [GS v 0 ...] 576-Dot Crisp 1-Bit Raster Image         │ <-- Game Grid Graphic (No duplicate titles!)
│  ┌───┬───┬───┐                                         │
│  │ 5 │ . │ 2 │                                         │
│  └───┴───┴───┘                                         │
│  - - - - - - - - - - - - - - - - - - - - - - - - - -   │ <-- Dashed Section Divider
│                                                        │
│  ... (Additional Puzzles: STARS, SEARCH, etc.) ...     │
│                                                        │
│  ================================================      │ <-- Footer Text
│  Printed on ESP32 80mm Commercial Thermal Receipt      │
│  ================================================      │
│  [LF x 4] Pre-Cut Feed (15-25mm)                       │
│  [GS V 66 3] Partial Paper Cut                         │
└────────────────────────────────────────────────────────┘
```

### Benefits of Hybrid Mode
1. **Header Spec Compliance**: Headers, difficulty, and instructions are rendered with native printer fonts for perfect character alignment and compliance with [`docs/PUZZLE_HEADER_SPEC.md`](file:///Users/brian.bimschleger/Documents/GitHub/MOrning%20Puzzles/docs/PUZZLE_HEADER_SPEC.md).
2. **Graphic Clarity**: Complex grids, territory hatchings, and circular clue badges are rendered as pixel-perfect 576-dot graphics adhering to [`docs/THERMAL_DRAWING_SPEC.md`](file:///Users/brian.bimschleger/Documents/GitHub/MOrning%20Puzzles/docs/THERMAL_DRAWING_SPEC.md).
3. **Data Efficiency**: Text sections stream instantly with tiny byte payloads; only puzzle boards require raster bytes.

---

## 8. Agentic Checklist for Onboarding / Modifying Puzzles

Whenever writing or modifying code that generates puzzle output for thermal receipt printers, verify each item before approval:

- [ ] **Width is Exactly 576 Dots**: The rendered image width is strictly `576` pixels ($72$ bytes per row).
- [ ] **Byte-Aligned Rows**: Scanline width in bytes is exactly $72$, with no bit shift or alignment errors.
- [ ] **MSB-First Bit Packing**: Pixel $(x)$ is mapped to `1 << (7 - (x % 8))`.
- [ ] **Polarity Inversion Checked**: `1` corresponds to black ink (burn dot), `0` corresponds to white paper.
- [ ] **No In-Image Titles or Rules**: The image contains ONLY the game drawing (grid, clues, checkboxes, scratchpad). Game title, difficulty, and one-sentence rules must be in standard text headers above the image.
- [ ] **Duty Cycle $\le 35\%$**: No solid black horizontal blocks or heavy inverted fills. Use 1-bit geometric hatches or Bayer dithering.
- [ ] **Safe Stroke Widths**: Grid lines use $1.0\text{px} - 3.5\text{px}$ strokes; interactive letter boxes use $1.5\text{px} - 1.8\text{px}$.
- [ ] **Pre-Cut Feed Included**: Receipt generator feeds $\ge 4$ lines before issuing the cut command.
- [ ] **Pacing / Chunking Enabled**: Long raster byte streams are streamed in chunks $\le 1024$ bytes with flow-control delays when targeting microcontrollers or serial ports.
- [ ] **Graceful Text Fallback**: System provides clear, formatted monospaced ASCII output when graphical rendering libraries (Pillow) are unavailable.
