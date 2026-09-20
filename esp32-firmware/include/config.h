#ifndef CONFIG_H
#define CONFIG_H

#include <Arduino.h>

// =============================================================================
// MORNING PUZZLES - CONFIGURATION
// =============================================================================

// -----------------------------------------------------------------------------
// 1. Operating Mode (100% Standalone Offline Appliance)
// -----------------------------------------------------------------------------
#define OFFLINE_ONLY_BUILD      1       // 1 = Strip all outbound network/API client code

// -----------------------------------------------------------------------------
// 2. On-Demand Puzzle Grade & Difficulty Configuration
// -----------------------------------------------------------------------------
#define OFFLINE_PUZZLE_COUNT        5       // Number of random games to select and print (1-16)
// 0 = Easy, 1 = Medium, 2 = Hard, 3 = Rotating (advances grade on each button press)
#define PUZZLE_GRADE_DEFAULT        3       // Default: Rotating grade on button press
#define PUZZLE_GRADE_CYCLE_ON_PRESS true    // Each hardware button press advances grade

// -----------------------------------------------------------------------------
// 2B. Print Presentation Style (Offline Appliance)
// -----------------------------------------------------------------------------
// STYLE_HYBRID = 1  (Text headers + on-device 1-bit raster graphics boards)
// STYLE_ASCII  = 2  (Classic monospaced ASCII text grids)
#define STYLE_HYBRID                1
#define STYLE_ASCII                 2
#define OFFLINE_PRINT_STYLE         STYLE_HYBRID

// -----------------------------------------------------------------------------
// 3. Daily Cron Schedule Settings (Default: Every morning at 7:00 AM)
// -----------------------------------------------------------------------------
#define DAILY_PRINT_ENABLED_DEFAULT  true    // Daily recurring schedule active by default
#define DAILY_PRINT_HOUR_DEFAULT     7       // Default 7:00 AM
#define DAILY_PRINT_MINUTE_DEFAULT   0

// Backward-compatible fallback aliases
#define DAILY_PRINT_HOUR             DAILY_PRINT_HOUR_DEFAULT
#define DAILY_PRINT_MINUTE           DAILY_PRINT_MINUTE_DEFAULT

// Timezone string (for internal POSIX time sync)
#define TIMEZONE_SPEC           "CST6CDT,M3.2.0,M11.1.0"

// -----------------------------------------------------------------------------
// 4. Printer Interface Settings
// -----------------------------------------------------------------------------
// Supported interface modes:
//   1 = PRINTER_MODE_WIFI_TCP   (Wi-Fi station connecting to printer across home router)
//   2 = PRINTER_MODE_SERIAL     (Direct UART2 serial jumper wires to pins 16 & 17)
//   3 = PRINTER_MODE_W5500_ETH  (Direct SPI W5500 RJ45 Ethernet cable, e.g. ESP32-S3-ETH board)
#define PRINTER_MODE_WIFI_TCP   1
#define PRINTER_MODE_SERIAL     2
#define PRINTER_MODE_W5500_ETH  3
#define PRINTER_MODE_ETHERNET   PRINTER_MODE_W5500_ETH  // Backward compatibility alias

// Active mode: set to PRINTER_MODE_W5500_ETH for direct cable connection on ESP32-S3-ETH
#define ACTIVE_PRINTER_MODE     PRINTER_MODE_W5500_ETH

// Target Printer IP & Port (Raw JetDirect Port 9100 on 80mm commercial printers)
// Factory default static IP for Munbyn, Xprinter, Vretti, Rongta is 192.168.123.100
#define PRINTER_IP_ADDR         "192.168.123.100"
#define PRINTER_TCP_PORT        9100
#define PRINTER_CONNECT_TIMEOUT 5000

// W5500 Hardware SPI Pins (ESP32-S3-ETH Dev Board Pinout)
#define W5500_CS_PIN            14
#define W5500_MOSI_PIN          11
#define W5500_MISO_PIN          12
#define W5500_SCK_PIN           13
#define W5500_RST_PIN            9
#define W5500_INT_PIN           10

// Point-to-Point Direct Static IP Settings for ESP32 (matches printer 192.168.123.x subnet)
#define ESP32_STATIC_IP         "192.168.123.50"
#define ESP32_STATIC_GATEWAY    "192.168.123.1"
#define ESP32_STATIC_SUBNET     "255.255.255.0"
#define ESP32_STATIC_DNS        "192.168.123.1"

// -----------------------------------------------------------------------------
// 4B. Power Switch Gestures & Automatic Print Triggers (Zero-Button Operation)
// -----------------------------------------------------------------------------
// 1. SETUP MODE: Turn printer ON first, then plug in ESP32.
//    ESP32 detects printer is already online at boot (<500ms probe) and launches
//    the SoftAP configuration portal ('Morning-Puzzles-Setup') and prints the QR setup ticket.
// 2. ON-DEMAND PRINT: While ESP32 is running, flip printer switch OFF, wait 1-2s, then ON.
//    ESP32 detects the printer power-on transition and prints a fresh puzzle bundle.
// 3. SCHEDULED CRON: Leave both ON. Operates quietly until daily scheduled print time.
// 4. POWER OUTAGE RECOVERY: Simultaneous power restore causes printer to take ~2-3s to boot,
//    so ESP32 detects simultaneous boot, skips setup mode, and quietly waits for scheduled time.
#define SETUP_MODE_ON_PRINTER_ONLINE_BOOT true // Enter setup mode if printer is already online at ESP32 boot
#define PRINTER_BOOT_PROBE_WINDOW_MS   500     // Settle window (<500ms) to distinguish printer-already-on vs simultaneous boot
#define AUTO_PRINT_ON_BOOT             false   // Normal cold boots stay quiet and wait for scheduled daily cron
#define AUTO_PRINT_ON_PRINTER_POWER    true    // Print on-demand when printer switch is flipped OFF then ON
#define PRINTER_POLL_INTERVAL_MS       200     // Background probe interval to sense power-on & rapid toggles
#define PRINTER_READY_SETTLE_MS        2000    // Settle time for thermal head homing and motor boot
#define PRINTER_OFFLINE_DEBOUNCE_MS    1000    // Continuous offline time required before confirming power-off (1s)
#define PRINTER_POST_PRINT_COOLDOWN_MS 15000   // Refractory cooldown after print job before new auto-prints

// Serial Fallback Settings (UART2)
#define PRINTER_SERIAL_BAUD     115200
#define PRINTER_RX_PIN          16
#define PRINTER_TX_PIN          17

// -----------------------------------------------------------------------------
// 5. Wi-Fi Network Settings
// -----------------------------------------------------------------------------
// Required only when ACTIVE_PRINTER_MODE is PRINTER_MODE_WIFI_TCP so the ESP32
// can connect to your router and reach the printer over TCP port 9100.
#define WIFI_SSID               "YOUR_WIFI_SSID"
#define WIFI_PASSWORD           "YOUR_WIFI_PASSWORD"
#define WIFI_CONNECT_TIMEOUT_MS 15000

// -----------------------------------------------------------------------------
// 6. Hardware Pins & User Interaction
// -----------------------------------------------------------------------------
// Built-in BOOT button on standard ESP32 boards (GPIO 0, active LOW)
//   - Short press (< 2.5s): Instantly generates and prints active configured puzzle mix!
//   - Long press (>= 2.5s): Launches SoftAP setup portal ("Morning-Puzzles-Setup") + prints QR slip
#define BUTTON_TRIGGER_PIN      0
#define BUTTON_LONG_PRESS_MS    2500    // Hold >= 2.5s to enter Wi-Fi Setup Mode
#define BUTTON_DEBOUNCE_MS      50      // 50ms button debounce

// Built-in status LED (GPIO 2 on most ESP32 DevKit modules)
#define STATUS_LED_PIN          2

// 80mm thermal receipt physical constants
#define PAPER_WIDTH_MM          80
#define PRINTABLE_WIDTH_DOTS    576     // 72mm @ 203 DPI = 576 dots
#define CHARACTERS_PER_LINE_A   48      // Standard Font A (12x24 dots)
#define CHARACTERS_PER_LINE_B   64      // Condensed Font B (9x17 dots)

#endif // CONFIG_H
