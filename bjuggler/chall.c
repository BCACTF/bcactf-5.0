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

int main() {
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
    setbuf(stdin, NULL);

    char flag[40];
    uint32_t turn_count = 5;
    char air[12];
    char left_hand[8];
    char right_hand[24];
    load_flag(flag, 40);

    printf("P.S the juggler animation is kind of tilted so you might need to look at it sideways.\n\n");
    sleep(1);

    while (1) {
        puts("Please help me, I am the juggler, but I can't stop juggling.");
        sleep(1);
        printf("Give me something for my left hand (not too heavy though please, I injured it)\n(or QUIT to quit):\n> ");
        fgets(left_hand, sizeof(left_hand), stdin);

        if (strncmp(left_hand, "QUIT", 4) == 0 || strncmp(left_hand, "quit", 4)) {
            puts("Goodbye!");
            return 0;
        }
        
        printf("Give me something for my right hand:\n> ");
        fgets(right_hand, sizeof(right_hand), stdin);
        strcpy(air, "");

        if (left_hand[strlen(left_hand) - 1] == '\n') {
            left_hand[strlen(left_hand) - 1] = '\0';
        }

        if (right_hand[strlen(right_hand) - 1] == '\n') {
            right_hand[strlen(right_hand) - 1] = '\0';
        }

        printf("Watch this!");

        for (int i = 0, turns = turn_count; i < turns; i++) {
            printf("-----------------------------------------=--||\n");
            printf("%24s 3----\\     __\n", right_hand);
            printf("%23s      O-|---<__\n", air);
            printf("%24s 3----/       \n", left_hand);

            if (i % 3 == 0) {
                strcpy(air, left_hand);
                strcpy(left_hand, right_hand);
                strcpy(right_hand, "");
            } else if (i % 3 == 1) {
                strcpy(right_hand, air);
                strcpy(air, left_hand);
                strcpy(left_hand, "");
            } else if (i % 3 == 2) {
                strcpy(left_hand, right_hand);
                strcpy(right_hand, air);
                strcpy(air, "");
            }

            sleepms(800);
        }
    }

    return 0;
}