#ifndef WIFI_MOCK_H
#define WIFI_MOCK_H
#include "Arduino.h"
class WiFiMock {
public:
    IPAddress localIP() const { return IPAddress(); }
};
static WiFiMock WiFi;
#endif
