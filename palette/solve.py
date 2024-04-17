'''

The first step is to analyze and understand the
named functions.

B(x)=IF(x<2,x,B(FLOOR(x/2))&MOD(x,2))
    This is a recursive function that converts an integer
    into a binary string - appends x % 2 to the binary
    representation of x // 2.

IC(x)=IF(CODE(RIGHT(x))<>57,LEFT(x,LEN(x)-1)&CHAR(CODE(RIGHT(x))+1),IF(x=CHAR(57),B(2),IC(LEFT(x,LEN(x)-1)))&CHAR(48))
    This increments a string of digits by 1. If the last
    character is not '9', it increments the last character
    by 1. If the last character is '9', it replaces the
    last character with '0' and increments the rest of
    the string.

IX(l,x,i)=IF(i=0,x,l(IX(l,x,i-1)))
    This function returns l(l(l(...l(x)...))) where the
    lambda l is applied i times. It calls l and then 
    IX recursively.

L(s,p,l)=IF(LEN(s)>=l,s,REPT(p,l-LEN(s))&s)
    This function pads a string with a character to a
    specified length. Padding is added to the left.

MU(x,k)=IF(LEN(x)=1,VALUE(x)*k,IX(IC,MU(LEFT(x,LEN(x)-1),k),FLOOR(VALUE(RIGHT(x))*k/10))&MOD(RIGHT(x)*k,10))
    This function multiplies a string of digits by an
    integer. It multiplies the last digit by k and
    appends the result to the product of the rest of
    the string multiplied by k. It then increments the
    product by 1 an appropriate number of times if
    a carry is needed.

RB(s)=IF(VALUE(s)<2,VALUE(s),2*RB(LEFT(s,LEN(s)-1))+VALUE(RIGHT(s)))
    This function converts a binary string to an integer.
    Once again, recursion is used by removing the last
    bit one at a time.

RV(s)=CONCATENATE(ARRAYFORMULA(MID(S,SEQUENCE(LEN(S),1,LEN(S),-1),1)))
    This function reverses a string.

SL(x)=SPARKLINE({1},{"charttype","bar";"color1","#"&x})
    This function creates a sparkline with a single bar
    of color x. This is how the colors are rendered.

V(i)=CONCATENATE(MAKEARRAY(LEN(i),1,LAMBDA(x,y,L(B(CODE(MID(i,x,1))),0,8))))
    This function converts a string into its binary
    representation (each letter is converted to Unicode,
    and then into 8-bit binary).

X(a,m)=LET(an,L(a,0,len(m)),mn,L(m,0,len(a)),CONCATENATE(MAKEARRAY(LEN(an),1,LAMBDA(x,y,IF(MID(an,x,1)=MID(mn,x,1),0,1)))))
    This function compares two strings and returns a
    binary string where 0 indicates that the characters
    are the same and 1 indicates that they are different.
    (essentially "xor"). The strings are first padded
    to the same length.

XT(s,l)=REGEXEXTRACT(s,REPT("("&REPT(".",l)&")",FLOOR(LEN(s)/l)))
    This function breaks up a string into chunks of a
    specified length.
     
Sidenote: when writing this up, it turns out that Copilot
is pretty good at this. 
'''

'''
Now we can analyze the main code.

Let's work from the inside out.

f1(in)=IX(LAMBDA(k,X(k,k&V("k"))),V(in),LEN(in))

The inner lambda XORs k (shifted by 8 bits) with k+"k".
This is easily reversible by considering 8 bits at a time.
'''
from Crypto.Util.number import long_to_bytes
def rev_f1_inner(in_bits):
    out_bits = in_bits[:8]
    for i in range(8, len(in_bits)-8, 8):
        for j in range(8):
            out_bits += str(int(in_bits[i+j]) ^ int(out_bits[i+j-8]))
    return out_bits

'''
This is repeated LEN(in) times, and the output is 8 chars
longer for every time X is run, so the output is 16*LEN(in)
chars long.
'''

def rev_f1(in_bits):
    out_bits = in_bits
    for _ in range(len(in_bits)//16):
        out_bits = rev_f1_inner(out_bits)
    return long_to_bytes(int(out_bits,2))

# test with fake flag
print("f1:",rev_f1("01100010000000010000001000000010000101110001001000011101000111010000011100001010000011100011101000111001000010100000110100000110011110000001011101101001000000100001011100010010000111010001110100000111000010100000111000111010001110010000101000001101000001100001101000010110"))
'''
Let's now look at this:

f2(in)=MU(RV(CONCATENATE(MAP(XT(f1(in),8),LAMBDA(C,L(RB(C),0,3))))),7)

This code splits up f1(in) into 8-bit chunks, which are 
converted to integers and padded to a length of 3.

The chunks are concatenated, reversed, and multiplied by 7.
'''

def rev_f2(in_int):
    temp = str(in_int//7)
    temp = '0'*((300-len(temp))%3) + temp
    temp = temp[::-1]
    temp = [temp[i:i+3] for i in range(0, len(temp), 3)]
    temp = [int(x) for x in temp]
    temp = ''.join(["{0:08b}".format(x) for x in temp])
    return rev_f1(temp)

# test with fake flag
print("f2:",rev_f2(1544344202170075255952870074906446445672241403509240151202170075255952870074906446445672241401400706230))

'''
Next:

f3(in) = TRANSPOSE(WRAPROWS(XT(LET(z, f2(in),L(z,0,2*CEILING(LEN(z)/2))),2),5,"17"))

This pads f2(in) to an even length and extracts
chunks of length 2.

WRAPROWS then rearranges it into rows of 5 (with "17" to
fill gaps), which are then transposed. We can reverse by
just flattening with 'F' mode in numpy.
'''

import numpy as np
def rev_f3(in_arr):
    arr = np.array(in_arr).flatten('F')
    text = ''.join([str(x) for x in arr])
    # remove trailing 17
    while text[-2:] == '17':
        text = text[:-2]
    return rev_f2(int(text))

# test with fake flag
print("f3:", rev_f3([["01","21","95","06","22","24","70","28","44","41","62"],["54","70","28","44","41","01","07","70","64","40","30"],["43","07","70","64","40","51","52","07","45","14","17"],["44","52","07","45","35","20","55","49","67","00","17"],["20","55","49","67","09","21","95","06","22","70","17"]]))

'''
f4(in) = TRANSPOSE(BYCOL(WRAPROWS(FLATTEN(f3(in)),5),LAMBDA(C,CONCATENATE(C))))

This flattens f3(in), wraps it into rows of 5, and then
concatenates each column (and transposes it to form
one column rather than one row).

f3(in) always has 5 rows, so we can reshape it, and each
element is 2 characters long.
Note that we have to transpose before reshaping
because of the use of BYCOL rather than BYROW.
'''
def rev_f4(in_arr):
    arr = [[x[i:i+2] for i in range(0,len(x),2)] for x in in_arr]
    arr = np.array(arr).T.reshape((5,-1))
    return rev_f3(arr)

# test with fake flag
print("f4:", rev_f4(["0124624140644507495595","2170540130401445674906","9528700743511735006722","0644287007524420170970","2241446470075255202117"]))


'''
f5(in) = FLATTEN(MAP(f4(in),LAMBDA(x,XT(L(x,"7",6*CEILING(LEN(x)/6)),6))))

This pads each element of f4(in) with "7" to make a
multiple of 6, breaks it up into chunks of 6, and
returns them as a hex code.

This is the last real step, as the only MAP around f5 is
just to render the colors. 

We need to be careful with the right dimension to reshape
our array to, but we can likely figure this out with the
padding. So, we'll take the length of each row as a
parameter so that we can manually set it.

'''

def rev_f5(pad, row_len, in_arr): # pad = # of 7s
    arr = [in_arr[i:i+row_len] for i in range(0, len(in_arr), row_len)]
    arr = [''.join(i)[pad:] for i in arr]
    return rev_f4(arr)

# test with fake flag
print("f5:", rev_f5(2, 4,["770124","624140","644507","495595","772170","540130","401445","674906","779528","700743","511735","006722","770644","287007","524420","170970","772241","446470","075255","202117"]))


# Finally, we need a way to extract the hex codes
# from palette.png. We count the number of pixels
# between rows manually and use Pillow.

from PIL import Image
img = Image.open("palette.png")
pixels = img.load()
width, height = img.size

pixel_gap = 29
starting_pixel = (400,17)

def extract_hex_codes():
    hex_codes = []
    for y in range(starting_pixel[1],img.height, pixel_gap):
       r, g, b = pixels[starting_pixel[0], y]
       hex_codes.append("{:02x}{:02x}{:02x}".format(r,g,b))
    return hex_codes

print(extract_hex_codes())

# padding of 4, 7 items per row
print(rev_f5(4, 7, extract_hex_codes()))