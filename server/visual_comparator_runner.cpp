#include "Arduino.h"
#include "WiFi.h"
#include "WiFiClient.h"
#include "HardwareSerial.h"

#include "../esp32-firmware/src/printer/EscPosPrinter.h"
#include "../esp32-firmware/src/printer/EscPosPrinter.cpp"
#include "../esp32-firmware/src/printer/qrcode.h"
#include "../esp32-firmware/src/printer/qrcode.c"
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

#include "../esp32-firmware/src/generators/LoopGen.h"
#include "../esp32-firmware/src/generators/LoopGen.cpp"

#include "../esp32-firmware/src/generators/NonogramGen.h"
#include "../esp32-firmware/src/generators/NonogramGen.cpp"

#include "../esp32-firmware/src/generators/LightsGen.h"
#include "../esp32-firmware/src/generators/LightsGen.cpp"

#include "../esp32-firmware/src/generators/KillerGen.h"
#include "../esp32-firmware/src/generators/KillerGen.cpp"

#include "../esp32-firmware/src/generators/CryptogramDataset.h"
#include "../esp32-firmware/src/generators/CryptogramGen.h"
#include "../esp32-firmware/src/generators/CryptogramGen.cpp"

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
    void print(const char*) {}
    void println(const char* = "") {}
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

    // 6. WORD SEARCH (Medium, 12x12)
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
        for (uint8_t r = 0; r < wsGen.getGridSize(); r++) {
            if (r > 0) std::cout << ", ";
            std::cout << "[";
            for (uint8_t c = 0; c < wsGen.getGridSize(); c++) {
                if (c > 0) std::cout << ", ";
                std::cout << "\"" << wsGen.getGridChar(r, c) << "\"";
            }
            std::cout << "]";
        }
        std::cout << "],\n";
        std::cout << "    \"raster_hex\": \"" << toHex(printer->lastBitmap) << "\"\n";
        std::cout << "  }";
    }

    // 6b. WORD SEARCH (Easy, 10x10)
    {
        WordSearchGen wsGenEasy;
        wsGenEasy.generate(WS_EASY, 0);
        printer->lastBitmap.clear();
        wsGenEasy.printRasterToReceipt(*printer);

        printSep();
        std::cout << "  {\n";
        std::cout << "    \"puzzle\": \"wordsearch_easy\",\n";
        std::cout << "    \"width\": " << printer->lastWidth << ",\n";
        std::cout << "    \"height\": " << printer->lastHeight << ",\n";
        std::cout << "    \"theme\": \"" << wsGenEasy.getThemeName() << "\",\n";
        std::cout << "    \"words\": [";
        for (size_t i = 0; i < wsGenEasy.getWordCount(); i++) {
            if (i > 0) std::cout << ", ";
            std::cout << "\"" << wsGenEasy.getPlacedWord(i) << "\"";
        }
        std::cout << "],\n";
        std::cout << "    \"grid\": [";
        for (uint8_t r = 0; r < wsGenEasy.getGridSize(); r++) {
            if (r > 0) std::cout << ", ";
            std::cout << "[";
            for (uint8_t c = 0; c < wsGenEasy.getGridSize(); c++) {
                if (c > 0) std::cout << ", ";
                std::cout << "\"" << wsGenEasy.getGridChar(r, c) << "\"";
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

    // 8. LOOP
    {
        LoopGen loopGen;
        loopGen.generate(LOOP_MEDIUM);
        printer->lastBitmap.clear();
        loopGen.printRasterToReceipt(*printer, LOOP_MEDIUM);

        printSep();
        std::cout << "  {\n";
        std::cout << "    \"puzzle\": \"loop\",\n";
        std::cout << "    \"difficulty\": \"medium\",\n";
        std::cout << "    \"width\": " << printer->lastWidth << ",\n";
        std::cout << "    \"height\": " << printer->lastHeight << ",\n";
        std::cout << "    \"size\": " << (int)loopGen.getSize() << ",\n";
        std::cout << "    \"clues\": [";
        for (uint8_t r = 0; r < loopGen.getSize(); r++) {
            if (r > 0) std::cout << ", ";
            std::cout << "[";
            for (uint8_t c = 0; c < loopGen.getSize(); c++) {
                if (c > 0) std::cout << ", ";
                std::cout << (int)loopGen.getClue(r, c);
            }
            std::cout << "]";
        }
        std::cout << "],\n";
        std::cout << "    \"raster_hex\": \"" << toHex(printer->lastBitmap) << "\"\n";
        std::cout << "  }";
    }

    // 9. NONOGRAM
    {
        NonogramGen nGen;
        nGen.generate(NONO_MEDIUM);
        printer->lastBitmap.clear();
        nGen.printRasterToReceipt(*printer);

        printSep();
        std::cout << "  {\n";
        std::cout << "    \"puzzle\": \"nonogram\",\n";
        std::cout << "    \"width\": " << printer->lastWidth << ",\n";
        std::cout << "    \"height\": " << printer->lastHeight << ",\n";
        std::cout << "    \"size\": " << (int)nGen.getSize() << ",\n";
        std::cout << "    \"row_clues\": [";
        for (uint8_t r = 0; r < nGen.getSize(); r++) {
            if (r > 0) std::cout << ", ";
            std::cout << "[";
            const auto& rc = nGen.getRowClues(r);
            for (size_t i = 0; i < rc.size(); i++) {
                if (i > 0) std::cout << ", ";
                std::cout << (int)rc[i];
            }
            std::cout << "]";
        }
        std::cout << "],\n";
        std::cout << "    \"col_clues\": [";
        for (uint8_t c = 0; c < nGen.getSize(); c++) {
            if (c > 0) std::cout << ", ";
            std::cout << "[";
            const auto& cc = nGen.getColClues(c);
            for (size_t i = 0; i < cc.size(); i++) {
                if (i > 0) std::cout << ", ";
                std::cout << (int)cc[i];
            }
            std::cout << "]";
        }
        std::cout << "],\n";
        std::cout << "    \"raster_hex\": \"" << toHex(printer->lastBitmap) << "\"\n";
        std::cout << "  }";
    }

    // 10. LIGHTS
    {
        LightsGen lGen;
        lGen.generate(LIGHTS_EASY);
        printer->lastBitmap.clear();
        lGen.printRasterToReceipt(*printer, LIGHTS_EASY);

        printSep();
        std::cout << "  {\n";
        std::cout << "    \"puzzle\": \"lights\",\n";
        std::cout << "    \"width\": " << printer->lastWidth << ",\n";
        std::cout << "    \"height\": " << printer->lastHeight << ",\n";
        std::cout << "    \"size\": " << (int)lGen.getSize() << ",\n";
        std::cout << "    \"grid\": [";
        for (uint8_t r = 0; r < lGen.getSize(); r++) {
            if (r > 0) std::cout << ", ";
            std::cout << "[";
            for (uint8_t c = 0; c < lGen.getSize(); c++) {
                if (c > 0) std::cout << ", ";
                std::cout << (int)lGen.getCell(r, c);
            }
            std::cout << "]";
        }
        std::cout << "],\n";
        std::cout << "    \"raster_hex\": \"" << toHex(printer->lastBitmap) << "\"\n";
        std::cout << "  }";
    }

    // 11. KILLER
    {
        KillerGen kGen;
        kGen.generate(KILLER_MEDIUM, 42);
        printer->lastBitmap.clear();
        kGen.printRasterToReceipt(*printer);

        printSep();
        std::cout << "  {\n";
        std::cout << "    \"puzzle\": \"killer\",\n";
        std::cout << "    \"difficulty\": \"medium\",\n";
        std::cout << "    \"width\": " << printer->lastWidth << ",\n";
        std::cout << "    \"height\": " << printer->lastHeight << ",\n";
        std::cout << "    \"size\": " << (int)kGen.getSize() << ",\n";
        std::cout << "    \"box_rows\": " << (int)kGen.getBoxRows() << ",\n";
        std::cout << "    \"box_cols\": " << (int)kGen.getBoxCols() << ",\n";
        std::cout << "    \"cages\": [\n";
        for (uint8_t i = 0; i < kGen.getNumCages(); i++) {
            if (i > 0) std::cout << ",\n";
            std::cout << "      {\"id\": " << (int)i << ", \"sum\": " << (int)kGen.getCageSum(i) << ", \"cells\": [";
            bool firstCell = true;
            for (uint8_t r = 0; r < kGen.getSize(); r++) {
                for (uint8_t c = 0; c < kGen.getSize(); c++) {
                    if (kGen.getCage(r, c) == i) {
                        if (!firstCell) std::cout << ", ";
                        std::cout << "[" << (int)r << ", " << (int)c << "]";
                        firstCell = false;
                    }
                }
            }
            std::cout << "]}";
        }
        std::cout << "\n    ],\n";
        std::cout << "    \"raster_hex\": \"" << toHex(printer->lastBitmap) << "\"\n";
        std::cout << "  }";
    }

    // 12. CRYPTOGRAM
    {
        CryptogramGen cGen;
        cGen.generateWithQuote("ACTIONS SPEAK LOUDER THAN WORDS.", "PROVERB", CRYPTO_EASY, 42);
        printer->lastBitmap.clear();
        cGen.printRasterToReceipt(*printer);

        printSep();
        std::cout << "  {\n";
        std::cout << "    \"puzzle\": \"cryptogram\",\n";
        std::cout << "    \"difficulty\": \"easy\",\n";
        std::cout << "    \"width\": " << printer->lastWidth << ",\n";
        std::cout << "    \"height\": " << printer->lastHeight << ",\n";
        std::cout << "    \"phrase\": \"" << cGen.getPhrase() << "\",\n";
        std::cout << "    \"author\": \"" << cGen.getAuthor() << "\",\n";
        std::cout << "    \"ciphertext\": \"" << cGen.getCiphertext() << "\",\n";
        std::cout << "    \"raster_hex\": \"" << toHex(printer->lastBitmap) << "\"\n";
        std::cout << "  }";
    }

    std::cout << "\n]\n";
    return 0;
}
