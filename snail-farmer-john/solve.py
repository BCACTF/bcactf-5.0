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

out = 0
for i in range(n, k-1, -3):
    num = sum + i - k # add i-k for the extra 1s at the end
    out += ((num+1) * (num) * (num - 1) * (num - 2)) // 8
fout.write("bcactf{" + str(out) + "}")
