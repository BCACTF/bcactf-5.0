from base64 import b64decode

with open('NOTflag.txt', 'r') as f:
    data = b64decode(f.read())
    s=''
    for byte in data:
        s+=chr(byte ^ 0xFF) # NOT all 8 bits
    print(s)

