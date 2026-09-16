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

// Supported modes:
//   1 = STANDALONE OFFLINE (All 7 puzzles generated 100% on ESP32, zero server needed)
//   2 = NETWORK SERVER     (Legacy: fetches pre-rendered puzzles from remote API)
//   3 = HYBRID             (Legacy: tries network server first; falls back to on-device generation)
#define MODE_STANDALONE_OFFLINE 1
#define MODE_NETWORK_SERVER     2
#define MODE_HYBRID             3
#define ACTIVE_OPERATION_MODE   MODE_STANDALONE_OFFLINE

// -----------------------------------------------------------------------------
// 2. On-Demand Puzzle Grade & Difficulty Configuration
// -----------------------------------------------------------------------------
#define OFFLINE_PUZZLE_COUNT        5       // Number of random games to select and print (1-12)
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
// 3. Daily Cron Schedule Settings (Every morning at 7:00 AM)
// -----------------------------------------------------------------------------
#define DAILY_PRINT_HOUR        7       // 7:00 AM
#define DAILY_PRINT_MINUTE      0

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
// 4B. Automatic Print Triggers (Zero-Button Operation)
// -----------------------------------------------------------------------------
#define AUTO_PRINT_ON_BOOT             true    // Print automatically once when ESP32 boots up
#define AUTO_PRINT_ON_PRINTER_POWER    true    // Print automatically when printer switch is turned ON
#define PRINTER_POLL_INTERVAL_MS       200     // Background probe interval to sense power-on & rapid toggles
#define PRINTER_READY_SETTLE_MS        2000    // Settle time for thermal head homing and motor boot

// Serial Fallback Settings (UART2)
#define PRINTER_SERIAL_BAUD     115200
#define PRINTER_RX_PIN          16
#define PRINTER_TX_PIN          17

// -----------------------------------------------------------------------------
// 5. Wi-Fi Network Settings
// -----------------------------------------------------------------------------
// Required when ACTIVE_PRINTER_MODE is PRINTER_MODE_ETHERNET so the ESP32
// can connect to your router and reach the printer over TCP port 9100.
#define WIFI_SSID               "YOUR_WIFI_SSID"
#define WIFI_PASSWORD           "YOUR_WIFI_PASSWORD"
#define WIFI_CONNECT_TIMEOUT_MS 15000

#define PUZZLE_API_HOST         "192.168.1.50"
#define PUZZLE_API_PORT         8000
#define PUZZLE_API_PATH         "/api/v1/daily-print"
#define PUZZLE_API_KEY          ""

// -----------------------------------------------------------------------------
// 6. Hardware Pins & User Interaction
// -----------------------------------------------------------------------------
// Built-in BOOT button on standard ESP32 boards (GPIO 0, active LOW)
//   - Short press (< 1.5s): Instantly generates and prints a random puzzle set!
//   - Long press (> 3.0s):  Launches SoftAP time-sync portal ("Morning-Puzzles-Setup")
#define BUTTON_TRIGGER_PIN      0

// Built-in status LED (GPIO 2 on most ESP32 DevKit modules)
#define STATUS_LED_PIN          2

// 80mm thermal receipt physical constants
#define PAPER_WIDTH_MM          80
#define PRINTABLE_WIDTH_DOTS    576     // 72mm @ 203 DPI = 576 dots
#define CHARACTERS_PER_LINE_A   48      // Standard Font A (12x24 dots)
#define CHARACTERS_PER_LINE_B   64      // Condensed Font B (9x17 dots)

#endif // CONFIG_H
