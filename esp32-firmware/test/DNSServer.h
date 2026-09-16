#ifndef DNS_SERVER_MOCK_H
#define DNS_SERVER_MOCK_H

#include <cstdint>
#include <string>
#include "WiFi.h"

class DNSServer {
public:
    void start(uint16_t port, const std::string& domain, IPAddress ip) {}
    void stop() {}
    void processNextRequest() {}
};

#endif
