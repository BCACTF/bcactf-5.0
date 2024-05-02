from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
import random
import math
import decimal

decimal.setcontext(decimal.Context(prec=2000))

def find_invpow(x,n):
    high = 1
    while high ** n < x:
        high *= 2
    low = high//2
    while low < high:
        mid = (low + high) // 2
        if low < mid and mid**n < x:
            low = mid
        elif high > mid and mid**n > x:
            high = mid
        else:
            return mid
    return mid + 1

def inv(a, m) :  
      
    m0 = m  
    x0 = 0
    x1 = 1
  
    if (m == 1) :  
        return 0
    while (a > 1) :
        q = a // m  
  
        t = m  
        m = a % m  
        a = t  
  
        t = x0  
  
        x0 = x1 - q * x0  
  
        x1 = t  
    if (x1 < 0) :  
        x1 = x1 + m0  
  
    return x1  
  

def findMinX(num, rem, k) :  
      
    # Compute product of all numbers  
    prod = 1
    for i in range(0, k) :  
        prod = prod * num[i]  
  
    # Initialize result  
    result = 0
  
    # Apply above formula  
    for i in range(0,k):  
        pp = prod // num[i]  
        result = result + rem[i] * inv(pp, num[i]) * pp  
      
      
    return result % prod

# Driver method  
num = [0, 0, 0]  
rem = [0, 0, 0]  
k = 3

num[0] = 0 #put the first modulus here
rem[0] = 0 #put the first ciphertext here
num[1] = 0 #put the second modulus here
rem[1] = 0 #put the second ciphertext here
num[2] = 0 #put the third modulus here
rem[2] = 0 #put the third ciphertext here

print(long_to_bytes(find_invpow(decimal.Decimal(findMinX(num, rem, k)),3)).decode('utf-8'))