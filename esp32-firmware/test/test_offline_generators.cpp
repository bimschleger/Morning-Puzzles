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
    void init() override { std::cout << "[PRINTER: INIT]" << std::endl; }
    void setBold(bool b) override {}
    void setAlign(TextAlignment a) override {}
    void print(const String& s) override { std::cout << s; }
    void println(const String& s = "") override { std::cout << s << std::endl; }
    void print(const char* s) override { std::cout << s; }
    void println(const char* s = "") override { std::cout << s << std::endl; }
    void printHorizontalLine(char c = '-') override { std::cout << std::string(48, c) << std::endl; }
    void printDoubleLine() override { std::cout << std::string(48, '=') << std::endl; }
    void printHeader(const String& t, const String& d = "") override {
        printDoubleLine();
        std::cout << "  " << t << " (" << d << ")" << std::endl;
        printDoubleLine();
    }
    void printKeyValue(const String& k, const String& v, int total = 48) override {
        int spaces = total - (int)k.length() - (int)v.length();
        if (spaces < 1) spaces = 1;
        std::cout << k << std::string(spaces, ' ') << v << std::endl;
    }
    void feed(uint8_t n = 1) override {}
    void cut(bool) override { std::cout << "[PRINTER: CUT PAPER]" << std::endl; }
    void printRasterBitmap(const uint8_t* bitmapData, uint16_t widthDots, uint16_t heightDots) override {
        std::cout << "[PRINTER: RASTER BITMAP " << widthDots << "x" << heightDots << " dots (" << ((widthDots + 7) / 8 * heightDots) << " bytes)]" << std::endl;
    }
};

#include "../src/printer/qrcode.h"
#include "../src/printer/qrcode.c"
#include "../src/printer/ThermalCanvas.h"
#include "../src/printer/ThermalCanvas.cpp"
#include "../src/config/OfflineConfigManager.h"
#include "../src/config/OfflineConfigManager.cpp"

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

#include "../src/generators/LoopGen.h"
#include "../src/generators/LoopGen.cpp"

#include "../src/generators/KillerGen.h"
#include "../src/generators/KillerGen.cpp"

#include "../src/generators/CryptogramDataset.h"
#include "../src/generators/CryptogramGen.h"
#include "../src/generators/CryptogramGen.cpp"

#include "../src/generators/LadderDataset.h"
#include "../src/generators/LadderGen.h"
#include "../src/generators/LadderGen.cpp"

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

    // Test 5: Custom Configured Game Pool (7 of 13 enabled, print 4)
    std::cout << "\n>>> TEST 5: CUSTOM CONFIGURED GAME POOL (7 of 13 enabled, print 4) <<<" << std::endl;
    OfflineConfigManager config;
    config.begin();
    // Enable 7 games: Sudoku, Queens, Mines, Bridges, Tango, Lights, Wheel
    uint16_t mask = (1 << PUZZLE_SUDOKU) | (1 << PUZZLE_QUEENS) | (1 << PUZZLE_MINES) |
                    (1 << PUZZLE_BRIDGES) | (1 << PUZZLE_TANGO) | (1 << PUZZLE_LIGHTS) | (1 << PUZZLE_WHEEL);
    config.setGameMask(mask);
    config.setPuzzleCount(4);
    config.setPuzzleGrade(GRADE_ESCALATING);
    if (config.getEnabledGameCount() != 7) {
        std::cerr << "FAILED: Expected 7 enabled games, got " << (int)config.getEnabledGameCount() << std::endl;
        return 1;
    }
    if (config.getPuzzleCount() != 4) {
        std::cerr << "FAILED: Expected count 4, got " << (int)config.getPuzzleCount() << std::endl;
        return 1;
    }
    bool okCustom = composer.generateAndPrintReceipt(printer, "Friday, September 18, 2026", (PuzzleGrade)-1, &config);
    if (!okCustom) {
        std::cerr << "FAILED on Custom Game Pool" << std::endl;
        return 1;
    }

    // Test 6: Escalating Difficulty
    std::cout << "\n>>> TEST 6: ESCALATING DIFFICULTY PROGRESSION <<<" << std::endl;
    config.setPuzzleCount(5);
    config.setPuzzleGrade(GRADE_ESCALATING);
    for (uint8_t i = 0; i < 5; i++) {
        PuzzleGrade slot = composer.getGradeForSlot(i, 5);
        std::cout << "  Slot " << (int)i << "/5 Grade: " << composer.getGradeName(slot) << std::endl;
    }

    // Test 7: QR Code Generation on ThermalCanvas
    std::cout << "\n>>> TEST 7: THERMAL CANVAS QR CODE GENERATION <<<" << std::endl;
    ThermalCanvas qrCanvas;
    if (!qrCanvas.begin(240)) {
        std::cerr << "FAILED to allocate QR canvas" << std::endl;
        return 1;
    }
    bool qr1 = qrCanvas.drawQrCode(288, 120, "WIFI:S:Morning-Puzzles-Setup;T:nopass;;", 6);
    if (!qr1) {
        std::cerr << "FAILED to render Wi-Fi QR code" << std::endl;
        return 1;
    }
    qrCanvas.printTo(printer);
    qrCanvas.end();

    if (!qrCanvas.begin(200)) {
        std::cerr << "FAILED to allocate URL QR canvas" << std::endl;
        return 1;
    }
    bool qr2 = qrCanvas.drawQrCode(288, 100, "http://192.168.4.1", 6);
    if (!qr2) {
        std::cerr << "FAILED to render URL QR code" << std::endl;
        return 1;
    }
    qrCanvas.printTo(printer);
    qrCanvas.end();
    std::cout << "  -> QR Code generation on ThermalCanvas: OK" << std::endl;

    std::cout << "\n==================================================" << std::endl;
    std::cout << ">>> SUCCESS: 100% OFFLINE CONFIG & MULTI-GRADE TESTS VERIFIED! <<<" << std::endl;
    std::cout << "==================================================" << std::endl;
    return 0;
}
