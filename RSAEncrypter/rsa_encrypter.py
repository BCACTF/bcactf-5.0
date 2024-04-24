from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
import random
import math
import decimal

decimal.setcontext(decimal.Context(prec=2000))
message = open("./flag.txt").read().encode('utf-8')

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

def encode():
    n = getPrime(256)*getPrime(256)
    # randNum = random.randrange(0,3)
    # if randNum==0:
    #     n = 99,991 * 11,113
    # elif randNum==1:
    #     n = 13,537 * 10,159
    # else:
    #     n = 12037 * 10061

    rsa_key = RSA.construct((n,3))
    cipher = PKCS1_OAEP.new(rsa_key)
    ciphertext1 = cipher.encrypt(message)
    ciphertext = pow(bytes_to_long(message), 3, n)
    return (ciphertext, n)

# Driver method  
num = [0, 0, 0]  
rem = [0, 0, 0]  
k = 3
count = 0

print("Return format: (ciphertext, modulus)")
t = encode()
num[count] = t[1]
rem[count] = t[0]
count+=1
#sent = input("Did you recieve the message? (y/n) ")
while count<3:#sent=='n':
    t = encode()
    num[count] = t[1]
    rem[count] = t[0]
    count+=1
    #sent = input("How about now? (y/n) ")

print(findMinX(num,rem,k)==bytes_to_long(message))
print(long_to_bytes(find_invpow(decimal.Decimal(findMinX(num, rem, k)),3)).decode('utf-8'))