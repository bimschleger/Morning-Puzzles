#ifndef WIFI_MOCK_H
#define WIFI_MOCK_H
#include "Arduino.h"

enum WiFiMode_t {
    WIFI_OFF = 0,
    WIFI_STA = 1,
    WIFI_AP = 2,
    WIFI_AP_STA = 3
};

class WiFiMock {
public:
    IPAddress localIP() const { return IPAddress(); }
    void mode(WiFiMode_t m) {}
    void setSleep(bool enable) {}
    bool softAPConfig(IPAddress ip, IPAddress gw, IPAddress sn) { return true; }
    bool softAP(const char* ssid, const char* pass = nullptr, int ch = 1, int ss = 0, int mc = 4) { return true; }
    bool softAPdisconnect(bool wifioff = false) { return true; }
};
static WiFiMock WiFi;
#endif
