# Hardware & Device Setup Guide: Step-by-Step

This comprehensive guide walks you through setting up a brand-new 80mm commercial thermal receipt printer and ESP32 microcontroller for **Pen and Paper Puzzles**, from initial unboxing to everyday morning prints.

---

## 🧰 What You Need

1. **80mm Thermal Receipt Printer with Ethernet (RJ-45)** (e.g., vretti USB+LAN, Munbyn ITPP047, Rongta RP326, or Epson TM-T20III/TM-T88).
2. **LilyGO T-ETH-Lite ESP32-S3** (or Olimex ESP32-EVB) with onboard RJ-45 Ethernet jack and USB-C.
3. **Cat5e or Cat6 Ethernet patch cable** (0.5 ft – 3 ft).
4. **USB-C cable** and a standard 5V USB wall phone charger (1A or higher).
5. **80mm thermal receipt paper roll** (standard BPA-free direct thermal paper).

> [!WARNING]
> **Ethernet / LAN Port Required**: Ensure your thermal printer includes an **RJ-45 Ethernet** port on the back. USB-only or Bluetooth-only models cannot connect directly to the ESP32.

---

## Step 1: Unbox and Run Printer Self-Test (Find Factory IP)

Commercial receipt printers include a built-in hardware diagnostic test that prints their factory network configuration:

1. Load an 80mm thermal paper roll into the printer (ensure the thermal side faces the printhead).
2. Connect the printer's 24V power adapter to the wall and to the printer's DC barrel jack.
3. **Press and hold the FEED button** on the front of the printer.
4. While continuing to hold **FEED**, flip the printer's power switch **ON**.
5. Keep holding **FEED** for 2 to 3 seconds until printing begins, then release it.
6. The printer will feed a self-test diagnostic slip:
   ```text
   *** SELF TEST ***
   IP Address:    192.168.123.100   <-- Note this IP!
   Subnet Mask:   255.255.255.0
   TCP Port:      9100
   ```
   *(Most vretti, Munbyn, Rongta, and Xprinter units come pre-configured to `192.168.123.100`)*.

---

## Step 2: Configure Firmware Settings

Open [`esp32-firmware/include/config.h`](../esp32-firmware/include/config.h) on your computer:

* **Verify Printer IP**: Ensure `PRINTER_IP_ADDR` matches the IP address printed on your self-test slip:
  ```cpp
  #define PRINTER_IP_ADDR         "192.168.123.100"
  #define PRINTER_TCP_PORT        9100
  ```
* **Verify Zero-Button Power Triggers**: Confirm default gesture actions:
  ```cpp
  #define SETUP_MODE_ON_PRINTER_ONLINE_BOOT true // Enter setup mode if printer is ON at ESP32 boot
  #define AUTO_PRINT_ON_PRINTER_POWER    true    // Print on-demand when printer switch is flipped OFF then ON
  #define AUTO_PRINT_ON_BOOT             false   // Cold boots stay quiet and wait for scheduled daily cron
  ```

---

## Step 3: Flash the ESP32 from Mac or PC

Connect your LilyGO T-ETH-Lite ESP32-S3 board to your computer using a USB-C data cable. You can upload using either the **Arduino IDE** GUI or the **PlatformIO** CLI:

### Option A: Arduino IDE (Recommended GUI)
1. Open Arduino IDE and go to **File $\rightarrow$ Open...**.
2. Select [`PenAndPaperPuzzles/PenAndPaperPuzzles.ino`](../PenAndPaperPuzzles/PenAndPaperPuzzles.ino).
3. Select your board (**ESP32S3 Dev Module** for LilyGO T-ETH-Lite, or **ESP32 Dev Module** for standard boards) and your USB serial port (`/dev/cu.usbmodem...` on Mac or `COMx` on Windows).
4. Under **Tools $\rightarrow$ Partition Scheme**, select **"Huge APP (3MB No OTA / 1MB SPIFFS)"**.
5. Click the **Upload** arrow button ($\rightarrow$).
6. Upload is complete when the console displays `Hard resetting via RTS pin...`.

### Option B: PlatformIO (VS Code / Command Line)
```bash
cd esp32-firmware
pio run -t upload
```

Once the upload completes, disconnect the ESP32 from your computer.

---

## Step 4: Direct Point-to-Point Physical Wiring

Connect the ESP32 directly to the printer using a standard Ethernet cable—no home router, network switch, or Wi-Fi required:

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
2. Plug the other end directly into the printer's RJ-45 jack (Auto-MDIX handles polarity automatically).
3. Plug the 5V USB wall charger into the ESP32's USB-C port.
4. Ensure the printer's 24V adapter is plugged into the wall and printer.

---

## Step 5: First-Time Setup Portal & Everyday Use

Pen and Paper Puzzles is designed to tuck away inside an enclosure or sit discreetly behind your printer without needing physical pushbuttons:

### 1. Initial Setup Mode
* Turn the printer **ON**.
* Plug in (or power cycle) the ESP32.
* Because the printer is detected online at startup, the ESP32 automatically prints a dual-QR setup slip and creates a temporary Wi-Fi network named `Pen-And-Paper-Puzzles`.
* Connect to `Pen-And-Paper-Puzzles` on your phone (or scan the QR code) to open the setup portal.
* In the portal, you can:
  * Sync device time to your phone's clock with one tap.
  * Set your preferred daily morning print time (e.g., 7:00 AM).
  * Choose how many puzzles print in each edition.
  * Set puzzle difficulty (Easy, Medium, Hard, or Mixed).
  * Select which of the 20 puzzle types are eligible to print.
* Save your settings; the device returns to silent scheduled operation.

### 2. Scheduled Daily Morning Prints
* Leave both the printer and ESP32 powered **ON**.
* The device operates silently in the background and prints your fresh puzzle bundle every morning at the scheduled time, cleanly auto-cutting the paper.

### 3. On-Demand Extra Prints Anytime
* Whenever you want an extra set of puzzles, simply flip the printer's power switch **OFF**, wait 3 seconds, and flip it back **ON**.
* The ESP32 detects the printer re-connecting and prints a fresh, randomized edition within 2 seconds.
* On-demand prints are independent and never cancel or alter your scheduled morning prints!

### 4. Smart Power-Outage Protection
* If household power blips or both devices are switched on at the exact same time from a shared power strip, the printer takes 2–3 seconds to initialize motors and network hardware.
* Because the printer is not online during the ESP32's initial 500ms boot window, the ESP32 recognizes simultaneous startup, skips Setup Mode, stays quiet, and waits for scheduled prints without waking you up.

### 5. Hardware Button Fallback (Optional)
* The onboard `BOOT` button on the ESP32 (GPIO 0) remains active:
  * **Short tap (< 1 sec)**: Prints an on-demand puzzle edition.
  * **Long press (> 2.5 sec)**: Toggles Setup Mode on and off.
* An external arcade-style pushbutton can optionally be connected across `GPIO 4` and `GND`.
