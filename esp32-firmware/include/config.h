#ifndef CONFIG_H
#define CONFIG_H

#include <Arduino.h>

// =============================================================================
// MORNING PUZZLES - CONFIGURATION
// =============================================================================

// -----------------------------------------------------------------------------
// 1. Operating Mode
// -----------------------------------------------------------------------------
// Supported modes:
//   1 = STANDALONE OFFLINE (All puzzles generated 100% on ESP32, zero server needed)
//   2 = NETWORK SERVER     (Fetches pre-rendered puzzles from remote API)
//   3 = HYBRID             (Tries network server first; falls back to on-device generation)
#define MODE_STANDALONE_OFFLINE 1
#define MODE_NETWORK_SERVER     2
#define MODE_HYBRID             3
#define ACTIVE_OPERATION_MODE   MODE_STANDALONE_OFFLINE

// -----------------------------------------------------------------------------
// 2. Daily Cron Schedule Settings (Every morning at 7:00 AM)
// -----------------------------------------------------------------------------
#define DAILY_PRINT_HOUR        7       // 7:00 AM
#define DAILY_PRINT_MINUTE      0

// Timezone string (for NTP/POSIX time sync)
#define TIMEZONE_SPEC           "CST6CDT,M3.2.0,M11.1.0"
#define NTP_SERVER_PRIMARY      "pool.ntp.org"
#define NTP_SERVER_BACKUP       "time.nist.gov"

// -----------------------------------------------------------------------------
// 3. Printer Interface Settings
// -----------------------------------------------------------------------------
#define PRINTER_MODE_ETHERNET   1
#define PRINTER_MODE_SERIAL     2
#define ACTIVE_PRINTER_MODE     PRINTER_MODE_ETHERNET

// Ethernet Printer Settings (Raw JetDirect Port 9100 on 80mm commercial printers)
#define PRINTER_IP_ADDR         "192.168.1.150"
#define PRINTER_TCP_PORT        9100
#define PRINTER_CONNECT_TIMEOUT 5000

// Serial Fallback Settings (UART2)
#define PRINTER_SERIAL_BAUD     115200
#define PRINTER_RX_PIN          16
#define PRINTER_TX_PIN          17

// -----------------------------------------------------------------------------
// 4. Wi-Fi & Web Service Settings (Used in Network / Hybrid Modes)
// -----------------------------------------------------------------------------
#define WIFI_SSID               "YOUR_WIFI_SSID"
#define WIFI_PASSWORD           "YOUR_WIFI_PASSWORD"
#define WIFI_CONNECT_TIMEOUT_MS 15000

#define PUZZLE_API_HOST         "192.168.1.50"
#define PUZZLE_API_PORT         8000
#define PUZZLE_API_PATH         "/api/v1/daily-print"
#define PUZZLE_API_KEY          ""

// -----------------------------------------------------------------------------
// 5. Hardware Pins & User Interaction
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
