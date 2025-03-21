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