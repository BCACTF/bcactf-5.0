given = input("Enter your least favorite number: ").strip()

# input list of hex numbers
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

# list of binary numbers converted from hex
binNumber = []
# iterating through the numbers
for b in range(len(numbers)):
    # convert to decimal from hex
    hexi = int(numbers[b], 16)
    # convert to binary from decimal
    binary = bin(hexi)
    # remove the '0x' part from above
    yex = binary[2:]
    # adding converted binary number to list
    binNumber.append(yex)

string = ""
# iterate through each bit of binary numbers
for c in range(len(binNumber[0])):
    summ = 0
    # iterate through all the binary numbers
    for d in range(len(binNumber)):
        # add the same bit of each binary number
        summ += int(binNumber[d][c])
    # checking if the numbers are all 0 or all 1
    if summ == 0 or summ == 15:
        # adding one according to XNOR algorithm
        string += "1"
    else:
        # adding zero according to XNOR algorithm
        string += "0"

# converting the string to decimal and then to hex
finHex = hex(int(string,2))
# remove the '0x' part from above
finHex = finHex[2:]
# print answer
if given == finHex:
    print("Good job! Have a cookie: bcactf{th3fl@gUsee33ek_g3tg00d}")
else:
    print("Incorrect...")