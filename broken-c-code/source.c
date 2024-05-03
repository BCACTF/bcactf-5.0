// source code

#include <stdio.h>
#include <math.h>


int main() {
    printf("Here's your flag!\n\n");
    int flag[] = {9607, 9804, 9412, 9804, 13459, 10407, 15132, 9804, 9028, 9804, 2307, 10003, 4764, 9028, 10407, 5332, 7747, 10204, 4627,9028, 3028, 5187, 2707, 6087, 5628, 2812, 9028, 3028, 2919, 2503, 2707, 3028, 3139, 2503, 3028, 2919, 15628, 103};

    for (int i = 0; i < sizeof(flag); flag[i]++)
        printf("%c",(char)sqrt(flag[i]-3));
    
    return 0;
}

