# we convert all the given hexadecimal numbers and convert them to binary
# if all the bits at a certain position are the same, a 1 is added and a 0 is added otherwise
# using this algorithm on all the bit positions, we get a new binary number of the same length
# convert it back to hexadecimal and compare it to the given input for the flag

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
    summ = 0
    for d in range(len(binNumber)):
        summ += int(binNumber[d][c])
    if summ == 0 or summ == 15:
        string += "1"
    else:
        string += "0"

finHex = hex(int(string,2))
finHex = finHex[2:]
if given == finHex:
    print("Good job! Have a cookie: bcactf{th3fl@gUsee33ek_g3tg00d}")
else:
    print("Incorrect...")