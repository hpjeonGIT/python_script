#! /usr/bin/python
#

print "==================================="
print " Self-Assembled Monolayer analyzer"
print " Z(height) finder"
print "==================================="
print

Nhead = 5 # number of alkanethiol head group atoms
inputfile = raw_input("Just return for default or Enter file name:")
if inputfile == '':
    inputfile = 'aaa.xyz'
    print "Input file is aaa.xyz"
else:
    print "Input file is", inputfile
print

input = open(inputfile)
line = input.readline()
word = line.split()
Natom = int(word[0])
line = input.readline()
while line:
	line = input.readline()
	word = line.split()
	if word[0] == 'S':
		thiol = float(word[3])
	if word[0] == 'Au':
		line = 0

Ncount = 1
line = input.readline()
temp = line
while temp:
	Ncount = Ncount + 1
	line = input.readline()
	temp = line
	word = line.split()
	if float(word[3]) > 0.1:
		temp = 0

for i in range(0, Natom - Nhead - Ncount - Ncount ):
	line = input.readline()

sum = 0.0
for i in range(0, Ncount):
	word = line.split()
	height = float(word[3])
	sum = sum + height
	line = input.readline()

average = sum/float(Ncount)

print " Height b/w average Au surface and thiol is", thiol - average

input.close()
