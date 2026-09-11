# Morning Puzzles: Header & Presentation Specification

This document establishes the official visual and structural standard for representing game titles, difficulty ratings, and puzzle layouts across the **Morning Puzzles** ecosystem (Web Simulator, Python Backend, and ESP32 Firmware).

All existing games—and any future games added to Morning Puzzles—must strictly conform to this specification.

---

## 1. Core Design Principles

1. **Strict One-Word Titles**: Every puzzle must have a single-word uppercase title (e.g. `STARS`, `SUDOKU`, `SEARCH`, `NONOGRAM`, `JUMBLE`). Multi-word names, compound descriptors, subtitles, and slash-delineated variants (such as *"Word Search"*, *"Daily Jumble"*, *"Queens / Star Battle"*, or *"Nonogram / Picross"*) are **strictly prohibited**.
2. **Uniform Visual Hierarchy**: Every puzzle begins with the same standardized header format regardless of whether it is rendered as a high-contrast thermal canvas graphic or a plain-text monospaced ASCII fallback.
3. **Zero Gameplay Descriptions**: Receipts must **never** include explanatory text describing how the game works (e.g., *"Unscramble these four words..."*, *"Find words hidden horizontally..."*, *"No two stars may touch diagonally"*). Thermal receipt space is premium, and puzzles should be clean, authentic, and self-explanatory.
4. **Difficulty Rating Placement**: For puzzles that feature a difficulty tier, the rating must be placed **immediately underneath the game title and immediately above the drawing of the game itself**.
5. **Contextual Metadata Placement**: Metadata specific to solving mechanics (such as Search themes, Jumble cartoon punchlines, or Nonogram row/column clue numbers) belongs in or directly adjacent to the interactive solving area—never in the top title header.
6. **No Grid Dimension Leaks**: Headers must never display grid dimensions (e.g. `8x8 Grid`, `5x5 Picross`, `Size: 10x10`).

---

## 2. Standard Header Hierarchy

```
[Section Separator / Spacing]
      --- [ONE-WORD TITLE] ---      <-- Line 1: Centered Single-Word Title
       DIFFICULTY: [LEVEL]          <-- Line 2: Centered Difficulty (if applicable)
[Spacing / Tear Line]
┌────────────────────────────────┐
│                                │
│   DRAWING OF THE GAME ITSELF   │  <-- Line 3: Grid / Interactive Puzzle Canvas
│                                │
└────────────────────────────────┘
[Solving Checklist / Clues]         <-- Line 4: Word Checklist, Riddle Punchline, etc.
```

### Formatting Details (48-Column Thermal Monospace / ESC/POS)
* **Title Format**: Centered, strictly one word, uppercase, enclosed by triple dashes:
  ```text
  --- STARS ---
  --- SUDOKU ---
  --- SEARCH ---
  --- NONOGRAM ---
  --- JUMBLE ---
  --- BINARY ---
  --- MINES ---
  ```
* **Difficulty Format**: Centered, uppercase, prefixed by `DIFFICULTY: `:
  ```text
  DIFFICULTY: EASY
  DIFFICULTY: MEDIUM
  DIFFICULTY: HARD
  DIFFICULTY: MASTER
  DIFFICULTY: EXPERT
  ```

---

## 3. Official Game Registry & Matrix

| Puzzle Name | Exact Title Header | Has Difficulty? | Standard Difficulty Values | Notes / Placement Rules |
| :--- | :--- | :---: | :--- | :--- |
| **Stars** | `--- STARS ---` | **Yes** | `EASY` (6x6), `MEDIUM` (8x8), `HARD` (9x9 2★), `MASTER` (10x10 2★) | Pure board drawing immediately follows difficulty. Replaces legacy "Queens" / "Star Battle". |
| **Sudoku** | `--- SUDOKU ---` | **Yes** | `EASY`, `MEDIUM`, `HARD` | Pure 9x9 grid immediately follows difficulty. No clue counts in header. |
| **Search** | `--- SEARCH ---` | **No** *(Theme)* | *None* | Letter grid starts directly below header. Replaces legacy "Word Search". `★ THEME: [NAME]` placed with checklist words below grid. |
| **Nonogram** | `--- NONOGRAM ---` | **Yes** | `EASY` (5x5), `MEDIUM` (8x8), `HARD` (10x10), `EXPERT` (15x15) | Board with row/column clues follows difficulty. Single-word name replaces "Nonogram / Picross". |
| **Jumble** | `--- JUMBLE ---` | **Yes** | `EASY`, `MEDIUM`, `HARD` | Clue boxes start directly below header. Single-word name replaces "Daily Jumble". |
| **Binary** | `--- BINARY ---` | **Yes** | `EASY` (6x6), `MEDIUM` (8x8), `HARD` (8x8) | Pure grid with 0 and 1 clues follows difficulty. |
| **Mines** | `--- MINES ---` | **Yes** | `EASY` (8 Mines), `MEDIUM` (12 Mines), `HARD` (15 Mines) | Solitaire paper Minesweeper on 8x8 grid. `TOTAL MINES: [N]` placed directly above drawing. 100% deductive solvability guarantee (zero guessing). |

---

## 4. Prohibited Elements Checklist

Before committing any puzzle renderer or generator update, verify that **NONE** of the following elements appear in the header or drawing:

- [x] **NO multi-word titles or slash-separated names** (*"Word Search"*, *"Daily Jumble"*, *"Queens / Star Battle"*, *"Nonogram / Picross"*). Titles must be strictly a single word.
- [x] **NO instructions or rules** (*"Find words hidden horizontally..."*, *"No two stars touch..."*, *"Place numbers 1-9..."*, *"Circled letters form..."*).
- [x] **NO grid dimension metadata in titles** (*"8x10 Grid"*, *"Size: 5x5"*).
- [x] **NO duplicate in-canvas titles** (e.g., drawing `S E A R C H` or `J U M B L E` inside the canvas when the standardized header is already present above it).
- [x] **NO simulator-only debug labels** on physical receipts (*"Thermal 203 DPI"*, *"Shaded by 1-Bit Dithering"*).

---

## 5. Specification for Adding New Games

When adding a new puzzle type to Morning Puzzles:

1. **Select Strict One-Word Title**: Choose a single uppercase English word (e.g., `--- CROSSWORD ---`, `--- TANGLE ---`, `--- KAKURO ---`, `--- BATTLESHIPS ---`, `--- NURIKABE ---`). Multi-word, hyphenated, or slash-separated names are strictly forbidden.
2. **Determine Difficulty Applicability**:
   - If the game has discrete difficulty levels, map them to standard keywords (`EASY`, `MEDIUM`, `HARD`, `EXPERT`, `MASTER`) and display via `DIFFICULTY: [LEVEL]`.
   - If the game is driven by theme or topic rather than difficulty, omit the difficulty line and group theme metadata with the solving area below the grid.
3. **Canvas Drawing**: Start the canvas directly with the visual puzzle component (borders, cells, or game clues). Do not draw a banner title inside the canvas.
4. **Checklist & Clues**: Place any answer verification or pencil-tracking tools (checkboxes `[ ]`, scratch lines) underneath the puzzle grid separated by a dashed tear-line.
