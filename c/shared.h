#ifndef SHARED_H
#define SHARED_H

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef uint8_t byte;

typedef enum {
    TYPE_INT,
    TYPE_STRING,
    TYPE_FLOAT,
    TYPE_BYTES
} DataType;

typedef struct {
	char *symbol;
	byte *ptr;
	int load;
	DataType dtype;
} Entry; // Define Entry struct

extern const int block_size;

#endif 