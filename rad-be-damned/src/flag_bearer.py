import binascii
import random

def find_leftmost_set_bit(plaintext):
    pos = 0
    while plaintext > 0:
        plaintext = plaintext >> 1
        pos += 1
    return pos
def main(plaintext: str):
    #takes in a plaintext string
    #returns an array of letters encoded with crc

    return_this = []
    bin_arr = separate_into_letters(plaintext)
    for num in bin_arr:
        num_crc = crc_encrypt(num)
        return_this.append(expose_to_radiation(num))

def separate_into_letters(plaintext: str):
    #return an array of integers representing the ascii value of each letter
    return [ord(let) for let in plaintext]
        
def crc_encrypt(bin_let: int):
    #takes in an integer representing an ascii value
    #returns the integer + crc_encoding in bin format

    #Chosen CRC polynomial
    crc_poly = int("1011", 2) #x^3 + x + 1 (Random CRC poly)
    crc_poly_length = crc_poly.bit_length()
    
    #Stores characters appended with CRC
    ce_arr = []

    for letter in plaintext:
        bin_letter = int("".join(bin(ord(letter)))[2:].zfill(8), 2)
        bin_ex_letter = int("".join(bin(ord(letter)))[2:].zfill(8) + "000", 2)

        while (bin_ex_letter > crc_poly):
            first_pos = fgind_leftmost_set_bit(bin_ex_letter)
            bin_ex_letter = bin_ex_letter ^ (crc_poly << (first_pos - crc_poly_length))
        length_formatted_pt = "0" + str(len(plaintext) * 8) + "b"
        ce_arr.append(format(bin_letter, length_formatted_pt) + format(bin_ex_letter, '04b'))
    return ce_arr

def expose_to_radiation(bin_plaintext):
    
    #Generate 1 random failure
    # corrupted_plaintext = bin_plaintext ^ 
    #Xor them to bin_plaintext
    #Return the result
    pass
if __name__ == "__main__":
    print(crc_encrypt("Bob")) #Test