#! /usr/bin/python
#
# Convert CONTCAR data into XYZ format
#
print "====================================="
print " Translator from VASP CONTCAR to XYZ"
print "====================================="
print
print "Default input file is CONTCAR"
#
# INPUT file name selection
#
inputfile = raw_input("Just return for default or Enter file name:")
if inputfile == '':
    inputfile = 'CONTCAR'
    print "Input file is CONTCAR"
else:
    print "Input file is", inputfile
print
#
# OUTPUT file name selection
#
print "Default outputfile is result.xyz"
outputfile = raw_input("Just return for default or Enter file name:")
if outputfile == '':
    outputfile = 'result.xyz'
    print "Output file is result.xyz"
else:
    print "Output file is", outputfile
print
#
# Open all files
#
input = open(inputfile)
output = open(outputfile, 'w')
#
# Header
line = input.readline()
#
# Scalefactor
line = input.readline()
word = line.split()
scalefactor = float(word[0])
#
# vector 1
line = input.readline()
word = line.split()
vector11 = float(word[0])
vector12 = float(word[1])
vector13 = float(word[2])
#
# vector 2
line = input.readline()
word = line.split()
vector21 = float(word[0])
vector22 = float(word[1])
vector23 = float(word[2])
#
# vector 3
line = input.readline()
word = line.split()
vector31 = float(word[0])
vector32 = float(word[1])
vector33 = float(word[2])
#
# Number of atoms
line = input.readline()
word = line.split()
kind = word
number = len(word)
natom = 0
for i in range(0,number):
	natom = natom + int(word[i])
	kind[i] = int(word[i])
print >> output, natom
print >> output, "frame = 1  energy = 1000"
#
# keyword
line = input.readline()
#
# keyword
line = input.readline()
for i in range(0,natom):
	line = input.readline()
	word = line.split()
	word[0] = float(word[0])
	word[1] = float(word[1])
	word[2] = float(word[2])
	xx = vector11*word[0]+vector21*word[1]+vector31*word[2]
	xx = xx*scalefactor
	yy = vector12*word[0]+vector22*word[1]+vector32*word[2]
	yy = yy*scalefactor
	zz = vector13*word[0]+vector23*word[1]+vector33*word[2]
	zz = zz*scalefactor

	if i < (kind[0]+kind[1]+kind[2]+kind[3]):
		text = "Au"
	if i < (kind[0]+kind[1]+kind[2]):
		text = "H"
	if i < (kind[0]+kind[1]):
		text = "C"
	if i < (kind[0]):
		text = "S"
	print >> output, text, '%19.16f %19.16f %19.16f' % (xx,yy,zz)," #",i+1
input.close()
output.close()    
