#ifndef PUZZLE_CLIENT_H
#define PUZZLE_CLIENT_H

#include <Arduino.h>
#include <WiFi.h>
#include <WiFiClient.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "config.h"
#include "printer/EscPosPrinter.h"

class PuzzleClient {
public:
    PuzzleClient();

    // Fetches the daily puzzle payload from the web service and streams to the printer
    bool fetchAndPrintDailyPuzzles(EscPosPrinter& printer);

private:
    bool streamEscPosBinary(HTTPClient& http, EscPosPrinter& printer);
    bool parseAndPrintJson(HTTPClient& http, EscPosPrinter& printer);
};

#endif // PUZZLE_CLIENT_H
