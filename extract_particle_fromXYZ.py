#! /usr/bin/python
inputfile = 'particle.xyz'
outputfile = 'data1.dat'
input = open(inputfile)
output = open(outputfile, 'w')
inpN  = raw_input("Number of particles?:")
inpN = int(inpN)
#
line = input.readline()
word = line.split()
Npt = int(word[0])
j = 0
while line:
    line = input.readline()
    for i in range(0, Npt):
        line = input.readline()
        word = line.split()
        if i == inpN-1:
            j = j + 1
            print >> output, j,  word[0],word[1],word[2] ,word[3]
    line = input.readline()
    
input.close()
output.close()
