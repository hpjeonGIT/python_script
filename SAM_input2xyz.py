#! /usr/bin/python
#
# Convert xyz data into poscar format for max. packed state
# 06/30/2004 Byoungseon Jeon @LANL
#
print "============================="
print " SAM restart -> xyz  converter "
print "============================="
print " Read restart.dat and export to input.xyz"
print
print "default input is \"restart.dat\" "
input1 = raw_input("Just return for default or Enter file name:")
if input1 == '':
    input1 = 'restart.dat'
    print "Input file is \"restart.dat\""
else:
    print "Input file is", input1
print
input = open(input1)
output = open("input.xyz",'w')
line = input.readline()
line = input.readline()
line = input.readline()
line = input.readline()
line = input.readline()
word = line.split()
Natom = int(word[0])
print >> output, Natom
print >> output, "frame =       1 energy =     0.0"
for i in range(0, Natom):
	line = input.readline()
	word = line.split()
	name = word[0]
	xx = float(word[1])
	yy = float(word[2])
	zz = float(word[3])
	id = int(word[4])
	if (id == 1):
		print >> output, "C", xx, yy, zz
	if (id == 2):
		print >> output, "S", xx, yy, zz
	if (id == 3):
		print >> output, "C", xx, yy, zz

input.close()
output.close()
