#include "Arduino.h"
#include "WiFi.h"
#include "WiFiClient.h"
#include "HardwareSerial.h"

#include "../src/printer/EscPosPrinter.h"
#include "../src/printer/EscPosPrinter.cpp"

// Implement a simple console-printing EscPosPrinter for verification
class ConsoleEscPosPrinter : public EscPosPrinter {
public:
    bool connect() { return true; }
    void disconnect() {}
    void init() { std::cout << "[PRINTER: INIT]" << std::endl; }
    void setBold(bool b) {}
    void setAlign(TextAlignment a) {}
    void print(const String& s) { std::cout << s; }
    void println(const String& s = "") { std::cout << s << std::endl; }
    void printHorizontalLine(char c = '-') { std::cout << std::string(48, c) << std::endl; }
    void printDoubleLine() { std::cout << std::string(48, '=') << std::endl; }
    void printHeader(const String& t, const String& d = "") {
        printDoubleLine();
        std::cout << "  " << t << " (" << d << ")" << std::endl;
        printDoubleLine();
    }
    void printKeyValue(const String& k, const String& v, int total = 48) {
        int spaces = total - (int)k.length() - (int)v.length();
        if (spaces < 1) spaces = 1;
        std::cout << k << std::string(spaces, ' ') << v << std::endl;
    }
    void feed(uint8_t n = 1) {}
    void cut(bool) { std::cout << "[PRINTER: CUT PAPER]" << std::endl; }
};

#include "../src/generators/SudokuGen.h"
#include "../src/generators/SudokuGen.cpp"

#include "../src/generators/WordSearchGen.h"
#include "../src/generators/WordSearchGen.cpp"

#include "../src/generators/NonogramGen.h"
#include "../src/generators/NonogramGen.cpp"

#include "../src/generators/QueensGen.h"
#include "../src/generators/QueensGen.cpp"

#include "../src/generators/JumbleGen.h"
#include "../src/generators/JumbleGen.cpp"

#include "../src/generators/BinaryGen.h"
#include "../src/generators/BinaryGen.cpp"

#include "../src/generators/MinesGen.h"
#include "../src/generators/MinesGen.cpp"

#include "../src/generators/OfflinePuzzleComposer.h"
#include "../src/generators/OfflinePuzzleComposer.cpp"

int main() {
    std::srand(time(nullptr));
    std::cout << "==================================================" << std::endl;
    std::cout << "TESTING ON-DEVICE ESP32 C++ OFFLINE GENERATORS" << std::endl;
    std::cout << "==================================================" << std::endl;

    ConsoleEscPosPrinter printer;
    OfflinePuzzleComposer composer;

    bool ok = composer.generateAndPrintReceipt(printer, "Monday, September 14, 2026");
    if (ok) {
        std::cout << "\n>>> SUCCESS: ALL 7 C++ GENERATORS EXECUTED PERFECTLY! <<<" << std::endl;
        return 0;
    } else {
        std::cerr << "FAILURE in composer" << std::endl;
        return 1;
    }
}
