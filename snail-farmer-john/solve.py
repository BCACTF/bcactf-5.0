# if the sum of entries in vec is n,
# then the sum of comb(vec) is n choose 2
# (n choose 2) choose 2 = 3 ((n+1) choose 4)
# (or just algebraically expand)

fin = open("input.txt", "r")
fout = open("fast.out", "w")
# Read the input
(n, k) = [int(x) for x in fin.readline().split(" ")]
arr = [int(x) for x in fin.readline().split(" ")]
assert len(arr) == k

sum = sum(arr)

start = sum + n - k + 1
out = 0
for i in range(start, sum, -3):
    out += (i * (i - 1) * (i - 2) * (i - 3)) // 8
fout.write("bcactf{" + str(out) + "}")
