#! /usr/local/bin/python
#
# Convert CONTCAR data into XYZ format
#
print "====================================="
print " Translator from VASP CONTCAR to XYZ"
print " And expand periodic str. into real "
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
print "Default outputfile is many.xyz"
outputfile = raw_input("Just return for default or Enter file name:")
if outputfile == '':
    outputfile = 'many.xyz'
    print "Output file is many.xyz"
else:
    print "Output file is", outputfile
print
#
# Expansion rate
nx = 4 
ny = 4 
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
print >> output, natom*nx*ny
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
    for j in range(0, nx):
        for k in range(0, ny):
            xx = vector11*word[0]+vector21*word[1]+vector31*word[2]
            xx = (xx+vector11*j+vector21*k)*scalefactor
            yy = vector12*word[0]+vector22*word[1]+vector32*word[2]
            yy = (yy+vector12*j+vector22*k)*scalefactor
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
            print >> output, text, '%19.16f %19.16f %19.16f' % (xx,yy,zz)," #",k+1+j*ny+i*nx*ny
input.close()
output.close()    
