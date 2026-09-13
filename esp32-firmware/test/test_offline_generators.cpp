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
    void printRasterBitmap(const uint8_t* bitmapData, uint16_t widthDots, uint16_t heightDots) override {
        std::cout << "[PRINTER: RASTER BITMAP " << widthDots << "x" << heightDots << " dots (" << ((widthDots + 7) / 8 * heightDots) << " bytes)]" << std::endl;
    }
};

#include "../src/printer/ThermalCanvas.h"
#include "../src/printer/ThermalCanvas.cpp"

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

#include "../src/generators/TentsGen.h"
#include "../src/generators/TentsGen.cpp"

#include "../src/generators/BridgesGen.h"
#include "../src/generators/BridgesGen.cpp"

#include "../src/generators/TangoGen.h"
#include "../src/generators/TangoGen.cpp"

#include "../src/generators/WheelGen.h"
#include "../src/generators/WheelGen.cpp"

#include "../src/generators/LightsGen.h"
#include "../src/generators/LightsGen.cpp"

#include "../src/generators/OfflinePuzzleComposer.h"
#include "../src/generators/OfflinePuzzleComposer.cpp"

int main() {
    std::srand(time(nullptr));
    std::cout << "==================================================" << std::endl;
    std::cout << "TESTING 100% OFFLINE 5-PUZZLE RANDOM MIX ENGINE ON ESP32" << std::endl;
    std::cout << "==================================================" << std::endl;

    ConsoleEscPosPrinter printer;
    OfflinePuzzleComposer composer;

    // Test 1: Generate 5-puzzle mix
    std::cout << "\n>>> TEST 1: GENERATE 5-PUZZLE RANDOM MIX <<<" << std::endl;
    bool okEasy = composer.generateAndPrintReceipt(printer, "Monday, September 14, 2026", GRADE_EASY);
    if (!okEasy) {
        std::cerr << "FAILED on Run 1" << std::endl;
        return 1;
    }

    // Test 2: Generate Hard Grade
    std::cout << "\n>>> TEST 2: GENERATE HARD GRADE BUNDLE <<<" << std::endl;
    bool okHard = composer.generateAndPrintReceipt(printer, "Tuesday, September 15, 2026", GRADE_HARD);
    if (!okHard) {
        std::cerr << "FAILED on Hard Grade" << std::endl;
        return 1;
    }

    // Test 3: Simulate 3 Hardware Button Presses (Rotating Grade)
    std::cout << "\n>>> TEST 3: SIMULATING 3 HARDWARE BUTTON PRESSES (ROTATING GRADE) <<<" << std::endl;
    for (int press = 1; press <= 3; press++) {
        std::cout << "\n--- [BUTTON PRESS #" << press << "] ---" << std::endl;
        bool okPress = composer.generateAndPrintReceipt(printer, "Wednesday, September 16, 2026", GRADE_ROTATING);
        if (!okPress) {
            std::cerr << "FAILED on Button Press #" << press << std::endl;
            return 1;
        }
    }

    // Test 4: Generate Random Difficulty per game (GRADE_RANDOM)
    std::cout << "\n>>> TEST 4: GENERATE RANDOM DIFFICULTY PER GAME (GRADE_RANDOM) <<<" << std::endl;
    bool okRandom = composer.generateAndPrintReceipt(printer, "Thursday, September 17, 2026", GRADE_RANDOM);
    if (!okRandom) {
        std::cerr << "FAILED on Random Grade" << std::endl;
        return 1;
    }

    std::cout << "\n==================================================" << std::endl;
    std::cout << ">>> SUCCESS: 100% OFFLINE MULTI-GRADE GENERATION VERIFIED! <<<" << std::endl;
    std::cout << "==================================================" << std::endl;
    return 0;
}
