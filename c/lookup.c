#include "lookup.h"

Table globalTable;

void InitGlobalTable(int capacity){
	// Initialize the global lookup table
	globalTable.entries = malloc(sizeof(Entry*) * capacity);
	globalTable.count = 0;
	globalTable.capacity = capacity;
}

Entry* CreateEntryWithoutReg(char *symbol, byte *ptr, int load, DataType dtype){
	// Create an entry and return the entry
	Entry *e = malloc(sizeof(Entry));
	e->symbol = symbol;
	e->ptr = ptr;
	e->load = load;
	e->dtype = dtype;
	return e;
}

void CreateAndRegisterEntry(char *symbol, byte *ptr, int load, DataType dtype){
	// Create and set the entry in table
	Entry *e = CreateEntryWithoutReg(symbol, ptr, load, dtype);
	globalTable.entries[globalTable.count] = e; 
	globalTable.count++;
}

int DeleteEntryWithIndex(int index){
    Table *t = &globalTable;	
    if (index < 0 || index >= t->count) return 1; // Check bounds

    // Free the entry itself
    free(t->entries[index]);

    // Shift everything left
    for (int i = index; i < t->count - 1; i++) {
        t->entries[i] = t->entries[i + 1];
    }

    // Decrement count to account for removed element
    t->count--;
    t->entries[t->count] = NULL;
    return 0;
}

int DeleteEntryWithSymbol(char* sym){
	for(int i = 0; i <= sizeof(globalTable.entries)/sizeof(Entry*); i++){
		if(*globalTable.entries[i]->symbol == *sym){
			if(DeleteEntryWithIndex(i) == 0){return 0;}
			else{return 1;}
		} else {return 1;}
	}
}

Entry* LookUp(char* symbol){
	for(int i = 0; i <= sizeof(globalTable.entries)/sizeof(Entry*); i++){
		if(globalTable.entries[i]->symbol == symbol){
			return globalTable.entries[i];
		} 
	}
}

void ClearMemory(){
	free(globalTable.entries);
}

/*int main(){
	"Test"
	InitGlobalTable(10);
	Table t = globalTable;
	int x =3; int y=5; int z=7; int w = 2;
	CreateAndRegisterEntry("X", &x);	
	CreateAndRegisterEntry("y", &y);
	CreateAndRegisterEntry("z", &z);
	CreateAndRegisterEntry("w", &w);

	int lookupX = *LookUp("X");
	printf("X:%d", lookupX);
	DeleteEntryWithSymbol("X");
	int lookupY = *LookUp("y");
	printf("Y:%d", lookupY);

	ClearMemory();
}*/