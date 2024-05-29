import random

def find_leftmost_set_bit(plaintext):
    #self-explanatory
    pos = 0
    while plaintext > 0:
        plaintext = plaintext >> 1
        pos += 1
    return pos
        
def crc_encrypt(letter: str):
    crc_poly = int("10011", 2)
    crc_poly_length = crc_poly.bit_length()

    bin_letter, crc_rem = ord(letter), ord(letter) * 2**(crc_poly_length - 1)

    while (crc_rem.bit_length() >= crc_poly_length):
        first_pos = find_leftmost_set_bit(crc_rem)
        crc_rem = crc_rem ^ (crc_poly << (first_pos - crc_poly_length))
    
    let_crc = format(bin_letter, "08b") + format(crc_rem, "0" + f"{crc_poly_length - 1}" + "b")
    return let_crc

def expose_to_radiation(letcrc: str):
    length_crc = len(letcrc)
    pos = random.randint(0, length_crc - 1)
    bit_mask = 2**pos
    rad_let = int(letcrc, base=2) ^ bit_mask
    rad_bin = format(rad_let, "0" + f"{length_crc}" + "b")
    return rad_bin

def main(plaintext: str):
    arr = []
    for letter in plaintext:
        letcrc = crc_encrypt(letter)
        arr.append(expose_to_radiation(letcrc))
    return arr