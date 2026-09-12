# Morning Puzzles 📰🧩

An automated physical morning puzzle dispenser that generates randomized, fresh puzzle editions and prints them to a commercial **80mm thermal receipt printer** with automatic paper cutting.

Runs **100% On-Device and Offline** on an **ESP32** in native C++ with zero cloud or internet dependencies, with an optional Python backend and interactive web simulator!

---

## 🌟 Key Features

* **100% Standalone & Air-Gapped**: All 9 puzzle algorithms run locally on the ESP32 microcontroller in **<50 milliseconds**. No Wi-Fi, no cloud subscriptions, and no external servers required.
* **Auto-Print on Startup / Power-On**: Flip your printer's power switch ON in the morning, and the dispenser automatically senses the printer, generates a brand-new randomized edition, prints the receipt, and cuts the paper.
* **On-Demand Extra Copies with On-Device Button**: Need another copy or want a different difficulty tier? Simply press the onboard **`BOOT`** button (or an external arcade button) on the device to immediately generate and print a fresh set!
* **Targeted for 80mm Commercial Receipt Printers**: Designed for standard 80mm receipt rolls at 203 DPI (**576 dots per line / 72 bytes per scanline**), using standard ESC/POS protocol (`GS v 0`), safe thermal duty cycles ($\le 35\%$), and automatic partial cutting.
* **Optional Daily 7:00 AM Cron Timer**: Supports scheduled daily morning printing via an offline phone sync web portal (hold `BOOT` for 3 seconds) or battery-backed DS3231 RTC module.

---

## 🧩 Featured Games (All 9 Included)

Every print job generates a randomized, unique daily edition featuring all 9 open-source (Apache 2.0 / MIT) puzzle types:

1. **Sudoku**: 9x9 grid with standard 3x3 block hierarchy, generated with a backtracking solver mathematically guaranteed to have exactly one unique solution.
2. **Search (Word Search)**: Dynamic 12x12 letter matrix with randomized hidden words (horizontal, vertical, diagonal) across curated themes (Morning, Space, Animals, Nature, Tech), complete with checkbox tracking.
3. **Nonogram (Picross)**: Deductive picture logic grids (5x5, 8x8, 10x10) with row and column clue numbers.
4. **Stars (Queens / Star Battle)**: LinkedIn Queens & 2-Star Battle format with irregular contiguous region partitioning where no two stars touch, even diagonally.
5. **Jumble**: 4 scrambled clue words with circled letter positions, ruled handwriting scratchpad lines, and a punchline riddle to solve.
6. **Binary (Takuzu / Binairo)**: 0 and 1 logic puzzle with strict adjacency rules (no three in a row) and equal row/column parity.
7. **Mines (Minesweeper Deduction)**: 100% deductive, guess-free minefield with adjacent mine count clues and total mine counter.
8. **Tents (Tents & Trees)**: Bipartite matching puzzle where each tree is paired with an orthogonally adjacent tent, tents never touch even diagonally, and margin numbers indicate line totals.
9. **Bridges (Hashiwokakero)**: Connect numbered circular islands with horizontal and vertical single/double bridges to form a single continuous spanning network without crossings.

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
* **Verify Auto-Print Settings**: Confirm startup and power-on printing are active:
  ```cpp
  #define AUTO_PRINT_ON_BOOT             true   // Print when ESP32 powers up
  #define AUTO_PRINT_ON_PRINTER_POWER    true   // Print when printer switch turns ON
  ```

---

### Step 3: Flash the ESP32 from your Mac / PC

1. Connect the LilyGO T-ETH-Lite board to your Mac or PC using a standard USB-C data cable.
2. Upload the firmware using **PlatformIO** or **Arduino IDE**:
   * **Using PlatformIO (Command Line or VS Code)**:
     ```bash
     cd esp32-firmware
     pio run -t upload
     ```
   * **Using Arduino IDE**:
     Open `esp32-firmware/src/main.cpp`, select your ESP32 board, and click the **Upload** arrow.
3. Once the upload finishes (typically 10–15 seconds), unplug the board from your computer.

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

### Step 5: Test & Use!

1. **Automatic Print on Power-ON**:
   * Flip the printer's power switch **ON**.
   * The green/yellow Ethernet link LEDs will light up.
   * Within 2 seconds, the ESP32 senses the printer, generates a randomized daily edition, streams the 576-dot receipt, and cuts the paper automatically!
2. **Print Extra Copies Anytime (On-Device Button)**:
   * With the printer on, short-press the small **`BOOT`** button located right on the ESP32 board.
   * A brand-new randomized edition prints immediately!
3. **Optional External Slam Button**:
   * If you prefer a big arcade button, connect 2 jumper wires between the arcade microswitch terminals and the ESP32's `GND` and `GPIO 4` pins (zero soldering needed).

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
