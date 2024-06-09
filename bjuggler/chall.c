#include <stdio.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stddef.h>
#include <time.h>
#include <unistd.h>

void sleepms(long ms) {
    // https://stackoverflow.com/questions/1157209/is-there-an-alternative-sleep-function-in-c-to-milliseconds
    struct timespec ts;
    ts.tv_sec = ms / 1000;
    ts.tv_nsec = (ms % 1000) * 1000000;
    nanosleep(&ts, NULL);
}

void load_flag(char* flag, size_t size) {
    FILE *fp = NULL;

    fp = fopen("./flag.txt", "r");
    if (fp == NULL) {
        puts("flag.txt could not be loaded; if you see this, please contact admin.");
        return;
    }

    fgets(flag, size, fp);
}

void strcpy_unsafe(char* dest, char* src, uint32_t max) {
    uint32_t i = 0;
    while (*src) {
        *dest = *src;
        dest++;
        src++;
        i++;
    }
    if (i >= max) return;
    *dest = '\0';
}

int main() {
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
    setbuf(stdin, NULL);

    static char flag_cache[80];
    load_flag(flag_cache, 4800);

    // Enforces stack struct
struct {
    char right_hand[24];
    uint64_t _spacer[16];
    char left_hand[12];
    uint64_t _spacer2[16];
    char air[12];
    char flag[80];
    uint32_t turn_count;
} scope;
    scope.turn_count = 5;

    printf("P.S the juggler animation is kind of tilted so you might need to look at it sideways.\n\n");
    sleep(1);

    while (1) {
        puts("Please help me, I am the juggler, but I can't stop juggling.");
        sleep(1);
        printf("Give me something for my left hand (not too heavy though please, I injured it)\n(or QUIT to quit):\n> ");
        fgets(scope.left_hand, sizeof(scope.left_hand), stdin);

        if (strncmp(scope.left_hand, "QUIT", 4) == 0 || strncmp(scope.left_hand, "quit", 4) == 0) {
            puts("Goodbye!");
            return 0;
        }
        
        printf("Give me something for my right hand:\n> ");
        fgets(scope.right_hand, sizeof(scope.right_hand), stdin);
        strcpy(scope.air, "");

        if (scope.left_hand[strlen(scope.left_hand) - 1] == '\n') {
            scope.left_hand[strlen(scope.left_hand) - 1] = '\0';
        }

        if (scope.right_hand[strlen(scope.right_hand) - 1] == '\n') {
            scope.right_hand[strlen(scope.right_hand) - 1] = '\0';
        }

        printf("Watch this!");

        for (int i = 0, turns = scope.turn_count; i < turns; i++) {
            printf("-----------------------------------------=--||\n");
            printf("%24s 3----\\     __\n", scope.right_hand);
            printf("%23s      O-|---<__\n", scope.air);
            printf("%24s 3----/       \n", scope.left_hand);

            if (i % 3 == 0) {
                strcpy_unsafe(scope.air, scope.left_hand, sizeof(scope.air));
                strcpy_unsafe(scope.left_hand, scope.right_hand, sizeof(scope.left_hand));
                strcpy_unsafe(scope.right_hand, "", sizeof(scope.right_hand));
            } else if (i % 3 == 1) {
                strcpy_unsafe(scope.right_hand, scope.air, sizeof(scope.right_hand));
                strcpy_unsafe(scope.air, scope.left_hand, sizeof(scope.air));
                strcpy_unsafe(scope.left_hand, "", sizeof(scope.left_hand));
            } else if (i % 3 == 2) {
                strcpy_unsafe(scope.left_hand, scope.right_hand, sizeof(scope.left_hand));
                strcpy_unsafe(scope.right_hand, scope.air, sizeof(scope.right_hand));
                strcpy_unsafe(scope.air, "", sizeof(scope.air));
            }

            strcpy(scope.flag, flag_cache);

            sleepms(800);
        }
    }

    return 0;
}