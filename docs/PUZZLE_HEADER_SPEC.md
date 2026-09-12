# Morning Puzzles: Header & Presentation Specification

This document establishes the official visual and structural standard for representing game titles, difficulty ratings, and puzzle layouts across the **Morning Puzzles** ecosystem (Web Simulator, Python Backend, and ESP32 Firmware).

All existing games—and any future games added to Morning Puzzles—must strictly conform to this specification.

---

## 1. Core Design Principles

1. **Strict One-Word Titles**: Every puzzle must have a single-word uppercase title (e.g. `STARS`, `SUDOKU`, `SEARCH`, `NONOGRAM`, `JUMBLE`, `BINARY`, `MINES`). Multi-word names, compound descriptors, subtitles, and slash-delineated variants (such as *"Word Search"*, *"Daily Jumble"*, *"Queens / Star Battle"*, or *"Nonogram / Picross"*) are **strictly prohibited**.
2. **Uniform Visual Hierarchy**: Every puzzle begins with the same standardized header format regardless of whether it is rendered as a high-contrast thermal canvas graphic or a plain-text monospaced ASCII fallback.
3. **Mandatory One-Sentence Gameplay Instruction**: Underneath the title header and underneath the difficulty (or directly beneath the title if no difficulty exists), every puzzle must feature **exactly one clear, concise sentence** explaining the goal or how to play the game so that new players can immediately understand the objective.
4. **Difficulty Rating Placement**: For puzzles that feature a difficulty tier, the rating must be placed **immediately underneath the game title and immediately above the one-sentence gameplay instruction**.
5. **Contextual Metadata Placement**: Metadata specific to solving mechanics (such as Search themes, Jumble cartoon punchlines, or Nonogram row/column clue numbers, or Mines total count) belongs in or directly adjacent to the interactive solving area—never in the top title header.
6. **No Grid Dimension Leaks**: Headers must never display grid dimensions (e.g. `8x8 Grid`, `5x5 Picross`, `Size: 10x10`).

---

## 2. Standard Header Hierarchy

```
[Section Separator / Spacing]
      --- [ONE-WORD TITLE] ---      <-- Line 1: Centered Single-Word Title
       DIFFICULTY: [LEVEL]          <-- Line 2: Centered Difficulty (if applicable)
  [One-sentence instruction line]   <-- Line 3: 1-Sentence Goal / How-to-Play Description
[Spacing / Context Metadata (e.g. TOTAL MINES: N)]
┌────────────────────────────────┐
│                                │
│   DRAWING OF THE GAME ITSELF   │  <-- Line 4: Grid / Interactive Puzzle Canvas
│                                │
└────────────────────────────────┘
[Solving Checklist / Clues]         <-- Line 5: Word Checklist, Riddle Punchline, etc.
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
* **One-Sentence Instruction Format**: Centered or wrapped across 48-column thermal monospace, italicized in simulator UI, concise single sentence.

---

## 3. Official Game Registry & Matrix

| Puzzle Name | Exact Title Header | Has Difficulty? | Standard Difficulty Values | Canonical One-Sentence Gameplay Instruction | Notes / Placement Rules |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **Stars** | `--- STARS ---` | **Yes** | `EASY` (5x5), `MEDIUM` (8x8), `HARD` (9x9 2★), `MASTER` (10x10 2★) | *Place stars so each row, column, and shaped region contains the required star count with no two stars touching, even diagonally.* | Replaces legacy "Queens" / "Star Battle". Board drawing follows instruction. |
| **Sudoku** | `--- SUDOKU ---` | **Yes** | `EASY`, `MEDIUM`, `HARD` | *Fill the grid so that every row, column, and 3x3 box contains digits 1 through 9 without repeating.* | Pure 9x9 grid follows instruction. |
| **Search** | `--- SEARCH ---` | **No** *(Theme)* | *None* | *Find and circle all of the listed words hidden horizontally, vertically, or diagonally within the letter grid.* | Instruction placed directly below title. `★ THEME: [NAME]` placed with checklist words below grid. |
| **Nonogram** | `--- NONOGRAM ---` | **Yes** | `EASY` (5x5), `MEDIUM` (8x8), `HARD` (10x10), `EXPERT` (15x15) | *Use the number clues outside the grid to shade the correct cells and reveal the hidden pixel picture.* | Board with row/column clues follows instruction. Single-word name replaces "Nonogram / Picross". |
| **Jumble** | `--- JUMBLE ---` | **Yes** | `EASY`, `MEDIUM`, `HARD` | *Unscramble the clue words, then arrange the circled letters to solve the punchline riddle.* | Clue boxes start directly below instruction. Single-word name replaces "Daily Jumble". |
| **Binary** | `--- BINARY ---` | **Yes** | `EASY` (6x6), `MEDIUM` (8x8), `HARD` (8x8) | *Fill the grid with 0s and 1s so no more than two identical numbers touch and each row and column has equal counts.* | Pure grid with 0 and 1 clues follows instruction. |
| **Mines** | `--- MINES ---` | **Yes** | `EASY` (8 Mines), `MEDIUM` (12 Mines), `HARD` (15 Mines) | *Use the numbered clues showing adjacent mine counts to deduce and mark every hidden mine across the grid.* | `TOTAL MINES: [N]` placed between instruction and drawing. 100% deductive solvability guarantee (zero guessing). |
| **Tents** | `--- TENTS ---` | **Yes** | `EASY` (6x6), `MEDIUM` (8x8), `HARD` (8x8) | *Pair each tree with an orthogonally adjacent tent such that tents never touch, even diagonally, matching the row and column counts.* | Board with pine trees and row/column margin counts follows instruction. |
| **Bridges** | `--- BRIDGES ---` | **Yes** | `EASY` (6x6), `MEDIUM` (8x8), `HARD` (8x8) | *Connect the numbered islands with horizontal and vertical bridges so all islands form a single network matching each island's bridge count.* | Clean grid with circular island badges and whitespace corridors follows instruction. |

---

## 4. Prohibited Elements Checklist

Before committing any puzzle renderer or generator update, verify that **NONE** of the following elements appear in the header or drawing:

- [x] **NO multi-word titles or slash-separated names** (*"Word Search"*, *"Daily Jumble"*, *"Queens / Star Battle"*, *"Nonogram / Picross"*, *"Tents and Trees"*, *"Hashiwokakero"*). Titles must be strictly a single word.
- [x] **NO multi-sentence rule essays or multi-paragraph tutorials** (gameplay instructions must be strictly one concise, clear sentence).
- [x] **NO missing or omitted gameplay instructions** (every game must include its canonical one-sentence goal between difficulty and drawing).
- [x] **NO grid dimension metadata in titles** (*"8x10 Grid"*, *"Size: 5x5"*).
- [x] **NO duplicate in-canvas titles** (e.g., drawing `S E A R C H` or `J U M B L E` inside the canvas when the standardized header is already present above it).
- [x] **NO simulator-only debug labels** on physical receipts (*"Thermal 203 DPI"*, *"Shaded by 1-Bit Dithering"*).

---

## 5. Specification for Adding New Games

When adding a new puzzle type to Morning Puzzles:

1. **Select Strict One-Word Title**: Choose a single uppercase English word (e.g., `--- CROSSWORD ---`, `--- TANGLE ---`, `--- KAKURO ---`, `--- BATTLESHIPS ---`, `--- NURIKABE ---`). Multi-word, hyphenated, or slash-separated names are strictly forbidden.
2. **Define One-Sentence Instruction**: Author exactly one clear, concise sentence explaining the objective so new players understand how to play immediately.
3. **Determine Difficulty Applicability**:
   - If the game has discrete difficulty levels, map them to standard keywords (`EASY`, `MEDIUM`, `HARD`, `EXPERT`, `MASTER`) and display via `DIFFICULTY: [LEVEL]`.
   - If the game is driven by theme or topic rather than difficulty, omit the difficulty line and place the one-sentence instruction directly below the title.
4. **Canvas Drawing**: Start the canvas directly with the visual puzzle component (borders, cells, or game clues). Do not draw a banner title inside the canvas.
5. **Checklist & Clues**: Place any answer verification or pencil-tracking tools (checkboxes `[ ]`, scratch lines) underneath the puzzle grid separated by a dashed tear-line.
6. **Solution Key Formatting**: Ensure the game's solution format strictly follows the monospaced ASCII requirements in [`docs/PUZZLE_SOLUTION_KEY_SPEC.md`](PUZZLE_SOLUTION_KEY_SPEC.md).

