#! /usr/local/bin/python
#
# AuSCH3 structure - self assembled monolayer result analysis program
# Using each atom's coordinates, estimate distance from gold surface
# and angle between them

print "==================================="
print " Self-Assembled Monolayer analyzer"
print "==================================="
print
S = raw_input(" coordinate of S(in Angstrom):")
print
S = S.split()
S[0] = float(S[0])
S[1] = float(S[1])
S[2] = float(S[2])
C = raw_input(" coordinate of C(in Angstrom):")
print
C = C.split()
C[0] = float(C[0])
C[1] = float(C[1])
C[2] = float(C[2])
print
au = "0 0 0"
au = au.split()
dir = raw_input(" 1 for atop, 2 for bridge, 3 for fcc & hcp :")
if dir == '1':
    au = raw_input(" coordinate of Au(in Angstrom):")
    au = au.split()
    au[0] = float(au[0])
    au[1] = float(au[1])
    au[2] = float(au[2])
elif dir == '2':
    au1 = raw_input(" coordinate of Au 1 (in Angstrom):")
    au2 = raw_input(" coordinate of Au 2 (in Angstrom):")
    au1 = au1.split()
    au1[0] = float(au1[0])
    au1[1] = float(au1[1])
    au1[2] = float(au1[2])
    au2 = au2.split()
    au2[0] = float(au2[0])
    au2[1] = float(au2[1])
    au2[2] = float(au2[2])
    au[0] = (au1[0]+au2[0])/2.
    au[1] = (au1[1]+au2[1])/2.
    au[2] = (au1[2]+au2[2])/2.
elif dir == '3':
    au1 = raw_input(" coordinate of Au 1 (in Angstrom):")
    au2 = raw_input(" coordinate of Au 2 (in Angstrom):")
    au3 = raw_input(" coordinate of Au 3 (in Angstrom):")
    au1 = au1.split()
    au1[0] = float(au1[0])
    au1[1] = float(au1[1])
    au1[2] = float(au1[2])
    au2 = au2.split()
    au2[0] = float(au2[0])
    au2[1] = float(au2[1])
    au2[2] = float(au2[2])
    au3 = au3.split()
    au3[0] = float(au3[0])
    au3[1] = float(au3[1])
    au3[2] = float(au3[2])
    au[0] = (au1[0]+au2[0]+au3[0])/3.
    au[1] = (au1[1]+au2[1]+au3[1])/3.
    au[2] = (au1[2]+au2[2]+au3[2])/3.
else:
    import sys
    print
    sys.exit(" YOU STUPID ! I told you 1 or 2 or 3 !!! ")


#
# Distance estimation
print
print "z-direction b/w Au surface and Sulfur =", S[2] - au[2]
print
#
# Angle estimation
import math
l1 = (C[0] - S[0])**2 + (C[1] - S[1])**2 + (C[2] - S[2])**2
l11 = math.sqrt(l1)
l2 = abs(S[2])
l3 = (C[0] - S[0])**2 + (C[1] - S[1])**2 + (C[2])**2
phi = math.acos((l1+l2**2 - l3)/2./l11/l2)
print " Angle along Carbon-Sulfur-Au slab =", phi*180./math.pi
print
phi = math.atan((-C[1]+S[1])/(C[0]-S[0]))
print " Angle along horizon-Sulfur-Carbon =", phi*180./math.pi
print
