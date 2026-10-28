---
description: Standards for Morning Puzzles game naming, difficulty representation, description authoring, and solution key layout
trigger: always_on
---

# Morning Puzzles: Game Naming, Description, Difficulty & Solution Key Standards

All agents and contributors working on Morning Puzzles must strictly follow these non-negotiable presentation and formatting standards across the Python backend, ESP32 firmware, and Web Simulator:

## 1. Game Titles & Naming
- **Strict One-Word Uppercase Title**: Every puzzle must have a single uppercase English word enclosed in triple dashes: `--- [TITLE] ---` (e.g., `--- STARS ---`, `--- SUDOKU ---`, `--- SEARCH ---`, `--- NONOGRAM ---`, `--- JUMBLE ---`, `--- BINARY ---`, `--- MINES ---`, `--- TENTS ---`, `--- BRIDGES ---`, `--- KILLER ---`, `--- CRYPTOGRAM ---`, `--- TANGO ---`).
- **Forbidden Titles**: Multi-word titles, subtitles, or slash-separated aliases (*"Word Search"*, *"Daily Jumble"*, *"Queens / Star Battle"*, *"Nonogram / Picross"*, *"Tents and Trees"*, *"Hashiwokakero"*) are strictly prohibited.
- **Subtitles in Solution Key**: Strictly single uppercase word matching the title, without dashes (e.g. `SUDOKU`, `SEARCH`, `NONOGRAM`, `STARS`, `JUMBLE`, `BINARY`, `MINES`, `TENTS`, `BRIDGES`, `KILLER`, `CRYPTOGRAM`, `TANGO`).
- **No Duplicate In-Canvas Titles**: Canvas graphics and ASCII renderers must not draw duplicate banner titles inside the puzzle board.

## 2. Difficulty Representation & Placement
- **Vertical Hierarchy**: When applicable, placed **immediately below the title header and immediately above the one-sentence gameplay instruction**:
  ```text
  --- [TITLE] ---
  DIFFICULTY: [LEVEL]
  [One-sentence instruction line]
  ```
- **Format**: Centered, uppercase, prefixed by `DIFFICULTY: ` (`DIFFICULTY: EASY`, `DIFFICULTY: MEDIUM`, `DIFFICULTY: HARD`, `DIFFICULTY: MASTER`, `DIFFICULTY: EXPERT`, `DIFFICULTY: EXTREME`).
- **Theme-Driven Exception**: Puzzles driven by theme rather than difficulty (`SEARCH`) **must completely omit** the difficulty line.

## 3. Gameplay Descriptions
- **Strict Character Limit ($\le 100$ Characters)**: The fully interpolated description string (including any dynamically inserted quantities) must **never exceed 100 characters** to guarantee clean $\le 2$-line wrapping at 44 printable columns on 80mm thermal receipt paper.
- **Canonical One-Sentence Formula**:
  `[Imperative Verb] + [Target with Dynamic Quantity] + [Context / Clues] + [Constraint]`
- **Approved Imperative Verbs**: Must begin directly with an action verb (*Place, Fill, Deduce, Connect, Pitch, Shade, Unscramble, Find*).
- **Dynamic Parameterization**: If difficulty alters any quantitative property, dynamically inject the exact count (e.g., `Place 1 star...` vs `Place 2 stars...`, `Deduce all [8 / 12 / 15] hidden mines...`, `Pitch [4 / 8 / 11] tents...`, `Find all [N] hidden words...`, digits `1-4` vs `1-6`).
- **Plain English Over Jargon**: Avoid algorithmic/geometric jargon (*no "orthogonally adjacent", "in a row", "polyomino", "connected component", "bipartite matching"*).
- **Generator Ground Truth**: Only state what the generation algorithm actually creates (do not claim procedural nonograms reveal a pixel picture).

## 4. Solution Key Layout & Presentation
- **Master Header**: Delimited by 48 dashes, centered `[ SOLUTION KEY ]`, followed by 48 dashes.
- **Column Restriction**: Standard ESC/POS Font A 48-column line limit. No line may exceed 48 characters. Coordinate lists and word lists must wrap to $\le 46$ characters.
- **Indentation**: 6 spaces left padding (`'      '`) for 2D ASCII grids to ensure visual centering.
- **Blank Line Separation**: Exactly one blank line must separate each puzzle's solution block.

## 5. Automated Verification
All changes must pass the automated validation suite:
```bash
python3 server/test_puzzle_standards.py
python3 server/test_game_onboarding.py
python3 server/test_game_rules.py
python3 server/test_thermal_format.py
python3 server/test_visual_consistency.py
python3 server/test_stars_deduction.py
python3 server/test_towers_deduction.py
python3 server/test_inequality_deduction.py
```

## 6. Puzzle Plugin Architecture & Extension Standards
All games in Morning Puzzles must be implemented as modular, self-contained plugins adhering to the `BasePuzzle` contract (`server/app/puzzles/base.py`):
- **Single Source of Truth**: Each game resides in `server/app/puzzles/<puzzle_name>.py` and encapsulates:
  - Procedural generation returning `BasePuzzleResult` (dict-compatible dataclass envelope)
  - Gameplay instruction generation complying with Section 3 formula ($\le 100$ characters)
  - ASCII text formatting for monospaced receipts
  - Solution key formatting (6-space pre-indented for grids, wrapped to $\le 46$ columns)
  - 576-dot thermal raster rendering via `ThermalCanvas` primitives conforming to Section 8 visual consistency
- **Registry Registration**: Every puzzle must be registered in `DEFAULT_REGISTRY` (`server/app/puzzles/registry.py`).
- **Zero Procedural Spaghetti & Pure Dynamic Routing**: Never introduce manual `elif puzzle_id == ...` branches or static per-game FastAPI route functions (`/api/v1/puzzles/<game>`) in `main.py`, `text_formatter.py`, or `composer.py`. All HTTP routing (`/api/v1/puzzles/{puzzle_id}`), difficulty resolution (`PuzzleRegistry._resolve_plugin_difficulty`), and receipt ordering (`DailyReceiptComposer._get_ordered_plugins`) are dynamically driven by `DEFAULT_REGISTRY`. Every registered puzzle must also expose a 2-line `render_<game>_raster` facade in `server/app/renderer/receipt_rasterizer.py`.
- **Exclusive `ThermalBitmap` Rendering (No Pillow/PIL in Plugins)**: Puzzle plugins must render 1-bit rasters exclusively through `ThermalBitmap` (`server/app/renderer/canvas.py`). Never import or branch on `HAS_PILLOW`, `PIL.ImageDraw`, `pil_to_escpos`, or `image_to_escpos_raster` inside `server/app/puzzles/*.py`. Raster graphics must be 576 dots wide, height aligned to 8 dots, with an average thermal duty cycle $\le 35\%$ and no more than 16 consecutive dense rows.

## 7. Arduino IDE Dual-Target Synchronization Standard
Morning Puzzles supports both PlatformIO (`esp32-firmware/`) and native Arduino IDE (`MorningPuzzles/MorningPuzzles.ino`):
- **Mandatory Mirroring**: Whenever any change, fix, generator, or configuration update is made to `esp32-firmware/` (including `include/config.h`, `src/generators/`, `src/printer/`, `src/time/`, or `src/main.cpp`), agents must immediately synchronize the Arduino sketch target so it compiles cleanly out of the box:
  ```bash
  ./scripts/sync_arduino_sketch.sh
  ```
- **Single-Folder Flat Includes**: In `MorningPuzzles/`, all sibling headers must use local flat `#include "Header.h"` rather than directory traversal paths (`../printer/` or `generators/`). The sync script handles this transformation automatically.

## 8. On-Device vs. Off-Device Visual Consistency Standard
All games in Morning Puzzles must deliver identical, pixel-harmonized visual experiences whether printed directly by the ESP32 microcontroller, served by the Python backend, or previewed in the Web Simulator:
- **Strict Tri-Target Parity**: Whenever a game with visual raster generation is created or updated, all three target environments must be implemented with identical geometry:
  1. Python server plugin (`server/app/puzzles/<game>.py`)
  2. ESP32 firmware generator (`esp32-firmware/src/generators/<Game>Gen.cpp`, mirrored to `MorningPuzzles/`)
  3. Web Simulator hardware emulation (`simulator/receipt_simulator.html` via `renderOffline<Game>`)
- **Exact Coordinate & Geometry Alignment**:
  - Canvas width must strictly be 576 dots; height must be aligned to a multiple of 8 dots.
  - Margins, cell sizes, coordinate formulas, and bounding boxes must be identical across Python (`ThermalBitmap`), C++ (`ThermalCanvas`), and JavaScript (`ThermalCanvasSimulator`).
- **Self-Contained Raster Output**:
  - In raster mode, the canvas must encapsulate all puzzle content (borders, inner grid lines, clues/letters, thematic banners, dividers, checkboxes, answer boxes) rather than drawing a partial strip followed by trailing ESC/POS text outside the image.
- **Standardized Typography & Scaling**:
  - Monospaced 5x7 bitmap font must use identical scale multipliers:
    - `scale=2` (10x14px glyph, 12px char width): Banners, headers, clues, instructions, scratchpad labels.
    - `scale=3` (15x21px glyph, 18px char width): Grid letters, Sudoku digits, clue words.
- **Standard Line Thickness Hierarchy**:
  - **4px**: Outer canvas boundary, puzzle grid frame, major 3x3 block borders.
  - **2px**: Secondary boxes, checkboxes, dashed tear lines, handwriting underlines.
  - **1px**: Inner cell dividers, minor grid lines, scratchpad dashed lines.
- **Crisp 1-Bit Geometric Hatching**:
  - Region shading (e.g. `STARS` / Queens) must exclusively use the 10 standard 1-bit geometric hatch patterns (`fillHatch` / `fill_hatch` patterns 0–9). Never use continuous grayscale tones or Floyd-Steinberg dithering for region shading.
- **Canonical Game Symbol & Geometry Decisions**:
  - `TANGO`: Always render `0` and `1` digits (`scale=3`) and `=` / `X` edge markers (`scale=2`) across Python, C++, and Web Simulator—never sun/moon icons or custom vector bars.
  - `BRIDGES`: Always use `padding = 32`, `islandRadius <= 24`, circle `thickness = 2`, and numeral `scale = 2`.
- **Mandatory Visual Parity Testing**:
  - Any new puzzle generator must be registered in `server/visual_comparator_runner.cpp`.
  - The side-by-side comparison suite (`python3 server/test_visual_consistency.py`) must pass with **100.00% bit-for-bit pixel similarity and 100.00% ink IoU overlap** between C++ and Python raster outputs.

## 9. Master Receipt Header & Footer Offline Standards
- **Offline-Safe Master Header**:
  - Centered double rule (`================================================`), followed by bold double-size `MORNING PUZZLES`, followed by generic offline tagline `Enjoy your morning puzzles` (or custom subtitle), and closing double rule (`================================================`).
  - Never require or display real-time clock (NTP/RTC) timestamps on receipts in offline mode.
- **Clean Master Footer**:
  - Separated by single dashed rules (`------------------------------------------------`).
  - Centered closing tagline: `Enjoy your day!`, followed by a blank line and centered setup instructions:
    `To modify settings:`
    `Leave printer on and reset power`
    `via the cable behind the printer.`
  - Zero diagnostics or debug info: Never print hardware status, IP addresses, memory diagnostics, or paper cut debug statements on customer receipts.
- **Mandatory Tri-Target Parity**: Header and footer implementations must remain identical across Python (`DailyReceiptComposer`), ESP32 C++ firmware (`OfflinePuzzleComposer`), Arduino IDE sketch, and Web Simulator (`receipt_simulator.html`).

## 10. Logical Opening Anchors & Curated Deductive Datasets
- **Guaranteed Solvability & Opening Anchors**: Logic puzzles requiring deductive reasoning (`STARS`, and future deduction games) must provide guaranteed logical opening anchors so players never need to guess:
  - Easy/Medium: At least one region of size 1 or 2 (immediate opening deduction).
  - Hard/Extreme: Compact opening anchor regions of size $\le 5$ cells.
- **Curated Datasets vs. Runtime Procedural Generation**: Avoid unanchored, backtrack-heavy procedural generation on microcontrollers to eliminate watchdog timer (WDT) resets and long generation latencies. Use pre-computed, verified datasets stored in `PROGMEM` flash arrays (`*Dataset.h`) on ESP32, mirrored in Python JSON and simulator JS.
- **8-Fold Dihedral Symmetry Invariance**: Replayability is expanded 8-fold via $D_4$ symmetry transformations (4 rotations $\times$ 2 reflections), generating 800 distinct daily layouts per tier from 100 stored base puzzles without extra storage.
- **Deduction Verification Suite**: All deduction datasets must pass automated verification (`python3 server/test_stars_deduction.py`) validating unique solvability, 4-connectivity, and transform invariance.

## 11. Thermal Shading, High-Contrast Cell Badges & Hatching Discipline
- **Prohibition of Solid Black Cells**: Puzzles must never render solid black fill on large grid cells or barrier blocks. Solid fills cause high thermal duty cycle, printhead overheating, and illegible text.
- **Standard 1-Bit Geometric Hatch Shading**: Barrier blocks and shaded territories must use light geometric hatching (Pattern 1, 45° forward diagonal hatch, ~16% duty cycle).
- **Circular White Badge Cutouts for Digits**: When a shaded or hatched cell contains a number (e.g. `LIGHTS`), render a circular white badge cutout (radius $\approx \frac{\text{cell\_size}}{2} - 3$) in the center of the cell and draw crisp black numerals (`scale=3`) inside the badge.
- **Unnumbered Shaded Cells**: Cells without digits retain uniform diagonal hatching without cutouts, cleanly distinguishing them from white corridors.

## 12. Grid Geometry Harmonization & Single-Frame Line Discipline
- **Standard 66px Cell Pitch**: Word boxes and grid cells should harmonize with the standard 8x8 cell pitch ($66 \times 66$ dots based on the 528-dot printable width: $528 \div 8 = 66$).
- **Single-Frame Discipline**: Connected word box arrays must be drawn using a single unified outer frame (`2px`) with internal dividing lines (`1px`). Never draw adjacent independent boxes that share borders, which creates double-drawn, uneven 2px/4px seam lines.
- **Symbol Placement Semantics**: Circle indicators are reserved strictly for clue write-in boxes mapped to final answers; final answer boxes must never contain inner circles.
- **Uniform Row Heights & Box Compression**: Boxes remain 66px squares unless word length exceeds 8 letters ($8 \times 66 = 528$), in which case box widths are compressed proportionally to fit 528px while maintaining uniform row height.
- **Typography Scale**: Primary riddle quotes, clues, or headers use `scale=3` with 28-character line wrapping.
- **Clean Unruled Scratchpad**: Brainstorming areas must provide a generous unruled blank rectangle (192 dots high) free of dashed lines or clutter for handwritten anagramming.

## 13. Clue Margins & Clean Playable Cell Standards
- **Clue-to-Border Margins**: Clues printed outside the grid (e.g. `NONOGRAM` row and column clues) must maintain a minimum 4–6 dot padding from the outer grid border. Numbers must never touch or bleed into the 4px grid frame.
- **Dynamic Multi-Digit Coordinate Offsets**: Coordinate calculations for row/column clues must right-align multi-digit numbers (e.g. "10", "12") with respect to the margin to prevent clipping into outer boundaries.
- **Clean Playable Cells (No Phantom Dots)**: Empty, playable grid cells (in `MINES`, `NONOGRAM`, `TENTS`, `SUDOKU`, `BINARY`, `TANGO`) must remain clean white space. Never draw center guide dots or phantom artifacts that players could confuse with placed symbols or pencil markings.

## 14. Standalone Offline Appliance Standard
- **100% Offline Operation**: The physical ESP32 printer appliance must operate 100% offline. Zero outbound runtime HTTP, NTP, or cloud API calls.
- **Prohibited Client Libraries**: Outbound client libraries (`HTTPClient`, `WiFiClient`, `ArduinoJson`) are prohibited in offline builds.
- **Constrained Wi-Fi Hardware**: Wi-Fi hardware is strictly reserved for local SoftAP captive portal setup (`Morning-Puzzles-Setup`) and local-subnet printer sockets (`PRINTER_MODE_WIFI_TCP`). Point-to-point Ethernet (`PRINTER_MODE_W5500_ETH`) and Serial (`PRINTER_MODE_SERIAL`) modes must compile with zero Wi-Fi dependencies or headers.
- **Trigger Mechanisms**: Receipts must print via local hardware button press, power toggle gesture, or on-device RTC daily cron.

## 15. Single Source of Truth for Curated Datasets
- **Canonical JSON Origin**: All curated puzzle datasets must originate as canonical JSON in `server/data/*.json`.
- **Automated Pipeline Compilation**: C++ PROGMEM headers (`*Dataset.h`) and Web Simulator JS datasets must be compiled from canonical JSON via `tools/datasets/build_all_datasets.py` using the shared top-level `pack_nibbles()` and `update_simulator_js()` helpers.
- **Prohibition of Manual Duplication**: Manual copy-pasting or parallel maintenance of puzzle datasets across targets is strictly prohibited.

## 16. Web Simulator Hardware Emulation Standard
- **Bit-Level Physical Thermal Emulation**: The Web Simulator must provide bit-level physical thermal emulation using `ThermalCanvasSimulator` (576-dot 1-bit raster) for both puzzle boards (`renderOffline<Game>`) and Game Guide visual diagrams (`drawSimGuideCanvas`, matching `OfflinePuzzleComposer::renderGameGuideRaster`).
- **Prohibition of Anti-Aliased Vector Canvas**: HTML5 Canvas 2D vector rendering (`ctx.fillText`, `ctx.strokeRect`, `ctx.arc`, or color emojis) is strictly prohibited on simulated thermal canvases.
- **Offline Appliance Terminology**: Simulator UI terminology must reflect standalone offline appliance concepts.

## 17. Shared Utilities, DRY Primitives & Dynamic Count Standard
- **Python Shared Dataset, $D_4$ & Solution Key Helpers (`server/app/puzzles/base.py`)**:
  - **Dataset Loading**: Always use `load_curated_dataset(filename)` for process-wide cached JSON loading. Never write custom `os.path.join` / `json.load` boilerplate or uncached disk reads in individual puzzle plugins.
  - **$D_4$ Dihedral Transforms**: Always use `select_seeded_d4()`, `transform_grid_d4()`, and `transform_coord_d4()` from `base.py` rather than writing inline rotation/reflection loops.
  - **Default Grid Solution Key**: Standard 2D grid puzzles (`SUDOKU`, `BINARY`, `TANGO`, `KILLER`, `TOWERS`, `INEQUALITY`) must inherit `BasePuzzle.format_solution_key()` (which delegates to `format_grid_solution()`) rather than overriding it with duplicate list comprehensions.
- **ESP32 C++ Shared Nibble Unpacker & Grade Lookup**:
  - Always unpack 4-bit `PROGMEM` nibble arrays via `mp_unpack_nibble_pgm(arr, idx)` in `GeneratorUtils.h` instead of inline `pgm_read_byte` bit-shifting.
  - Always resolve `PuzzleGrade` names via `OfflineConfigManager::getGradeName(grade)`.
- **Dynamic Total Game Counts (`OFFLINE_PUZZLE_TOTAL`)**:
  - Never hardcode the total number of games in C++ log strings—always reference `OFFLINE_PUZZLE_TOTAL`. When adding a new game, update `OFFLINE_PUZZLE_TOTAL`, the range comment in `esp32-firmware/include/config.h`, and the `All Games (N)` label in `simulator/receipt_simulator.html`.

## 18. Game Onboarding, Setup Portal, Documentation & Parity Standard
Every game added to Morning Puzzles must complete the mandatory full-lifecycle onboarding contract before merge:
- **Canonical How-to-Play Rules & Guide Dataset**:
  - Registered in `server/data/game_rules.json` with strict single-word title, one-sentence imperative instruction ($\le 100$ characters, approved verb), objective, 3–4 rules of play, valid/invalid visual move examples with captions, 1–2 opening anchors, and 1–2 FAQs.
  - Generates monospaced ASCII guide (`plugin.format_guide_ascii()`) and 576-dot 1-bit thermal raster guide (`plugin.render_guide_raster(576)`).
  - Automatically compiled to `GameRulesDataset.h`, `docs/GAME_RULES_FAQ.md`, and injected into `portal.html` and `receipt_simulator.html` via `tools/datasets/build_game_rules.py`.
- **SoftAP Setup Portal Inclusion**:
  - Registered in `portal.html`'s `const GAMES = [...]` array with unique sequential `id`, display `name`, and non-empty `desc`.
  - Eligible games checklist renders the game title alongside `.game-desc` and the ℹ️ guide button.
  - Setup portal controls (enable/disable bitmask, "All", "None", and max count stepper) dynamically adapt to `(1 << GAMES.length) - 1`.
  - SoftAP embedded header (`PortalHtml.h`) in `esp32-firmware/src/time/` and `MorningPuzzles/` must be synchronized without uncompiled changes.
- **README.md Inclusion & Count Parity**:
  - Featured in `README.md` under `## 🧩 Featured Games (All N Included)` with updated total count matching the game inventory.
  - Numbered list item formatted as: `N. **Title** *(Aliases)*: [Description]`.
- **Tri-Target Game Description Parity**:
  - The game description displayed on the setup portal (`GAMES[i].desc`) must match the description on `README.md` bit-for-bit (normalized for markdown formatting/backticks).
- **Initial Setup Receipt & Offline Config Name Parity**:
  - Every game added to `OfflinePuzzleType` must be explicitly handled in `OfflineConfigManager::getPuzzleName()` across `esp32-firmware/` and `MorningPuzzles/`.
  - Must return the canonical Title Case game name matching `DEFAULT_REGISTRY` and `portal.html` (e.g. `"Maze"`), never falling back to `default: return "Unknown Puzzle";`.
  - Guarantees clean two-column listing on the initial setup ticket (`WELCOME TO PUZZLES`) and configuration summary receipts printed by `OfflineTimeManager`.
- **Mandatory Pull Request Verification**:
  - All onboarding requirements are enforced by `python3 server/test_game_onboarding.py`, wired into GitHub Actions CI, `run_tests.py` standards tier, and `/pr` pre-flight checks.
