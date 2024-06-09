#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>

#define ART_WIDTH 0x28
#define ART_HEIGHT 0x10

static uint8_t raw_art_canvas[ART_HEIGHT * ART_WIDTH];
static char* pwd_env;
static uint8_t* art_canvas = raw_art_canvas;

void print_canvas() {
    printf("#");
    for (uint32_t x = 0; x < ART_WIDTH; x++)  {
        printf("-");
    }
    printf("#");
    printf("\n");

    for (uint32_t y = 0; y < ART_HEIGHT; y++) {
        printf("|");
        for (uint32_t x = 0; x < ART_WIDTH; x++) {
            printf("%c", art_canvas[y * ART_WIDTH + x]);
        }
        printf("|");
        printf("\n");
    }

    printf("#");
    for (uint32_t x = 0; x < ART_WIDTH; x++)  {
        printf("-");
    }
    printf("#");
    printf("\n");
}

int main() {
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);
    pwd_env = getenv("PWD");
    memset(raw_art_canvas, ' ', sizeof(raw_art_canvas));

    printf("Welcome to the ASCII Art Canvas!\n");

    char input[2];
    char cursor;
    int16_t x = ART_WIDTH / 2, y = ART_HEIGHT / 2;

    PAINT_START:
    printf("Pick the character you want to paint with: ");

    read(0, input, 2);

    cursor = input[0];

    while (1) {
        art_canvas[y * ART_WIDTH + x] = cursor;
        print_canvas();

        printf("Now use WASD to move\n> ");

        read(0, input, 2);

        if (input[0] == 'x') {
            return 0;
        }

        if (input[0] == 'w' || input[0] == 'W') {
            y -= 1;
        } else if (input[0] == 'a' || input[0] == 'A') {
            x -= 1;
        } else if (input[0] == 's' || input[0] == 'S') {
            y += 1;
        } else if (input[0] == 'd' || input[0] == 'D') {
            x += 1;
        } else {
            goto PAINT_START;
        }
    }

    return 0;
}