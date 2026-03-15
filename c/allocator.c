#include "allocator.h"

const int block_size = 512;
const int totalBlocks = 1024;
const int reservedBlocks = 12;
const int usableBlocks = totalBlocks - reservedBlocks;

byte *memory;

int CreateMemory(){
	memory = (byte *)calloc(0, 1024 * block_size * sizeof(byte));
	if (memory == NULL){
		return 0; // Allocation failed
	} return 1; // Allocation succeded
}

void DestroyMemory(){
	free(memory);
	memory = NULL;
}

void findFirstFreeIndex(int blockId,int payLoad, int *memoryIndex){
	// Takes a blockId and finds the position in the block with payLoad number of free spaces
	int blockIndex = blockId * block_size;
	int flag = 0;
	for (int index = blockIndex; index<blockIndex+block_size; index++){
		if(memory[index] == 0){
			// Check if the byte at index is free
			flag = 1;
			for(int i = 1; i<payLoad; i++){
				// Iterate through the memory for free space
				if(memory[index+i]!=0){
					// Break out of the loop and set flag to 0 if non-continuous
					flag = 0;
					break;
				}
			}
			if(flag == 1){
				*memoryIndex = index;
				return;
			}
		}		
	}	
	
}

byte* AllocateMemory(int blockId, byte value[], size_t dataSize){
	// Sets the first postion with payLoad(number of bytes) amount of free space with value
	if (blockId > usableBlocks){
		return memory+(dataSize-1);
	}
	int memoryIndex = 0;
	findFirstFreeIndex(blockId,dataSize, &memoryIndex);
	for(int i = 0; i < dataSize; i++){
		memory[memoryIndex+i] = value[i];
	}
	return (memory+memoryIndex);
}

int FreeMemory(int byteAddr[2], int byteCount){
	// [BlockId, ByteId], Number of bytes from that position to be removed
	void *start = memory+(byteAddr[0]*block_size)+(byteAddr[1]);
	memset(start, 0, byteCount);
	return 1;
}

byte* RetrieveData(int byteAddr[2], int byteCount){
	byte *start = memory+(byteAddr[0]*block_size)+(byteAddr[1]);
	byte *data = malloc(sizeof(byte)*byteCount);
	for(int i = 0; i<byteCount; i++){
		data[i] = *(start + i);
	}
	return data;
}

byte* RetrieveDataFromPtr(byte* ptr, int byteCount){
	byte *data = malloc(sizeof(byte)*byteCount);
	for(int i = 0; i<byteCount; i++){
		data[i] = *(ptr + i);
	}
	return data;
}