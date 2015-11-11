#! /usr/bin/python
#
# Translator from VASP OUTCHAR file to XMOL XYZ file
# Especially remap the positions of atoms
#
# 01/08/2003 Byoungseon Jeon @ LANL
#
print "===================================="
print " Translator from VASP OUTCAR to XYZ"
print "===================================="
print
print "Default input file is OUTCAR"
#
# INPUT file name selection
#
inputfile = raw_input("Just return for default or Enter file name:")
if inputfile == '':
    inputfile = 'OUTCAR'
    print "Input file is OUTCAR"
else:
    print "Input file is", inputfile
print

#
# OUTPUT file name selection
#
print "Default outputfile is vasp.xyz"
outputfile = raw_input("Just return for default or Enter file name:")
if outputfile == '':
    outputfile = 'vasp.xyz'
    print "Output file is vasp.xyz"
else:
    print "Output file is", outputfile
print

#
# Open all files
#
input = open(inputfile)
output = open(outputfile, 'w')

#
# initialize all variables
#
count = 1  # counter number in the XYZ file
Nlist = 0  # dummy variabe for array of atoms
Ntype = 0  # number of kinds of atoms 
i = 0
j = 0
k = 0
Nall = 0  # number of all atoms

line = input.readline()
atom = ['']
Natom = ['']

#
# search how many kind of atoms are estimated
#
while line:  
    line = input.readline()
    word = line.split()
    while word:
        if word[0] == 'POTCAR:':
            atom.append(word[2])
            Ntype = Ntype + 1
        if word[0] == 'VRHFIN':
            Ntype = Ntype - 1
            line = 0
            word = 0
            break
        word = 0


del atom[0]  # delete dummy array
del atom[Ntype] # last array is duplicated, therefore delete


line = input.readline()
#
# find the number of atoms of each kind
#
while line:  
    line = input.readline()
    word = line.split()
    while word:
        if word[0] == 'ions':
            for i in range(0, Ntype):
                Natom.append(word[i+4])
                i = i + 1
            line = 0
        word = 0

del Natom[0] # delete dummy array

#
# remapping of atomic names along atom numbers
#
type = [''] 
for j in range(0, i):
    Nall = Nall + int(Natom[j])
    for k in range(0,int(Natom[j])):
        type.append(atom[j])
        k = k+1
    j = j + 1
del type[0] # delete dummy array


#
# search for position of atoms
#
line = input.readline()
while line:  
    word = line.split()
    while word:
        if len(word) > 2:
            if word[1] == 'ENERGIE':
                line = input.readline()
                line = input.readline()
		line = input.readline()
		line = input.readline()
                word = line.split()
                energy = word[6]
        if len(word) > 2 :
            if word[2] == '(eV/Angst)':
                print >> output, Nall
                print >> output, 'frame = ', count, ' energy = ', energy
                count = count + 1
                input.readline()
                for Nlist in range(0,Nall):
                    line = input.readline()
                    xyz = line.split()
                    print >> output, type[Nlist], xyz[0], xyz[1], xyz[2], "#", Nlist + 1
                    Nlist = Nlist + 1
                Nlist = 0
        word = 0
    line = input.readline()
        
input.close()
output.close()

