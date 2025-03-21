#include "functions.c"

void initializeMemory (int memSize, struct space *mem){
    //setup struct fields
    mem->memory = malloc(memSize * sizeof(char));
    mem->sizes = malloc(memSize * sizeof(int));
    mem->len = memSize;

    //set all memory and sizes to free
    int i = 0;
    while (i < mem->len) {
        *(mem->memory + i) = FREE;
        *(mem->sizes + i) = FREESIZE;
        i++;
    }

    printMemory(mem);
    printSizes(mem);
}

void cleanMemory(struct space *mem){
    int i = 0;
    while (i < mem->len) {
        *(mem->memory + i) = FREE;
        *(mem->sizes + i) = FREESIZE;
        i++;
    }

    printMemory(mem);
    printSizes(mem);

    free(mem->memory);
    free(mem->sizes);
}

int stackAllocator(int nbytes, struct space *mem) {
    int i = 0;
    //search for free block of memory with enough space
    while (i + nbytes < mem->len && *(mem->sizes + i) != FREESIZE) {
        i++;
    }
    
    //if not block found return len
    if (i + nbytes >= mem->len){
        return mem->len;
    }

    //mark memory as busy
    int t = 0;
    while(t < nbytes && t + i < mem->len){
        *(mem->memory + i + t) = BUSY;
        *(mem->sizes + i + t) = BUSYSIZE;
        t++;
    }

    //set first byte to size of block
    *(mem->sizes + i) = nbytes;
    return i;

}

void deallocator(int p, struct space *mem) {
    //check for invalid index
    if (p == mem->len || p < 0) return;

    int nbytes =  *(mem->sizes + p);
    int t = 0;
    while(t < nbytes){
        *(mem->memory + p + t) = FREE;
        *(mem->sizes + p + t) = FREESIZE;
        t++;
    }

}