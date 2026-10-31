# Pen and Paper Puzzles 📰🧩

An automated physical morning puzzle dispenser that generates randomized, fresh puzzle editions and prints them to a commercial **80mm thermal receipt printer** with automatic paper cutting.

Runs **100% On-Device and Offline** on an **ESP32** in native C++ with zero cloud or internet dependencies, with an optional Python backend and interactive web simulator!

---

## 🌟 Key Features

* **100% Fully Offline**: No accounts, usernames, passwords, cloud subscriptions, or internet connection required. Runs completely self-contained on an ESP32 microcontroller with zero network dependencies.
* **Scheduled Daily Morning Delivery**: Wake up to fresh, procedurally generated puzzles waiting in the printer tray every morning at your chosen time, cleanly auto-cut and ready for your morning coffee.
* **On-Demand Fresh Prints**: Want another batch of puzzles anytime? Simply flip the printer power switch off and on (or tap the button) to instantly print an extra edition without disturbing your morning schedule.
* **Simple Phone Setup Portal**: Connect your phone directly to the device's setup Wi-Fi hotspot to sync time and customize your daily print schedule, how many puzzles to print, difficulty level, and which games are included.
* **Commercial Thermal Printing**: Uses standard 80mm commercial receipt printers with automatic paper cutting—meaning zero ink, zero toner ribbons, whisper-fast prints, and pennies per roll.

---

## 🧩 Featured Games (All 20 Included)

Every print job generates a randomized, unique daily edition featuring all 20 open-source (Apache 2.0 / MIT) puzzle types conforming to strict presentation standards:

1. **Sudoku**: Fill every row, column, and 3x3 box with digits 1-9 without repeating.
2. **Search** *(Word Search)*: Find all hidden words horizontally, vertically, or diagonally.
3. **Nonogram** *(Picross)*: Shade cells to match row and column run counts with at least one blank between runs.
4. **Stars** *(Queens / Star Battle)*: Place stars in every row, column, and outlined region without touching, even diagonally.
5. **Jumble**: Unscramble each clue word, then use the circled letters to solve the final pun.
6. **Binary** *(Takuzu / Binairo)*: Fill every cell with 0 or 1 so no more than two identical numbers are adjacent.
7. **Mines** *(Minesweeper Deduction)*: Deduce all hidden mines using numbers showing how many adjacent cells contain mines.
8. **Tents** *(Tents & Trees)*: Pitch tents beside trees; no tents may touch even diagonally, matching row/column quotas.
9. **Bridges** *(Hashiwokakero)*: Connect islands with up to two orthogonal bridges matching numbers into one network.
10. **Killer** *(Killer Sudoku)*: Fill the grid with digits so cages sum to their clue without repeating digits.
11. **Cryptogram**: Deduce the hidden quotation where each letter is consistently substituted with another.
12. **Tango**: Fill grid with 0s and 1s so equal symbols match and opposite symbols differ.
13. **Ladder** *(Word Ladder / Doublets)*: Deduce words changing one letter at a time to transform start word into end word.
14. **Wheel** *(Word Wheel / Target Anagram)*: Find words of 4+ letters using the wheel letters, always including the center letter.
15. **Lights** *(Akari / Light Up)*: Place bulbs to light corridors without facing each other; numbers show how many bulbs share an edge.
16. **Loop** *(Slitherlink / Fences)*: Draw a single continuous closed loop around numbers indicating surrounding line count.
17. **Towers** *(Skyscrapers)*: Place building heights so edge clues match how many towers are visible in that line.
18. **Inequality** *(Futoshiki)*: Fill grid with digits so each digit appears once per line and inequality signs hold.
19. **Maze** *(Labyrinth)*: Draw a path from the entrance to the exit without crossing any walls.
20. **Sudokito** *(Mini Sudoku)*: Fill every row, column, and 2x3 box with digits 1-6 without repeating.

> [!NOTE]
> All puzzle presentation formatting (single-word uppercase titles, $\le 100$-character one-sentence descriptions, centered difficulty placement, and 48-column ASCII solution keys) strictly adheres to [`docs/PUZZLE_HEADER_SPEC.md`](docs/PUZZLE_HEADER_SPEC.md), [`docs/PUZZLE_DESCRIPTION_GUIDELINES.md`](docs/PUZZLE_DESCRIPTION_GUIDELINES.md), and [`docs/PUZZLE_SOLUTION_KEY_SPEC.md`](docs/PUZZLE_SOLUTION_KEY_SPEC.md), verified by `python3 server/test_puzzle_standards.py`.

---

## 🖨️ What This Prints To (Hardware Target)

This system is engineered specifically for **commercial 80mm (3 1/8") direct thermal receipt printers** equipped with an **RJ-45 Ethernet / LAN port**:

* **Supported & Recommended Models**:
  * **vretti 80mm Thermal Receipt Printer (USB + LAN version)** (~$55–$75, budget favorite)
  * **Munbyn ITPP047 (Ethernet version)** (~$90–$110, reliable restaurant workhorse)
  * **Rongta RP326 (Ethernet version)** (~$65–$80)
  * **Epson TM-T20III or TM-T88 series (Ethernet)** (~$150–$200, industrial standard)
* **Printhead Specifications**:
  * **Paper Roll**: 80 mm (3 1/8 in) wide thermal paper (BPA-free).
  * **Printhead Width**: 72 mm active print line (flanked by 4mm physical paper borders).
  * **Resolution**: 203.2 DPI (8 dots/mm) $\rightarrow$ **strictly 576 dots per line**.
  * **Cutting**: Automatic partial cutter (`GS V 66 3`) with 4-line pre-cut feed margin.
  * **Communication**: Raw TCP socket on **Port 9100** (JetDirect).

> [!WARNING]
> **Port Verification**: When purchasing your thermal printer, verify that the listing includes **Ethernet / LAN / RJ-45**. Do not purchase USB-only or Bluetooth-only models, as they lack the physical network jack required for the direct cable connection.

---

## 🛠️ Quick Start & Everyday Use

### What You Need
1. **80mm Thermal Receipt Printer with Ethernet** (e.g., vretti USB+LAN).
2. **LilyGO T-ETH-Lite ESP32-S3** (or Olimex ESP32-EVB) with onboard RJ-45 jack and USB-C.
3. **Cat5e or Cat6 Ethernet patch cable** (0.5 ft – 3 ft).
4. **USB-C cable** and a standard 5V USB wall phone charger.
5. **80mm thermal paper roll**.

👉 **For complete unboxing, diagnostic self-test, firmware flashing (Arduino IDE & PlatformIO), and direct-cable wiring, see the [Step-by-Step Hardware Setup Guide](docs/HARDWARE_SETUP_GUIDE.md).**

### Everyday Controls
Once set up, Pen and Paper Puzzles operates seamlessly without needing you to touch any micro-buttons:
* **Setup Mode**: Plug in the ESP32 while the printer is ON $\rightarrow$ Senses printer online, prints a dual-QR setup slip, and opens the local `Pen-And-Paper-Puzzles` Wi-Fi portal on your phone to configure daily print time, puzzle count, difficulty, and game selection.
* **Scheduled Daily Prints**: Leave both devices ON $\rightarrow$ Operates silently in the background and prints your fresh puzzle bundle every morning at your configured time.
* **On-Demand Extra Prints**: Flip the printer's power switch OFF, wait 3 seconds, then flip it ON $\rightarrow$ Prints an instant, fresh randomized edition anytime.

---

## 📁 Project Structure & Testing

<details>
<summary><b>📁 Project Structure</b> (click to expand)</summary>

```
pen-and-paper-puzzles/
├── esp32-firmware/                 # 100% Offline C++ ESP32 Firmware
│   ├── platformio.ini              # PlatformIO configuration
│   ├── include/config.h            # Network, static IPs, pins, auto-print triggers
│   ├── src/
│   │   ├── main.cpp                # App loop, power-on detection, button handling
│   │   ├── generators/             # Native C++ puzzle engines (<50ms generation)
│   │   │   ├── SudokuGen.cpp
│   │   │   ├── WordSearchGen.cpp
│   │   │   ├── NonogramGen.cpp
│   │   │   ├── QueensGen.cpp
│   │   │   ├── JumbleGen.cpp
│   │   │   ├── BinaryGen.cpp
│   │   │   ├── MinesGen.cpp
│   │   │   └── OfflinePuzzleComposer.cpp
│   │   ├── printer/                # 80mm ESC/POS driver (Port 9100 TCP & Serial)
│   │   │   ├── EscPosPrinter.h
│   │   │   └── EscPosPrinter.cpp
│   │   └── time/                   # Offline time management & SoftAP portal
│   └── test/                       # Native C++ test runner
├── server/                         # Python Backend Service & Rasterizer
│   ├── app/
│   │   ├── main.py                 # FastAPI & standalone HTTP server
│   │   ├── puzzles/                # Modular puzzle plugins (BasePuzzle)
│   │   └── renderer/
│   │       ├── receipt_rasterizer.py# 576-dot 1-bit rasterizer & duty cycle checker
│   │       └── text_formatter.py   # Hybrid ESC/POS receipt builder
│   ├── test_thermal_format.py      # Automated 80mm format & duty cycle test suite
│   └── requirements.txt
├── simulator/
│   └── receipt_simulator.html      # Interactive browser-based thermal simulator
└── docs/
    ├── HARDWARE_SETUP_GUIDE.md     # Step-by-step unboxing, flashing & wiring guide
    ├── THERMAL_80MM_PRINT_GUIDE.md # Master 80mm engineering specification & guide
    ├── PUZZLE_HEADER_SPEC.md       # Visual header & instruction standards
    ├── THERMAL_DRAWING_SPEC.md     # 1-bit hatching patterns & stroke tokens
    ├── HARDWARE_ETHERNET_SETUP.md  # Port 9100 network discovery & wiring
    └── OFFLINE_AND_TIME_GUIDE.md   # Offline timekeeping & RTC configuration
```

</details>

<details>
<summary><b>🧪 Testing & Verification</b> (click to expand)</summary>

* **Automated 80mm Thermal Receipt Format Verification**:
  ```bash
  python3 server/test_thermal_format.py
  ```
  *Tests 576-dot width, 72-byte row alignment, GS v 0 raster encoding, duty cycle thermal safety ($\le 35\%$), and cutter commands across all games.*

* **Game Onboarding, Setup Portal & Presentation Standards**:
  ```bash
  python3 server/test_game_onboarding.py
  python3 server/test_puzzle_standards.py
  ```

* **Tri-Target Visual Consistency Verification**:
  ```bash
  python3 server/test_visual_consistency.py
  ```

* **Native ESP32 C++ Puzzle Generation Test**:
  ```bash
  clang++ -std=c++17 -Iesp32-firmware/test -Iesp32-firmware/include \
    esp32-firmware/test/test_offline_generators.cpp -o esp32-firmware/test/test_offline && \
    ./esp32-firmware/test/test_offline && rm esp32-firmware/test/test_offline
  ```

</details>

---

## 📚 Technical Reference Documentation

* [**Step-by-Step Hardware & Device Setup Guide**](docs/HARDWARE_SETUP_GUIDE.md): Unboxing, factory IP discovery, ESP32 flashing (Arduino IDE & PlatformIO), direct Ethernet wiring, and power gestures.
* [**80mm Thermal Receipt Printer Master Guide**](docs/THERMAL_80MM_PRINT_GUIDE.md): Complete engineering specification covering 576-dot raster geometry, peak current management, 35% duty cycle limits, cutter offset mechanics, and ESC/POS protocol commands.
* [**Puzzle Presentation & Header Specification**](docs/PUZZLE_HEADER_SPEC.md): Single-word titles, standardized difficulty tags, and canonical one-sentence gameplay rules.
* [**Thermal Drawing & 1-Bit Hatching Specification**](docs/THERMAL_DRAWING_SPEC.md): 4-tier stroke hierarchy and 8 deterministic geometric hatching algorithms for shading on physical thermal heads.

---

## 📜 License

All code and puzzle generators in this repository are licensed under the **Apache License, Version 2.0**.
