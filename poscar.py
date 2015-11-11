#! /usr/local/bin/python
#
# Convert cartesian coordinate data
# into POSCAR format
input = open("ex.dat")
output = open("exx.dat","w")

line = input.readline()
while line:
	word = line.split()
	word[0] = float(word[0])/8.1600000000000001/0.7071067811865475
	word[1] = float(word[1])/8.1600000000000001/1.2247448713915889
	word[2] = float(word[2])/8.1600000000000001/2.0484472022418716
	print >> output, ' %19.16f %19.16f %19.16f' % (word[0],word[1],word[2]), " F  F  F "
	line = input.readline()

input.close()
output.close()    
