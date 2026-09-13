#ifndef THERMAL_CANVAS_H
#define THERMAL_CANVAS_H

#include <Arduino.h>

class EscPosPrinter;

#define THERMAL_CANVAS_WIDTH       576
#define THERMAL_CANVAS_WIDTH_BYTES 72   // 576 / 8

class ThermalCanvas {
public:
    ThermalCanvas();
    ~ThermalCanvas();

    // Buffer lifecycle
    bool begin(uint16_t heightDots);
    void end();
    void clear(uint8_t color = 0);

    bool isValid() const { return _buffer != nullptr && _height > 0; }
    uint16_t getWidth() const { return THERMAL_CANVAS_WIDTH; }
    uint16_t getHeight() const { return _height; }
    uint8_t* getBuffer() const { return _buffer; }
    size_t getBufferSize() const { return (size_t)THERMAL_CANVAS_WIDTH_BYTES * _height; }

    // Drawing Primitives
    void setPixel(int16_t x, int16_t y, uint8_t color = 1);
    void drawHLine(int16_t x, int16_t y, int16_t w, uint8_t thickness = 1, uint8_t color = 1);
    void drawVLine(int16_t x, int16_t y, int16_t h, uint8_t thickness = 1, uint8_t color = 1);
    void drawRect(int16_t x, int16_t y, int16_t w, int16_t h, uint8_t thickness = 1, uint8_t color = 1);
    void fillRect(int16_t x, int16_t y, int16_t w, int16_t h, uint8_t color = 1);
    void fillHatch(int16_t x, int16_t y, int16_t w, int16_t h, uint8_t patternId);

    // Circles
    void drawCircle(int16_t cx, int16_t cy, int16_t radius, uint8_t thickness = 2, uint8_t color = 1);
    void fillCircle(int16_t cx, int16_t cy, int16_t radius, uint8_t color = 1);

    // Text & Fonts (5x7 standard bitmap font)
    void drawChar(int16_t x, int16_t y, char c, uint8_t scale = 2, uint8_t color = 1);
    void drawText(int16_t x, int16_t y, const char* text, uint8_t scale = 2, uint8_t color = 1);
    void drawCenteredText(int16_t y, const char* text, uint8_t scale = 2, uint8_t color = 1);
    int16_t getTextWidth(const char* text, uint8_t scale = 2) const;

    // Direct stream to thermal printer
    bool printTo(EscPosPrinter& printer);

private:
    uint16_t _height;
    uint8_t* _buffer;
};

#endif // THERMAL_CANVAS_H
