#! /usr/bin/python
#
# FCC crystal point generator
# After point generation, they are translated into
# POSCAR format
#
# 01/20/2004 Byoungseon Jeon @ LANL
#
print "============================="
print " FCC crystal point generator "
print "============================="
print
print "Default lattice constants, a = 4.08"

#
# X-direction
xinput = raw_input( "Number of points for x-dir(default=5)")
if xinput == '':
	xinput = 5
	print "Number of points for x-dir is 5"
else:
	print "Number of points for x-dir is", xinput
	xinput = int(xinput)
	#
# Y-direction
yinput = raw_input( "Number of points for y-dir(default=5)")
if yinput == '':
	yinput = 5
	print "Number of points for y-dir is 5"
else:
	print "Number of points for y-dir is", yinput
	yinput = int(yinput)
#
# Z-direction
zinput = raw_input( "Number of layers (z-dir, default=2)")
if zinput == '':
	zinput = 2
	print "Number of layers is 2"
else:
	print "Number of points for x-dir is", zinput
	zinput = int(zinput)
#
# lattice constant
a = raw_input( "lattice constant(default = 4.08)" )
if a == '':
	a = 4.08
	print "lattice constant is 4.08"
else:
	print "lattice constant is", a
	a = float(a)
#
# Configuration of origin
xyz = raw_input(" Origin point(default = 1 1 1)" )
if xyz == '':
	xyz = ' 1 1 1'
	print "Origin point is 1 1 1 "
else:
	print "Origin point is", xyz
#
# Initialization
xyz = xyz.split()
xx = xyz[0]
yy = xyz[1]
zz = xyz[2]
xx = float(xx)
yy = float(yy)
zz = float(zz)
zero = 0
i=0
j=0
k=0
pi = 3.1415926535897931
sqrt2 = 1.4142135623730951
sqrt3 = 1.7320508075688772
sqrt6 = 2.4494897427831779
#
# OUTPUT file 
print "Default output file is crystal.xyz"
outputfile = 'crystal.xyz'
output = open(outputfile,'w')
#
#
n = 1
minx = 1.0
miny = 1.0
minz = 1.0
print >> output, xinput*yinput*zinput
print >> output, "Frame = 1   Energy = 100" # dummy string
for k in range(0, zinput):
	for j in range(0, yinput):
		for i in range(zero, xinput):
			# 
			# lattice vector operation
			x = float(xyz[0]) + j*a*.5 + k*a*.5
			y = float(xyz[1]) + i*a*.5 + k*a*.5
			z = float(xyz[2]) + i*a*.5 + j*a*.5
			#
			# matrix rotation
			xx = x/sqrt2 + z/sqrt2
			if xx > (a*(yinput)/sqrt2 + 1. ):
				xx = xx - a*(yinput)/sqrt2
			if xx < minx:
				minx = xx
			yy = (-x + 2*y + z)/sqrt2/sqrt3
			if yy > (a*(xinput-1)/sqrt2 + 1. ):
				yy = yy - a*(xinput)*sqrt6/4.
			if yy < miny:
				miny = yy
			zz = (x + y - z)/sqrt3
			if zz < minz:
				minz = zz
			print >> output,"Au",  xx, yy, zz , "# ",n 
			i = i + 1
			n = n + 1
		i = 0
		j = j + 1
	j = 0
	k = k + 1

output.close()
input = open(outputfile)
poscar = open('poscar','w')
print "==========================="
print " POSCAR format translation "
print "==========================="
print
print "Origin point will be 0.10766937  1.15769148  0.00000000"
orig = raw_input( "Return for default or Enter new position")
if orig == '':
	orig = '0.10766937  1.15769148  0.0000000'
	print "Origin point will be", orig
else:
	print "Origin point will be", orig
print
lattc = raw_input("lattice constant? default is 8.1600000000000001")
if lattc == '':
	lattc = 8.1600000000000001
	print "Lattice constant is", lattc
else:
	print "Lattice constant is", lattc

lattc = float(lattc)

lattvx = raw_input("lattice vector for x?  default is 0.7071067810000000")
if lattvx == '':
	lattvx = 0.7071067810000000
	print "Lattice vector for x is", lattvx
else:
	print "Lattice constant is", lattvx

lattvx = float(lattvx)

lattvy = raw_input("lattice vector for y?  default is  1.2247448700000001")
if lattvy == '':
	lattvy = 1.2247448700000001
	print "Lattice vector for y is", lattvy
else:
	print "Lattice constant is", lattvy

lattvy = float(lattvy)

lattvz = raw_input("lattice vector for z?  default is 2.5980762110000000")

if lattvz == '':
	lattvz = 2.5980762110000000
	print "Lattice vector for z is", lattvz
else:
	print "Lattice constant is", lattvz

lattvz = float(lattvz)



pnt = orig.split()
pntx = pnt[0]
pnty = pnt[1]
pntz = pnt[2]
pntx = float(pntx)
pnty = float(pnty)
pntz = float(pntz)

line = input.readline()
word = line.split()
n = word[0]
n = int(n)
i = 0
line = input.readline()
line = input.readline()
word = line.split()

xx = float(word[1]) - minx + pntx
yy = float(word[2]) - miny + pnty
zz = float(word[3]) - minz + pntz
xx = xx /lattc/lattvx
yy = yy /lattc/lattvy
zz = zz /lattc/lattvz
print minz, pntz, zz
print >> poscar, ' %19.16f %19.16f %19.16f' % (xx, yy, zz), "  F   F   F  # 1"
for i in range(0,n-1):
	line = input.readline()
	word = line.split()
	xx = float(word[1]) - minx + pntx
	yy = float(word[2]) - miny + pnty
	zz = float(word[3]) - minz + pntz
	xx = xx /lattc/lattvx
	if xx > 1.0:
		xx = xx - 1.0
	yy = yy /lattc/lattvy
	if yy > 1.0:
		yy = yy - 1.0
	zz = zz /lattc/lattvz
	if zz > 1.0:
		zz = zz - 1.0
	print >> poscar, ' %19.16f %19.16f %19.16f' % (xx, yy, zz), "  F   F   F  #", i+2
	i = i + 1

input.close()
poscar.close()

