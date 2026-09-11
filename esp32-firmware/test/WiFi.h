#ifndef WIFI_MOCK_H
#define WIFI_MOCK_H
#include "Arduino.h"
class IPAddress {
public:
    String toString() const { return "192.168.1.55"; }
};
class WiFiMock {
public:
    IPAddress localIP() const { return IPAddress(); }
};
static WiFiMock WiFi;
#endif
