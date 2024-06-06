#include<stdio.h>

int c(int n) {
  if (n == 0) {
    return 1;
  } else {
    return ((2.0 * ((2 * n) - 1)) / (n + 1)) * (c(n - 1));
  }
}

int f(int n)
{
    int a = 0, b = 1, c, i;
    if (n == 0)
        return a;
    for (i = 2; i <= n; i++) {
        c = a + b;
        a = b;
        b = c;
    }
    return b;
}
long b[37] = {-1,-82,-16,-6,-50,-264,-169,-378,-476,-550,-6586,-9792,-6524,-2639,-45140,-39480,-49507,-7752,-142154,-588555,-963248,-1133504,-2235246,-3616704,-3601200,-1820895,-2749852,-9534330,-15941099,-60738920,-57889567,-174264720,-140983120,-45623096,-719742270,-537492672,-676418876};
char i2[37] = {12,13,9,12,12,12,12,12,11,12,13,13,13,12,13,12,13,12,13,13,13,13,13,13,13,11,11,12,13,13,13,13,13,9,13,13,12};
char i4[37] = {4,3,6,4,3,5,0,5,6,2,0,1,2,1,0,5,1,4,3,4,3,2,3,2,4,6,6,5,1,5,4,3,3,6,1,0,4};

int win() {
    char out[40];
    memset(out, 0, 40);

    for(int i = 0; i < 37; i++) {
        long k = b[i]/(f(i+1));
        out[i] = k + f(i2[i]) + c(i4[i]);
        out[i] ^= 0xff;
    }
    printf("%s\n", out);
}
int main() {
    printf("No flag for you >:(\n");
    return 0;
}