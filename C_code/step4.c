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

void copyArray(int *aIn, int *aOut, int len){
    int t = 0;
    while (t < len){
        *(aOut + t) = *(aIn + t);
        t++;
    }
}

int spaceScanner(int nbytes, struct space *mem){
    int i = 0;
    int s = 0;
    while (s == 0 && i < mem->len){
        int t = 0;
        //check size of free block
        while(t + i < mem->len && *(mem->sizes + i + t) == FREESIZE) {
            t++;
        }
        if (t >= nbytes){ //if block is big enough exit loop
            s=1;
        } else {
            i++;
        }
    }
    return i;
}


void increaseMemory(int nbytes, struct space *mem){
    int newLen = mem->len;
    while (newLen - mem->len < nbytes){
        newLen = 2 * (newLen + 1);
    }

    char *s = mem->memory;
    int *a = mem->sizes;
    int oldLen = mem->len;
    initializeMemory(newLen, mem);
    copyString(s, mem->memory, oldLen);
    copyArray(a, mem->sizes, oldLen);
    free(s);
    free(a);

}

int heapAllocator(int nbytes, struct space *mem){
    int i = spaceScanner(nbytes, mem);
    if (i == mem->len) {
        //if no heap found, increase memory
        int t0;
        while ((t0 = spaceScanner(nbytes, mem))== mem->len){
            increaseMemory(nbytes, mem);
        } //scan again using new space
        i = spaceScanner(nbytes, mem);

    }
    //allocate heap
    int t = 0;
    while(t < nbytes){
        *(mem->memory + i + t) = BUSY;
        *(mem->sizes + i + t) = BUSYSIZE;
        t++;
    }
    *(mem->sizes + i) = nbytes;
    return i;
}

int readString(char **s) {
    int t = 0;
    char c = getchar();
    *s = malloc(1); // Allocate memory for the initial string
    (*s)[0] = '\0'; // Ensure the initial string is null-terminated

    while (c != '\n' && c != EOF) {
        char *p = *s; // Store the current string
        t++;
        char *temp = malloc(t + 1); // Reallocate memory for the new string
        *s = temp;
        copyString(p, *s, t); // Copy the content of the old string to the new one
        free(p); 
        (*s)[t - 1] = c; 
        (*s)[t] = '\0'; // Null-terminate the string
        c = getchar();
    }

    if (c == EOF) return 0; 
    return 1; 
}



