#include <stdio.h>

int main() {
    // read input in as char array
    char flag[40];
    printf("what: ");
    scanf("%s", flag);
    unsigned int cd[20];
    // Interleave
    for (int i = 0; i < 20; i ++) {
        cd[i] = ((flag[2*i] * 0x0101010101010101ULL & 0x8040201008040201ULL) *
                     0x0102040810204081ULL >>
                 49) &
                    0x5555 |
                ((flag[2*i + 1] * 0x0101010101010101ULL & 0x8040201008040201ULL) *
                     0x0102040810204081ULL >>
                 48) &
                    0xAAAA;
    }
    // XOR Swap
    int ind1[20] = {11, 19, 14, 1, 3, 5, 18, 13, 0, 17, 6, 7, 8, 16, 12, 10, 4, 9, 15, 2};
    for (int i = 0; i < 19; i += 2) {
        cd[ind1[i]] = cd[ind1[i]] ^ cd[ind1[i + 1]];
        cd[ind1[i + 1]] = cd[ind1[i + 1]] ^ cd[ind1[i]];
        cd[ind1[i]] = cd[ind1[i]] ^ cd[ind1[i + 1]];
    }
    // Max and min
    int ind2[20] = {18, 6, 17, 4, 13, 12, 10, 5, 0, 14, 8, 11, 16, 7, 15, 1, 2, 19, 9, 3};
    unsigned int check = 0;
    for (int i = 0; i < 19; i += 2) {
        unsigned int c = (cd[ind2[i]] < cd[ind2[i + 1]]);
        check += c << i;
        unsigned int temp = cd[ind2[i + 1]] ^ ((cd[ind2[i]] ^ cd[ind2[i + 1]]) & -c);
        cd[ind2[i]] ^= ((cd[ind2[i]] ^ cd[ind2[i + 1]]) & -c);
        cd[ind2[i + 1]] = temp;
    }
    // Get bit count and remove last bit
    for (int i = 0; i < 20; i++) {
        unsigned int t = cd[i];
        t = t - ((t >> 1) & 0x55555555);
        t = (t & 0x33333333) + ((t >> 2) & 0x33333333);
        t = (((t + (t >> 4)) & 0x0F0F0F0F) * 0x01010101) >> 24;
        cd[i] >>= 1;
        cd[i] += t << 16;
    }
    // Advance bit permutations
    for (int i = 0; i < 20; i++) {
        for (int j = 0; j < i; j++) {
            unsigned int temp = cd[i] | (cd[i]-1);
            cd[i] = (temp + 1) | (((~temp & -~temp) - 1) >> (__builtin_ctz(cd[i]) + 1));  
        }
    }

    unsigned int goal_check = 333072;
    unsigned int goal[20] = {466437, 528153, 333852, 530074, 728060, 531211, 400528, 399745, 396035, 530846, 662759, 395326, 397355, 663164, 399371, 532170, 465419, 466482, 532038, 399114};
    if (check == goal_check) {
        for (int i = 0; i < 20; i++) {
            if (cd[i] != goal[i]) {
                printf("no\n");
                return 0;
            }
        }
        printf("yes\n");
    } else {
        printf("no\n");
    }
    return 0;
}
