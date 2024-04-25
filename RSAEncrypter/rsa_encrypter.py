from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
import random
import math

message = open("./flag.txt").read().encode('utf-8')  


def encode():
    n = getPrime(256)*getPrime(256)
    rsa_key = RSA.construct((n,3))
    cipher = PKCS1_OAEP.new(rsa_key)
    ciphertext1 = cipher.encrypt(message)
    ciphertext = pow(bytes_to_long(message), 3, n)
    return (ciphertext, n)

print("Return format: (ciphertext, modulus)")
print(encode())
sent = input("Did you recieve the message? (y/n) ")
while sent=='n':
    print(encode())
    sent = input("How about now? (y/n) ")
print("Message acknowledged.")