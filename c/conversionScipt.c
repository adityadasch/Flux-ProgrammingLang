#include "conversionScript.h"

void convertIntegerIntoByte(const int data, byte* bytes){
    bytes[0] = (data >> 24) & 0xFF;
    bytes[1] = (data >> 16) & 0xFF;
    bytes[2] = (data >> 8) & 0xFF;
    bytes[3] = data & 0xFF;
}

int convertByteIntoInteger(const byte *bytes) {
    return (bytes[0] << 24) |
           (bytes[1] << 16) |
           (bytes[2] << 8)  |
           (bytes[3]);
}

void convertStringIntoByte(const char* data, byte* bytes){
    // Return bytes through buffer
    while (*data) {
        *bytes++ = (byte)*data++;
    } 
}

void convertFloatIntoBytes(float value, byte *out) {
    memcpy(out, &value, sizeof(float));
}

float convertBytesIntoFloat(const byte *in) {
    float value;
    memcpy(&value, in, sizeof(float));
    return value;
}


/*int main(){
    float data = 22.6f;
    byte bytes[4]; // All elements + null

    convertFloatIntoBytes(data, bytes);

    printf("%02X %02X %02X %02X\n", bytes[0], bytes[1], bytes[2], bytes[3]);
    
    printf("%f", convertBytesIntoFloat(bytes));
}*/