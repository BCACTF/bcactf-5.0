#include <stdio.h>
#include <string.h>
#include <unistd.h>

int main() {
    char left_hand[15];
    char right_hand[50];
    char air[30];
    char flag[40] = "flag{this_is_a_fake_flag}";

    printf("Give me something for my left hand (not too heavy though please, I injured it):\n   ");
    fgets(left_hand, 15, stdin);
    printf("Give me something for my right hand:\n   ");
    fgets(right_hand, 50, stdin);

    printf("Watch this!");

    for (int i = 0; i < 30; i++) {
        printf("     %s\n", air);
        printf("%s     o     %s\n", left_hand, right_hand);
        printf("  \\---|----/\n");
        printf("      /\\  \n\n\n\n");

        if (i % 3 == 0) {
            strcpy(air, left_hand);
            strcpy(left_hand, right_hand);
            strcpy(right_hand, "");
        } else if (i % 3 == 1) {
            strcpy(right_hand, air);
            strcpy(air, left_hand);
            strcpy(left_hand, "");
        } else {
            strcpy(left_hand, right_hand);
            strcpy(right_hand, air);
            strcpy(air, "");
        }
        sleep(1);
    }

    return 0;
}