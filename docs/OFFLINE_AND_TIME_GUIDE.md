# 100% Offline & Timekeeping Guide: Morning Puzzles

This guide explains how **Morning Puzzles** operates completely **offline** on the **ESP32**, how to set the time without internet access, and how on-demand puzzle printing works.

---

## 1. Overview of the Offline Architecture

In **Standalone Offline Mode** (`MODE_STANDALONE_OFFLINE`), the ESP32 does not require an external web service, Python server, or internet connection:
*   **On-Chip Generation**: Sudoku, Word Search, Nonogram, Queens / Star Battle, and Jumble are generated directly in native C++ using the ESP32's dual-core 240MHz CPU.
*   **Blazing Speed**: Complete generation of all 5 puzzles takes **under 50 milliseconds**.
*   **Low Memory Footprint**: Uses less than 40KB of RAM (out of 520KB available).
*   **Direct Thermal Printing**: Formatted ESC/POS receipts are streamed directly over Ethernet (port 9100) or Serial to your 80mm commercial printer.

---

## 2. Instant On-Demand Printing (No Time Setup Needed)

If you simply want a fresh puzzle receipt whenever you want:
1. Walk up to the printer.
2. **Short-press the onboard `BOOT` button (GPIO 0)** on the ESP32 (or type `'P'` in the Serial monitor).
3. The ESP32's hardware random number generator (`esp_random()`) immediately creates a unique, randomized instance of all 5 puzzles and prints the 80mm receipt within seconds!

---

## 3. Running Every Morning at 7:00 AM (Offline Time Setting)

Because an ESP32 loses its time when unplugged if no internet connection is available for NTP, we provide two easy ways to set and keep accurate time offline:

### Method A: Wi-Fi SoftAP One-Tap Phone Sync & Settings (Zero Extra Hardware)

You can configure your puzzle preferences and sync the exact clock from your phone in under 30 seconds without an internet connection:

1. **Enter Setup Mode**:
   - **Press and hold the `BOOT` button (GPIO 0) for 2.5 seconds** (or type `'W'` in the Serial monitor).
   - The thermal printer automatically prints a **SETUP MODE** instruction ticket with dual QR codes!
2. **Follow the 3 Ticket Steps**:
   - **Step 1: Scan to Join the Network**: Scan the Wi-Fi QR code (or manually connect to SSID `Morning-Puzzles-Setup` - Open Network, no password).
   - **Step 2: Scan to View Settings**: Scan the URL QR code (or navigate to `http://192.168.4.1`).
   - **Step 3: Choose Games & Settings**: In your browser, pick which games you want, how many to print, your difficulty level, and your daily morning print schedule.
3. **Save & Confirm**:
   - Tap **"Save Settings & Exit Setup"**.
   - The printer immediately prints a **CONFIGURATION SAVED** ticket summarizing all your active settings, the hotspot turns off, and your printer is ready to go!

---

### Method B: Hardware RTC Module (DS3231 - Permanent Set-and-Forget)

If you want the ESP32 to retain accurate time for 5–10 years even across power outages and reboots without ever needing a phone sync:

```
[ ESP32 Dev Board ]               [ DS3231 I2C RTC Module ]
GPIO 21 (SDA)    ───────────────> SDA
GPIO 22 (SCL)    ───────────────> SCL
3.3V             ───────────────> VCC
GND              ───────────────> GND
                                  [ CR2032 Coin Cell ]
```

1. Wire a standard **DS3231 RTC module** (~$2 on Amazon / AliExpress) to I2C pins `GPIO 21 (SDA)` and `GPIO 22 (SCL)`.
2. On boot, the firmware automatically detects the DS3231 on I2C address `0x68` and synchronizes the system clock.
3. When you sync time via the SoftAP phone portal, the firmware automatically writes the new time to the DS3231's battery-backed registers.

---

## 4. Configuration Options (`config.h`)

Open `esp32-firmware/include/config.h` to customize behavior:

```cpp
// 1. Operating Mode
//    MODE_STANDALONE_OFFLINE: 100% on-device C++ generation (Default)
//    MODE_NETWORK_SERVER:     Fetch from Python web service
//    MODE_HYBRID:             Try web service first, fallback to on-device
#define ACTIVE_OPERATION_MODE   MODE_STANDALONE_OFFLINE

// 2. Schedule
#define DAILY_PRINT_HOUR        7       // 7:00 AM
#define DAILY_PRINT_MINUTE      0

// 3. Printer Target
#define PRINTER_IP_ADDR         "192.168.1.150"
#define PRINTER_TCP_PORT        9100
```

---

## 5. Serial Monitor Debug Controls (115200 Baud)

When plugged into your computer via USB:
*   `P` : Trigger instant puzzle generation and print.
*   `W` : Toggle the SoftAP Time Setup Hotspot on/off.
*   `T` : Print a hardware self-test diagnostic ticket.
*   `S` : Display system status (current time, time-sync state, printer IP).
