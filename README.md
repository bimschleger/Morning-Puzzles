# Morning Puzzles 📰🧩

An automated physical morning puzzle dispenser using an **ESP32** connected to a commercial **80mm thermal receipt printer** over Ethernet (Port 9100) or Serial UART.

Supports both **100% On-Device Offline Operation** (all puzzles generated on the ESP32 chip in C++) and **Network/Hybrid Operation** with a Python backend!

---

## 🌟 Key Features

1. **100% Standalone Offline Mode**: All 5 puzzle types are generated in native C++ directly on the ESP32 in **<50 milliseconds** with zero cloud or server dependencies.
2. **On-Demand Printing**: Walk up to the printer and tap the onboard `BOOT` button (GPIO 0) at any time to instantly generate and print a brand-new, randomized daily puzzle receipt!
3. **Daily Scheduled Print at 7:00 AM**:
   * **One-Tap Phone Sync (Offline)**: Hold the `BOOT` button for 3 seconds to launch a local hotspot (`Morning-Puzzles-Setup`). Open `http://192.168.4.1` on your phone to sync time in 1 tap!
   * **Optional DS3231 RTC Module**: Automatic battery-backed hardware timekeeping across power cycles.
   * **Internet NTP (Online/Hybrid)**: Automatically syncs time via SNTP when connected to Wi-Fi.
4. **Commercial 80mm ESC/POS Printing**: Streams formatted 576-dot receipts directly over Ethernet (TCP Port 9100) or Serial UART, with automatic paper cutting.
5. **All Open-Source (Apache 2.0)**:
   * **Sudoku**: Backtracking solver with mathematical unique solution guarantee.
   * **Word Search**: Dynamic 12x12 matrix with embedded themes (Morning, Nature, Space, Animals, Tech).
   * **Nonogram / Picross**: 5x5, 8x8, and 10x10 grids with row/column clues.
   * **Queens / Star Battle**: 1-Star (LinkedIn Queens style) and 2-Star variations with contiguous region partitioning.
   * **Daily Jumble**: 4 scrambled words with circled letters spelling out the answer to a punchline riddle.

---

## Project Structure

```
Morning-Puzzles/
├── esp32-firmware/                 # ESP32 C++ firmware (PlatformIO & Arduino IDE)
│   ├── platformio.ini              # PlatformIO configuration (esp32dev)
│   ├── include/config.h            # Operating mode, schedule, printer IP, and Wi-Fi
│   ├── src/
│   │   ├── main.cpp                # App loop, on-demand button, 7:00 AM cron
│   │   ├── generators/             # Native C++ puzzle generators (100% Offline)
│   │   │   ├── SudokuGen.cpp
│   │   │   ├── WordSearchGen.cpp
│   │   │   ├── NonogramGen.cpp
│   │   │   ├── QueensGen.cpp
│   │   │   ├── JumbleGen.cpp
│   │   │   └── OfflinePuzzleComposer.cpp
│   │   ├── time/                   # Offline time management & SoftAP portal
│   │   │   ├── OfflineTimeManager.h
│   │   │   └── OfflineTimeManager.cpp
│   │   ├── printer/                # 80mm ESC/POS driver (TCP socket & Serial)
│   │   ├── scheduler/              # Online NTP cron scheduler
│   │   └── net/                    # HTTP streaming client
│   └── test/                       # Native C++ test runner
├── server/                         # Optional Python Web Service API & Renderer
│   ├── app/
│   │   ├── main.py                 # FastAPI & standalone HTTP server
│   │   ├── generators/             # Python Apache-2.0 puzzle generators
│   │   └── renderer/               # 80mm ESC/POS layout & 1-bit rasterizer
│   ├── requirements.txt
│   └── run_server.py               # Single-command launcher
└── docs/
    ├── OFFLINE_AND_TIME_GUIDE.md   # Complete guide for offline operation & time setting
    ├── HARDWARE_ETHERNET_SETUP.md  # Port 9100 configuration & IP discovery guide
    └── APACHE_2_PUZZLE_LIBRARIES.md# Deep-dive on Apache 2.0 puzzle algorithms
```

---

## Quick Start (100% Offline Mode)

### 1. Configure the Firmware
Open `esp32-firmware/include/config.h`:
* Set `PRINTER_IP_ADDR` to your printer's IP (e.g. `192.168.1.150` — see [Hardware Guide](docs/HARDWARE_ETHERNET_SETUP.md)).
* Verify `ACTIVE_OPERATION_MODE` is set to `MODE_STANDALONE_OFFLINE`.
* Set your desired morning print time (default `DAILY_PRINT_HOUR = 7`, `DAILY_PRINT_MINUTE = 0`).

### 2. Flash the ESP32
* **Using PlatformIO**:
  ```bash
  cd esp32-firmware
  pio run -t upload && pio device monitor -b 115200
  ```
* **Using Arduino IDE**:
  Open `esp32-firmware/src/main.cpp`, select your ESP32 board, and click Upload.

### 3. Print & Set Time
* **Print on Demand**: Short-press the onboard **`BOOT`** button (GPIO 0) at any time to instantly generate and print a fresh, randomized puzzle receipt!
* **Set Time for 7:00 AM Cron**: Hold the **`BOOT`** button for 3 seconds. Connect your phone to `Morning-Puzzles-Setup` (password `puzzles123`), visit `http://192.168.4.1`, and tap **"Sync Time from This Phone"**!

---

## Documentation
* [**Offline & Timekeeping Guide**](docs/OFFLINE_AND_TIME_GUIDE.md): Full walkthrough of on-device generation, SoftAP time setting, and DS3231 RTC.
* [**Hardware & Ethernet Setup Guide**](docs/HARDWARE_ETHERNET_SETUP.md): Commercial printer Port 9100 discovery, IP settings, and wiring.
* [**Apache 2.0 Puzzle Libraries Reference**](docs/APACHE_2_PUZZLE_LIBRARIES.md): Algorithms, benchmarks, and upstream repositories.

---

## License
All code and puzzle generators in this repository are licensed under the **Apache License, Version 2.0**.
