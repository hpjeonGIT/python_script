#! /usr/bin/python
#
#
print "==============================================="
print " Select each column from each file and combine "
print "==============================================="
print

print "default input 1 is afmtip.dat with 2nd column"
input1 = raw_input("Just return for default or Enter file name:")
if input1 == '':
    input1 = 'afmtip.dat'
    print "Input file is \"afmtip.dat\""
else:
    print "Input file is", input1
print
n1 = raw_input("Just return for default or column number:")
if n1 == '':
    n1 = 2
    print "Input1 column is \"2\""
else:
    print "Input1 column is", n1
print

n1 = int(n1)

print "default input 2 is result.dat with 2nd column"
input2 = raw_input("Just return for default or Enter file name:")
if input2 == '':
    input2 = 'result.dat'
    print "Input file is \"result.dat\""
else:
    print "Input file is", input2
print
n2 = raw_input("Just return for default or column number:")
if n2 == '':
    n2 = 2
    print "Input2 column is \"2\""
else:
    print "Input2 column is", n2
print

n2 = int(n2)




inp1 = open(input1)
inp2 = open(input2)
output = open("combo.dat",'w')
line1 = inp1.readline()
line2 = inp2.readline()
while line1:
	word1 = line1.split()
	word2 = line2.split()
	xx = float(word1[n1-1])
	yy = float(word2[n2-1])
	print >> output, xx, yy
	line1 = inp1.readline()
	line2 = inp2.readline()
	
inp1.close()
inp2.close()
output.close()
