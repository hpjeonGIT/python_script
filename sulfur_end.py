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
#output = open("headgroup.dat", 'w')
import math
import array
#
# Number set
Nhead = 2000
Nfft = 80
Nfftx = int(box[0]/math.pi) + 1
Nffty = int(box[1]/math.pi) + 1
Nffty = Nfftx
hfile = "xyvmap"
#
#
hx = array.array("f", range(Nhead))
hy = array.array("f", range(Nhead))
vx = array.array("f", range(Nhead))
vy = array.array("f", range(Nhead))
line = input.readline()
n = -1 
while line:
    word = line.split()
    Nptcl = int(word[0])
    line = input.readline()
    m = 0
    l = 0
    #print >> output, "Headgroup data for", n+1, "th dump"
    for i in range(0, Nptcl):
        line = input.readline()
        word = line.split()
        if (word[0] == 'S'):
            xx = float(word[1])
            xy = float(word[2])
            l = 0
            m = m + 1 
            hx[m-1] = xx
            hy[m-1] = xy
        else:            
            l = l + 1
            x = float(word[1])
            y = float(word[2])            
            x = x - xx
            y = y - xy
            x = x - box[0]*NINT(x/box[0])
            y = y - box[1]*NINT(y/box[1])
            vx[m-1] = x
            vy[m-1] = y
    n = n + 1
    print n
    title = hfile + str(n) + '.dat'
    output2 = open(title, 'w')
    for i in range(0,m):
        print >> output2, hx[i], hy[i], vx[i]/box[0]/1., vy[i]/box[1]/1.
    output2.close()
    line = input.readline()


input.close()
#output.close()
            
        

    
