#! /usr/local/bin/python
#
# Read xyz and map into new positions
#
# 07/01/2004 Byoungseon Jeon @LANL
#
print "===================="
print " All re-mapper "
print "Read post.xyz and write result.xyz"
print "===================="
print
#
#
coord = raw_input( " Enter new position of sulfur:")
word = coord.split()
xx = float(word[0])
yy = float(word[1])
zz = float(word[2])

input = open("post.xyz")
output = open("result.xyz",'w')
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
for i in range(0,Natom-1):
	line = input.readline()
	word = line.split()
	name = word[0]
	x = float(word[1]) - sx + xx
	y = float(word[2]) - sy + yy
	z = float(word[3])
	print >> output, word[0], '%19.16f %19.16f %19.16f' % (x, y, z)
input.close()
output.close()
