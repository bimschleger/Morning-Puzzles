#ifndef HARDWARE_SERIAL_MOCK_H
#define HARDWARE_SERIAL_MOCK_H
#include "WiFiClient.h"
#define SERIAL_8N1 0
class HardwareSerial : public Print {
public:
    void begin(unsigned long b, uint32_t c, int8_t rx, int8_t tx) {}
};
static HardwareSerial Serial2;
#endif
