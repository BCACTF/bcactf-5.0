#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define XOR_KEY "ClkvKOR8JQA1JB731LeGkU7J4d2khDvrOPI63mM7"

void xorEncrypt(char* input, char* output, size_t length) {
    size_t keyLength = strlen(XOR_KEY);
    for (size_t i = 0; i < length; i++) {
        // Convert each byte to 2 hexadecimal characters and append a space, writing directly to the output buffer
        sprintf(&output[i * 3], "%02X ", input[i] ^ XOR_KEY[i % keyLength]);
    }
    output[length * 3] = '\0'; // Null-terminate the output string
}

int main() {
    FILE* file = fopen("flag.txt", "r");
    if (file == NULL) {
        printf("Failed to open file.\n");
        return 1;
    }

    // Determine the file size
    fseek(file, 0, SEEK_END);
    long fileSize = ftell(file);
    fseek(file, 0, SEEK_SET);

    // Allocate memory for the input buffer
    char* input = malloc(fileSize + 1);
    if (input == NULL) {
        printf("Memory allocation failed for input.\n");
        fclose(file);
        return 1;
    }

    // Read the file content into the input buffer
    fread(input, 1, fileSize, file);
    input[fileSize] = '\0'; // Null-terminate the input string

    fclose(file);

    // Allocate memory for the output buffer, considering the expansion in size due to hex encoding
    char* output = malloc(fileSize * 3 + 1); // Each input byte becomes three characters in the output
    if (output == NULL) {
        printf("Memory allocation failed for output.\n");
        free(input); // Free the input buffer before returning
        return 1;
    }

    xorEncrypt(input, output, fileSize);

    printf("Encrypted flag: %s\n", output);

    // Clean up
    free(input);
    free(output);

    return 0;
}
