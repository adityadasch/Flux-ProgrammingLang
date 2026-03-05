#include allocator.h

block_size = 512;
totalBlocks = 1024;
reservedBlocks = 12;
usableBlocks = totalBlocks - reservedBlocks;

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
	for (index = blockIndex; index<blockIndex+block_size, index++){
		if(memory[index] == 0){
			// Check if the byte at index is free
			flag = 1;
			for(int i = 1; i<payload; i++){
				// Iterate through the memory for free space
				if(memory[index+i]!=0){
					// Break out of the loop and set flag to 0 if non-continuous
					flag = 0;
					break
				}
			}
			if(flag == 1){
				memoryIndex = index;
				return;
			}
		}		
	}	
	
}

int AllocateMemory(int blockId, byte value){
	// Sets the first postion with payLoad(number of bytes) amount of free space with value
	if (blockId > usableBlocks){
		return 0;
	}
	int memoryIndex = 0;
	findFirstFreeIndex(blockId,sizeof(value)/sizeof(value[0]), &memoryIndex);
	memory[memoryIndex] = value;
	return 1;
}

int FreeMemory(int byteAddr[2], int byteCount){
	// [BlockId, ByteId], Number of bytes from that position to be removed
	void *start = memory+(byteAddr[0]*block_size)+(byteAddr[1]);
	memset(start, 0, byteCount);
}
