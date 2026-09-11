# Morning Puzzles: Thermal Drawing & Graphic Design Specification

This specification defines the visual standards, geometric tokens, stroke hierarchies, typography formulas, and 1-bit thermal shading algorithms for rendering puzzle games across the **Morning Puzzles** ecosystem.

Whether rendered via HTML5 Canvas in the interactive simulator or converted to 1-bit ESC/POS raster bitmaps for physical 80mm thermal receipt printers, all game drawings must strictly adhere to these standards.

---

## 1. Physical Hardware & Canvas Geometry

### A. Thermal Printhead Specifications
* **Paper Roll Width**: 80 mm (3.15 in)
* **Printhead Resolution**: 203 DPI (8 dots per mm)
* **Native Pixel Width**: 576 dots across the printhead
* **Usable Printable Width**: 576 dots (margins handled in firmware or virtual canvas padding)

### B. Virtual Canvas Coordinate System (Simulator Scaling)
To ensure identical visual proportion on desktop/mobile screens matching physical 80mm receipt paper:
* **`totalWidth`**: `345px` (outer boundary of the thermal receipt strip)
* **`padding`**: `12px` (left and right margins)
* **`innerWidth`**: `321px` (`345px - 2 * 12px = 321px`)
* **Scale Ratio**: $\approx 0.557 \times$ of native 576-dot thermal hardware ($321\text{px} \times 1.794 \approx 576\text{ dots}$). Every $1\text{px}$ in the canvas maps directly to $\approx 1.8\text{ dots}$ on physical thermal paper.

---

## 2. Color Palette & High-Contrast Tokens

Thermal receipt printers only support **binary 1-bit ink state**: a dot is either burned black or left as unburned paper. No true grayscales or anti-aliasing exist on physical thermal heads.

| Token Name | Hex Value | RGB Value | Purpose / Usage |
| :--- | :--- | :--- | :--- |
| `INK_BLACK` | `#111111` | `(18, 18, 18)` | Outer borders, major lines, digits, letters, checkmarks |
| `PAPER_IVORY` | `#fafaf7` | `(250, 250, 247)` | Background canvas color (simulates warm thermal paper) |
| `HAIRLINE_DIVIDER` | `rgba(0, 0, 0, 0.22)` | `(0, 0, 0, 0.22)` | Minor cell dividers, internal grid lines for scanning |
| `TEAR_DIVIDER` | `#888888` | `(136, 136, 136)` | Dashed rule separating puzzle grid from checklist / clues |
| `CORNER_TILE_BG` | `#eeebe3` | `(238, 235, 227)` | Nonogram/Picross top-left inactive tile header |
| `GUIDE_DOT` | `#bbbbbb` | `(187, 187, 187)` | Center guide dots in empty Nonogram cells for pencil work |
| `SCRATCHPAD_RULE` | `#999999` | `(153, 153, 153)` | Ruled handwriting lines for letter brainstorming |

---

## 3. Four-Tier Stroke & Border Hierarchy

To establish consistent visual weight across games of differing sizes (e.g. 5x5 Nonogram vs 12x12 Word Search vs 9x9 Sudoku), all line work must adhere to the following 4 tiers:

```
┌────────────────────────────────────────────────────────┐  <-- Tier 1: 3.5px Heavy Outer Perimeter
│                                                        │
│   ┌───────────────┬───────────────┬────────────────┐   │  <-- Tier 2: 2.5px - 3.5px Major Subdivisions
│   │ .   .   .   . │ .   .   .   . │ .   .   .   .  │   │
│   │ ─ ─ ─ ─ ─ ─ ─ │ ─ ─ ─ ─ ─ ─ ─ │ ─ ─ ─ ─ ─ ─ ─  │   │  <-- Tier 4: 1.0px Subtle Cell Dividers
│   │ .   .   .   . │ .   .   .   . │ .   .   .   .  │   │
│   └───────────────┴───────────────┴────────────────┘   │
└────────────────────────────────────────────────────────┘
 - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  <-- Tier 4: 1.2px Dashed Tear Divider [3, 3]
 [ ] CHECKBOX                                               <-- Tier 3: 1.5px Component Stroke
```

### Tier 1: Heavy Perimeter Border (`3.5px`)
* **Stroke Width**: `3.5px`
* **Stroke Color**: `#111111`
* **Line Cap / Join**: `lineCap = 'square'`, `lineJoin = 'miter'`
* **Usage**: The solid bounding box around the puzzle grid (Sudoku 9x9 outer box, Stars outer boundary, Search outer grid, Nonogram composite frame, Binary & Mines grids).

### Tier 2: Major Subdivisions & Territory Boundaries (`2.5px` – `3.5px`)
* **Stroke Width**:
  * Sudoku $3 \times 3$ Box Boundaries: `3.5px`
  * Stars Territory Borders: `3.5px`
  * Nonogram 5-Cell Major Accent Lines: `2.5px`
* **Stroke Color**: `#111111`
* **Usage**: Separates mathematically significant gameplay regions.

### Tier 3: Interactive Component Outlines (`1.5px` – `1.8px`)
* **Stroke Width**:
  * Search Checkboxes (`11x11px`): `1.5px` (`#222222`)
  * Jumble Clue & Answer Letter Squares / Circles: `1.8px` (`#111111`)
  * Nonogram Clue Header Border: `1.5px` (`#111111`)
* **Usage**: Focused interactive targets that players interact with using a pen or pencil.

### Tier 4: Minor Grid Lines & Guide Separators (`1.0px` – `1.2px`)
* **Stroke Width**:
  * Internal Cell Dividers: `1.0px` (`rgba(0, 0, 0, 0.22)`)
  * Stars Same-Territory Guide Lines: `1.0px`, dashed `[2, 2]`
  * Dashed Tear Dividers: `1.2px` (`#888888`), dashed `[3, 3]`
  * Handwriting Scratchpad Lines: `1.2px` (`#999999`), dashed `[4, 4]`

---

## 4. Standard 1-Bit Geometric Hatching Palette

Because thermal printers cannot produce continuous grayscales, shaded regions (e.g. Star Battle territories, future shaded-cell games like Nurikabe, Hitori, Heyawake, Battleships) must use **deterministic pixel-level geometric hatching**.

Each pattern is evaluated on the pixel coordinates `(px, py)` of the rendered grid:

```text
Pattern 0: CLEAR         Pattern 1: 45° FORWARD      Pattern 2: -45° BACKWARD
┌────────────────┐       ┌──/───/───/───/─┐          ┌─\───\───\───\──┐
│                │       │ /   /   /   /  │          │  \   \   \   \ │
│   (Unshaded)   │       │/   /   /   /   │          │   \   \   \   \│
└────────────────┘       └────────────────┘          └────────────────┘

Pattern 3: CROSSHATCH    Pattern 4: DENSE 45°        Pattern 5: STIPPLE DOTS
┌──┼───┼───┼───┼─┐       ┌─/─/─/─/─/─/─/─/┐          ┌  ·   ·   ·   · ┐
│──┼───┼───┼───┼─│       │/ / / / / / / / ┼          │    ·   ·   ·   │
│──┼───┼───┼───┼─│       │ / / / / / / / /│          │  ·   ·   ·   · │
└────────────────┘       └────────────────┘          └────────────────┘

Pattern 6: DIAMOND       Pattern 7: PINSTRIPES
┌──╳───╳───╳───╳─┐       ┌────────────────┐
│ ╳ ╳ ╳ ╳ ╳ ╳ ╳ ╳│       │────────────────│
│╳   ╳   ╳   ╳   │       │────────────────│
└────────────────┘       └────────────────┘
```

### Mathematical Formulation Matrix
| ID | Pattern Name | Exact Pixel Boolean Formula | Visual Density | Recommended Usage |
| :-: | :--- | :--- | :-: | :--- |
| **0** | **Clear White** | `false` | 0% | Region 0 / unshaded cells / high contrast |
| **1** | **Forward Diagonal ($45^\circ$)** | `(px + py) % 6 === 0` | ~16% | Region 1 / primary diagonal territory |
| **2** | **Backward Diagonal ($-45^\circ$)**| `(px - py + 1000) % 6 === 0` | ~16% | Region 2 / opposing diagonal territory |
| **3** | **Square Crosshatch** | `px % 4 === 0 \|\| py % 4 === 0`| ~44% | Region 3 / high-contrast woven territory |
| **4** | **Dense Forward ($45^\circ$)** | `(px + py) % 4 === 0` | ~25% | Region 4 / medium-dark diagonal |
| **5** | **Dot Stipple Matrix** | `px % 3 === 0 && py % 3 === 0` | ~11% | Region 5 / subtle stippled background |
| **6** | **Diamond Crosshatch** | `(px + py) % 3 === 0 \|\| (px - py + 1000) % 3 === 0` | ~55% | Region 6 / textured diamond fill |
| **7** | **Horizontal Pinstripes** | `py % 3 === 0` | ~33% | Region 7 / linear directional texture |

### Code Implementation Snippet
```javascript
function getGeometricHatchPixel(patternId, px, py) {
  const pat = patternId % 8;
  switch (pat) {
    case 0: return false;
    case 1: return (px + py) % 6 === 0;
    case 2: return (px - py + 1000) % 6 === 0;
    case 3: return (px % 4 === 0 || py % 4 === 0);
    case 4: return (px + py) % 4 === 0;
    case 5: return (px % 3 === 0 && py % 3 === 0);
    case 6: return ((px + py) % 3 === 0 || (px - py + 1000) % 3 === 0);
    case 7: return py % 3 === 0;
    default: return false;
  }
}
```

---

## 5. Cell Geometry & Typography Scaling Formulas

To maintain proportional balance regardless of board dimensions, use deterministic scaling equations:

### A. Cell Size Calculation
$$W_{\text{cell}} = \left\lfloor \frac{W_{\text{inner}}}{N_{\text{cols}}} \right\rfloor$$
Where $W_{\text{inner}} = 321\text{px}$ (or $576\text{ dots}$ natively).

* **6 Columns** (Binary Easy): $\lfloor 321 / 6 \rfloor = \mathbf{53\text{px}}$ per cell ($S_{\text{font}} \approx \mathbf{28\text{px}}$ bold).
* **8 Columns** (Mines, Binary Medium/Hard, Search): $\lfloor 321 / 8 \rfloor = \mathbf{40\text{px}}$ per cell (Exact match to Jumble clue boxes, $S_{\text{font}} \approx \mathbf{21\text{px}}$ bold).
* **9 Columns** (Sudoku): $\lfloor 321 / 9 \rfloor = \mathbf{35\text{px}}$ per cell.
* **10 Columns** (Stars 10x10): $\lfloor 321 / 10 \rfloor = \mathbf{32\text{px}}$ per cell.

### B. Font Sizing & Typography Stack
* **Font Family**: `"Space Mono", "Courier New", monospace`
* **Character Centering**:
  ```javascript
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ```
* **Letter / Digit Font Size Ratio**:
  $$S_{\text{font}} = \text{round}(W_{\text{cell}} \times 0.52)$$
  * For 40px cell: $40 \times 0.52 \approx \mathbf{21\text{px}}$ bold
  * For 35px cell: $35 \times 0.52 \approx \mathbf{18\text{px}}$ bold
  * For 24px cell: $24 \times 0.52 \approx \mathbf{12\text{px}}$ bold

---

## 6. Interactive Checklists & Solving Controls

Any pencil-tracking elements placed below the puzzle grid must follow these exact dimensions:

### A. Search Checkboxes
* **Outer Size**: $11 \times 11\text{px}$
* **Border Width**: `1.5px` (`#222222`)
* **Layout**: 2 columns distributed across $W_{\text{inner}}$
* **Row Pitch**: `22px` height per row
* **Label Offset**: Checkbox drawn at `(itemX, itemY + 2)`, text at `itemX + 17` centered vertically at `itemY + 8`.

### B. Handwriting Scratchpad Lines (Daily Jumble / Word Puzzles)
* **Stroke Width**: `1.2px` (`#999999`)
* **Dash Pattern**: `[4, 4]`
* **Line Pitch**: `24px` line height (generous space for cursive or block letters)
* **Count**: Exactly 2 full-width ruled lines.

### C. Dashed Section Divider (Tear Line)
* **Stroke Width**: `1.2px` (`#888888`)
* **Dash Pattern**: `[3, 3]`
* **Margin Spacing**: `12px` top margin after grid, `12px` bottom margin before clues.

---

## 7. Checklist for Onboarding Future Puzzle Drawings

When building a canvas renderer for a new puzzle game:

- [ ] Set `canvas.width = 345` with `padding = 12` ($W_{\text{inner}} = 321$).
- [ ] Fill background with `PAPER_IVORY` (`#fafaf7`).
- [ ] Use `3.5px` solid `#111111` for the outer perimeter border.
- [ ] Use `1.0px` `rgba(0,0,0,0.22)` for internal cell divider lines.
- [ ] Scale letter/number fonts to $W_{\text{cell}} \times 0.52$ using `"Space Mono"`, centered with `textAlign = 'center'` and `textBaseline = 'middle'`.
- [ ] If applying territory shading, use `getGeometricHatchPixel(patternId, px, py)` for deterministic 1-bit hatching.
- [ ] Do **NOT** draw banner titles or rules inside the canvas—the standardized header (`--- [GAME NAME] ---` and `DIFFICULTY: [LEVEL]`) is placed above the canvas.
- [ ] If adding checklists or scratch lines, separate from the grid with the standard $1.2\text{px}$ dashed tear-line (`[3, 3]`).
