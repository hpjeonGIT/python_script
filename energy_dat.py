#! /usr/bin/python
#
# Translator from VASP OUTCHAR file to XMOL XYZ file
# Especially remap the positions of atoms
#
# 01/08/2003 Byoungseon Jeon @ LANL
#
print "=========================="
print " Energy data plot of VASP "
print "=========================="
print
print "Default input file is \"OUTCAR\""
#
# INPUT file name selection
#
inputfile = raw_input("Just return for default or Enter file name:")
if inputfile == '':
    inputfile = 'OUTCAR'
    print "Input file is \"OUTCAR\""
else:
    print "Input file is", inputfile
print

#
# OUTPUT file name selection
#
print "Default outputfile is \"energy.dat\""
outputfile = raw_input("Just return for default or Enter file name:")
if outputfile == '':
    outputfile = 'energy.dat'
    print "Output file is \"energy.dat\""
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

print >> output, "# frame number, energy(eV), dE b/w step"
#
# search for energy of structure
#
line = input.readline()
temp = 1
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
                oldE = energy
                temp = 0
        word = 0
    line = input.readline()
    if temp == 0:
        line = 0
        
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
                count = count + 1
                print >> output, count, energy , float(energy) - float(oldE)
                oldE = energy
                Nlist = 0
        word = 0
    line = input.readline()
input.close()
output.close()

