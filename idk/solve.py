# most things stolen from https://graphics.stanford.edu/~seander/bithacks.html

goal_check = 333072
goal = [466437, 528153, 333852, 530074, 728060, 531211, 400528, 399745, 396035, 530846, 662759, 395326, 397355, 663164, 399371, 532170, 465419, 466482, 532038, 399114]

def bits(n):
    c = 0
    while n:
        c += 1
        n &= n - 1
    return c


# previous bit permutation
for i in range(20):
    for j in range(i):
        bit_count = bits(goal[i])
        goal[i] -= 1
        while bits(goal[i]) != bit_count:
            goal[i] -= 1

print(goal)

# reverse this thing "Get bit count and remove last bit"
for i in range(20):
    bit_count = goal[i] >> 16
    goal[i] = goal[i] & ((1 << 16) - 1)
    goal[i] <<= 1
    t = bits(goal[i])
    if (t == bit_count): continue
    if (t == bit_count - 1): goal[i] += 1; continue
    raise Exception("???", t, bit_count)
print(goal)
# reverse Max and min with help of check
ind2 = [18, 6, 17, 4, 13, 12, 10, 5, 0, 14, 8, 11, 16, 7, 15, 1, 2, 19, 9, 3]
for i in range(0, 20, 2):
    if not (goal_check & (1 << i)): # if 1st > 2nd in orig
        # already correct order (this part sets the 2nd one to the min)
        continue
    goal[ind2[i]], goal[ind2[i + 1]] = goal[ind2[i + 1]], goal[ind2[i]]
print(goal)
# reverse XOR swap
ind = [11, 19, 14, 1, 3, 5, 18, 13, 0, 17, 6, 7, 8, 16, 12, 10, 4, 9, 15, 2]
for i in range(0, 20, 2):
    goal[ind[i]], goal[ind[i + 1]] = goal[ind[i + 1]], goal[ind[i]]

flag = []
print(goal)
# uninterleave
for i in range(20):
    temp_x = 0
    temp_y = 0
    for j in range(0, 16, 2):
        temp_x |= ((goal[i] >> j) & 1) << (j//2)
        temp_y |= ((goal[i] >> (j+1)) & 1) << (j//2)
    flag.append(temp_x)
    flag.append(temp_y)

print("".join([chr(x) for x in flag]))