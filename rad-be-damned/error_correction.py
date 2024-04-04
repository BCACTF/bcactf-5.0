poly = int("10011", base=2) #x^4 + x + 1 (CRC-4-ITU)
poly_length = poly.bit_length()

def find_leftmost_set_bit(plaintext):
    pos = 0
    while plaintext > 0:
        plaintext = plaintext >> 1
        pos += 1
    return pos

def error_lookup_table():
    lookup_table = {}
    for i in range(0, (poly_length - 1) + 8):
        error = 2**i
        while (error.bit_length() >= poly_length):
            first_pos = find_leftmost_set_bit(error)
            error = error ^ (poly << (first_pos - poly_length))
        lookup_table[error] = i
        # if (i == 5):
        #     lookup_table[3] = 5
    return lookup_table

def error_corrector(lookup_table: dict, bitstring: str):
    bit_error = int(bitstring, base=2)
    while (bit_error.bit_length() >= poly_length): #finding the position of the bit error
        first_pos = find_leftmost_set_bit(bit_error)
        bit_error = bit_error ^ (poly << (first_pos - poly_length))
    bit_pos = lookup_table[bit_error]
    return chr((int(bitstring, base=2) ^ (2**bit_pos)) >> poly_length - 1)

def main():
    user_input = input()
    received_bytes = user_input.split(" ")
    lookup_table = error_lookup_table() #Uses the poly defined above

    for byte in received_bytes:
        print(error_corrector(lookup_table, byte), end = '')

main()