#include "ThermalCanvas.h"
#include "EscPosPrinter.h"
#include <algorithm>
#include <cstdlib>

#ifndef min
#define min(a,b) (((a)<(b))?(a):(b))
#endif
#ifndef max
#define max(a,b) (((a)>(b))?(a):(b))
#endif

// 5x7 Font representation: 7 rows of 6 bits per character
struct FontGlyph {
    char c;
    uint8_t rows[7];
};

static const FontGlyph GLYPH_TABLE[] = {
    { '0', {0x1E, 0x21, 0x21, 0x21, 0x21, 0x21, 0x1E} },
    { '1', {0x08, 0x18, 0x28, 0x08, 0x08, 0x08, 0x3E} },
    { '2', {0x1E, 0x21, 0x01, 0x0E, 0x18, 0x20, 0x3F} },
    { '3', {0x1E, 0x21, 0x01, 0x0E, 0x01, 0x21, 0x1E} },
    { '4', {0x02, 0x06, 0x0A, 0x12, 0x3F, 0x02, 0x02} },
    { '5', {0x3F, 0x20, 0x3E, 0x01, 0x01, 0x21, 0x1E} },
    { '6', {0x1E, 0x21, 0x20, 0x3E, 0x21, 0x21, 0x1E} },
    { '7', {0x3F, 0x01, 0x02, 0x04, 0x08, 0x10, 0x10} },
    { '8', {0x1E, 0x21, 0x21, 0x1E, 0x21, 0x21, 0x1E} },
    { '9', {0x1E, 0x21, 0x21, 0x1F, 0x01, 0x21, 0x1E} },
    { 'A', {0x0C, 0x12, 0x21, 0x3F, 0x21, 0x21, 0x21} },
    { 'B', {0x3E, 0x21, 0x21, 0x3E, 0x21, 0x21, 0x3E} },
    { 'C', {0x1E, 0x21, 0x20, 0x20, 0x20, 0x21, 0x1E} },
    { 'D', {0x3C, 0x22, 0x21, 0x21, 0x21, 0x22, 0x3C} },
    { 'E', {0x3F, 0x20, 0x20, 0x3E, 0x20, 0x20, 0x3F} },
    { 'F', {0x3F, 0x20, 0x20, 0x3E, 0x20, 0x20, 0x20} },
    { 'G', {0x1E, 0x21, 0x20, 0x27, 0x21, 0x21, 0x1E} },
    { 'H', {0x21, 0x21, 0x21, 0x3F, 0x21, 0x21, 0x21} },
    { 'I', {0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x1F} },
    { 'J', {0x07, 0x02, 0x02, 0x02, 0x22, 0x22, 0x1C} },
    { 'K', {0x21, 0x22, 0x24, 0x38, 0x24, 0x22, 0x21} },
    { 'L', {0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x3F} },
    { 'M', {0x21, 0x33, 0x2D, 0x21, 0x21, 0x21, 0x21} },
    { 'N', {0x21, 0x31, 0x29, 0x25, 0x23, 0x21, 0x21} },
    { 'O', {0x1E, 0x21, 0x21, 0x21, 0x21, 0x21, 0x1E} },
    { 'P', {0x3E, 0x21, 0x21, 0x3E, 0x20, 0x20, 0x20} },
    { 'Q', {0x1E, 0x21, 0x21, 0x21, 0x25, 0x22, 0x1D} },
    { 'R', {0x3E, 0x21, 0x21, 0x3E, 0x24, 0x22, 0x21} },
    { 'S', {0x1E, 0x21, 0x20, 0x1E, 0x01, 0x21, 0x1E} },
    { 'T', {0x3F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04} },
    { 'U', {0x21, 0x21, 0x21, 0x21, 0x21, 0x21, 0x1E} },
    { 'V', {0x21, 0x21, 0x21, 0x12, 0x12, 0x0C, 0x0C} },
    { 'W', {0x21, 0x21, 0x21, 0x21, 0x2D, 0x33, 0x21} },
    { 'X', {0x21, 0x12, 0x0C, 0x0C, 0x12, 0x21, 0x21} },
    { 'Y', {0x21, 0x12, 0x0C, 0x04, 0x04, 0x04, 0x04} },
    { 'Z', {0x3F, 0x02, 0x04, 0x08, 0x10, 0x20, 0x3F} },
    { ' ', {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00} },
    { '.', {0x00, 0x00, 0x00, 0x00, 0x00, 0x0C, 0x0C} },
    { ':', {0x00, 0x0C, 0x0C, 0x00, 0x0C, 0x0C, 0x00} },
    { '-', {0x00, 0x00, 0x00, 0x3E, 0x00, 0x00, 0x00} },
    { '+', {0x00, 0x08, 0x08, 0x3E, 0x08, 0x08, 0x00} },
    { '=', {0x00, 0x3E, 0x00, 0x3E, 0x00, 0x00, 0x00} },
    { '*', {0x00, 0x2A, 0x1C, 0x3E, 0x1C, 0x2A, 0x00} },
    { '/', {0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x00} },
    { '(', {0x04, 0x08, 0x10, 0x10, 0x10, 0x08, 0x04} },
    { ')', {0x10, 0x08, 0x04, 0x04, 0x04, 0x08, 0x10} },
    { '?', {0x1E, 0x21, 0x02, 0x04, 0x04, 0x00, 0x04} },
    { '!', {0x04, 0x04, 0x04, 0x04, 0x04, 0x00, 0x04} },
    { '[', {0x1E, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1E} },
    { ']', {0x1E, 0x02, 0x02, 0x02, 0x02, 0x02, 0x1E} },
    { '_', {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3F} },
    { ',', {0x00, 0x00, 0x00, 0x00, 0x0C, 0x04, 0x08} }
};
static const size_t GLYPH_COUNT = sizeof(GLYPH_TABLE) / sizeof(GLYPH_TABLE[0]);

static const uint8_t* getGlyphRows(char c) {
    char upperC = toupper((unsigned char)c);
    for (size_t i = 0; i < GLYPH_COUNT; i++) {
        if (GLYPH_TABLE[i].c == upperC) {
            return GLYPH_TABLE[i].rows;
        }
    }
    // Return space for unknown glyphs
    return GLYPH_TABLE[36].rows;
}

ThermalCanvas::ThermalCanvas() : _height(0), _buffer(nullptr) {
}

ThermalCanvas::~ThermalCanvas() {
    end();
}

bool ThermalCanvas::begin(uint16_t heightDots) {
    end();
    _height = heightDots;
    size_t totalBytes = (size_t)THERMAL_CANVAS_WIDTH_BYTES * _height;
    _buffer = (uint8_t*)malloc(totalBytes);
    if (_buffer) {
        memset(_buffer, 0, totalBytes);
        return true;
    }
    _height = 0;
    return false;
}

void ThermalCanvas::end() {
    if (_buffer) {
        free(_buffer);
        _buffer = nullptr;
    }
    _height = 0;
}

void ThermalCanvas::clear(uint8_t color) {
    if (_buffer && _height > 0) {
        size_t totalBytes = (size_t)THERMAL_CANVAS_WIDTH_BYTES * _height;
        memset(_buffer, color ? 0xFF : 0x00, totalBytes);
    }
}

void ThermalCanvas::setPixel(int16_t x, int16_t y, uint8_t color) {
    if (!_buffer || x < 0 || x >= THERMAL_CANVAS_WIDTH || y < 0 || y >= _height) {
        return;
    }
    size_t byteIdx = (size_t)y * THERMAL_CANVAS_WIDTH_BYTES + (x >> 3);
    uint8_t bitMask = 1 << (7 - (x & 7));
    if (color) {
        _buffer[byteIdx] |= bitMask;
    } else {
        _buffer[byteIdx] &= ~bitMask;
    }
}

void ThermalCanvas::drawHLine(int16_t x, int16_t y, int16_t w, uint8_t thickness, uint8_t color) {
    if (w <= 0 || thickness <= 0) return;
    for (uint8_t t = 0; t < thickness; t++) {
        int16_t py = y + t;
        if (py >= 0 && py < _height) {
            int16_t startX = max((int16_t)0, x);
            int16_t endX = min((int16_t)THERMAL_CANVAS_WIDTH, (int16_t)(x + w));
            for (int16_t px = startX; px < endX; px++) {
                setPixel(px, py, color);
            }
        }
    }
}

void ThermalCanvas::drawVLine(int16_t x, int16_t y, int16_t h, uint8_t thickness, uint8_t color) {
    if (h <= 0 || thickness <= 0) return;
    for (uint8_t t = 0; t < thickness; t++) {
        int16_t px = x + t;
        if (px >= 0 && px < THERMAL_CANVAS_WIDTH) {
            int16_t startY = max((int16_t)0, y);
            int16_t endY = min((int16_t)_height, (int16_t)(y + h));
            for (int16_t py = startY; py < endY; py++) {
                setPixel(px, py, color);
            }
        }
    }
}

void ThermalCanvas::drawRect(int16_t x, int16_t y, int16_t w, int16_t h, uint8_t thickness, uint8_t color) {
    if (w <= 0 || h <= 0) return;
    drawHLine(x, y, w, thickness, color);
    drawHLine(x, y + h - thickness, w, thickness, color);
    drawVLine(x, y, h, thickness, color);
    drawVLine(x + w - thickness, y, h, thickness, color);
}

void ThermalCanvas::fillRect(int16_t x, int16_t y, int16_t w, int16_t h, uint8_t color) {
    if (w <= 0 || h <= 0) return;
    int16_t startY = max((int16_t)0, y);
    int16_t endY = min((int16_t)_height, (int16_t)(y + h));
    int16_t startX = max((int16_t)0, x);
    int16_t endX = min((int16_t)THERMAL_CANVAS_WIDTH, (int16_t)(x + w));

    for (int16_t py = startY; py < endY; py++) {
        for (int16_t px = startX; px < endX; px++) {
            setPixel(px, py, color);
        }
    }
}

void ThermalCanvas::fillHatch(int16_t x, int16_t y, int16_t w, int16_t h, uint8_t patternId) {
    if (w <= 0 || h <= 0) return;
    uint8_t pat = patternId % 8;
    int16_t startY = max((int16_t)0, y);
    int16_t endY = min((int16_t)_height, (int16_t)(y + h));
    int16_t startX = max((int16_t)0, x);
    int16_t endX = min((int16_t)THERMAL_CANVAS_WIDTH, (int16_t)(x + w));

    for (int16_t py = startY; py < endY; py++) {
        for (int16_t px = startX; px < endX; px++) {
            bool isBurn = false;
            switch (pat) {
                case 0: isBurn = false; break;
                case 1: isBurn = ((px + py) % 6 == 0); break;
                case 2: isBurn = ((px - py + 1000) % 6 == 0); break;
                case 3: isBurn = (px % 4 == 0 || py % 4 == 0); break;
                case 4: isBurn = ((px + py) % 4 == 0); break;
                case 5: isBurn = (px % 3 == 0 && py % 3 == 0); break;
                case 6: isBurn = ((px + py) % 3 == 0 || (px - py + 1000) % 3 == 0); break;
                case 7: isBurn = (py % 3 == 0); break;
            }
            if (isBurn) {
                setPixel(px, py, 1);
            }
        }
    }
}

void ThermalCanvas::drawCircle(int16_t cx, int16_t cy, int16_t radius, uint8_t thickness, uint8_t color) {
    if (radius <= 0) return;
    int32_t rInnerSq = (radius >= thickness) ? (int32_t)(radius - thickness) * (radius - thickness) : 0;
    int32_t rOuterSq = (int32_t)radius * radius;
    int16_t yStart = max((int16_t)0, (int16_t)(cy - radius));
    int16_t yEnd = min((int16_t)_height, (int16_t)(cy + radius + 1));
    int16_t xStart = max((int16_t)0, (int16_t)(cx - radius));
    int16_t xEnd = min((int16_t)THERMAL_CANVAS_WIDTH, (int16_t)(cx + radius + 1));

    for (int16_t py = yStart; py < yEnd; py++) {
        int32_t dy = py - cy;
        int32_t dySq = dy * dy;
        for (int16_t px = xStart; px < xEnd; px++) {
            int32_t dx = px - cx;
            int32_t distSq = dx * dx + dySq;
            if (distSq >= rInnerSq && distSq <= rOuterSq) {
                setPixel(px, py, color);
            }
        }
    }
}

void ThermalCanvas::fillCircle(int16_t cx, int16_t cy, int16_t radius, uint8_t color) {
    if (radius <= 0) return;
    int32_t rSq = (int32_t)radius * radius;
    int16_t yStart = max((int16_t)0, (int16_t)(cy - radius));
    int16_t yEnd = min((int16_t)_height, (int16_t)(cy + radius + 1));
    int16_t xStart = max((int16_t)0, (int16_t)(cx - radius));
    int16_t xEnd = min((int16_t)THERMAL_CANVAS_WIDTH, (int16_t)(cx + radius + 1));

    for (int16_t py = yStart; py < yEnd; py++) {
        int32_t dy = py - cy;
        int32_t dySq = dy * dy;
        for (int16_t px = xStart; px < xEnd; px++) {
            int32_t dx = px - cx;
            if (dx * dx + dySq <= rSq) {
                setPixel(px, py, color);
            }
        }
    }
}

void ThermalCanvas::drawChar(int16_t x, int16_t y, char c, uint8_t scale, uint8_t color) {
    if (scale == 0) return;
    const uint8_t* rows = getGlyphRows(c);
    for (uint8_t rowIdx = 0; rowIdx < 7; rowIdx++) {
        uint8_t rowByte = rows[rowIdx];
        for (uint8_t colIdx = 0; colIdx < 6; colIdx++) {
            if ((rowByte >> (5 - colIdx)) & 1) {
                for (uint8_t sy = 0; sy < scale; sy++) {
                    for (uint8_t sx = 0; sx < scale; sx++) {
                        setPixel(x + colIdx * scale + sx, y + rowIdx * scale + sy, color);
                    }
                }
            }
        }
    }
}

void ThermalCanvas::drawText(int16_t x, int16_t y, const char* text, uint8_t scale, uint8_t color) {
    if (!text || scale == 0) return;
    int16_t curX = x;
    int16_t charW = 6 * scale + max(1, scale / 2);
    while (*text) {
        drawChar(curX, y, *text, scale, color);
        curX += charW;
        text++;
    }
}

void ThermalCanvas::drawCenteredText(int16_t y, const char* text, uint8_t scale, uint8_t color) {
    if (!text) return;
    int16_t w = getTextWidth(text, scale);
    int16_t x = (THERMAL_CANVAS_WIDTH - w) / 2;
    drawText(x, y, text, scale, color);
}

int16_t ThermalCanvas::getTextWidth(const char* text, uint8_t scale) const {
    if (!text || scale == 0) return 0;
    int len = strlen(text);
    if (len == 0) return 0;
    int16_t charW = 6 * scale + max(1, scale / 2);
    return len * charW;
}

bool ThermalCanvas::printTo(EscPosPrinter& printer) {
    if (!_buffer || _height == 0) return false;
    printer.printRasterBitmap(_buffer, THERMAL_CANVAS_WIDTH, _height);
    return true;
}
