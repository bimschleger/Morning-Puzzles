#ifndef WIFI_MOCK_H
#define WIFI_MOCK_H
#include "Arduino.h"
class IPAddress {
public:
    IPAddress() {}
    IPAddress(uint8_t a, uint8_t b, uint8_t c, uint8_t d) {}
    bool fromString(const char* s) { return true; }
    bool fromString(const String& s) { return true; }
    String toString() const { return "192.168.123.50"; }
};
class WiFiMock {
public:
    IPAddress localIP() const { return IPAddress(); }
};
static WiFiMock WiFi;
#endif
