#ifndef LOOKUPH

#include "shared.h"

typedef struct{
	Entry **entries;
	int count;
	int capacity;
} Table ; // Lookup table

extern Table globalTable;

void InitGlobalTable(int capacity);

Entry* CreateEntryWithoutReg(char *symbol, byte *ptr, int load, DataType dtype);

void CreateAndRegisterEntry(char *symbol, byte *ptr, int load, DataType dtype);

int DeleteEntryWithIndex(int index);

int DeleteEntryWithSymbol(char* sym);

Entry* LookUp(char* symbol);

void ClearMemory();

#else
#define LOOKUPH
#endif