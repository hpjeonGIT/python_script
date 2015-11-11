#! /usr/bin/python
#
#
import math
print "===================================="
print
print "Default input file is sfactor4.dat"
#
# INPUT file name selection
#
inputfile = raw_input("Just return for default or Enter file name:")
if inputfile == '':
    inputfile = 'sfactor4.dat'
    print "Input file is sfactor4.dat"
else:
    print "Input file is", inputfile
print

#
input = open(inputfile)
output = open('temp.dat', 'w')
line = input.readline()
#
# find the number of atoms of each kind
#
line = input.readline()
while line:  
	word = line.split()
	if ( word[0] != '0' or word[1] != '0'):
		print >> output, word[0], word[1], math.sqrt(float(word[2]))
    	line = input.readline()

input.close()
output.close()

