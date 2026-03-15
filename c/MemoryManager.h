#ifndef MMH
#define MMH
#include "shared.h"
#include "allocator.h"
#include "lookup.h"
#include "conversionScript.h"

#ifdef _WIN32
#define DLLE __declspec(dllexport)
#else
#define DLLE
#endif

typedef struct {
    int currentBlock;
} Meta;

typedef struct {
    byte* value;
    byte* ptr;
    char* bitString;
    int load;
    int intValue;
    float floatValue;
} EntryData;

extern Meta meta;

void CreateAllMemory();

void CreateEntry(char* symbol, byte value[], int load, DataType dtype);

void CreateEntryFromInteger(char* symbol, int value, int load, DataType dtype);

void CreateEntryFromFloat(char* symbol, float value, int load, DataType dtype);

void CreateEntryFromString(char* symbol, const char* value, int load, DataType dtype);

EntryData RetrieveEntryData(char* symbol);

EntryData RetrieveEntryDataAsInteger(char* symbol);

EntryData RetrieveEntryDataAsFloat(char* symbol);

#endif