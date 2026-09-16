#ifndef PREFERENCES_MOCK_H
#define PREFERENCES_MOCK_H

#include <cstdint>
#include <string>
#include <map>

class Preferences {
public:
    Preferences() : _started(false) {}
    bool begin(const char* name, bool readOnly = false) {
        _started = true;
        return true;
    }
    void end() { _started = false; }
    static std::map<std::string, uint32_t>& storage() {
        static std::map<std::string, uint32_t> s;
        return s;
    }

    void clear() { storage().clear(); }

    uint16_t getUShort(const char* key, uint16_t defaultValue = 0) {
        if (storage().find(key) != storage().end()) return (uint16_t)storage()[key];
        return defaultValue;
    }
    size_t putUShort(const char* key, uint16_t value) {
        storage()[key] = value;
        return 2;
    }

    uint8_t getUChar(const char* key, uint8_t defaultValue = 0) {
        if (storage().find(key) != storage().end()) return (uint8_t)storage()[key];
        return defaultValue;
    }
    size_t putUChar(const char* key, uint8_t value) {
        storage()[key] = value;
        return 1;
    }

    bool getBool(const char* key, bool defaultValue = false) {
        if (storage().find(key) != storage().end()) return storage()[key] != 0;
        return defaultValue;
    }
    size_t putBool(const char* key, bool value) {
        storage()[key] = value ? 1 : 0;
        return 1;
    }

private:
    bool _started;
};

#endif // PREFERENCES_MOCK_H
