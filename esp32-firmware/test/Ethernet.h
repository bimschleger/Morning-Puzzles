#ifndef ETHERNET_MOCK_H
#define ETHERNET_MOCK_H
#include "Arduino.h"
#include "WiFiClient.h"

class EthernetClient : public Print {
public:
    bool connect(const char* host, uint16_t port) { return true; }
    bool connect(IPAddress ip, uint16_t port) { return true; }
    bool connected() { return true; }
    void flush() {}
    void stop() {}
};

class EthernetClass {
public:
    void init(uint8_t csPin) {}
    void begin(uint8_t* mac, IPAddress ip, IPAddress dns, IPAddress gateway, IPAddress subnet) {}
    IPAddress localIP() { return IPAddress(192, 168, 123, 50); }
};

static EthernetClass Ethernet;

#endif // ETHERNET_MOCK_H
