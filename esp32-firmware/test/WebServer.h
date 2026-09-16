#ifndef WEB_SERVER_MOCK_H
#define WEB_SERVER_MOCK_H

#include <functional>
#include <string>
#include "Arduino.h"

enum HTTPMethod {
    HTTP_ANY,
    HTTP_GET,
    HTTP_POST
};

class WebServer {
public:
    WebServer(int port = 80) {}
    void begin() {}
    void stop() {}
    void handleClient() {}
    void on(const char* uri, HTTPMethod method, std::function<void()> fn) {}
    void onNotFound(std::function<void()> fn) {}
    void sendHeader(const char* name, const char* value, bool first = false) {}
    void send_P(int code, const char* content_type, const char* content, size_t contentLength) {}
    void send(int code, const char* content_type, const String& content) {}
    void send(int code, const char* content_type, const char* content) {}
    bool hasArg(const char* name) { return false; }
    String arg(const char* name) { return String(""); }
};

#endif
