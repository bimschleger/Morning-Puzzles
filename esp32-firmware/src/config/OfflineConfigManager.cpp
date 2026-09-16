#include "OfflineConfigManager.h"
#include "config.h"

OfflineConfigManager::OfflineConfigManager() :
    _gameMask(0xFFFF),
    _puzzleCount(5),
    _puzzleGrade(GRADE_ESCALATING),
    _dailyScheduleEnabled(DAILY_PRINT_ENABLED_DEFAULT),
    _dailyScheduleHour(DAILY_PRINT_HOUR_DEFAULT),
    _dailyScheduleMinute(DAILY_PRINT_MINUTE_DEFAULT) {
}

void OfflineConfigManager::begin() {
    _prefs.begin("mp_config", false);
    _gameMask = _prefs.getUShort("mask", 0xFFFF);
    _puzzleCount = _prefs.getUChar("count", 5);
    uint8_t savedGrade = _prefs.getUChar("grade", (uint8_t)GRADE_ESCALATING);
    _puzzleGrade = (PuzzleGrade)savedGrade;
    _dailyScheduleEnabled = _prefs.getBool("daily_en", DAILY_PRINT_ENABLED_DEFAULT);
    _dailyScheduleHour = _prefs.getUChar("daily_hr", DAILY_PRINT_HOUR_DEFAULT);
    _dailyScheduleMinute = _prefs.getUChar("daily_min", DAILY_PRINT_MINUTE_DEFAULT);

    // Validate mask (ensure at least 1 game is enabled)
    if ((_gameMask & 0xFFFF) == 0) {
        _gameMask = 0xFFFF;
    }

    // Validate count
    uint8_t enabledCount = getEnabledGameCount();
    if (_puzzleCount < 1) _puzzleCount = 1;
    if (_puzzleCount > enabledCount) _puzzleCount = enabledCount;

    // Validate grade
    if (_puzzleGrade > GRADE_EXTREME) {
        _puzzleGrade = GRADE_ESCALATING;
    }

    // Validate daily schedule
    if (_dailyScheduleHour > 23) _dailyScheduleHour = DAILY_PRINT_HOUR_DEFAULT;
    if (_dailyScheduleMinute > 59) _dailyScheduleMinute = DAILY_PRINT_MINUTE_DEFAULT;
}

void OfflineConfigManager::save() {
    _prefs.putUShort("mask", _gameMask);
    _prefs.putUChar("count", _puzzleCount);
    _prefs.putUChar("grade", (uint8_t)_puzzleGrade);
    _prefs.putBool("daily_en", _dailyScheduleEnabled);
    _prefs.putUChar("daily_hr", _dailyScheduleHour);
    _prefs.putUChar("daily_min", _dailyScheduleMinute);
}

void OfflineConfigManager::resetToDefaults() {
    _gameMask = 0xFFFF;
    _puzzleCount = 5;
    _puzzleGrade = GRADE_ESCALATING;
    _dailyScheduleEnabled = DAILY_PRINT_ENABLED_DEFAULT;
    _dailyScheduleHour = DAILY_PRINT_HOUR_DEFAULT;
    _dailyScheduleMinute = DAILY_PRINT_MINUTE_DEFAULT;
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
    if ((_gameMask & 0xFFFF) == 0) {
        _gameMask = (1 << (uint8_t)type);
    }
    // Re-clamp puzzle count
    uint8_t enabledCount = getEnabledGameCount();
    if (_puzzleCount > enabledCount) {
        _puzzleCount = enabledCount;
    }
}

void OfflineConfigManager::setGameMask(uint16_t mask) {
    uint16_t validMask = mask & 0xFFFF;
    if (validMask == 0) validMask = 0xFFFF;
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

void OfflineConfigManager::setDailyScheduleEnabled(bool enabled) {
    _dailyScheduleEnabled = enabled;
}

void OfflineConfigManager::setDailyScheduleHour(uint8_t hour) {
    if (hour > 23) hour = 23;
    _dailyScheduleHour = hour;
}

void OfflineConfigManager::setDailyScheduleMinute(uint8_t min) {
    if (min > 59) min = 59;
    _dailyScheduleMinute = min;
}

String OfflineConfigManager::getDailyScheduleTimeString() const {
    if (!_dailyScheduleEnabled) {
        return "Disabled";
    }
    uint8_t h = _dailyScheduleHour;
    uint8_t m = _dailyScheduleMinute;
    const char* ampm = (h >= 12) ? "PM" : "AM";
    uint8_t displayH = h % 12;
    if (displayH == 0) displayH = 12;
    char buf[16];
    snprintf(buf, sizeof(buf), "%02d:%02d %s", displayH, m, ampm);
    return String(buf);
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
        case PUZZLE_WORDSEARCH: return "Search";
        case PUZZLE_NONOGRAM:   return "Nonogram";
        case PUZZLE_QUEENS:     return "Stars";
        case PUZZLE_JUMBLE:     return "Jumble";
        case PUZZLE_BINARY:     return "Binary";
        case PUZZLE_MINES:      return "Mines";
        case PUZZLE_TENTS:      return "Tents";
        case PUZZLE_BRIDGES:    return "Bridges";
        case PUZZLE_TANGO:      return "Tango";
        case PUZZLE_WHEEL:      return "Wheel";
        case PUZZLE_LIGHTS:     return "Lights";
        case PUZZLE_LOOP:       return "Loop";
        case PUZZLE_KILLER:     return "Killer";
        case PUZZLE_CRYPTOGRAM: return "Cryptogram";
        case PUZZLE_LADDER:     return "Ladder";
        default:                return "Unknown Puzzle";
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
