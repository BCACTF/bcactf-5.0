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
    arr = in_arr.flatten('F')
    text = ''.join([str(x) for x in arr])
    # remove leading 0 and trailing 17


# more kneading, then the bycol and transpose
    

# TODO: finish