#include "MemoryManager.h"

Meta meta = {0};

char *bytes_to_bitstring(byte *data, size_t len) {
    // Each byte -> 8 bits, plus null terminator
    char *bitstr = malloc(len * 8 + 1);
    if (!bitstr) return NULL;

    for (size_t i = 0; i < len; i++) {
        for (int b = 7; b >= 0; b--) {
            bitstr[i*8 + (7-b)] = ((data[i] >> b) & 1) ? '1' : '0';
        }
    }
    bitstr[len*8] = '\0';
    return bitstr;
}

DLLE void CreateAllMemory(){
    CreateMemory();
    InitGlobalTable(1000);
}

DLLE void CreateEntry(char* symbol, byte value[], int load, DataType dtype){
    byte *ptr = AllocateMemory(meta.currentBlock, value, load);
    CreateAndRegisterEntry(symbol, ptr, load, dtype);
}

DLLE void CreateEntryFromInteger(char* symbol, int value, int load, DataType dtype){
    byte data[load];
    convertIntegerIntoByte(value, data);
    CreateEntry(symbol, data, load, dtype);
}

DLLE void CreateEntryFromFloat(char* symbol, float value, int load, DataType dtype){
    byte data[4];
    convertFloatIntoBytes(value, data);
    CreateEntry(symbol, data, load, dtype);
}

DLLE void CreateEntryFromString(char* symbol, const char* value, int load, DataType dtype){
    byte data[load+1];
    convertStringIntoByte(value, data);
    CreateEntry(symbol, data, load, dtype);
}

DLLE EntryData RetrieveEntryData(char* symbol){
    Entry *e = LookUp(symbol);
    byte* data = RetrieveDataFromPtr(e->ptr, e->load);
    EntryData ed;
    ed.bitString = bytes_to_bitstring(data, e->load);
    ed.value = data;
    ed.load = e->load;
    ed.ptr = e->ptr;
    return ed;
}

DLLE EntryData RetrieveEntryDataAsInteger(char* symbol){
    EntryData ed = RetrieveEntryData(symbol);
    ed.intValue = convertByteIntoInteger(ed.value);
    return ed;
}

DLLE EntryData RetrieveEntryDataAsFloat(char* symbol){
    EntryData ed = RetrieveEntryData(symbol);
    ed.floatValue = convertBytesIntoFloat(ed.value);
    return ed;
}

