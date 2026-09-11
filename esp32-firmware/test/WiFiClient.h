#ifndef WIFICLIENT_MOCK_H
#define WIFICLIENT_MOCK_H
#include "Arduino.h"
class Print {
public:
    virtual size_t write(const uint8_t* b, size_t s) { return s; }
    virtual size_t write(uint8_t c) { return 1; }
    virtual void print(const String& s) {}
    virtual void println(const String& s = "") {}
};
class WiFiClient : public Print {
public:
    bool connect(const char* host, uint16_t port, int timeout = 0) { return true; }
    bool connected() { return true; }
    void flush() {}
    void stop() {}
};
#endif
