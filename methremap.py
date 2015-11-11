#! /usr/local/bin/python
#
# Read xyz of methane and map into new positions
#
# 06/30/2004 Byoungseon Jeon @LANL
#
print "===================="
print " Methane re-mapper "
print "===================="
print " Read result.xyz and export temp.xyz"
print
#
#
coord = raw_input( " Enter new position of sulfur:")
word = coord.split()
xx = float(word[0])
yy = float(word[1])
zz = float(word[2])

input = open("result.xyz")
output = open("temp.xyz",'w')
#
# Read result.xyz
line = input.readline()
print >> output, line, 
word = line.split()
Natom = int(word[0])
line = input.readline()
print >> output, line,
#
# For sulfur
j = 1
line = input.readline()
word = line.split()
sx = float(word[1])
sy = float(word[2])
sz = float(word[3])
print >> output, word[0], '%19.16f %19.16f %19.16f' % (xx, yy, sz)
#
# For methane
#
for i in range(0,4):
	line = input.readline()
	word = line.split()
	name = word[0]
	x = float(word[1]) - sx + xx
	y = float(word[2]) - sy + yy
	z = float(word[3])
	print >> output, word[0], '%19.16f %19.16f %19.16f' % (x, y, z)
#
# Au data start
for i in range(0, Natom-5):
	line = input.readline()
	print >> output, line,
input.close()
output.close()
