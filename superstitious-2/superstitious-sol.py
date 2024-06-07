from Crypto.Util.number import *
n = 550201148354755741271315125069984668413716061796183554308291706476140978529375848655819753667593579308959498512392008673328929157581219035186964125404507736120739215348759388064536447663960474781494820693212364523703341226714116205457869455356277737202439784607342540447463472816215050993875701429638490180199815506308698408730404219351173549572700738532419937183041379726568197333982735249868511771330859806268212026233242635600099895587053175025078998220267857284923478523586874031245098448804533507730432495577952519158565255345194711612376226297640371430160273971165373431548882970946865209008499974693758670929
e = 65537
c = 12785320910832143088122342957660384847883123024416376075086619647021969680401296902000223390419402987207599720081750892719692986089224687862496368722454869160470101334513312534671470957897816352186267364039566768347665078311312979099890672319750445450996125821736515659224070277556345919426352317110605563901547710417861311613471239486750428623317970117574821881877688142593093266784366282508041153548993479036139219677970329934829870592931817113498603787339747542136956697591131562660228145606363369396262955676629503331736406313979079546532031753085902491581634604928829965989997727970438591537519511620204387132

# The restriction is that every other bit must be 0
# Equivalently, in base 4, the primes must only
# have digits 0 and 1.
# This means that there are 2 total bits of info in
# each base-4 digit of the primes (one from each)
# and we get 2 bits of info from the product, so
# we can recover the primes just by brute force.
# We start from the least significant bit and
# work our way up, adding two bits at a time and
# keeping track of all of the candidates.

bits = 2 # number of bits we have so far
candidates = [(1,1)] # primes must be odd

def lastBits(n, b): # last b bits of n
    return n & ((1 << b) - 1)

while bits < 1025:
    step = 1 << bits # some power of 4
    bits += 2
    target = lastBits(n, bits)
    new_candidates = []
    # check each possibilities for the next 2 bits
    # either 00 or 01 (i.e. keep the same or add step)
    for (i, j) in candidates:
        if lastBits(i*j, bits) == target:
            new_candidates.append((i, j))
        if lastBits((i+step)*j, bits) == target:
            new_candidates.append((i+step, j))
        if lastBits(i*(j+step), bits) == target:
            new_candidates.append((i, j+step))
        if lastBits((i+step)*(j+step), bits) == target:
            new_candidates.append((i+step, j+step))
    candidates = new_candidates
    print(bits, "bits:", len(candidates), "candidates")

p = q = 0
for (i, j) in candidates:
    if i*j == n:
        print("Found factors",i, j)
        p = i
        q = j
        break

phi = (p-1)*(q-1)
d = pow(e, -1, phi)
m = pow(c, d, n)
print(long_to_bytes(m))
