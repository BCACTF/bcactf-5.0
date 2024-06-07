#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <stdbool.h>
#include <time.h>
#include <unistd.h>
#include <string.h>

void load_flag(char* flag, size_t size) {
    FILE *fp = NULL;

    fp = fopen("./flag.txt", "r");
    if (fp == NULL) {
        puts("flag.txt could not be loaded; if you see this, please contact admin.");
        return;
    }

    fgets(flag, size, fp);
}

void wait_for(int nseconds) {
    for (int i = 0; i < nseconds; ++i) {
        printf(" .");
        sleep(1);
    }
    printf("\n");
}

char* read_pointer() {
    char* out;
    // I have no idea if this is safe
    scanf("%p", &out);

    return out;
}

int main() {
    void** first_var;
    char* guess;
    char flag[100];
    load_flag(flag, 100);

    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

    puts("Welcome to the most tasmastic game of all time!");
    wait_for(3);
    puts("Basically it's just too simple, I've put the");
    puts("flag into the memory and your job is ... to");
    puts("guess where it is!!");
    wait_for(2);
    puts("How fun is that!");
    wait_for(1);
    puts("Oh and before you start, I'll give you a little");
    puts("hint, the address of the current stackframe I'm");
    printf("in is %p\n", &(&first_var)[-2]);
    wait_for(3);
    puts("Okay anyway, back to the game. Make your guess!");
    puts("(hexadecimals only, so something like 0xA would work)");
    printf("guess> ");

    guess = read_pointer();

    wait_for(3);

    puts("Okay, prepare yourself. If you're right this");
    puts("will print out the flag");
    
    wait_for(1);
    puts("Oh, and if your wrong, this might crash and");
    puts("disconnect you\nGood luck!");

    printf("%s\n", guess);

    return 1;
}