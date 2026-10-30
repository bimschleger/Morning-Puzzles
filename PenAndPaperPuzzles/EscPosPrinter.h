#ifndef ESC_POS_PRINTER_H
#define ESC_POS_PRINTER_H

#include "config.h"

#if (ACTIVE_PRINTER_MODE == PRINTER_MODE_W5500_ETH)
#include <SPI.h>
#include <Ethernet.h>
#elif (ACTIVE_PRINTER_MODE == PRINTER_MODE_WIFI_TCP)
#include <WiFi.h>
#include <WiFiClient.h>
#endif
#include <HardwareSerial.h>

enum TextAlignment {
    ALIGN_LEFT   = 0,
    ALIGN_CENTER = 1,
    ALIGN_RIGHT  = 2
};

class EscPosPrinter {
public:
    EscPosPrinter();
    ~EscPosPrinter();

    // Lifecycle
    bool begin();
    bool connect();
    void disconnect();
    bool isConnected();
    bool isPrinterOnline(uint32_t timeoutMs = 300);

    // Basic ESC/POS Formatting
    virtual void init();
    virtual void setAlign(TextAlignment align);
    virtual void setBold(bool enable);
    virtual void setUnderline(uint8_t mode = 1);  // 0=off, 1=1-dot, 2=2-dot
    virtual void setInvert(bool enable);
    virtual void setTextSize(uint8_t widthMultiplier = 1, uint8_t heightMultiplier = 1); // 1 to 8
    virtual void setFontB(bool enable);           // true = Font B (64 chars/line), false = Font A (48 chars/line)

    // Printing primitives
    virtual void print(const String& text);
    virtual void println(const String& text = "");
    virtual void print(const char* text);
    virtual void println(const char* text = "");
    virtual void feed(uint8_t lines = 1);
    virtual void cut(bool fullCut = false);

    // Decorative / Receipt elements
    virtual void printHorizontalLine(char pattern = '-');
    virtual void printDoubleLine();
    virtual void printHeader(const String& title, const String& subtitle = "");
    virtual void printKeyValue(const String& key, const String& value, int totalCols = 48);

    // Raw byte stream & Raster Graphics
    virtual size_t writeRaw(const uint8_t* buffer, size_t size);
    virtual void printRasterBitmap(const uint8_t* bitmapData, uint16_t widthDots, uint16_t heightDots);

    // Diagnostic Self Test
    void printSelfTest(const String& ipAddress, const String& currentTimeStr);

private:
    uint8_t _mode;
#if (ACTIVE_PRINTER_MODE == PRINTER_MODE_W5500_ETH)
    EthernetClient _ethClient;
#elif (ACTIVE_PRINTER_MODE == PRINTER_MODE_WIFI_TCP)
    WiFiClient _tcpClient;
#endif
    HardwareSerial* _serial;
    Print* _outputStream;

    void sendCommand(const uint8_t* cmd, size_t length);
};

#endif // ESC_POS_PRINTER_H
