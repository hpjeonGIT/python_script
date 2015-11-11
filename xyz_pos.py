#! /usr/bin/python
#
# Convert xyz data into poscar format for max. packed state
# 06/30/2004 Byoungseon Jeon @LANL
#
print "================================================"
print " XYZ -> POSCAR converter for max. packed state"
print "================================================"
print " Read temp.xyz and export to poscar"
print
print "Default lattice constants, a = 4.08"
a = 4.08
sqrt2 = 1.4142135623730951
sqrt3 = 1.7320508075688772
sqrt6 = 2.4494897427831779
print 
print "Enter z-length"
print " 2 layer Au - 2.0484472022418716"
print " 3 layer Au - 2.3371223368366847"
print " 4 layer Au - 2.6257974714314973"
print " 5 layer Au - 2.9144726060263104"
z = raw_input("Input appropriate length:")
z = float(z)
input = open("temp.xyz")
poscar = open("poscar",'w')

print >> poscar, "Maximum packing SAM"
print >> poscar, ' %19.16f ' %  (a*2.)
print >> poscar,  '     %19.16f %19.16f %19.16f' % (1.5/sqrt2/2.0, -sqrt6/8., 0.0)
print >> poscar,  '     %19.16f %19.16f %19.16f' % (1.5/sqrt2/2.0, sqrt6/8., 0.0)
print >> poscar,  '     %19.16f %19.16f %19.16f' % (0.0, 0.0, z)
print >> poscar, "1  1  3  6" 
print >> poscar, "Selective dynamics"
print >> poscar, "Direct"

line = input.readline()
word = line.split()
Natom = int(word[0])
line = input.readline()
j=1
for i in range(0, Natom):
	line = input.readline()
	word = line.split()
	name = word[0]
	xx = float(word[1])
	yy = float(word[2])
	zz = float(word[3])
	alpha = (xx/sqrt3 - yy)*sqrt6/a/3.0
	beta = (xx/sqrt3 + yy)*sqrt6/a/3.0	
	print "alpha, beta", alpha, beta
	print >> poscar, ' %19.16f %19.16f %19.16f' % ( alpha, beta, zz/z/a/2.),  "F  F  T   #", name, j
	j = j + 1 

input.close()
poscar.close()
