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
    void clear() { _data.clear(); }

    uint16_t getUShort(const char* key, uint16_t defaultValue = 0) {
        if (_data.find(key) != _data.end()) return (uint16_t)_data[key];
        return defaultValue;
    }
    size_t putUShort(const char* key, uint16_t value) {
        _data[key] = value;
        return 2;
    }

    uint8_t getUChar(const char* key, uint8_t defaultValue = 0) {
        if (_data.find(key) != _data.end()) return (uint8_t)_data[key];
        return defaultValue;
    }
    size_t putUChar(const char* key, uint8_t value) {
        _data[key] = value;
        return 1;
    }

private:
    bool _started;
    std::map<std::string, uint32_t> _data;
};

#endif // PREFERENCES_MOCK_H
