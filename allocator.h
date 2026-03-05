#ifndef HEADER
#define HEADER

#include <stdint.h>
#include <stdbool.h> 
#include <stdio.h>
#include <string.h>

typedef uint8_t byte;

// Global variables
extern int block_size;
extern byte *memory;

 
#define DLL_EXPORT __declspec(dllexport) 


// Function prototypes
DLL_EXPORT int CreateMemory();
DLL_EXPORT void DestroyMemory();
DLL_EXPORT bool AllocateMemory(int blockId, byte value);
DLL_EXPORT bool FreeMemory(int byteAddr[2]);

#endif
