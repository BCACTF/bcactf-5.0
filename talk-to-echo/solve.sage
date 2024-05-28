#!/bin/sage

# This is a simple application of the "Invalid Curve Attack".
# Refer to https://iacr.org/archive/pkc2003/25670211/25670211.pdf
# Essentially, the implementation of adding/multiplying points
# on the elliptic curve does not rely on the curve's b parameter
# so we can send Echo a point rA that only has a few options for
# mul(priv, rA), eventually leaking the private key.
from pwn import *
from random import randint
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def add(p, q):
    if p == (0, 0):
        return q
    if q == (0, 0):
        return p
    if p[0] == q[0] and p[1] != q[1]:
        return (0, 0)
    if p != q:
        l = ((q[1] - p[1]) * pow(q[0] - p[0], -1, n)) % n
    else:
        l = ((3 * p[0] * p[0] + a) * pow(2 * p[1], -1, n)) % n
    x = (l * l - p[0] - q[0]) % n
    y = (l * (p[0] - x) - p[1]) % n
    return (x, y)


def mul(k, p):
    q = (0, 0)
    while k > 0:
        if k & 1:
            q = add(q, p)
        p = add(p, p)
        k >>= 1
    return q


def enc(m, key=0):
    if key == 0:
        r = randint(1, n - 1)
        R = mul(r, G)
        K = mul(r, pub)
    else:
        R = None
        K = key
    h = SHA256.new()
    h.update(str(K[0]).encode())
    k = h.digest()[:16]
    cipher = AES.new(k, AES.MODE_ECB)
    if R:
        return (R, cipher.encrypt(pad(m, 16)))
    return cipher.encrypt(pad(m, 16))


n = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
K = GF(n)
a = K(0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC)


# Use remote() on the real challenge
p = process(["python", "echo.py"])

# Get the (R, cipher.encrypt(pad([flag], 16))) for later
flag_msg = eval(p.recvline_contains(b"mumble")[10:-25])

# Get the public key
public_key = eval(p.recvline_contains(b","))

# for future CRT usage
residues = []
moduli = []


# don't need to fully factor these large numbers
def small_prime_factors(N, bound):
    out = []
    for prime in Primes():
        if prime > bound:
            break
        if N % prime == 0:
            out.append(prime)
    return out


# this operation is really slow, so set a timeout
@fork(timeout=5)
def order_with_timeout(pt):
    return pt.order()

start = time.time()
# We will eventually find the square of the private key using CRT
# and it is bounded above by n^2, so we will continue getting
# factors until we reach that number.
goal = n ^ 2
while prod(moduli) < goal:

    # Find a low-order point on a curve that with the same a coeff
    # as the curve used by the server.
    # Any random curve likely has some low-order points
    b = randint(1, n - 1)
    print("\033[31;1mTrying curve with b =", b, "\033[0m")
    print(
        "-- Still need a factor of 2 ^\033[34;1m",
        (goal // prod(moduli)).nbits(),
        "\033[0m",
    )
    E = EllipticCurve(K, (a, b))
    # Take a random point, hope its order has a small prime factor
    # That way, we can find a low-order point by multiplying it
    # pt.order can be super slow, so set a time limit
    # the time limit doesn't really work all the time but whatever
    # its good enough for its job i think
    pt = E.random_point()
    pt_order = order_with_timeout(pt)
    if isinstance(pt_order, str):
        print("Too slow, killing")
        continue
    print("Timer defused")

    # let's use a cutoff of like, 500000, for the factors we use
    prime_fs = small_prime_factors(pt_order, 500000)

    for prime in prime_fs:
        if prime in moduli:
            continue
        # get a point of order prime
        rA = pt * (pt_order // prime)

        # avoid error
        if gcd(rA.y(), n) != 1:
            continue

        print(f"---- trying ({rA.x()},{rA.y()}), order {prime}")

        # give it to Echo
        p.recvuntil(b"x:")
        p.sendline(str(rA.x()).encode())
        p.recvuntil(b"y:")
        p.sendline(str(rA.y()).encode())

        # here's the result
        output = eval(p.recvline())

        # try "priv"s to see what would yield the same output
        priv = 1
        key = rA
        while enc(b"Hey there! Thanks for talking to me :)", key) != output:
            priv += 1
            key = add(key, rA)

        # now, the private key could be either this priv or -priv
        # since k*P and -k*P have the same x-coordinate
        # which is used in encoding
        # but either way, we know priv^2
        print(f"----- priv^2 = {pow(priv,2,prime)} mod {prime}")
        residues.append(pow(priv, 2, prime))
        moduli.append(prime)

        p.recvuntil(b"(y/n)")
        p.sendline(b"y")

end = time.time()
print("Done!")
print(f"Took {end - start} seconds")
# personal best: 181 seconds
# can tweak timeout and prime factor cutoff to optimize ig

# use CRT to find priv^2
print("residues:", residues)
print("moduli:", moduli)
priv_squared = CRT_list(residues, moduli)
priv_squared = K(priv_squared)
print("priv^2:", priv_squared)
priv_keys = priv_squared.sqrt(extend=False, all=True)
print("Candidates:", priv_keys)


# Decode when given private key:
def dec(priv, R, c):
    key = mul(priv, R)
    h = SHA256.new()
    h.update(str(key[0]).encode())
    k = h.digest()[:16]
    cipher = AES.new(k, AES.MODE_ECB)
    return cipher.decrypt(c)


print(dec(Integer(priv_keys[0]), *flag_msg))
print(dec(Integer(priv_keys[1]), *flag_msg))
