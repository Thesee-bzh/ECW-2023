from z3 import *
from hashlib import md5

D = [ 0x01, 0x01, 0x01, 0x01, 0x02, 0x03, 0x03, 0x04, 0x05, 0x06, 0x01, 0x07, 0x02, 0x02, 0x03, 0x04, 0x04, 0x05, 0x06, 0x07, 0x07, 0x07, 0x02, 0x02, 0x08, 0x04, 0x05, 0x06, 0x07, 0x09, 0x09, 0x09, 0x09, 0x08, 0x04, 0x05, 0x06, 0x0a, 0x09, 0x0b, 0x0b, 0x08, 0x08, 0x08, 0x0d, 0x0a, 0x0a, 0x0a, 0x0c, 0x0b, 0x0b, 0x0e, 0x0d, 0x0d, 0x0a, 0x0f, 0x0f, 0x0c, 0x0b, 0x0e, 0x0e, 0x0e, 0x0d, 0x10, 0x0f, 0x0f, 0x0f, 0x12, 0x13, 0x13, 0x13, 0x0d, 0x10, 0x10, 0x11, 0x12, 0x12, 0x12, 0x12, 0x13, 0x13 ]

N = 81

# Build list of indexes in D sharing same value
L = []
for i in range(0x1, 0x14):
    l = [ x for x in range(len(D)) if D[x] == i ]
    if len(l) > 1:
        L.append(l)

# Build list of neighbors in a 9*9 square (mind the borders and corners !)
L_ = [ [] for i in range(N) ]
for i in range(9):
    for chunk in range(9):
        for j in range(-1, 2):
            for k in range(-1, 2):
                if ((-1 < k + i)
                    and (-1 < j + chunk)
                    and (k + i < 9)
                    and (j + chunk < 9)
	            and (k != 0 or j != 0)):
                    L_[i+9*chunk].append(k + i + (chunk + j) * 9)

# Create a list of N integers (representing characters in the string)
S = [Int("x_%s" % i) for i in range(N)]

# Create the SMT solver instance and feed it with constraints
s = Solver()
s.add( [ And(S[i] >= ord('a'), S[i] <= ord('e'), S[i] <= D.count(D[i]) + 0x60) for i in range(N) ])
s.add( [ Distinct([ S[i] for i in l]) for l in L ])
s.add( [ And( [ S[i] != S[neighbor] for neighbor in L_[i] ] ) for i in range(N) ] )

# Solve the problem
if s.check() == sat:
    # We have a solution !
    m = s.model()
    r = [m.evaluate(S[i]) for i in range(N)]
    m = ''.join([chr(i.as_long()) for i in r])
    print(m, '\n')
    # Show it as a 9*9 square
    chunks = [m[i:i+9] for i in range(0, len(m), 9)]
    for chunk in chunks:
        print(chunk)
    # Craft flag as requested
    print("\nECW{", md5(m.encode()).hexdigest(), "}", sep='')

"""
bcaedbabaadbcacdcdbcadbebabdebecaceccadadedabdbebcbcedcacaedababebdbcedcacacedaba

bcaedbaba
adbcacdcd
bcadbebab
debecacec
cadadedab
dbebcbced
cacaedaba
bebdbcedc
acacedaba

ECW{8b39553c944cdce4ea4f9a692168093b}
"""
