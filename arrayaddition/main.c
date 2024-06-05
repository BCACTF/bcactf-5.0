// flag is this
// bcactf{w0W_cHa4aCt3R_aDD}
#include <stdio.h>

char arr[30] = {'b', 'b', '_', '`', 'p', 'a', 'u', 'p', '(', 'N', 'U', 'X', '<', 'T', '&', 'R', '3', 'c', '!', '?', 'K', 'L', '.', '-', 'e'};
int main() {
    // this will show how the text was generated which you can find w/ strings
    // for(int i = 0; i < 25; i++) {
    //     printf("%c", arr[i] + i);
    // }

    // solution:
    // the same as above but subtract i instead of add

    printf("Alright, here's the deal:\n");
    printf("There is an array hiding somewhere in this program..\n");
    printf("But it is a little bit odd.\n");
    printf("I think there's a correlation between the individual data in the array's placement and what the data actually means.");
    return 0;
}
