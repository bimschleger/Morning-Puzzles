#include "Arduino.h"
#include "WiFi.h"
#include "WiFiClient.h"
#include "HardwareSerial.h"

#include "../esp32-firmware/src/printer/EscPosPrinter.h"
#include "../esp32-firmware/src/printer/EscPosPrinter.cpp"
#include "../esp32-firmware/src/printer/ThermalCanvas.h"
#include "../esp32-firmware/src/printer/ThermalCanvas.cpp"

#include "../esp32-firmware/src/generators/JumbleDataset.h"
#include "../esp32-firmware/src/generators/JumbleGen.h"
#include "../esp32-firmware/src/generators/JumbleGen.cpp"

#include "../esp32-firmware/src/generators/WheelDataset.h"
#include "../esp32-firmware/src/generators/WheelGen.h"
#include "../esp32-firmware/src/generators/WheelGen.cpp"

#include "../esp32-firmware/src/generators/WordSearchDataset.h"
#include "../esp32-firmware/src/generators/WordSearchGen.h"
#include "../esp32-firmware/src/generators/WordSearchGen.cpp"

#include "../esp32-firmware/src/generators/MinesGen.h"
#include "../esp32-firmware/src/generators/MinesGen.cpp"

#include "../esp32-firmware/src/generators/TentsGen.h"
#include "../esp32-firmware/src/generators/TentsGen.cpp"

#include "../esp32-firmware/src/generators/QueensGen.h"
#include "../esp32-firmware/src/generators/QueensGen.cpp"

#include "../esp32-firmware/src/generators/SudokuGen.h"
#include "../esp32-firmware/src/generators/SudokuGen.cpp"

#include "../esp32-firmware/src/generators/BinaryGen.h"
#include "../esp32-firmware/src/generators/BinaryGen.cpp"

#include <iostream>
#include <iomanip>
#include <sstream>
#include <string>
#include <vector>

class CapturePrinter : public EscPosPrinter {
public:
    std::vector<uint8_t> lastBitmap;
    uint16_t lastWidth = 0;
    uint16_t lastHeight = 0;

    bool connect() { return true; }
    void disconnect() {}
    void init() {}
    void setBold(bool) {}
    void setAlign(TextAlignment) {}
    void print(const String&) {}
    void println(const String& = "") {}
    void feed(uint8_t = 1) {}
    void cut(bool = false) {}

    void printRasterBitmap(const uint8_t* bitmapData, uint16_t widthDots, uint16_t heightDots) override {
        lastWidth = widthDots;
        lastHeight = heightDots;
        size_t totalBytes = ((widthDots + 7) / 8) * heightDots;
        lastBitmap.assign(bitmapData, bitmapData + totalBytes);
    }
};

static std::string toHex(const std::vector<uint8_t>& bytes) {
    std::ostringstream oss;
    for (uint8_t b : bytes) {
        oss << std::hex << std::setw(2) << std::setfill('0') << (int)b;
    }
    return oss.str();
}

int main(int argc, char** argv) {
    std::srand(42);
    CapturePrinter* printer = new CapturePrinter();

    std::cout << "[\n";
    bool first = true;

    auto printSep = [&]() {
        if (!first) std::cout << ",\n";
        first = false;
    };

    // 1. JUMBLE
    {
        JumbleGen jGen;
        jGen.generate(JUMBLE_EASY);
        printer->lastBitmap.clear();
        jGen.printRasterToReceipt(*printer);

        printSep();
        std::cout << "  {\n";
        std::cout << "    \"puzzle\": \"jumble\",\n";
        std::cout << "    \"width\": " << printer->lastWidth << ",\n";
        std::cout << "    \"height\": " << printer->lastHeight << ",\n";
        std::cout << "    \"riddle\": \"" << jGen.getRiddle() << "\",\n";
        std::cout << "    \"answer\": \"" << jGen.getAnswer() << "\",\n";
        std::cout << "    \"words\": [";
        for (uint8_t i = 0; i < jGen.getNumWords(); i++) {
            if (i > 0) std::cout << ", ";
            std::cout << "\"" << jGen.getWord(i).original << "\"";
        }
        std::cout << "],\n";
        std::cout << "    \"scrambled\": [";
        for (uint8_t i = 0; i < jGen.getNumWords(); i++) {
            if (i > 0) std::cout << ", ";
            std::cout << "\"" << jGen.getWord(i).scrambled << "\"";
        }
        std::cout << "],\n";
        std::cout << "    \"circles\": [";
        for (uint8_t i = 0; i < jGen.getNumWords(); i++) {
            if (i > 0) std::cout << ", ";
            std::cout << "[";
            const auto& w = jGen.getWord(i);
            for (uint8_t c = 0; c < w.numCircles; c++) {
                if (c > 0) std::cout << ", ";
                std::cout << (int)w.circleIndices[c];
            }
            std::cout << "]";
        }
        std::cout << "],\n";
        std::cout << "    \"raster_hex\": \"" << toHex(printer->lastBitmap) << "\"\n";
        std::cout << "  }";
    }

    // 2. WHEEL
    {
        WheelGen wGen;
        wGen.generate(WHEEL_EASY);
        printer->lastBitmap.clear();
        wGen.printRasterToReceipt(*printer);

        printSep();
        std::cout << "  {\n";
        std::cout << "    \"puzzle\": \"wheel\",\n";
        std::cout << "    \"width\": " << printer->lastWidth << ",\n";
        std::cout << "    \"height\": " << printer->lastHeight << ",\n";
        std::cout << "    \"center_letter\": \"" << wGen.getCenterLetter() << "\",\n";
        std::cout << "    \"outer_letters\": [";
        const char* outer = wGen.getOuterLetters();
        for (int i = 0; i < 6; i++) {
            if (i > 0) std::cout << ", ";
            std::cout << "\"" << outer[i] << "\"";
        }
        std::cout << "],\n";
        std::cout << "    \"good\": " << (int)wGen.getGood() << ",\n";
        std::cout << "    \"great\": " << (int)wGen.getGreat() << ",\n";
        std::cout << "    \"genius\": " << (int)wGen.getGenius() << ",\n";
        std::cout << "    \"raster_hex\": \"" << toHex(printer->lastBitmap) << "\"\n";
        std::cout << "  }";
    }

    // 3. MINES
    {
        MinesGen mGen;
        mGen.generate(MINES_MEDIUM);
        printer->lastBitmap.clear();
        mGen.printRasterToReceipt(*printer, MINES_MEDIUM);

        printSep();
        std::cout << "  {\n";
        std::cout << "    \"puzzle\": \"mines\",\n";
        std::cout << "    \"width\": " << printer->lastWidth << ",\n";
        std::cout << "    \"height\": " << printer->lastHeight << ",\n";
        std::cout << "    \"total_mines\": " << (int)mGen.getTotalMines() << ",\n";
        std::cout << "    \"rows\": 8,\n";
        std::cout << "    \"cols\": 8,\n";
        std::cout << "    \"grid\": [";
        for (uint8_t r = 0; r < 8; r++) {
            if (r > 0) std::cout << ", ";
            std::cout << "[";
            for (uint8_t c = 0; c < 8; c++) {
                if (c > 0) std::cout << ", ";
                std::cout << (int)mGen.getCell(r, c);
            }
            std::cout << "]";
        }
        std::cout << "],\n";
        std::cout << "    \"raster_hex\": \"" << toHex(printer->lastBitmap) << "\"\n";
        std::cout << "  }";
    }

    // 4. TENTS
    {
        TentsGen tGen;
        tGen.generate(TENTS_MEDIUM);
        printer->lastBitmap.clear();
        tGen.printRasterToReceipt(*printer, TENTS_MEDIUM);

        printSep();
        std::cout << "  {\n";
        std::cout << "    \"puzzle\": \"tents\",\n";
        std::cout << "    \"width\": " << printer->lastWidth << ",\n";
        std::cout << "    \"height\": " << printer->lastHeight << ",\n";
        std::cout << "    \"size\": " << (int)tGen.getSize() << ",\n";
        std::cout << "    \"row_clues\": [";
        for (uint8_t r = 0; r < tGen.getSize(); r++) {
            if (r > 0) std::cout << ", ";
            std::cout << (int)tGen.getRowClue(r);
        }
        std::cout << "],\n";
        std::cout << "    \"col_clues\": [";
        for (uint8_t c = 0; c < tGen.getSize(); c++) {
            if (c > 0) std::cout << ", ";
            std::cout << (int)tGen.getColClue(c);
        }
        std::cout << "],\n";
        std::cout << "    \"grid\": [";
        for (uint8_t r = 0; r < tGen.getSize(); r++) {
            if (r > 0) std::cout << ", ";
            std::cout << "[";
            for (uint8_t c = 0; c < tGen.getSize(); c++) {
                if (c > 0) std::cout << ", ";
                std::cout << (tGen.isTree(r, c) ? 1 : 0);
            }
            std::cout << "]";
        }
        std::cout << "],\n";
        std::cout << "    \"raster_hex\": \"" << toHex(printer->lastBitmap) << "\"\n";
        std::cout << "  }";
    }

    // 5. STARS (QUEENS)
    {
        QueensGen qGen;
        qGen.generate(QUEENS_MEDIUM);
        printer->lastBitmap.clear();
        qGen.printRasterToReceipt(*printer);

        printSep();
        std::cout << "  {\n";
        std::cout << "    \"puzzle\": \"stars\",\n";
        std::cout << "    \"width\": " << printer->lastWidth << ",\n";
        std::cout << "    \"height\": " << printer->lastHeight << ",\n";
        std::cout << "    \"size\": " << (int)qGen.getSize() << ",\n";
        std::cout << "    \"regions\": [";
        for (uint8_t r = 0; r < qGen.getSize(); r++) {
            if (r > 0) std::cout << ", ";
            std::cout << "[";
            for (uint8_t c = 0; c < qGen.getSize(); c++) {
                if (c > 0) std::cout << ", ";
                std::cout << (int)qGen.getRegion(r, c);
            }
            std::cout << "]";
        }
        std::cout << "],\n";
        std::cout << "    \"raster_hex\": \"" << toHex(printer->lastBitmap) << "\"\n";
        std::cout << "  }";
    }

    // 6. WORD SEARCH
    {
        WordSearchGen wsGen;
        wsGen.generate(WS_MEDIUM, 0);
        printer->lastBitmap.clear();
        wsGen.printRasterToReceipt(*printer);

        printSep();
        std::cout << "  {\n";
        std::cout << "    \"puzzle\": \"wordsearch\",\n";
        std::cout << "    \"width\": " << printer->lastWidth << ",\n";
        std::cout << "    \"height\": " << printer->lastHeight << ",\n";
        std::cout << "    \"theme\": \"" << wsGen.getThemeName() << "\",\n";
        std::cout << "    \"words\": [";
        for (size_t i = 0; i < wsGen.getWordCount(); i++) {
            if (i > 0) std::cout << ", ";
            std::cout << "\"" << wsGen.getPlacedWord(i) << "\"";
        }
        std::cout << "],\n";
        std::cout << "    \"grid\": [";
        for (uint8_t r = 0; r < WordSearchGen::GRID_SIZE; r++) {
            if (r > 0) std::cout << ", ";
            std::cout << "[";
            for (uint8_t c = 0; c < WordSearchGen::GRID_SIZE; c++) {
                if (c > 0) std::cout << ", ";
                std::cout << "\"" << wsGen.getGridChar(r, c) << "\"";
            }
            std::cout << "]";
        }
        std::cout << "],\n";
        std::cout << "    \"raster_hex\": \"" << toHex(printer->lastBitmap) << "\"\n";
        std::cout << "  }";
    }

    // 7. SUDOKU
    {
        SudokuGen sGen;
        sGen.generate(SUDOKU_EASY);
        printer->lastBitmap.clear();
        sGen.printRasterToReceipt(*printer, SUDOKU_EASY);

        printSep();
        std::cout << "  {\n";
        std::cout << "    \"puzzle\": \"sudoku\",\n";
        std::cout << "    \"width\": " << printer->lastWidth << ",\n";
        std::cout << "    \"height\": " << printer->lastHeight << ",\n";
        std::cout << "    \"grid\": [";
        for (uint8_t r = 0; r < 9; r++) {
            if (r > 0) std::cout << ", ";
            std::cout << "[";
            for (uint8_t c = 0; c < 9; c++) {
                if (c > 0) std::cout << ", ";
                std::cout << (int)sGen.getCell(r, c);
            }
            std::cout << "]";
        }
        std::cout << "],\n";
        std::cout << "    \"raster_hex\": \"" << toHex(printer->lastBitmap) << "\"\n";
        std::cout << "  }";
    }

    std::cout << "\n]\n";
    return 0;
}
