#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define XOR_KEY "ClkvKOR8JQA1JB731LeGkU7J4d2khDvrOPI63mM7"

void xorEncrypt(char* input, char* output, size_t length) {
    size_t keyLength = strlen(XOR_KEY);
    for (size_t i = 0; i < length; i++) {
        sprintf(&output[i * 3], "%02X ", input[i] ^ XOR_KEY[i % keyLength]);
    }
}

int main() {
    FILE* file = fopen("flag.txt", "r");
    if (file == NULL) {
        printf("Failed to open file.\n");
        return 1;
    }

    fseek(file, 0, SEEK_END);
    long fileSize = ftell(file);
    fseek(file, 0, SEEK_SET);

    char* input = malloc(fileSize + 1);
    fread(input, 1, fileSize, file);
    input[fileSize] = '\0';

    fclose(file);

    char* output = malloc(fileSize + 1);
    xorEncrypt(input, output, fileSize);

    printf("Encrypted flag: %s\n", output);

    free(input);
    free(output);

    return 0;
}
