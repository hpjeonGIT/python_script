#! /usr/bin/python
#
# FCC crystal point generator
# After point generation, they are translated into
# POSCAR format
#
# 01/29/2004 Byoungseon Jeon @ LANL
#
print "============================="
print " Self-Assembled Monolayer generator "
print "============================="
print
print "Default lattice constants, a = 4.08"

#
# X-direction
yinput = raw_input( "Number of Au for x-dir(default=5)")
if yinput == '':
	yinput = 5
	print "Number of Au for x-dir is 5"
else:
	print "Number of Au for x-dir is", yinput
	yinput = int(yinput)
	#
# Y-direction
xinput = raw_input( "Number of Au for y-dir(default=5)")
if xinput == '':
	xinput = 5
	print "Number of Au for y-dir is 5"
else:
	print "Number of Au for y-dir is", xinput
	xinput = int(xinput)
#
# Z-direction
zinput = raw_input( "Number of layers (z-dir, default=2)")
if zinput == '':
	zinput = 2
	print "Number of layers is 2"
else:
	print "Number of Au for z-dir is", zinput
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
xyz = raw_input(" Origin point(default = 0 0 0)" )
if xyz == '':
	xyz = ' 0 0 0 '
	print "Origin point is 0 0 0 "
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
outputfile = 'crystal_pre.xyz'
output = open(outputfile,'w')
#
#
n = 1
minx = 100.0
miny = 100.0
minz = 100.0
maxx = 0.0
maxy = 0.0
maxz = 0.0
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
			if xx < minx:
				minx = xx
			if xx > maxx:
				maxx = xx
			yy = (-x + 2*y + z)/sqrt2/sqrt3
			if yy < miny:
				miny = yy
			if yy > maxy:
				maxy = yy
			zz = (x + y - z)/sqrt3
			if zz < minz:
				minz = zz
			if zz > maxz:
				maxz = zz
			print >> output,"Au",  xx,yy, zz , "# ",n 
			i = i + 1
			n = n + 1
		i = 0
		j = j + 1
	j = 0
	k = k + 1

output.close()
input = open(outputfile)
poscar = open('poscar','w')
crystal = open('crystal_post.xyz','w')
print "==========================="
print " POSCAR format translation "
print "==========================="
print
print "Origin point will be 0.10766937  1.15769148  0.00000000"
orig = raw_input( "Return for default or Enter new position")
if orig == '':
	orig = '0.10766937  1.15769148  0.00000000'
	print 'Origin will be ', orig
else:
	print 'Origin will be ', orig

print
print " length of x/y-dir. will be estimated by itself considering periodic B/C"
print " vacuum thickness will be 22.6444 A"
lz = raw_input( "Return for default or Enter new vacuum thickness:" )
if lz == '':
	lz = 22.6444
	print "length of z-dir. is", lz
else:
	lz = float(lz)
	print "length of z-dir. is", lz
lx = float(yinput) * a /sqrt2
ly = float(xinput) * a * sqrt6 /4.
#
# add SCH3 to lz
lz = (float(zinput) - 1.) * a / sqrt3 + 4.359740072 + lz
print  " Enter 3 Au atom numbers where sulfur will be located "
print  " If 1 or 2 atoms are given, enter 100 as the others. "
sulfur = raw_input( " Default number is 8 9 10. Return or Enter numbers: ")
if sulfur == '':
	sulfur = '8 9 10'
	print " 3 Au atoms are ", sulfur
else:
	print " 3 Au atoms are ", sulfur
tri = sulfur.split()
tri[0] = int(tri[0])
tri[1] = int(tri[1])
tri[2] = int(tri[2])

print " Enter another 3 Au atom numbers - like fcc-bridge"
print " If these atoms are not needed, just enter 100 100 100"
sulfur = raw_input( " Default number is 100 100 100. Return or Enter numbers: ")
if sulfur == '':
        sulfur = '100 100 100'
        print " 3 Au atoms are ", sulfur
else:
        print " 3 Au atoms are ", sulfur
ttri = sulfur.split()
ttri[0] = int(ttri[0])
ttri[1] = int(ttri[1])
ttri[2] = int(ttri[2])

sx = 0.0
sy = 0.0
sz = 0.0
ssx = 0.0
ssy = 0.0
ssz = 0.0
ss = '   1.5501658715130164 5.3218165755521376 4.4026222589718955 '
cc = '   2.6760829241636337 4.8087360947839448 5.7753633342946804' 
hh1 = '  2.2236502370035001 5.1456056738704925 6.7153291470920138'
hh2 = '  3.6694764832537698 5.2534635773103755 5.6523101982802695'
hh3 = '  2.7477746053778658 3.7173327983241387 5.7541425809290265 '

s = ss.split()
c = cc.split()
h1 = hh1.split()
h2 = hh2.split()
h3 = hh3.split()

s[0] = float(s[0])
s[1] = float(s[1])
s[2] = float(s[2])
c[0] = float(c[0])
c[1] = float(c[1])
c[2] = float(c[2])
h1[0] = float(h1[0])
h1[1] = float(h1[1])
h1[2] = float(h1[2])
h2[0] = float(h2[0])
h2[1] = float(h2[1])
h2[2] = float(h2[2])
h3[0] = float(h3[0])
h3[1] = float(h3[1])
h3[2] = float(h3[2])

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
xx = xx /lx
yy = yy /ly
zz = zz /lz

print >> poscar, "poscar"
print >> poscar, ' %19.16f ' %  (a*2.)
print >> poscar,  '     %19.16f %19.16f %19.16f' % (lx/a/2., 0.0, 0.0)
print >> poscar,  '     %19.16f %19.16f %19.16f' % (0.0, ly/a/2., 0.0)
print >> poscar,  '     %19.16f %19.16f %19.16f' % (0.0, 0.0, lz/a/2.)
print >> poscar, "1  1  3 ", n
print >> poscar, "Selective dynamics"
print >> poscar, "Direct"
print >> crystal, n+5
print >> crystal, "Frame = 1   Energy = 100"
k=0
kk = 0
for i in range(0,n-1):
	line = input.readline()
	word = line.split()
	xx = float(word[1]) - minx + pntx
	yy = float(word[2]) - miny + pnty
	zz = float(word[3]) - minz + pntz
	xx = xx/lx
	if xx > 1.0:
		xx = xx - 1.0
		if xx > 1.0:
			xx = xx - 1.0
	yy = yy/ly
	if yy > 1.0:
		yy = yy - 1.0
		if yy > 1.0:
			yy = yy - 1.0
	zz = zz/lz
	if zz > 1.0:
		zz = zz - 1.0
		if zz > 1.0:
			zz = zz - 1.0
	if (i+2) == tri[0]:
		sx = sx + xx
		sy = sy + yy
		k = k + 1
	if (i+2) == tri[1]:
		sx = sx + xx
		sy = sy + yy
		k = k + 1
	if (i+2) == tri[2]:
		sx = sx + xx
		sy = sy + yy
		k = k + 1
        if (i+2) == ttri[0]:
                ssx = ssx + xx
                ssy = ssy + yy
                kk = kk + 1
        if (i+2) == ttri[1]:
                ssx = ssx + xx
                ssy = ssy + yy
                kk = kk + 1
        if (i+2) == ttri[2]:
                ssx = ssx + xx
                ssy = ssy + yy
                kk = kk + 1

	i = i + 1

sx = sx /float(k)
sy = sy /float(k)
if kk > 0 :
	ssx = ssx /float(kk)
	ssy = ssy /float(kk)
	sx = (sx+ssx)/2.
	sy = (sy+ssy)/2.
sz = maxz + 2.04703319
c[0] = c[0] - s[0] + sx*lx
c[1] = c[1] - s[1] + sy*ly
c[2] = c[2] - s[2] + sz
h1[0] = h1[0] - s[0] + sx*lx
h1[1] = h1[1] - s[1] + sy*ly
h1[2] = h1[2] - s[2] + sz
h2[0] = h2[0] - s[0] + sx*lx
h2[1] = h2[1] - s[1] + sy*ly
h2[2] = h2[2] - s[2] + sz
h3[0] = h3[0] - s[0] + sx*lx
h3[1] = h3[1] - s[1] + sy*ly
h3[2] = h3[2] - s[2] + sz

print >> crystal, 'S', sx*lx, sy*ly, sz, '# S'
print >> crystal, 'C', c[0], c[1], c[2], '# C'
print >> crystal, 'H', h1[0], h1[1], h1[2], '# H'
print >> crystal, 'H', h2[0], h2[1], h2[2], '# H'
print >> crystal, 'H', h3[0], h3[1], h3[2], '# H'

print >> poscar ,  ' %19.16f %19.16f %19.16f' % ( sx, sy, sz/lz), "  F   F   T  # S "
print >> poscar ,  ' %19.16f %19.16f %19.16f' % ( c[0]/lx, c[1]/ly, c[2]/lz), "  T   T   T  # C "
print >> poscar ,  ' %19.16f %19.16f %19.16f' % ( h1[0]/lx, h1[1]/ly, h1[2]/lz), "  T   T   T  # H "
print >> poscar ,  ' %19.16f %19.16f %19.16f' % ( h2[0]/lx, h2[1]/ly, h2[2]/lz), "  T   T   T  # H "
print >> poscar ,  ' %19.16f %19.16f %19.16f' % ( h3[0]/lx, h3[1]/ly, h3[2]/lz), "  T   T   T  # H "

input.close()
input = open(outputfile)
line = input.readline()
line = input.readline()
line = input.readline()
word = line.split()
xx = float(word[1]) - minx + pntx
yy = float(word[2]) - miny + pnty
zz = float(word[3]) - minz + pntz
xx = xx /lx
yy = yy /ly
zz = zz /lz

i = 0
print >> poscar, ' %19.16f %19.16f %19.16f' % (xx, yy, zz), "  F   F   F  # 1"
print >> crystal, 'Au', xx*lx, yy*ly, zz*lz, '#', i+1

for i in range(0,n-1):
	line = input.readline()
	word = line.split()
	xx = float(word[1]) - minx + pntx
	yy = float(word[2]) - miny + pnty
	zz = float(word[3]) - minz + pntz
	xx = xx/lx
	if xx > 1.0:
		xx = xx - 1.0
		if xx > 1.0:
			print i+2, "th atom location for x-dir. is modified"
			xx = xx - 1.0
	yy = yy/ly
	if yy > 1.0:
		yy = yy - 1.0
		if yy > 1.0:
			print i+2, "th atom location for y-dir. is modified"
			yy = yy - 1.0
	zz = zz/lz
	if zz > 1.0:
		zz = zz - 1.0
		if zz > 1.0:
			print i+2, "th atom location for z-dir. is modified"
			zz = zz - 1.0
	print >> poscar, ' %19.16f %19.16f %19.16f' % (xx, yy, zz), "  F   F   T  #", i+2
	print >> crystal, 'Au', xx*lx, yy*ly, zz*lz, '#', i+2
	i = i + 1

input.close()
poscar.close()
crystal.close()
