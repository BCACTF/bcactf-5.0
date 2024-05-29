def find_leftmost_set_bit(plaintext):
    pos = 0
    while plaintext > 0:
        plaintext = plaintext >> 1
        pos += 1
    return pos
        
def crc_encrypt(plaintext: str):
    crc_plaintext = ""
    for letter in plaintext:
        crc_poly = int("10011", 2)
        crc_poly_length = crc_poly.bit_length()
        bin_letter, crc_rem = ord(letter), ord(letter) * 2**(crc_poly_length - 1)
        while (crc_rem.bit_length() >= crc_poly_length):
            first_pos = find_leftmost_set_bit(crc_rem)
            crc_rem = crc_rem ^ (crc_poly << (first_pos - crc_poly_length))
        let_crc = format(bin_letter, "08b") + format(crc_rem, "0" + f"{crc_poly_length - 1}" + "b")
        crc_plaintext += let_crc
    return crc_plaintext

def expose_to_radiation(text: str):
    corrupted_str = ""
    with open("error_pattern.txt") as f:
        for ind in range(0, len(text), 12):
            let = f.read(1) #between a and l inclusive
            if let != "":
                bit_mask = 2 ** (ord(let) - 97)
                rad_let = int(text[ind:ind+12], base=2) ^ bit_mask
                corrupted_str += format(rad_let, "012b")
    return corrupted_str

def main():
    with open('flag.txt') as f:
        plaintext = f.read().strip()
    crc_plaintext = crc_encrypt(plaintext)
    cor_text = expose_to_radiation(crc_plaintext)
    print(f"Here's flag: {cor_text}")

if __name__ == '__main__':
    main()