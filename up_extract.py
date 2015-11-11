#! /usr/bin/python
#
# Extract energy and pressure from OUTCAR
#
# 11/22/2005 Byoungseon Jeon @ LANL
#
import array
print "=========================="
print " Energy data plot of VASP "
print "=========================="
print
print "Default input file is \"OUTCAR\""
#
# INPUT file name selection
#
inputfile = raw_input("Just return for default or Enter file name:")
if inputfile == '':
    inputfile = 'OUTCAR'
    print "Input file is \"OUTCAR\""
else:
    print "Input file is", inputfile
print

#
# Open all files
#
input = open(inputfile)
output = open("u_p.dat", 'w')
Nmax = 10000
e0 = array.array("f", range(Nmax))
es = array.array("f", range(Nmax))
pr = array.array("f", range(Nmax))
ps = array.array("f", range(Nmax))
#
# initialize all variables
#
count = 1  # counter number in the XYZ file
Nlist = 0  # dummy variabe for array of atoms
Ntype = 0  # number of kinds of atoms 
i = 0
j = 0
k = 0
Nall = 0  # number of all atoms

line = input.readline()
line = input.readline()
#
# find the number of atoms of each kind
#
print >> output, "# frame no., E w/o entropy (eV), E(sigma->0) (eV), External press.(kB), Pullay stress (kB)"
#
# search for energy of structure
#
line = input.readline()
temp = 1
ie = -1
ip = -1
while line:
    word = line.split()
    while word:
        if len(word) > 2:
            if word[1] == 'ENERGIE':
                line = input.readline()
                line = input.readline()
		line = input.readline()
		line = input.readline()
                word = line.split()
                ie = ie + 1
                #e0[ie] = float(word[3])
                #es[ie] = float(word[6])
                ee = float(word[3])
                ep = float(word[6])
                temp = 0
            if (word[0] == 'external' and word[1] == 'pressure'):
                ip = ip + 1
                pr[ip] = float(word[3])
                ps[ip] = float(word[8])
                print >> output, '%5i     %16.6f     %16.6f     %10.2f     %10.2f' %( ip+1, ee, ep,  float(word[3]), float(word[8]))
                
        word = 0
    line = input.readline()

if (Nmax < ip):
    print "Array size is not enough. Increase as ", ip
#for i in range(0, ip+1):    
#    print >> output,'%5i  %16.6f   %16.6f  %10.2f  %10.2f' % (i+1, e0[i], es[i], pr[i], ps[i])
    
input.close()
output.close()

