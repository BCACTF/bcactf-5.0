from Crypto.Util.number import long_to_bytes

smallest_7_bit_num = 0b1000000
largest_7_bit_num = 0b1111111
n = 17361742620725829882898847100829589
e = 65537
c = 10661928665864844893859522372811722

#copy over the lucas-lehmer test from the original code
def yes(p):
    if p == 2:
        return True
    s = 4
    M = 2**p - 1
    for i in range(3, p+1):
        s = (s**2 - 2) % M
    return s == 0


for i in range(smallest_7_bit_num, largest_7_bit_num + 1):
    if yes(i):
        q = i
        p = 2**i - 1
        phi = (p-1)*(q-1)
        n = p*q
        d = pow(e, -1, phi)
        r = pow(c, d, n)
        print(long_to_bytes(r))