#ifndef CSH
#define CSH

#include "shared.h"

void convertIntegerIntoByte(const int data, byte* bytes);

int convertByteIntoInteger(const byte *bytes);

void convertStringIntoByte(const char* data, byte* bytes);

void convertFloatIntoBytes(float value, byte *out) ;

float convertBytesIntoFloat(const byte *in);

#endif