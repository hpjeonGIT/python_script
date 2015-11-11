#! /usr/bin/python
#
# Read xyz and calculate tilt angle of alkanechain and extract
# headgroup position data
# 10/11/2005 Byoungseon Jeon @LANL
#
def NINT(x):
    if (x >= 0.):
        y = int(x)
        z = int(x+0.5)
        if (y == z):
            ans = float(y)
        else:
            ans = float(z)
    else :
        y = int(x)
        z = int(x-0.5)
        if (y == z):
            ans = float(y)
        else:
            ans = float(z)        
    return ans

print "============================================================"
print " XYZ analysis for alkanethiol type Self assembled monolayer "
print "============================================================"
print " Read post.xyz"
print
inp = raw_input(" input box size x/y/z :")
inp = inp.split()
box = ['1', '2','3']
box[0] = float(inp[0])
box[1] = float(inp[1])
box[2] = float(inp[2])
print box
#
#
input = open("post.xyz")
output = open("angle.dat", 'w')
import math
import array
#
# Number set
Nhead = 1000
Nfft = 40
hfile = "head_sf"
#
#
hx = array.array("f", range(Nhead))
hy = array.array("f", range(Nhead))
hz = array.array("f", range(Nhead))
line = input.readline()
n = -1 
while line:
    word = line.split()
    Nptcl = int(word[0])
    line = input.readline()
    theta = 0.
    vz = 1.
    m = 0
    s = 1.
    sum = 0.0
    l = 0
    #print >> output, "Headgroup data for", n+1, "th dump"
    for i in range(0, Nptcl):
        line = input.readline()
        word = line.split()
        if (word[0] == 'S'):
            theta = math.acos(vz/s)
            sum = sum + theta
            #print m, sum*180./math.pi, theta*180./math.pi
            xx = float(word[1])
            xy = float(word[2])
            xz = float(word[3])
            vx = 0.
            vy = 0.
            vz = 0.
            l = 0
            m = m + 1 
            #print >> output, '%5i %10.5f %10.5f %10.5f' % (m, xx, xy, xz)
            hx[m-1] = xx
            hy[m-1] = xy
            hz[m-1] = xz
        else:            
            l = l + 1
        if ( l == 1 and word[0] == 'C'):
            x = float(word[1])
            y = float(word[2])
            z = float(word[3])
            x = x - xx
            y = y - xy
            z = z - xz
            x = x - box[0]*NINT(x/box[0])
            y = y - box[1]*NINT(y/box[1])
            z = z - box[2]*NINT(z/box[2])
            xx = xx + 0.29866*x
            xy = xy + 0.29866*y
            xz = xz + 0.29866*z
           
        if ((l+1)%2 == 1 and word[0] != 'S'):
            yx = float(word[1])
            yy = float(word[2])
            yz = float(word[3])
            x = yx - xx
            x = x - box[0]*NINT(x/box[0])
            y = yy - xy
            y = y - box[1]*NINT(y/box[1])
            z = yz - xz
            z = z - box[2]*NINT(z/box[2])
            s = math.sqrt(x*x + y*y + z*z)
            vx = vx + x/s
            vy = vy + y/s
            vz = vz + z/s
            s = math.sqrt(vx*vx + vy*vy + vz*vz)
    theta = math.acos(vz/s)
    sum = sum + theta
    n = n + 1
    print >> output,  n, m, 180.*sum/m/math.pi
    line = input.readline()


input.close()
output.close()
            
        

    
