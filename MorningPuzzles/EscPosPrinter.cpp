#include "EscPosPrinter.h"

EscPosPrinter::EscPosPrinter() : 
    _mode(ACTIVE_PRINTER_MODE), 
    _serial(nullptr), 
    _outputStream(nullptr) {
}

EscPosPrinter::~EscPosPrinter() {
    disconnect();
}

bool EscPosPrinter::begin() {
    if (_mode == PRINTER_MODE_SERIAL) {
        _serial = &Serial2;
        _serial->begin(PRINTER_SERIAL_BAUD, SERIAL_8N1, PRINTER_RX_PIN, PRINTER_TX_PIN);
        _outputStream = _serial;
        Serial.printf("[PRINTER] Initialized Serial2 on RX=%d, TX=%d @ %d baud\n", 
                      PRINTER_RX_PIN, PRINTER_TX_PIN, PRINTER_SERIAL_BAUD);
        init();
        return true;
    }
#if (ACTIVE_PRINTER_MODE == PRINTER_MODE_W5500_ETH)
    if (_mode == PRINTER_MODE_W5500_ETH) {
        Serial.println("\n[ETH] Initializing W5500 SPI Ethernet (ESP32-S3-ETH)...");
        Serial.printf("[ETH] Hardware SPI: SCK=%d, MISO=%d, MOSI=%d, CS=%d\n",
                      W5500_SCK_PIN, W5500_MISO_PIN, W5500_MOSI_PIN, W5500_CS_PIN);
        SPI.begin(W5500_SCK_PIN, W5500_MISO_PIN, W5500_MOSI_PIN, W5500_CS_PIN);
        Ethernet.init(W5500_CS_PIN);

        uint8_t mac[6] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
        IPAddress ip, gw, mask, dns;
        ip.fromString(ESP32_STATIC_IP);
        gw.fromString(ESP32_STATIC_GATEWAY);
        mask.fromString(ESP32_STATIC_SUBNET);
        dns.fromString(ESP32_STATIC_DNS);

        Ethernet.begin(mac, ip, dns, gw, mask);
        delay(200);

        Serial.printf("[ETH] W5500 Configured! ESP32 IP: %s | Subnet: %s | Gateway: %s\n",
                      Ethernet.localIP().toString().c_str(), ESP32_STATIC_SUBNET, ESP32_STATIC_GATEWAY);
        Serial.printf("[ETH] Point-to-Point Direct Target Printer: %s:%d\n\n", PRINTER_IP_ADDR, PRINTER_TCP_PORT);
        return true;
    }
#endif
    
    Serial.printf("[PRINTER] Configured for Wi-Fi TCP: %s:%d\n", PRINTER_IP_ADDR, PRINTER_TCP_PORT);
    return true;
}

bool EscPosPrinter::connect() {
    if (_mode == PRINTER_MODE_SERIAL) {
        return true; // Always connected for UART
    }

#if (ACTIVE_PRINTER_MODE == PRINTER_MODE_W5500_ETH)
    if (_mode == PRINTER_MODE_W5500_ETH) {
        if (_ethClient.connected()) {
            return true;
        }

        Serial.printf("[PRINTER] Connecting via W5500 Ethernet to %s:%d...\n", PRINTER_IP_ADDR, PRINTER_TCP_PORT);
        IPAddress targetIP;
        targetIP.fromString(PRINTER_IP_ADDR);
        if (_ethClient.connect(targetIP, PRINTER_TCP_PORT)) {
            _outputStream = &_ethClient;
            Serial.println("[PRINTER] Connected successfully via W5500 direct Ethernet port 9100!");
            init();
            return true;
        }

        Serial.println("[PRINTER] ERROR: Failed to connect to printer via W5500 direct Ethernet.");
        _outputStream = nullptr;
        return false;
    }
#else
    if (_tcpClient.connected()) {
        return true;
    }

    Serial.printf("[PRINTER] Connecting to printer at %s:%d...\n", PRINTER_IP_ADDR, PRINTER_TCP_PORT);
    if (_tcpClient.connect(PRINTER_IP_ADDR, PRINTER_TCP_PORT, PRINTER_CONNECT_TIMEOUT)) {
        _outputStream = &_tcpClient;
        Serial.println("[PRINTER] Connected successfully via TCP port 9100!");
        init();
        return true;
    }

    Serial.println("[PRINTER] ERROR: Failed to connect to printer via TCP port 9100.");
    _outputStream = nullptr;
    return false;
#endif
    return false;
}

void EscPosPrinter::disconnect() {
#if (ACTIVE_PRINTER_MODE == PRINTER_MODE_W5500_ETH)
    if (_mode == PRINTER_MODE_W5500_ETH && _ethClient.connected()) {
        _ethClient.flush();
        _ethClient.stop();
        _outputStream = nullptr;
        Serial.println("[PRINTER] Disconnected W5500 Ethernet socket.");
    }
#else
    if (_mode != PRINTER_MODE_SERIAL && _tcpClient.connected()) {
        _tcpClient.flush();
        _tcpClient.stop();
        _outputStream = nullptr;
        Serial.println("[PRINTER] Disconnected TCP socket.");
    }
#endif
}

bool EscPosPrinter::isConnected() {
    if (_mode == PRINTER_MODE_SERIAL) {
        return (_serial != nullptr);
    }
#if (ACTIVE_PRINTER_MODE == PRINTER_MODE_W5500_ETH)
    return _ethClient.connected();
#else
    return _tcpClient.connected();
#endif
}

bool EscPosPrinter::isPrinterOnline(uint32_t timeoutMs) {
    if (_mode == PRINTER_MODE_SERIAL) {
        return (_serial != nullptr);
    }
#if (ACTIVE_PRINTER_MODE == PRINTER_MODE_W5500_ETH)
    static unsigned long lastSuccessMs = 0;
    static bool wasOnline = false;
    unsigned long now = millis();

    if (_ethClient.connected()) {
        wasOnline = true;
        lastSuccessMs = now;
        return true;
    }
    // Fast physical PHY link check (zero-latency SPI read, ~50 microseconds)
    // When the direct-cabled printer is powered OFF, the link drops immediately!
    if (Ethernet.linkStatus() == LinkOFF) {
        wasOnline = false;
        lastSuccessMs = 0;
        return false;
    }

    // Cache a recent successful probe for up to 1000ms so we do not flood the printer's
    // embedded TCP stack with 5 new TCP connections per second during idle loop polling.
    if (wasOnline && (now - lastSuccessMs < 1000)) {
        return true;
    }

    // PHY link is ON. Probe TCP port 9100 with bounded retransmission (max ~100ms total)
    // to prevent blocking the ESP32 CPU loop if the printer IP is temporarily unreachable.
    uint16_t rtr = (timeoutMs > 0 && timeoutMs < 200) ? timeoutMs : 50;
    Ethernet.setRetransmissionTimeout(rtr);
    Ethernet.setRetransmissionCount(1);

    EthernetClient probe;
    IPAddress targetIP;
    targetIP.fromString(PRINTER_IP_ADDR);
    bool online = probe.connect(targetIP, PRINTER_TCP_PORT);
    if (online) {
        probe.stop();
        wasOnline = true;
        lastSuccessMs = now;
    } else {
        wasOnline = false;
    }

    // Restore standard retransmission parameters for print jobs
    Ethernet.setRetransmissionTimeout(2000);
    Ethernet.setRetransmissionCount(8);

    return online;
#else
    if (_tcpClient.connected()) {
        return true;
    }
    WiFiClient probe;
    if (probe.connect(PRINTER_IP_ADDR, PRINTER_TCP_PORT, timeoutMs)) {
        probe.stop();
        return true;
    }
    return false;
#endif
}

void EscPosPrinter::sendCommand(const uint8_t* cmd, size_t length) {
    if (_outputStream) {
        _outputStream->write(cmd, length);
    }
}

void EscPosPrinter::init() {
    const uint8_t cmd[] = { 0x1B, 0x40 }; // ESC @
    sendCommand(cmd, sizeof(cmd));
}

void EscPosPrinter::setAlign(TextAlignment align) {
    uint8_t val = 0;
    if (align == ALIGN_CENTER) val = 1;
    else if (align == ALIGN_RIGHT) val = 2;
    
    const uint8_t cmd[] = { 0x1B, 0x61, val }; // ESC a n
    sendCommand(cmd, sizeof(cmd));
}

void EscPosPrinter::setBold(bool enable) {
    const uint8_t cmd[] = { 0x1B, 0x45, (uint8_t)(enable ? 1 : 0) }; // ESC E n
    sendCommand(cmd, sizeof(cmd));
}

void EscPosPrinter::setUnderline(uint8_t mode) {
    const uint8_t cmd[] = { 0x1B, 0x2D, mode }; // ESC - n
    sendCommand(cmd, sizeof(cmd));
}

void EscPosPrinter::setInvert(bool enable) {
    const uint8_t cmd[] = { 0x1D, 0x42, (uint8_t)(enable ? 1 : 0) }; // GS B n
    sendCommand(cmd, sizeof(cmd));
}

void EscPosPrinter::setTextSize(uint8_t widthMultiplier, uint8_t heightMultiplier) {
    if (widthMultiplier < 1) widthMultiplier = 1;
    if (widthMultiplier > 8) widthMultiplier = 8;
    if (heightMultiplier < 1) heightMultiplier = 1;
    if (heightMultiplier > 8) heightMultiplier = 8;

    uint8_t n = ((widthMultiplier - 1) << 4) | (heightMultiplier - 1);
    const uint8_t cmd[] = { 0x1D, 0x21, n }; // GS ! n
    sendCommand(cmd, sizeof(cmd));
}

void EscPosPrinter::setFontB(bool enable) {
    const uint8_t cmd[] = { 0x1B, 0x4D, (uint8_t)(enable ? 1 : 0) }; // ESC M n
    sendCommand(cmd, sizeof(cmd));
}

void EscPosPrinter::print(const String& text) {
    if (_outputStream) {
        _outputStream->print(text);
    }
}

void EscPosPrinter::println(const String& text) {
    if (_outputStream) {
        if (text.length() > 0) {
            _outputStream->print(text);
        }
        _outputStream->write(0x0A); // LF
    }
}

void EscPosPrinter::feed(uint8_t lines) {
    const uint8_t cmd[] = { 0x1B, 0x64, lines }; // ESC d n
    sendCommand(cmd, sizeof(cmd));
}

void EscPosPrinter::cut(bool fullCut) {
    // Feed 3 lines then cut
    // GS V m n (m=65 full cut, m=66 partial cut)
    uint8_t cutType = fullCut ? 65 : 66;
    const uint8_t cmd[] = { 0x1D, 0x56, cutType, 0x03 };
    sendCommand(cmd, sizeof(cmd));
}

void EscPosPrinter::printHorizontalLine(char pattern) {
    setAlign(ALIGN_LEFT);
    String line = "";
    for (int i = 0; i < CHARACTERS_PER_LINE_A; i++) {
        line += pattern;
    }
    println(line);
}

void EscPosPrinter::printDoubleLine() {
    printHorizontalLine('=');
}

void EscPosPrinter::printHeader(const String& title, const String& subtitle) {
    setAlign(ALIGN_CENTER);
    printDoubleLine();
    
    setBold(true);
    setTextSize(2, 2);
    println(title);
    
    setTextSize(1, 1);
    setBold(false);
    
    if (subtitle.length() > 0) {
        println(subtitle);
    }
    printDoubleLine();
    setAlign(ALIGN_LEFT);
}

void EscPosPrinter::printKeyValue(const String& key, const String& value, int totalCols) {
    setAlign(ALIGN_LEFT);
    int keyLen = key.length();
    int valLen = value.length();
    int spaces = totalCols - keyLen - valLen;
    
    if (spaces < 1) {
        println(key + " " + value);
        return;
    }
    
    String line = key;
    for (int i = 0; i < spaces; i++) {
        line += ' ';
    }
    line += value;
    println(line);
}

size_t EscPosPrinter::writeRaw(const uint8_t* buffer, size_t size) {
    if (_outputStream && size > 0) {
        return _outputStream->write(buffer, size);
    }
    return 0;
}

void EscPosPrinter::printRasterBitmap(const uint8_t* bitmapData, uint16_t widthDots, uint16_t heightDots) {
    if (!_outputStream || !bitmapData) return;

    // Width must be rounded up to bytes (8 bits per byte)
    uint16_t widthBytes = (widthDots + 7) / 8;
    
    // Standard ESC/POS GS v 0 command:
    // Format: 0x1D, 0x76, 0x30, m, xL, xH, yL, yH, [data...]
    // m = 0 (normal density)
    uint8_t xL = widthBytes & 0xFF;
    uint8_t xH = (widthBytes >> 8) & 0xFF;
    uint8_t yL = heightDots & 0xFF;
    uint8_t yH = (heightDots >> 8) & 0xFF;

    const uint8_t header[] = {
        0x1D, 0x76, 0x30, 0x00,
        xL, xH, yL, yH
    };

    sendCommand(header, sizeof(header));
    
    // Stream data in chunks to prevent network socket / UART buffer overflow
    size_t totalBytes = (size_t)widthBytes * heightDots;
    size_t chunkSize = 512;
    size_t sent = 0;

    while (sent < totalBytes) {
        size_t toSend = (chunkSize < totalBytes - sent) ? chunkSize : (totalBytes - sent);
        _outputStream->write(bitmapData + sent, toSend);
        sent += toSend;
        delay(2); // Gentle flow-control pacing
    }

    feed(1);
}

void EscPosPrinter::printSelfTest(const String& ipAddress, const String& currentTimeStr) {
    if (!connect()) return;

    init();
    printHeader("MORNING PUZZLES", "Thermal Printer Diagnostic Test");
    
    println("");
    setBold(true);
    println("SYSTEM STATUS:");
    const char* ifaceName = (_mode == PRINTER_MODE_W5500_ETH) ? "Direct W5500 RJ45 (Port 9100)" : 
                            ((_mode == PRINTER_MODE_SERIAL) ? "Serial UART2" : "Wi-Fi TCP (Port 9100)");
    printKeyValue("Interface:", ifaceName);
    printKeyValue("ESP32 IP:", ipAddress);
    printKeyValue("Printer Target:", String(PRINTER_IP_ADDR) + ":" + String(PRINTER_TCP_PORT));
    printKeyValue("Date & Time:", currentTimeStr);
    printKeyValue("Paper Width:", String(PAPER_WIDTH_MM) + "mm (80mm)");
    printKeyValue("Printable Area:", String(PRINTABLE_WIDTH_DOTS) + " dots (72mm)");
    
    println("");
    setBold(true);
    println("TYPOGRAPHY & STYLES:");
    setBold(false);
    println("Standard Font A (48 columns per line):");
    println("123456789012345678901234567890123456789012345678");
    printHorizontalLine('.');
    
    setFontB(true);
    println("Condensed Font B (64 columns per line):");
    println("1234567890123456789012345678901234567890123456789012345678901234");
    setFontB(false);
    printHorizontalLine('.');

    setBold(true);
    println("Text Formatting: Bold active");
    setBold(false);
    setUnderline(1);
    println("Text Formatting: Underline active");
    setUnderline(0);

    setInvert(true);
    setAlign(ALIGN_CENTER);
    println(" INVERTED WHITE-ON-BLACK BANNER ");
    setInvert(false);
    setAlign(ALIGN_LEFT);

    println("");
    printHorizontalLine('=');
    setAlign(ALIGN_CENTER);
    println("Printer self-test successful!");
    println("Ready to fetch and print daily puzzles.");
    printHorizontalLine('=');

    feed(3);
    cut(false); // Partial cut
    disconnect();
}
