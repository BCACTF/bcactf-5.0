#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#define base "0123456789ABCDEF"
int main() {
    srand(time(NULL));
    FILE* fptr;
    fptr = fopen("secret.txt", "r");
    char flag[40];
    if (fptr == NULL) {
        printf("err");
        exit(1);
    }
    fgets(flag, 40, fptr);
    char bits[320];
    for (int i = 0; i < strlen(flag); i++) {
        for (int j = 0; j < 8; j++) {
            bits[i * 8 + j] = rand() % 2;
        }
    }
    FILE* fout;
    fout = fopen("output.txt", "a");
    for (int ctr = 0; ctr < 15; ctr++) {
        char out[80];
        for (int i = 0; i < strlen(flag); i++) {
            int val = 0;
            for (int j = 7; j > 3; j--) {
                val <<= 1;
                val += (((flag[i] >> j) & 1) ? bits[i * 8 + j] : (rand() % 2));
            }
            out[2 * i] = base[val];
            val = 0;
            for (int j = 3; j > -1; j--) {
                val <<= 1;
                val += (((flag[i] >> j) & 1) ? bits[i * 8 + j] : (rand() % 2));
            }
            out[2 * i + 1] = base[val];
        }
        fprintf(fout, "%s\n", out);
    }
}