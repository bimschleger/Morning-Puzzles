#include "PuzzleClient.h"

PuzzleClient::PuzzleClient() {
}

bool PuzzleClient::fetchAndPrintDailyPuzzles(EscPosPrinter& printer) {
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("[HTTP] ERROR: Wi-Fi is not connected. Cannot fetch puzzles.");
        return false;
    }

    WiFiClient client;
    HTTPClient http;

    String url = "http://" + String(PUZZLE_API_HOST) + ":" + String(PUZZLE_API_PORT) + String(PUZZLE_API_PATH);
    Serial.printf("[HTTP] Fetching daily puzzles from: %s\n", url.c_str());

    http.begin(client, url);
    http.addHeader("Accept", "application/octet-stream, application/json");
    if (strlen(PUZZLE_API_KEY) > 0) {
        http.addHeader("Authorization", PUZZLE_API_KEY);
    }
    http.setTimeout(15000); // 15 second timeout for puzzle generation

    int httpCode = http.GET();
    Serial.printf("[HTTP] Response status code: %d\n", httpCode);

    if (httpCode != HTTP_CODE_OK) {
        Serial.printf("[HTTP] ERROR: Failed GET request. Error: %s\n", http.errorToString(httpCode).c_str());
        http.end();
        return false;
    }

    String contentType = http.header("Content-Type");
    Serial.printf("[HTTP] Content-Type: %s, Length: %d\n", contentType.c_str(), http.getSize());

    bool success = false;
    if (contentType.indexOf("application/json") >= 0) {
        success = parseAndPrintJson(http, printer);
    } else {
        // Default to streaming binary ESC/POS data
        success = streamEscPosBinary(http, printer);
    }

    http.end();
    return success;
}

bool PuzzleClient::streamEscPosBinary(HTTPClient& http, EscPosPrinter& printer) {
    Serial.println("[HTTP] Streaming raw ESC/POS binary directly to printer...");

    if (!printer.connect()) {
        Serial.println("[HTTP] ERROR: Could not connect to printer socket.");
        return false;
    }

    WiFiClient* stream = http.getStreamPtr();
    size_t totalBytes = 0;
    uint8_t buffer[512];

    while (http.connected() && (http.getSize() > 0 || http.getSize() == -1)) {
        size_t available = stream->available();
        if (available > 0) {
            size_t bytesToRead = min(available, sizeof(buffer));
            int bytesRead = stream->readBytes(buffer, bytesToRead);
            if (bytesRead > 0) {
                printer.writeRaw(buffer, bytesRead);
                totalBytes += bytesRead;
            }
        } else {
            delay(10);
            if (!stream->connected() && stream->available() == 0) {
                break;
            }
        }
    }

    Serial.printf("[HTTP] Successfully streamed %d bytes to printer!\n", totalBytes);

    // Ensure clean end of receipt and cut paper
    printer.feed(3);
    printer.cut(false);
    printer.disconnect();
    return true;
}

bool PuzzleClient::parseAndPrintJson(HTTPClient& http, EscPosPrinter& printer) {
    Serial.println("[HTTP] Parsing JSON puzzle response...");

    String payload = http.getString();
    JsonDocument doc;
    DeserializationError error = deserializeJson(doc, payload);

    if (error) {
        Serial.printf("[HTTP] JSON Deserialization error: %s\n", error.c_str());
        return false;
    }

    if (!printer.connect()) {
        Serial.println("[HTTP] ERROR: Could not connect to printer socket.");
        return false;
    }

    printer.init();
    
    // Header
    const char* date = doc["date"] | "Daily Edition";
    const char* title = doc["title"] | "MORNING PUZZLES";
    printer.printHeader(title, date);
    printer.println("");

    // 1. Sudoku Section
    if (doc["sudoku"].is<JsonObject>()) {
        JsonObject s = doc["sudoku"];
        printer.setBold(true);
        printer.println("--- SUDOKU ---");
        printer.setBold(false);
        printer.println("Difficulty: " + String((const char*)s["difficulty"]));
        printer.println("");

        JsonArray grid = s["grid"];
        for (JsonArray row : grid) {
            String rowStr = " ";
            for (int col = 0; col < row.size(); col++) {
                int val = row[col];
                if (val == 0) rowStr += ". ";
                else rowStr += String(val) + " ";
                if (col == 2 || col == 5) rowStr += "| ";
            }
            printer.println(rowStr);
        }
        printer.println("");
    }

    // 2. Word Search Section
    if (doc["wordsearch"].is<JsonObject>()) {
        JsonObject ws = doc["wordsearch"];
        printer.setBold(true);
        printer.println("--- WORD SEARCH ---");
        printer.setBold(false);
        printer.println("Theme: " + String((const char*)ws["theme"] | "General"));
        printer.println("");

        JsonArray grid = ws["grid"];
        for (JsonArray row : grid) {
            String rowStr = " ";
            for (const char* letter : row) {
                rowStr += String(letter) + " ";
            }
            printer.println(rowStr);
        }
        printer.println("");
        printer.println("Words to find:");
        JsonArray words = ws["words"];
        String wordsLine = "";
        for (int i = 0; i < words.size(); i++) {
            wordsLine += "[ ] " + String((const char*)words[i]) + "   ";
            if ((i + 1) % 2 == 0 || i == words.size() - 1) {
                printer.println(wordsLine);
                wordsLine = "";
            }
        }
        printer.println("");
    }

    // 3. Jumble Section
    if (doc["jumble"].is<JsonObject>()) {
        JsonObject j = doc["jumble"];
        printer.setBold(true);
        printer.println("--- JUMBLE ---");
        printer.setBold(false);
        printer.println("Unscramble the letters:");
        
        JsonArray scrambled = j["words"];
        for (JsonObject item : scrambled) {
            printer.printKeyValue(String((const char*)item["scrambled"]), "___________");
        }
        printer.println("");
        printer.println("Punchline Clue: " + String((const char*)j["clue"]));
        printer.println("Answer: _______________________");
        printer.println("");
    }

    // Footer
    printer.printDoubleLine();
    printer.setAlign(ALIGN_CENTER);
    printer.println("Have a great morning!");
    printer.println("morningpuzzles.local");
    printer.feed(3);
    printer.cut(false);
    printer.disconnect();

    return true;
}
