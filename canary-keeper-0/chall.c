#include <string.h>
#include <stdio.h>

#define CANARY_VALUE "canary\0"
#define FLAG_VALUE "bcactf{s1mple_CANaRY_9b36bd9f3fd2f}\0"

int check_canary(const char* canary) {
    return strcmp(canary, CANARY_VALUE) == 0;
}

int check_flag(const char* flag) {
    return strcmp(flag, FLAG_VALUE) == 0;
}

int main() {
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

    char flag[64] = FLAG_VALUE;
    char canary[7] = CANARY_VALUE;
    char buffer[64];

    printf("Enter a string: ");
    gets(buffer);

    if (!check_canary(canary)) {
        printf("Buffer overflow detected!\n");
        return 1;
    }

    if (check_flag(flag)) {
        printf("No changes in flag detected!\n");
        return 1;
    }

    printf("Flag: %s\n", FLAG_VALUE);

    return 0;
}