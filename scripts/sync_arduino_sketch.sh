#!/usr/bin/env bash
set -e

# ==============================================================================
# Synchronize esp32-firmware into Arduino IDE MorningPuzzles sketch folder
# ==============================================================================

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKETCH_DIR="$ROOT_DIR/MorningPuzzles"
FW_DIR="$ROOT_DIR/esp32-firmware"

echo "Syncing esp32-firmware -> MorningPuzzles Arduino sketch..."
mkdir -p "$SKETCH_DIR"

# Copy config, drivers, generators, and main sketch
cp "$FW_DIR/include/config.h" "$SKETCH_DIR/"
cp "$FW_DIR/src/config/"* "$SKETCH_DIR/"
cp "$FW_DIR/src/printer/"* "$SKETCH_DIR/"
cp "$FW_DIR/src/time/"* "$SKETCH_DIR/"
cp "$FW_DIR/src/generators/"* "$SKETCH_DIR/"
cp "$FW_DIR/src/main.cpp" "$SKETCH_DIR/MorningPuzzles.ino"

# Flatten relative include paths for Arduino IDE single-folder compilation
if [[ "$OSTYPE" == "darwin"* ]]; then
  sed -i '' 's|#include "../printer/EscPosPrinter.h"|#include "EscPosPrinter.h"|g' "$SKETCH_DIR"/*.h
  sed -i '' 's|#include "../printer/EscPosPrinter.h"|#include "EscPosPrinter.h"|g' "$SKETCH_DIR"/*.cpp
  sed -i '' 's|#include "../printer/ThermalCanvas.h"|#include "ThermalCanvas.h"|g' "$SKETCH_DIR"/*.h
  sed -i '' 's|#include "../printer/ThermalCanvas.h"|#include "ThermalCanvas.h"|g' "$SKETCH_DIR"/*.cpp
  sed -i '' 's|#include "../config/OfflineConfigManager.h"|#include "OfflineConfigManager.h"|g' "$SKETCH_DIR"/*.h
  sed -i '' 's|#include "../config/OfflineConfigManager.h"|#include "OfflineConfigManager.h"|g' "$SKETCH_DIR"/*.cpp
  sed -i '' 's|#include "../config.h"|#include "config.h"|g' "$SKETCH_DIR"/*.h
  sed -i '' 's|#include "../config.h"|#include "config.h"|g' "$SKETCH_DIR"/*.cpp
  sed -i '' 's|#include "printer/EscPosPrinter.h"|#include "EscPosPrinter.h"|g' "$SKETCH_DIR"/MorningPuzzles.ino
  sed -i '' 's|#include "time/OfflineTimeManager.h"|#include "OfflineTimeManager.h"|g' "$SKETCH_DIR"/MorningPuzzles.ino
  sed -i '' 's|#include "config/OfflineConfigManager.h"|#include "OfflineConfigManager.h"|g' "$SKETCH_DIR"/MorningPuzzles.ino
  sed -i '' 's|#include "generators/OfflinePuzzleComposer.h"|#include "OfflinePuzzleComposer.h"|g' "$SKETCH_DIR"/MorningPuzzles.ino
else
  sed -i 's|#include "../printer/EscPosPrinter.h"|#include "EscPosPrinter.h"|g' "$SKETCH_DIR"/*.h
  sed -i 's|#include "../printer/EscPosPrinter.h"|#include "EscPosPrinter.h"|g' "$SKETCH_DIR"/*.cpp
  sed -i 's|#include "../printer/ThermalCanvas.h"|#include "ThermalCanvas.h"|g' "$SKETCH_DIR"/*.h
  sed -i 's|#include "../printer/ThermalCanvas.h"|#include "ThermalCanvas.h"|g' "$SKETCH_DIR"/*.cpp
  sed -i 's|#include "../config/OfflineConfigManager.h"|#include "OfflineConfigManager.h"|g' "$SKETCH_DIR"/*.h
  sed -i 's|#include "../config/OfflineConfigManager.h"|#include "OfflineConfigManager.h"|g' "$SKETCH_DIR"/*.cpp
  sed -i 's|#include "../config.h"|#include "config.h"|g' "$SKETCH_DIR"/*.h
  sed -i 's|#include "../config.h"|#include "config.h"|g' "$SKETCH_DIR"/*.cpp
  sed -i 's|#include "printer/EscPosPrinter.h"|#include "EscPosPrinter.h"|g' "$SKETCH_DIR"/MorningPuzzles.ino
  sed -i 's|#include "time/OfflineTimeManager.h"|#include "OfflineTimeManager.h"|g' "$SKETCH_DIR"/MorningPuzzles.ino
  sed -i 's|#include "config/OfflineConfigManager.h"|#include "OfflineConfigManager.h"|g' "$SKETCH_DIR"/MorningPuzzles.ino
  sed -i 's|#include "generators/OfflinePuzzleComposer.h"|#include "OfflinePuzzleComposer.h"|g' "$SKETCH_DIR"/MorningPuzzles.ino
fi

echo "Successfully synchronized MorningPuzzles Arduino sketch!"
