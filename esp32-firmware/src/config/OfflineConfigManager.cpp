#include "OfflineConfigManager.h"

OfflineConfigManager::OfflineConfigManager() :
    _gameMask(0x1FFF),
    _puzzleCount(5),
    _puzzleGrade(GRADE_ESCALATING) {
}

void OfflineConfigManager::begin() {
    _prefs.begin("mp_config", false);
    _gameMask = _prefs.getUShort("mask", 0x1FFF);
    _puzzleCount = _prefs.getUChar("count", 5);
    uint8_t savedGrade = _prefs.getUChar("grade", (uint8_t)GRADE_ESCALATING);
    _puzzleGrade = (PuzzleGrade)savedGrade;

    // Validate mask (ensure at least 1 game is enabled)
    if ((_gameMask & 0x1FFF) == 0) {
        _gameMask = 0x1FFF;
    }

    // Validate count
    uint8_t enabledCount = getEnabledGameCount();
    if (_puzzleCount < 1) _puzzleCount = 1;
    if (_puzzleCount > enabledCount) _puzzleCount = enabledCount;

    // Validate grade
    if (_puzzleGrade > GRADE_EXTREME) {
        _puzzleGrade = GRADE_ESCALATING;
    }
}

void OfflineConfigManager::save() {
    _prefs.putUShort("mask", _gameMask);
    _prefs.putUChar("count", _puzzleCount);
    _prefs.putUChar("grade", (uint8_t)_puzzleGrade);
}

void OfflineConfigManager::resetToDefaults() {
    _gameMask = 0x1FFF;
    _puzzleCount = 5;
    _puzzleGrade = GRADE_ESCALATING;
    save();
}

bool OfflineConfigManager::isGameEnabled(OfflinePuzzleType type) const {
    if ((uint8_t)type >= OFFLINE_PUZZLE_TOTAL) return false;
    return (_gameMask & (1 << (uint8_t)type)) != 0;
}

void OfflineConfigManager::setGameEnabled(OfflinePuzzleType type, bool enabled) {
    if ((uint8_t)type >= OFFLINE_PUZZLE_TOTAL) return;
    if (enabled) {
        _gameMask |= (1 << (uint8_t)type);
    } else {
        _gameMask &= ~(1 << (uint8_t)type);
    }
    // Guard against all disabled
    if ((_gameMask & 0x1FFF) == 0) {
        _gameMask = (1 << (uint8_t)type);
    }
    // Re-clamp puzzle count
    uint8_t enabledCount = getEnabledGameCount();
    if (_puzzleCount > enabledCount) {
        _puzzleCount = enabledCount;
    }
}

void OfflineConfigManager::setGameMask(uint16_t mask) {
    uint16_t validMask = mask & 0x1FFF;
    if (validMask == 0) validMask = 0x1FFF;
    _gameMask = validMask;

    uint8_t enabledCount = getEnabledGameCount();
    if (_puzzleCount > enabledCount) {
        _puzzleCount = enabledCount;
    }
}

void OfflineConfigManager::setPuzzleCount(uint8_t count) {
    uint8_t enabledCount = getEnabledGameCount();
    if (count < 1) count = 1;
    if (count > enabledCount) count = enabledCount;
    _puzzleCount = count;
}

void OfflineConfigManager::setPuzzleGrade(PuzzleGrade grade) {
    if (grade > GRADE_EXTREME) grade = GRADE_ESCALATING;
    _puzzleGrade = grade;
}

uint8_t OfflineConfigManager::getEnabledGameCount() const {
    uint8_t count = 0;
    for (uint8_t i = 0; i < (uint8_t)OFFLINE_PUZZLE_TOTAL; i++) {
        if (_gameMask & (1 << i)) count++;
    }
    return count;
}

uint8_t OfflineConfigManager::getEnabledPuzzles(OfflinePuzzleType* outBuffer, uint8_t maxCapacity) const {
    if (!outBuffer || maxCapacity == 0) return 0;
    uint8_t count = 0;
    for (uint8_t i = 0; i < (uint8_t)OFFLINE_PUZZLE_TOTAL && count < maxCapacity; i++) {
        if (_gameMask & (1 << i)) {
            outBuffer[count++] = (OfflinePuzzleType)i;
        }
    }
    return count;
}

const char* OfflineConfigManager::getPuzzleName(OfflinePuzzleType type) const {
    switch (type) {
        case PUZZLE_SUDOKU:     return "Sudoku";
        case PUZZLE_WORDSEARCH: return "Word Search";
        case PUZZLE_NONOGRAM:   return "Nonogram";
        case PUZZLE_QUEENS:     return "Queens";
        case PUZZLE_JUMBLE:     return "Daily Jumble";
        case PUZZLE_BINARY:     return "Binary Grid";
        case PUZZLE_MINES:      return "Minesweeper";
        case PUZZLE_TENTS:      return "Tents & Trees";
        case PUZZLE_BRIDGES:    return "Bridges";
        case PUZZLE_TANGO:      return "Tango";
        case PUZZLE_WHEEL:      return "Word Wheel";
        case PUZZLE_LIGHTS:     return "Lights Out";
        case PUZZLE_LOOP:       return "Numberlink Loop";
        default:                return "Unknown Puzzle";
    }
}

const char* OfflineConfigManager::getPuzzleCategory(OfflinePuzzleType type) const {
    switch (type) {
        case PUZZLE_SUDOKU:     return "Number Placement";
        case PUZZLE_WORDSEARCH: return "Word Puzzle";
        case PUZZLE_NONOGRAM:   return "Picture Logic";
        case PUZZLE_QUEENS:     return "Grid Logic";
        case PUZZLE_JUMBLE:     return "Word Puzzle";
        case PUZZLE_BINARY:     return "Binary Logic";
        case PUZZLE_MINES:      return "Deduction";
        case PUZZLE_TENTS:      return "Grid Logic";
        case PUZZLE_BRIDGES:    return "Network Logic";
        case PUZZLE_TANGO:      return "Grid Logic";
        case PUZZLE_WHEEL:      return "Word Puzzle";
        case PUZZLE_LIGHTS:     return "Illumination";
        case PUZZLE_LOOP:       return "Path Puzzle";
        default:                return "Logic";
    }
}

const char* OfflineConfigManager::getGradeName(PuzzleGrade grade) const {
    switch (grade) {
        case GRADE_EASY:       return "EASY";
        case GRADE_HARD:       return "HARD";
        case GRADE_ROTATING:   return "ROTATING";
        case GRADE_ESCALATING: return "ESCALATING";
        case GRADE_EXTREME:    return "EXTREME";
        case GRADE_MEDIUM:
        default:               return "MEDIUM";
    }
}
