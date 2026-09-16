# Morning Puzzles 📰🧩

An automated physical morning puzzle dispenser that generates randomized, fresh puzzle editions and prints them to a commercial **80mm thermal receipt printer** with automatic paper cutting.

Runs **100% On-Device and Offline** on an **ESP32** in native C++ with zero cloud or internet dependencies, with an optional Python backend and interactive web simulator!

---

## 🌟 Key Features

* **100% Standalone & Air-Gapped**: All 16 puzzle algorithms run locally on the ESP32 microcontroller in **<50 milliseconds**. No Wi-Fi, no cloud subscriptions, and no external servers required.
* **Zero-Button Power Gestures**: Completely eliminates the need for exposed buttons. Use standard power switches for all everyday actions:
  * **Setup Mode**: Leave printer ON, plug in ESP32 $\rightarrow$ Senses printer online, prints dual-QR setup slip, and opens web setup portal.
  * **On-Demand Print**: Flip printer switch OFF, wait 3s, then ON $\rightarrow$ Prints a fresh puzzle bundle immediately.
  * **Scheduled Daily Prints**: Leave both ON $\rightarrow$ Operates silently in the background until your configured morning print time.
* **Smart Power-Outage Protection**: If household power blips or both devices power on together, the ESP32 detects simultaneous startup, stays quiet, and waits for scheduled prints without printing in the middle of the night.
* **Targeted for 80mm Commercial Receipt Printers**: Designed for standard 80mm receipt rolls at 203 DPI (**576 dots per line / 72 bytes per scanline**), using standard ESC/POS protocol (`GS v 0`), safe thermal duty cycles ($\le 35\%$), and automatic partial cutting.
* **Optional RTC & 1-Click Phone Time Sync**: Built-in SoftAP web portal syncs clock from your phone in 1 click, with optional battery-backed DS3231 I2C RTC support for power-loss resilience.

---

## 🧩 Featured Games (All 16 Included)

Every print job generates a randomized, unique daily edition featuring all 16 open-source (Apache 2.0 / MIT) puzzle types conforming to strict presentation standards:

1. **Sudoku**: 9x9 grid with standard 3x3 block hierarchy, generated with a backtracking solver mathematically guaranteed to have exactly one unique solution.
2. **Search** *(Word Search)*: Dynamic letter matrix with randomized hidden words (horizontal, vertical, diagonal) across curated themes (Morning, Space, Animals, Nature, Tech), complete with checkbox tracking. Theme-driven with no difficulty line.
3. **Nonogram** *(Picross)*: Deductive picture logic grids (5x5, 8x8, 10x10) with row and column clue numbers.
4. **Stars** *(Queens / Star Battle)*: LinkedIn Queens & 2-Star Battle format with irregular contiguous region partitioning where no two stars touch, even diagonally.
5. **Jumble**: 4 scrambled clue words with circled letter positions, ruled handwriting scratchpad lines, and a punchline riddle to solve.
6. **Binary** *(Takuzu / Binairo)*: 0 and 1 logic puzzle with strict adjacency rules (no two consecutive identical symbols) and equal row/column parity.
7. **Mines** *(Minesweeper Deduction)*: 100% deductive, guess-free minefield with adjacent mine count clues and total mine counter.
8. **Tents** *(Tents & Trees)*: Bipartite matching puzzle where each tree is paired with a tent next to it, tents never touch even diagonally, and margin numbers indicate line totals.
9. **Bridges** *(Hashiwokakero)*: Connect numbered circular islands with horizontal and vertical single/double bridges to form a single continuous spanning network without crossings.
10. **Killer** *(Killer Sudoku)*: Cage-sum deduction puzzle (4x4 on Easy/Medium, 6x6 on Extreme) combining Latin-square non-repeating digits with dashed cage arithmetic sums.
11. **Cryptogram**: Monoalphabetic substitution cipher featuring famous quotes, riddles, and proverbs with letter hint scaffolding.
12. **Tango**: Sun and Moon parity logic grid with edge equality (`=`) and opposite (`x`) constraints.
13. **Ladder** *(Word Ladder / Doublets)*: Deduce intermediate words linking a start word to a target word, changing exactly one letter per step.
14. **Wheel** *(Word Wheel / Target Anagram)*: 7-letter hexagonal honeycomb anagram challenge requiring words formed with a mandatory center letter and a 7-letter pangram.
15. **Lights** *(Akari / Light Up)*: Line-of-sight illumination puzzle placing light bulbs to light up all corridors without shining on one another or exceeding wall clue limits.
16. **Loop** *(Slitherlink / Fences)*: Loop deduction drawing a single continuous closed circuit where cell numbers indicate the exact number of surrounding loop segments.

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

## 🛠️ Step-by-Step: Setting Up a New Printer & Device

Follow this straightforward guide to get a brand-new printer and ESP32 out of the box and printing in minutes.

### What You Need:
1. **80mm Thermal Receipt Printer with Ethernet** (e.g. vretti USB+LAN).
2. **LilyGO T-ETH-Lite ESP32-S3** (or Olimex ESP32-EVB) with onboard RJ-45 jack and USB-C.
3. **Cat5e or Cat6 Ethernet patch cable** (0.5 ft – 3 ft).
4. **USB-C cable** and a standard 5V USB wall phone charger.
5. **80mm thermal paper roll**.

---

### Step 1: Unbox and Run Printer Self-Test (Find Factory IP)

1. Load an 80mm thermal paper roll into the printer (ensure thermal side faces the printhead).
2. Plug the printer's 24V power brick into the wall and connect it to the printer's DC jack.
3. **Hold down the FEED button** on the front of the printer.
4. While still holding **FEED**, flip the printer's power switch **ON**.
5. Keep holding **FEED** for 2 to 3 seconds until the printer starts printing, then release it.
6. The printer will feed a diagnostic self-test slip displaying its network settings:
   ```text
   *** SELF TEST ***
   IP Address:    192.168.123.100   <-- Note this IP!
   Subnet Mask:   255.255.255.0
   TCP Port:      9100
   ```
   *(Most vretti, Munbyn, and Rongta printers ship pre-configured to `192.168.123.100`)*.

---

### Step 2: Configure Firmware

Open [`esp32-firmware/include/config.h`](esp32-firmware/include/config.h) on your computer:
* **Check Printer IP**: Ensure `PRINTER_IP_ADDR` matches the IP from your self-test slip (pre-set to `"192.168.123.100"`):
  ```cpp
  #define PRINTER_IP_ADDR         "192.168.123.100"
  #define PRINTER_TCP_PORT        9100
  ```
* **Verify Zero-Button Power Settings**: Confirm power gesture triggers in `config.h`:
  ```cpp
  #define SETUP_MODE_ON_PRINTER_ONLINE_BOOT true // Enter setup mode if printer is ON at ESP32 boot
  #define AUTO_PRINT_ON_PRINTER_POWER    true    // Print on-demand when printer switch is flipped OFF then ON
  #define AUTO_PRINT_ON_BOOT             false   // Cold boots stay quiet and wait for scheduled daily cron
  ```

---

### Step 3: Flash the ESP32 from your Mac / PC

1. Connect the LilyGO T-ETH-Lite board to your Mac or PC using a standard USB-C data cable.
2. Upload the firmware using **Arduino IDE** or **PlatformIO**:
   * **Using Arduino IDE (Recommended GUI)**:
     1. Open Arduino IDE and select **File $\rightarrow$ Open...**
     2. Choose `MorningPuzzles/MorningPuzzles.ino`.
     3. Select your board (**ESP32S3 Dev Module** for LilyGO T-ETH-Lite or **ESP32 Dev Module** for standard boards) and your USB port (`/dev/cu.usbmodem...` or `/dev/cu.usbserial-...`).
     4. Under **Tools $\rightarrow$ Partition Scheme**, select **"Huge APP (3MB No OTA / 1MB SPIFFS)"**.
     5. Click the **Upload** arrow button ($\rightarrow$).
     6. Upload is complete when the console displays `Hard resetting via RTS pin...` with verified hashes.
   * **Using PlatformIO (Command Line / VS Code)**:
     ```bash
     cd esp32-firmware
     pio run -t upload
     ```
3. Once the upload finishes, unplug the board from your computer.

---

### Step 4: Direct Point-to-Point Physical Wiring

Connect the devices directly together—no router, switch, or Wi-Fi network needed:

```text
 ┌───────────────────────────┐                ┌───────────────────────────┐
 │       ESP32 Board         │                │   80mm Thermal Printer    │
 │   (LilyGO T-ETH-Lite)     │                │   (vretti / Munbyn)       │
 │                           │                │                           │
 │   [USB-C Port] (5V Power) │                │   [24V DC Jack] (Wall)    │
 │                           │                │                           │
 │   [RJ-45 Jack] ───────────┼────────────────┼──> [RJ-45 Jack]           │
 │        │                  │ Ethernet Patch │   (Static: 192.168.123.100│
 │   [BOOT Button] (Onboard) │ Cable (Cat5e)  └───────────────────────────┘
 └───────────────────────────┘
```

1. Plug one end of the Ethernet cable into the ESP32's RJ-45 jack.
2. Plug the other end directly into the printer's RJ-45 jack (Auto-MDIX automatically routes the connection).
3. Plug the 5V USB phone charger into the ESP32's USB-C port.
4. Ensure the printer's 24V adapter is plugged in.

---

### Step 5: Everyday Controls & Daily Use (Zero-Button Gestures)

Morning Puzzles is designed to be tucked away inside an enclosure behind or underneath your printer. You never need to touch the micro-sized `BOOT` button on the board:

1. **Initial Setup (or Re-Entering Setup Mode)**:
   * Leave the printer **ON**.
   * Plug in (or unplug and replug) the ESP32 power cable.
   * Because the printer is already online at boot, the ESP32 immediately launches the `Morning-Puzzles-Setup` Wi-Fi hotspot and prints the dual-QR setup slip.
   * Scan the QR code with your phone to choose your games, puzzle count, difficulty, and daily morning print time.
2. **Daily Scheduled Morning Prints**:
   * Leave both the printer and ESP32 **ON**.
   * The appliance operates silently in the background and prints fresh puzzles every day at your scheduled time (e.g. 7:00 AM), cutting the paper automatically.
3. **On-Demand Extra Prints Anytime**:
   * With the ESP32 powered, flip the printer's power switch **OFF**, wait 3 seconds, then flip it **ON**.
   * Within 2 seconds of settling, the ESP32 prints a fresh puzzle mix following your settings.
   * On-demand prints are independent and never cancel or interfere with your scheduled morning prints!
4. **Power Outage & Simultaneous Power Recovery**:
   * If household power drops or both devices are switched on together from a shared power strip, the printer takes 2–3 seconds to initialize motors and network PHY.
   * Because the printer is offline during the ESP32's initial 500ms boot window, the ESP32 recognizes simultaneous power restoration, skips Setup Mode, stays quiet, and waits for scheduled prints.
5. **Developer & External Button Fallback**:
   * The onboard `BOOT` button on GPIO 0 remains functional for bench testing (short press = on-demand print, hold $\ge 2.5\text{s}$ = toggle setup portal).
   * If you prefer a big physical arcade button, you can wire a microswitch to `GND` and `GPIO 4`.

---

## 📁 Project Structure

```
Morning-Puzzles/
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
│   │   ├── generators/             # Python puzzle generators
│   │   └── renderer/
│   │       ├── receipt_rasterizer.py# 576-dot 1-bit rasterizer & duty cycle checker
│   │       └── text_formatter.py   # Hybrid ESC/POS receipt builder
│   ├── test_thermal_format.py      # Automated 80mm format & duty cycle test suite
│   └── requirements.txt
├── simulator/
│   └── receipt_simulator.html      # Interactive browser-based thermal simulator
└── docs/
    ├── THERMAL_80MM_PRINT_GUIDE.md # Master 80mm engineering specification & guide
    ├── PUZZLE_HEADER_SPEC.md       # Visual header & instruction standards
    ├── THERMAL_DRAWING_SPEC.md     # 1-bit hatching patterns & stroke tokens
    ├── HARDWARE_ETHERNET_SETUP.md  # Port 9100 network discovery & wiring
    └── OFFLINE_AND_TIME_GUIDE.md   # Offline timekeeping & RTC configuration
```

---

## 🧪 Testing & Verification

* **Automated 80mm Thermal Receipt Format Verification**:
  ```bash
  python3 server/test_thermal_format.py
  ```
  *Tests 576-dot width, 72-byte row alignment, GS v 0 raster encoding, duty cycle thermal safety ($\le 35\%$), and cutter commands across all 9 games.*

* **Native ESP32 C++ Puzzle Generation Test**:
  ```bash
  clang++ -std=c++17 -Iesp32-firmware/test -Iesp32-firmware/include \
    esp32-firmware/test/test_offline_generators.cpp -o esp32-firmware/test/test_offline && \
    ./esp32-firmware/test/test_offline && rm esp32-firmware/test/test_offline
  ```

---

## 📚 Technical Reference Documentation

* [**80mm Thermal Receipt Printer Master Guide**](docs/THERMAL_80MM_PRINT_GUIDE.md): Complete engineering specification covering 576-dot raster geometry, peak current management, 35% duty cycle limits, cutter offset mechanics, and ESC/POS protocol commands.
* [**Puzzle Presentation & Header Specification**](docs/PUZZLE_HEADER_SPEC.md): Single-word titles, standardized difficulty tags, and canonical one-sentence gameplay rules.
* [**Thermal Drawing & 1-Bit Hatching Specification**](docs/THERMAL_DRAWING_SPEC.md): 4-tier stroke hierarchy and 8 deterministic geometric hatching algorithms for shading on physical thermal heads.

---

## 📜 License

All code and puzzle generators in this repository are licensed under the **Apache License, Version 2.0**.
