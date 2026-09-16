#ifndef WIRE_MOCK_H
#define WIRE_MOCK_H

#include <cstdint>

class TwoWire {
public:
    void begin(int sda = -1, int scl = -1) {}
    void beginTransmission(uint8_t addr) {}
    uint8_t endTransmission() { return 1; }
    void requestFrom(uint8_t addr, uint8_t count) {}
    int available() { return 0; }
    uint8_t read() { return 0; }
    size_t write(uint8_t data) { return 1; }
};

extern TwoWire Wire;

#endif
