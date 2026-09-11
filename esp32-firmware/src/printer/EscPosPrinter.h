#ifndef ESC_POS_PRINTER_H
#define ESC_POS_PRINTER_H

#include <Arduino.h>
#include <WiFi.h>
#include <WiFiClient.h>
#include <HardwareSerial.h>
#include "config.h"

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

    // Basic ESC/POS Formatting
    void init();
    void setAlign(TextAlignment align);
    void setBold(bool enable);
    void setUnderline(uint8_t mode = 1);  // 0=off, 1=1-dot, 2=2-dot
    void setInvert(bool enable);
    void setTextSize(uint8_t widthMultiplier = 1, uint8_t heightMultiplier = 1); // 1 to 8
    void setFontB(bool enable);           // true = Font B (64 chars/line), false = Font A (48 chars/line)

    // Printing primitives
    void print(const String& text);
    void println(const String& text = "");
    void feed(uint8_t lines = 1);
    void cut(bool fullCut = false);

    // Decorative / Receipt elements
    void printHorizontalLine(char pattern = '-');
    void printDoubleLine();
    void printHeader(const String& title, const String& subtitle = "");
    void printKeyValue(const String& key, const String& value, int totalCols = 48);

    // Raw byte stream & Raster Graphics
    size_t writeRaw(const uint8_t* buffer, size_t size);
    void printRasterBitmap(const uint8_t* bitmapData, uint16_t widthDots, uint16_t heightDots);

    // Diagnostic Self Test
    void printSelfTest(const String& ipAddress, const String& currentTimeStr);

private:
    uint8_t _mode;
    WiFiClient _tcpClient;
    HardwareSerial* _serial;
    Print* _outputStream;

    void sendCommand(const uint8_t* cmd, size_t length);
};

#endif // ESC_POS_PRINTER_H
