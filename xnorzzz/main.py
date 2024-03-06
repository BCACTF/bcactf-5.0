given = input("Enter your least favorite number: ").strip()

numbers = ["BDC9B3CBA3",
           "FDCC8EDEEB",
           "F9CD1B89C1",
           "F9E8820BF1",
           "8DCE874881",
           "ADFA869981",
           "8CDD069DCB",
           "C9EC871CF1",
           "9CEB3F5DC3",
           "A8EDAE5EA3",
           "CDCE9ADDD1",
           "8DD90FDDD3",
           "BDCB36599B",
           "89E9970ABB",
           "DCF91AC8A1"]

binNumber = []
for b in range(len(numbers)):
    hexi = int(numbers[b], 16)
    binary = bin(hexi)
    yex = binary[2:]
    binNumber.append(yex)

string = ""
for c in range(len(binNumber[0])):
    same = True
    prev = binNumber[0][c]
    for a in range(1,len(binNumber)):
        if binNumber[a][c] != prev:
            same = False
            break
    if not same:
        string += "0"
    else:
        string += "1"

finHex = hex(int(string,2))
finHex = finHex[2:]
if given == finHex:
    print("Good job! Have a cookie: bcactf{th3fl@gUsee33ek_g3tg00d}")
else:
    print("Incorrect...")