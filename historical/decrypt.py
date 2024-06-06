
plaintext = "hsggna0stiaeaetteyc4ehvdatyporwtyseefregrstaf_etposruouoy{qnirroiybrbs5edmothssavetc8hebhwuibihh72eyaoepmlvoet9lobulpkyenf4xpulsloinmelllisyassnousa31mebneedtctg_}eeedeboghbihpatesyyfolus1lnhnooeliotb5ebidfueonnactayseyle"

ciphertext = ""
currentIndex = 0

lengthOfCylinder = 13

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