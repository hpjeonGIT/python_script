#! /usr/bin/python
#
# Extract and plot energy data from OUTCAR, VASP code results
# Byoungseon Jeon, LANL, T-12
# 02/20/04
#
# Add function for dE(E - E_old)
# 03/17/04
#

from Tkinter import *
import sys

# Parsing and data extraction
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
# OUTPUT file name selection
#
print "Default outputfile is \"energy.dat\""
outputfile = raw_input("Just return for default or Enter file name:")
if outputfile == '':
    outputfile = 'energy.dat'
    print "Output file is \"energy.dat\""
else:
    print "Output file is", outputfile
print

#
# Open all files
#
input = open(inputfile)
output = open(outputfile, 'w')

#
# initialize all variables
count = 1  # counter number in the XYZ file
Nlist = 0  # dummy variabe for array of atoms
Ntype = 0  # number of kinds of atoms 
i = 0
j = 0
k = 0
Nall = 0  # number of all atoms

line = input.readline()
atom = ['']
Natom = ['']

#
# search how many kind of atoms are estimated
#
while line:  
    line = input.readline()
    word = line.split()
    while word:
        if word[0] == 'POTCAR:':
            atom.append(word[2])
            Ntype = Ntype + 1
        if word[0] == 'VRHFIN':
            Ntype = Ntype - 1
            line = 0
            word = 0
            break
        word = 0


del atom[0]  # delete dummy array
del atom[Ntype] # last array is duplicated, therefore delete


line = input.readline()
#
# find the number of atoms of each kind
#
while line:  
    line = input.readline()
    word = line.split()
    while word:
        if word[0] == 'ions':
            for i in range(0, Ntype):
                Natom.append(word[i+4])
                i = i + 1
            line = 0
        word = 0

del Natom[0] # delete dummy array

#
# remapping of atomic names along atom numbers
#
type = [''] 
for j in range(0, i):
    Nall = Nall + int(Natom[j])
    for k in range(0,int(Natom[j])):
        type.append(atom[j])
        k = k+1
    j = j + 1
del type[0] # delete dummy array

print >> output, "# frame number, energy(eV), dE b/w step"
#
# search for energy of structure
#
line = input.readline()
temp = 1
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
                energy = word[6]
                oldE = energy
                temp = 0
                miny = float(energy)
                maxy = miny
                iniy = miny
		maxz = 0.0
		minz = 0.0
        word = 0
    line = input.readline()
    if temp == 0:
        line = 0
        
line = input.readline()
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
                energy = word[6]
                count = count + 1
                print >> output, count, energy , float(energy) - float(oldE)
                if float(energy) > maxy :
                    maxy = float(energy)
                if float(energy) < miny :
                    miny = float(energy)
		if (float(energy) - float(oldE)) > maxz :
		    maxz = abs(float(energy) - float(oldE))
		if (float(energy) - float(oldE)) < minz :
                    minz = float(energy) - float(oldE)

                oldE = energy
                Nlist = 0
        word = 0
    line = input.readline()
input.close()
output.close()

#
# Visualization


minx = 1.0
maxx = float(count)
if abs(minz) > maxz:
    maxz = abs(minz)
    minz = -maxz
if abs(minz) < maxz:
    minz = - maxz
dx = maxx - minx
dy = abs(maxy - miny)
dz = abs(maxz - minz)

class Application:
        
 
    def __init__(self, master):
        self.canvas = Canvas(master,bg="white",width="500", height="300")
        self.toolbar = Frame(master)

        # Button for quit
        self.QUIT = Button(self.toolbar,
                           text = "Quit",
                           command = self.quit)
        # pack
        self.QUIT.pack(side=TOP, padx=2, pady=2)

        self.toolbar.pack(side=TOP, fill=X)
        
        self.canvas.config(closeenough=4.0)
        self.canvas.pack(side=BOTTOM, fill=BOTH,expand=1)



        #
        # Configure base of plot pattern
        self.canvas.create_rectangle(80,50, 430,250, fill="PeachPuff")
        self.canvas.create_line(80,150, 430,150, fill="black",
                                stipple="gray25")
        self.canvas.create_line(255, 50, 255, 250, fill="black",
                                stipple="gray12")
        self.canvas.create_text(300,25, text="E(sigma->0)")
        self.canvas.create_line(220,25, 250,25, fill="blue")
        self.canvas.create_text(400,25, text="dE")
        self.canvas.create_line(350,25, 380,25, fill="red")

        #
        # X-axis tick
        self.canvas.create_text(80, 260, text=str(int(minx)))
        self.canvas.create_text(255, 260, text=str(int((maxx-minx)/2+minx)))
        self.canvas.create_text(425, 260, text=str(int(maxx)))
        self.canvas.create_text(255, 280, text="Number of geo. iterations")
        #
        # Y-axis tick
        self.canvas.create_text(41,30, text="(eV)")
        self.canvas.create_text(41,52, text=str(maxy))
        self.canvas.create_text(41,151, text=str(round((maxy - miny)/2+miny,6)))
        self.canvas.create_text(41,248, text=str(miny))
	# Y-axis tick for dE
        self.canvas.create_text(468,30, text="(eV)")
        self.canvas.create_text(464,52, text=str(round(maxz,5)))
        self.canvas.create_text(445,151, text="0.0")
        self.canvas.create_text(464,248, text=str(round(minz,5)))
        #
        # Data plot
        input = open("energy.dat")
        line = input.readline()
        oldx = 1.
        oldy = iniy
	oldz =  0.0 
        line = input.readline()
        while line:
            word = line.split()
            x = float(word[0])
            y = float(word[1])
	    z = float(word[2])
            self.canvas.create_line(350*(oldx-minx)/dx+80, 200*(maxy-oldy)/dy+50,
                                    350*(x-minx)/dx+80, 200*(maxy-y)/dy+50, fill="blue")
            self.canvas.create_line(350*(oldx-minx)/dx+80, 200*(maxz-oldz)/dz+50,
                                    350*(x-minx)/dx+80, 200*(maxz-z)/dz+50, fill="red")
            oldx = x
            oldy = y
	    oldz = z
            line = input.readline()
        input.close()
    def quit(self):
        sys.exit()



root = Tk()
root.title("VASP energy data plot")

app = Application(root)
root.mainloop()
