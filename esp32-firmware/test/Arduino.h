#ifndef ARDUINO_MOCK_H
#define ARDUINO_MOCK_H

#include <iostream>
#include <string>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <cstring>
#include <cstdint>
#include <algorithm>
#include <sstream>

#define PROGMEM
#define memcpy_P memcpy
#define pgm_read_byte(addr) (*(const uint8_t*)(addr))
#define pgm_read_word(addr) (*(const uint16_t*)(addr))
class String : public std::string {
public:
    String() : std::string() {}
    String(const char* s) : std::string(s ? s : "") {}
    String(const std::string& s) : std::string(s) {}
    String(char c) : std::string(1, c) {}
    String(int v) : std::string(std::to_string(v)) {}
    String(unsigned int v) : std::string(std::to_string(v)) {}
    String(long v) : std::string(std::to_string(v)) {}
    String(unsigned long v) : std::string(std::to_string(v)) {}

    const char* c_str() const { return std::string::c_str(); }
};

inline String operator+(const String& lhs, const String& rhs) {
    return String(static_cast<const std::string&>(lhs) + static_cast<const std::string&>(rhs));
}
inline String operator+(const char* lhs, const String& rhs) {
    return String(std::string(lhs) + static_cast<const std::string&>(rhs));
}
inline String operator+(const String& lhs, const char* rhs) {
    return String(static_cast<const std::string&>(lhs) + std::string(rhs));
}
inline String operator+(const String& lhs, char rhs) {
    return String(static_cast<const std::string&>(lhs) + std::string(1, rhs));
}
inline String operator+(char lhs, const String& rhs) {
    return String(std::string(1, lhs) + static_cast<const std::string&>(rhs));
}

inline std::ostream& operator<<(std::ostream& os, const String& s) {
    return os << s.c_str();
}

inline long random(long max) { return (max > 0) ? (std::rand() % max) : 0; }
inline long random(long min, long max) { return min + random(max - min); }
inline uint32_t esp_random() { return (uint32_t)std::rand(); }
inline void randomSeed(unsigned long seed) { std::srand(seed); }
inline unsigned long millis() { return (unsigned long)(clock() * 1000 / CLOCKS_PER_SEC); }
inline unsigned long micros() { return (unsigned long)(clock() * 1000000 / CLOCKS_PER_SEC); }
inline void delay(int ms) {}

typedef uint8_t byte;

class SerialMock {
public:
    void print(const String& s) { std::cout << s; }
    void println(const String& s = "") { std::cout << s << std::endl; }
    template<typename... Args>
    void printf(const char* fmt, Args... args) { ::printf(fmt, args...); }
};

static SerialMock Serial;

#endif // ARDUINO_MOCK_H
