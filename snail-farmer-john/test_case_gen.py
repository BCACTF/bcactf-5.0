import random
n = 500000
k = 200000
fout = open("input.txt", "w")
fout.write(f"{n} {k}\n")
for (i, x) in enumerate([random.randint(1, 1000000) for _ in range(n)]):
    fout.write(f"{x}")
    if i != n - 1:
        fout.write(" ")