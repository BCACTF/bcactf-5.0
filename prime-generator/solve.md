A script can be found in [solve.py](solve.py)

Essentially, we can abuse the fact that the only possible values for p are [Mersenne primes](https://en.wikipedia.org/wiki/Mersenne_prime)

In addition, q is a 7-bit prime, and $p = 2^q - 1$

We can brute force p and q by looping through all the 7-bit numbers and testing which ones are Mersenne primes.

