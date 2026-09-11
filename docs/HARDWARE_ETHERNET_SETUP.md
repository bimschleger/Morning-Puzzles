# Hardware & Ethernet Setup Guide: ESP32 to 80mm Thermal Printer

This guide explains how to connect your **ESP32** to a **commercial 80mm thermal receipt printer** over Ethernet (Port 9100), configure network settings, and troubleshoot printing.

---

## 1. Network Topology

```
                  ┌───────────────────────────────┐
                  │          Wi-Fi Router         │
                  │   DHCP Server: 192.168.1.1    │
                  └───────┬───────────────┬───────┘
                          │ (Wi-Fi)       │ (Ethernet RJ45)
                          ▼               ▼
                  ┌──────────────┐ ┌──────────────────────┐
                  │    ESP32     │ │ Commercial 80mm      │
                  │ Dev Board    │ │ Thermal Printer      │
                  │              │ │ Port 9100 (JetDirect)│
                  │ 192.168.1.55 │ │ 192.168.1.150        │
                  └──────────────┘ └──────────────────────┘
                          │ (HTTP Fetch via Wi-Fi)
                          ▼
                  ┌──────────────┐
                  │ Web Service  │
                  │ Puzzle API   │
                  │ 192.168.1.50 │
                  └──────────────┘
```

1. **Commercial Printer**: Plugged into your router or switch using a standard Ethernet cable (RJ45).
2. **ESP32**: Connects to the local network via its onboard 2.4GHz Wi-Fi.
3. **Communication**: The ESP32 opens a direct TCP socket connection to `PRINTER_IP_ADDR` on **port 9100** (the standard JetDirect / RAW print socket supported by 100% of network thermal printers).

---

## 2. Finding Your Thermal Printer's IP Address

Nearly all commercial 80mm receipt printers (Epson TM-T88, Munbyn, Xprinter, Rongta, Bixolon, Star Micronics) include a built-in hardware self-test:

1. Turn the printer's power switch **OFF**.
2. Press and hold down the **FEED** button on the front of the printer.
3. While still holding the **FEED** button, flip the power switch **ON**.
4. Keep holding the **FEED** button for 2 to 3 seconds until the printer starts printing, then release it.
5. The printer will feed a diagnostic ticket listing:
   - **IP Address** (e.g., `192.168.1.150` or default `192.168.123.100`)
   - **Subnet Mask** (e.g., `255.255.255.0`)
   - **Gateway IP** (e.g., `192.168.1.1`)
   - **MAC Address**

> [!TIP]
> **Factory Default Subnet Mismatch**:
> Some printers come pre-configured with a static IP on a different subnet (e.g., `192.168.123.100`). If your home network uses `192.168.1.x`, you will need to temporarily set your computer's Ethernet adapter to `192.168.123.50`, open the printer's web configuration interface in a browser (`http://192.168.123.100`), and switch it to **DHCP** or an IP matching your network (e.g. `192.168.1.150`). Then assign a DHCP reservation for the printer in your router.

---

## 3. Verifying Printer Port 9100 from your Mac / Terminal

Before flashing the ESP32, you can verify your printer is accepting raw ESC/POS commands across your network directly from your Mac terminal:

```bash
# Check if Port 9100 is open
nc -zv 192.168.1.150 9100

# Print a quick test message directly over Ethernet
printf "\x1b\x40Hello from Ethernet Thermal Printer!\n\n\n\x1d\x56\x42\x03" | nc 192.168.1.150 9100
```
*(Where `192.168.1.150` is your printer's IP address)*. If the printer prints "Hello from Ethernet Thermal Printer!" and cuts the paper, your network printing path is verified!

---

## 4. Configuring the ESP32 Firmware

Open `esp32-firmware/include/config.h` and configure your settings:

```cpp
// 1. Wi-Fi Credentials
#define WIFI_SSID               "YourNetworkName"
#define WIFI_PASSWORD           "YourNetworkPassword"

// 2. Printer Network Target
#define ACTIVE_PRINTER_MODE     PRINTER_MODE_ETHERNET
#define PRINTER_IP_ADDR         "192.168.1.150"       // Match your printer's IP
#define PRINTER_TCP_PORT        9100

// 3. Web Service Host
#define PUZZLE_API_HOST         "192.168.1.50"        // IP of your computer / server
#define PUZZLE_API_PORT         8000
#define PUZZLE_API_PATH         "/api/v1/daily-print"

// 4. Daily Cron Schedule
#define TIMEZONE_SPEC           "CST6CDT,M3.2.0,M11.1.0" // Your POSIX timezone
#define DAILY_PRINT_HOUR        6                        // 6 AM
#define DAILY_PRINT_MINUTE      30                       // 6:30 AM
```

---

## 5. Alternative Serial Fallback (RS-232 vs TTL)

If you ever need to connect via Serial rather than Ethernet:

```
[ ESP32 ]                          [ MAX3232 Transceiver ]              [ Commercial Printer ]
GPIO 17 (TX2) ──> 3.3V TTL ──────> T1IN            T1OUT ──> RS232 ───> Pin 2 (RXD)
GPIO 16 (RX2) <── 3.3V TTL <────── R1OUT            R1IN <── RS232 <─── Pin 3 (TXD)
GND           ───────────────────> GND              GND  ─────────────> Pin 5 (GND)
3V3           ───────────────────> VCC (3.3V)
```

> [!CAUTION]
> **Never wire ESP32 GPIOs directly to a DB9 RS-232 port!** DB9 RS-232 signals use $\pm 3\text{V}$ to $\pm 12\text{V}$, which will permanently destroy the ESP32's 3.3V silicon. Always use a MAX3232 transceiver board for DB9 connections.
