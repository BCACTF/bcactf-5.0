plaintext = "heyguysimkindoflostprobablynotgoingtosurvivemuchlongertobehonestbutanywaystheflagisbcactf{5c7t4l3_h15t04y_qe829xl1}pleasesendhelpimeanbythetimeyouseethisiveprobablybeendeadforthousandsofyearsohwellseeyoulaterisupposebyeee"

ciphertext = ""
currentIndex = 0

lengthOfCylinder = 17

print(len(plaintext))
while True:
    ciphertext += plaintext[currentIndex]
    if (currentIndex==len(plaintext)-1):
        break
    currentIndex += lengthOfCylinder
    
    if (currentIndex >=len(plaintext)):
        currentIndex %= lengthOfCylinder
        currentIndex += 1
print(ciphertext)