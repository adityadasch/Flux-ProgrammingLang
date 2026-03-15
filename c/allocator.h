#ifndef HEADER
#define HEADER

#include "shared.h"
#include <corecrt.h>

int CreateMemory();
void DestroyMemory();

void findFirstFreeIndex(int blockId,int payLoad, int *memoryIndex);
byte* AllocateMemory(int blockId, byte value[], size_t dataSize);
int FreeMemory(int byteAddr[2], int byteCount);
byte* RetrieveData(int byteAddr[2], int byteCount);
byte* RetrieveDataFromPtr(byte* ptr, int byteCount);

#endif