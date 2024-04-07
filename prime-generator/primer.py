from Crypto.Util.number import *

def yes(p):
    if p == 2:
        return True
    s = 4
    M = 2**p - 1
    for i in range(3, p+1):
        s = (s**2 - 2) % M
    return s == 0

p = getPrime(7)
while not yes(p):
    p = getPrime(7)
q = p
p = 2**p - 1
phi = (p-1)*(q-1)
n = p*q
e = 65537
d = pow(e, -1, phi)

m = bytes_to_long(open('flag.txt', 'rb').read().replace(b'bcactf{', b'').replace(b'}', b''))
c = pow(m, e, n)

output = open('output.txt', 'w')

output.write(f'n = {n}\n')
output.write(f'e = {e}\n')
output.write(f'c = {c}\n')

output.close()
