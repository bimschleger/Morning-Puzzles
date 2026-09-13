#ifndef SPI_MOCK_H
#define SPI_MOCK_H
#include "Arduino.h"

class SPIClass {
public:
    void begin(int sck=-1, int miso=-1, int mosi=-1, int ss=-1) {}
};

static SPIClass SPI;

#endif // SPI_MOCK_H
