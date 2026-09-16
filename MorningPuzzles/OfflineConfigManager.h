#ifndef OFFLINE_CONFIG_MANAGER_H
#define OFFLINE_CONFIG_MANAGER_H

#include <Arduino.h>
#include <Preferences.h>

enum PuzzleGrade : uint8_t {
    GRADE_EASY = 0,
    GRADE_MEDIUM = 1,
    GRADE_HARD = 2,
    GRADE_ESCALATING = 3,
    GRADE_ROTATING = 4,
    GRADE_RANDOM = GRADE_ESCALATING,
    GRADE_EXTREME = 5
};

enum OfflinePuzzleType : uint8_t {
    PUZZLE_SUDOKU = 0,
    PUZZLE_WORDSEARCH,
    PUZZLE_NONOGRAM,
    PUZZLE_QUEENS,
    PUZZLE_JUMBLE,
    PUZZLE_BINARY,
    PUZZLE_MINES,
    PUZZLE_TENTS,
    PUZZLE_BRIDGES,
    PUZZLE_TANGO,
    PUZZLE_WHEEL,
    PUZZLE_LIGHTS,
    PUZZLE_LOOP,
    PUZZLE_KILLER,
    OFFLINE_PUZZLE_TOTAL
};

class OfflineConfigManager {
public:
    OfflineConfigManager();

    void begin();
    void save();
    void resetToDefaults();

    // Enabled games
    bool isGameEnabled(OfflinePuzzleType type) const;
    void setGameEnabled(OfflinePuzzleType type, bool enabled);
    uint16_t getGameMask() const { return _gameMask; }
    void setGameMask(uint16_t mask);

    // Number of puzzles to draw and print
    uint8_t getPuzzleCount() const { return _puzzleCount; }
    void setPuzzleCount(uint8_t count);

    // Active difficulty grade
    PuzzleGrade getPuzzleGrade() const { return _puzzleGrade; }
    void setPuzzleGrade(PuzzleGrade grade);

    // Daily recurring schedule
    bool isDailyScheduleEnabled() const { return _dailyScheduleEnabled; }
    void setDailyScheduleEnabled(bool enabled);
    uint8_t getDailyScheduleHour() const { return _dailyScheduleHour; }
    void setDailyScheduleHour(uint8_t hour);
    uint8_t getDailyScheduleMinute() const { return _dailyScheduleMinute; }
    void setDailyScheduleMinute(uint8_t min);
    String getDailyScheduleTimeString() const;

    // Helpers
    uint8_t getEnabledGameCount() const;
    uint8_t getEnabledPuzzles(OfflinePuzzleType* outBuffer, uint8_t maxCapacity) const;

    const char* getPuzzleName(OfflinePuzzleType type) const;
    const char* getGradeName(PuzzleGrade grade) const;

private:
    uint16_t    _gameMask;
    uint8_t     _puzzleCount;
    PuzzleGrade _puzzleGrade;
    bool        _dailyScheduleEnabled;
    uint8_t     _dailyScheduleHour;
    uint8_t     _dailyScheduleMinute;
    Preferences _prefs;
};

#endif // OFFLINE_CONFIG_MANAGER_H
