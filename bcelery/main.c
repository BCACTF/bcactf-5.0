#include <stdio.h>

int main() {
    lose();
    return 0;
}

int lose() {
    char input[112];
    printf("Enter your name: ");
    gets(input);
    char out[112];
    sprintf(out, "Hello, %s!\n", input);
    printf(out);
}

int win() {
    FILE* fp = fopen("flag.txt", "r");
    if (fp == NULL) {
        printf("flag.txt not found\n");
        return 1;
    }
    char flag[64];
    fgets(flag, sizeof(flag), fp);
    printf("flag: %s\n", flag);
    fclose(fp);
    return 0;
}
