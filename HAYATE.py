#! /usr/bin/python
#

from Tkinter import *
import sys
import array

print "Default geometric file is \"hybrid00.geo\""
#
input = raw_input("Return for default or Enter file name:")
if input == '':
    input = 'hybrid00.geo'
    print "Geometric file is \"hybrid00.geo\""
else:
    print "Geometric file is", input
print
#
temp = input[:-3] + "res"
input = open(input)
#
#
res = 0
print "Default result file is ", temp
input2 = raw_input(\
    "Return for default or Enter file name or Enter \"off\" for none:")
if input2 == '':
    input2 = temp
    print "Result file is ", input2
elif (input2 == 'off'):
    res = 1
else:
    print "Result file is", input2
print
#
if res == 0:
    input2 = open(input2)

refx = 800
refy = 600
Nnode = 0
Nel = 0
Npt = 0
#
# Node parsor
input.readline()
input.readline()
input.readline()
input.readline()
line = input.readline()
word = line.split()
Nnode = int(word[0])
print "Number of nodes is ", Nnode
xi = array.array("f", range(Nnode))
yi = array.array("f", range(Nnode))
#zi = array.array("f", range(Nnode))
xx = array.array("f", range(Nnode))
yy = array.array("f", range(Nnode))
##zz = array.array("f", range(Nnode))

for i in range(0, Nnode):
    line = input.readline()
    word = line.split()
    xi[i] = float(word[1])
    yi[i] = float(word[2])
    #zi[i] = float(word[3])
#
# Element parsor
input.readline()
line = input.readline()
word = line.split()
Nel = int(word[0])
print "Number of elements is ", Nel
e1 = array.array("i", range(Nel))
e2 = array.array("i", range(Nel))
e3 = array.array("i", range(Nel))
e4 = array.array("i", range(Nel))
sxx = array.array("f", range(Nel*4))
syy = array.array("f", range(Nel*4))
sxy = array.array("f", range(Nel*4))
ixx = array.array("i", range(Nel*4))
iyy = array.array("i", range(Nel*4))
ixy = array.array("i", range(Nel*4))
for i in range(0, Nel):
    line = input.readline()
    word = line.split()
    e1[i] = int(word[1])-1
    e2[i] = int(word[2])-1
    e3[i] = int(word[3])-1
    e4[i] = int(word[4])-1
#
# particle parsor
input.readline()
line = input.readline()
word = line.split()
Npt = int(word[0])
print "Number of particles is ", Npt
px = array.array("f", range(Npt))
py = array.array("f", range(Npt))
pxx = array.array("f", range(Npt))
pyy = array.array("f", range(Npt))
tp = array.array("f", range(Npt))
ip = array.array("i", range(Npt))
for i in range(0, Npt):
    line = input.readline()
    word = line.split()
    px[i] = float(word[1])
    py[i] = float(word[2])

#
# transform coordinate into python graphic form
#
maxx = 1.0
max2 = 1.0
maxy = 1.0
may2 = 1.0
if Nel != 0:
	maxx = max(xi)
	maxy = max(yi)
if Npt != 0:
	max2 = max(px)
	may2 = max(py)
minx = 1000.0
min2  = 1000.0
miny = 1000.0
miy2 = 1000.0
if Nel != 0:
	minx = min(xi)
	miny = min(yi)
if Npt != 0:
	min2 = min(px)
	miy2 = min(py)
maxx = max(maxx, max2)
minx = min(minx,min2)
maxy = max(maxy,max2)
miny = min(miny,miy2)
cx = (maxx + minx)/2.
cy = (maxy + miny)/2.
rrefx = float(refx)*0.4
rrefy = float(refy)*0.4

if (cx/rrefx > cy/rrefy):
    dx = cx/rrefx
else:
    dx = cy/rrefy

for i in range(0, Nnode):
    xi[i] = (xi[i]-cx)/dx + refx*0.5
    yi[i] = (cy - yi[i])/dx + refy*.5
    xx[i] = xi[i]
    yy[i] = yi[i]
for i in range(0, Npt):
    px[i] = (px[i]-cx)/dx + refx*0.5
    py[i] = (cy - py[i])/dx + refy*.5
    pxx[i] = px[i]
    pyy[i] = py[i]

#
# parsing analysis results
#
if res == 0:
    input2.readline()
    input2.readline()
    input2.readline()
    input2.readline()
    input2.readline()
    input2.readline()
    input2.readline()
    input2.readline()
    # element results
    j = 0
    for i in range(0, Nel*4):
        line = input2.readline()
        word = line.split()
        if (len(word) > 3):
            sxx[j] = float(word[1])
            syy[j] = float(word[2])
            sxy[j] = float(word[3])
        else:
            sxx[j] = float(word[0])
            syy[j] = float(word[1])
            sxy[j] = float(word[2])
        j = j + 1
    if Nel != 0:        
        imaxx = max(max(sxx),max(syy),max(sxy))
        iminx = min(min(sxx),min(syy),min(sxy))
    
        idx = (imaxx - iminx)/10.
        j = 0
        for i in range(0, Nel*4):
            ixx[j] = int((sxx[j] - iminx)/idx)
            iyy[j] = int((syy[j] - iminx)/idx)
            ixy[j] = int((sxy[j] - iminx)/idx)
            j = j + 1
    else:
        ixx = 1
        iyy = 1
        ixy = 1
        idx = 1.

    # particle results
    input2.readline()
    input2.readline()
    input2.readline()
    input2.readline()
    for i in range(0, Npt):
        line = input2.readline()
        word = line.split()
        tp[i] = float(word[1])
    if Npt != 0:
        imax2 = max(tp)
        imin2 = min(tp)
        idx2 = (imax2 - imin2)/10.
        for i in range(0, Npt):
            ip[i] = int((tp[i] - imin2)/idx2)
    else:
        ip = 1
        idx2 = 1.
        imax2 = imaxx
        imin2 = iminx
        
    input.close()
    input2.close()

print "end"
#
# Visualization
#
class Application:

    def __init__(self, master):
        self.canvas = Canvas(master,bg="white",width=refx, height=refy)
        self.master = master
        frame = Frame(master)

        self.var1 = IntVar()
        self.var2 = IntVar()
        self.var3 = IntVar()
        self.var4 = IntVar()
        self.var5 = IntVar()
        self.var6 = IntVar()
        self.var7 = IntVar()
        self.var8 = IntVar()
        self.var9 = StringVar()
        self.var10 = IntVar()
        self.var11 = IntVar()

        # border around frame
        spacerFrame = Frame(frame,borderwidth=10)
        # Bind mouse events
        self.canvas.bind("<Button-1>", self.OnCanvasClicked)
        self.canvas.bind("<B1-Motion>", self.OnCanvasMouseDrag)
        self.canvas.bind("<ButtonRelease-1>", self.OnCanvasMouseUp)

        # Canvas
        self.canvas.config()
        self.canvas.pack(side=RIGHT, fill=BOTH, expand=1)

        # Label as a header
        self.headLbl = Label(spacerFrame, text="STRUCTURE", relief = \
                             RIDGE, pady=5)
        self.headLbl.pack(side=TOP, fill=X)

        # checkbutton
        self.var2.set(1)
        self.var6.set(1)
        self.check1 = Checkbutton(spacerFrame, text="Node",  variable = \
                                  self.var1)
        self.check2 = Checkbutton(spacerFrame, text="Element",  variable = \
                                  self.var2)
        self.check3 = Checkbutton(spacerFrame, text="Element fill", variable =\
                                  self.var3)
        self.check4 = Checkbutton(spacerFrame, text="Node number", variable = \
                                  self.var4)
        self.check5 = Checkbutton(spacerFrame, text="Element number",  \
                                  variable = self.var5)
        self.check6 = Checkbutton(spacerFrame, text="Particle", variable = \
                                  self.var6)
        self.check7 = Checkbutton(spacerFrame, text="Particle fill",  \
                                  variable = self.var7)
        self.check8 = Checkbutton(spacerFrame, text="Particle number", \
                                  variable = self.var8)
        self.check10= Checkbutton(spacerFrame, text="Header", variable = \
                                  self.var10)
        self.check1.pack(side=TOP, padx=2, pady=2, anchor=W)
        self.check2.pack(side=TOP, padx=2, pady=2, anchor=W)
        self.check3.pack(side=TOP, padx=2, pady=2, anchor=W)
        self.check4.pack(side=TOP, padx=2, pady=2, anchor=W)
        self.check5.pack(side=TOP, padx=2, pady=2, anchor=W)
        self.check6.pack(side=TOP, padx=2, pady=2, anchor=W)
        self.check7.pack(side=TOP, padx=2, pady=2, anchor=W)
        self.check8.pack(side=TOP, padx=2, pady=2, anchor=W)
        self.check10.pack(side=TOP, padx=2, pady=2, anchor=W)

        # Reset button
        Button(spacerFrame, text = "Reset", fg="navy",  activebackground = \
               "grey60", command = self.reset).pack(side=TOP,fill=X)
        # Clear button
        Button(spacerFrame, text = "Clean", fg="navy",  activebackground = \
               "grey60", command = self.clean).pack(side=TOP,fill=X)
        # Redraw button
        Button(spacerFrame, text = "Redraw", fg="navy",  activebackground = \
               "grey60", command = self.redraw).pack(side=TOP,fill=X)

        # Label as a header
        self.headLb2 = Label(spacerFrame, text="ANALYSIS", relief = RIDGE, \
                             pady=5)
        self.headLb2.pack(side=TOP, fill=X)

        # Radio button
        MODES = [ ("XX","1"), ("YY","2"), ("XY","3") ]
        self.var9.set("1")
        for text, mode in MODES:
            b = Radiobutton(spacerFrame, text=text, variable = self.var9, \
                            value=mode)
            b.pack(side=TOP,padx=2, pady=2, anchor=W)

        #  Show button
        Button(spacerFrame, text = "Show", fg="navy",  activebackground = \
               "grey60", command = self.indexplot).pack(side=TOP,fill=X)

        # Quit button
        Button(spacerFrame, text = "Quit", fg="navy",  activebackground = \
               "grey60", command = self.quit).pack(side=BOTTOM,fill=X)
        # Info button
        Button(spacerFrame, text = "Info.", fg="navy",  activebackground = \
               "grey60", command = self.showInfo).pack(side=BOTTOM,fill=X)
        # postscript button
        Button(spacerFrame, text = "Postscript", fg="navy",  activebackground \
               = "grey60", command = self.post).pack(side=BOTTOM,fill=X)

        # Frame packing
        spacerFrame.pack(side=TOP,expand=YES,fill=BOTH)
        frame.pack(expand=YES, fill=BOTH)
        # default element outline view
        for i in range(0,Nel):
            self.canvas.create_polygon(xi[e1[i]],yi[e1[i]],\
                                       xi[e2[i]],yi[e2[i]],\
                                       xi[e3[i]],yi[e3[i]],\
                                       xi[e4[i]],yi[e4[i]],\
                                       fill="", outline="black")
        # default particle view
        for i in range(0,Npt):
            self.canvas.create_oval(px[i]-3,py[i]+3,px[i]+3,py[i]-3,
                                    outline="grey40")

        self.canvas.create_rectangle(550, 150, 750, 320, fill="white", \
                                     outline="black")
        self.canvas.create_text(640, 180, text = "System info." ,font=\
                                "Arial 14")
        self.canvas.create_text(630, 220, text = Nnode ,font="Arial 14", \
                                anchor=E)
        self.canvas.create_text(640, 220, text = "nodes" ,font="Arial 14", \
                                anchor=W)
        self.canvas.create_text(630, 250, text = Nel ,font="Arial 14", \
                                anchor=E)
        self.canvas.create_text(640, 250, text = "elements" ,font="Arial 14", \
                                anchor=W)
        self.canvas.create_text(630,280, text = Npt, font="Arial 14", anchor=E)
        self.canvas.create_text(640,280, text = "particles" ,font="Arial 14", \
                                anchor=W)
        self.var11 = 0

    def showInfo(self):
        toplevel = Toplevel(self.master, bg="white")
        toplevel.transient(self.master)
        toplevel.title("Information on program")
        Label(toplevel, text=\
              " Postprocessing tool for MD and FEM coupling anlysis ", \
              fg="blue",bg="white").pack(pady=20)
        Label(toplevel, text="Written by Byoungseon Jeon",fg="navy",\
              bg="white").pack(pady=20)
        Label(toplevel, text="UC.Davis Applied Science",fg="blue",\
              bg="white").pack()
        Label(toplevel, text="and",fg="blue",bg="white").pack()
        Label(toplevel, text="LANL T-12",fg="blue",bg="white").pack()
        Button(toplevel, text="Close", fg="navy",  activebackground = \
               "grey60", command=toplevel.withdraw).pack(pady=30)

    def clean(self):
        self.canvas.delete(ALL)

    def post(self):
        self.canvas.postscript(file="aaa.ps")
        self.canvas.create_rectangle(100, 450, 350, 400, fill="cyan", \
                                     outline="black")
        self.canvas.create_text(150, 425, text = \
                                "\"aaa.ps\" has been produced" , anchor=W)

    def reset(self):
        self.canvas.delete(ALL)
        # element fill view
        if (self.var3.get() != 0):
            for i in range(0,Nel):
                self.canvas.create_polygon(xi[e1[i]],yi[e1[i]],\
                                           xi[e2[i]],yi[e2[i]],\
                                           xi[e3[i]],yi[e3[i]],\
                                           xi[e4[i]],yi[e4[i]],\
                                           fill="green", outline="")
        # node view
        if (self.var1.get() != 0):
            for i in range(0,Nnode):
                self.canvas.create_oval(xi[i]-3,yi[i]+3,xi[i]+3,yi[i]-3, \
                                        outline="grey40")
        # element outline view
        if (self.var2.get() != 0):
            for i in range(0,Nel):
                self.canvas.create_polygon(xi[e1[i]],yi[e1[i]],\
                                           xi[e2[i]],yi[e2[i]],\
                                           xi[e3[i]],yi[e3[i]],\
                                           xi[e4[i]],yi[e4[i]],\
                                           fill="", outline="black")
        # node numbering
        if (self.var4.get() != 0):
            for i in range(0,Nnode):
                self.canvas.create_text(xi[i]-10,yi[i]+10,text=i+1,fill="blue")
        # element numbering
        if (self.var5.get() != 0):
            for i in range(0,Nel):
                self.canvas.create_text((xi[e1[i]]+xi[e2[i]]+\
                                         xi[e3[i]]+xi[e4[i]])/4,\
                                        (yi[e1[i]]+yi[e2[i]]+\
                                         yi[e3[i]]+yi[e4[i]])/4,\
                                        tex=i+1, fill="magenta")
        # particle view
        if (self.var6.get() != 0):
            for i in range(0,Npt):
                self.canvas.create_oval(px[i]-3,py[i]+3,px[i]+3,py[i]-3, \
                                        outline="grey40")
        # particle fill view
        if (self.var7.get() != 0):
            for i in range(0,Npt):
                self.canvas.create_oval(px[i]-3,py[i]+3,px[i]+3,py[i]-3, \
                                        fill = "grey40")
        # particle numbering
        if (self.var8.get() != 0):
            for i in range(0,Npt):
                self.canvas.create_text(px[i]-10,py[i]+10,text=i+1, \
                                        fill="grey20")
        # header
        if (self.var10.get() != 0):
            self.canvas.create_rectangle(550, 150, 750, 320, fill="white", \
                                         outline="black")
            self.canvas.create_text(640, 180, text = "System info.", \
                                    font="Arial 14")
            self.canvas.create_text(630, 220, text = Nnode, \
                                    font="Arial 14", anchor=E)
            self.canvas.create_text(640, 220, text = "nodes", \
                                    font="Arial 14", anchor=W)
            self.canvas.create_text(630, 250, text = Nel ,\
                                    font="Arial 14", anchor=E)
            self.canvas.create_text(640, 250, text = "elements", \
                                    font="Arial 14", anchor=W)
            self.canvas.create_text(630, 280, text = Npt, \
                                    font="Arial 14", anchor=E)
            self.canvas.create_text(640, 280, text = "particles", \
                                    font="Arial 14", anchor=W)

        for i in range(0,Nnode):
            xx[i] = xi[i]
            yy[i] = yi[i]
        for i in range(0, Npt):
            pxx[i] = px[i]
            pyy[i] = py[i]
        self.var11 = 0

    def redraw(self):
        self.canvas.delete(ALL)
        # element fill view
        if (self.var3.get() != 0):
            for i in range(0,Nel):
                self.canvas.create_polygon(xx[e1[i]],yy[e1[i]],\
                                           xx[e2[i]],yy[e2[i]],\
                                           xx[e3[i]],yy[e3[i]],\
                                           xx[e4[i]],yy[e4[i]],\
                                           fill="green", outline="")
        # node view
        if (self.var1.get() != 0):
            for i in range(0,Nnode):
                self.canvas.create_oval(xx[i]-3,yy[i]+3,xx[i]+3,yy[i]-3, \
                                        outline="grey40")
        # element outline view
        if (self.var2.get() != 0):
            for i in range(0,Nel):
                self.canvas.create_polygon(xx[e1[i]],yy[e1[i]],\
                                           xx[e2[i]],yy[e2[i]],\
                                           xx[e3[i]],yy[e3[i]],\
                                           xx[e4[i]],yy[e4[i]],\
                                           fill="", outline="black")
        # node numbering
        if (self.var4.get() != 0):
            for i in range(0,Nnode):
                self.canvas.create_text(xx[i]-10,yy[i]+10,text=i+1,fill="blue")
        # element numbering
        if (self.var5.get() != 0):
            for i in range(0,Nel):
                self.canvas.create_text((xx[e1[i]]+xx[e2[i]]+\
                                         xx[e3[i]]+xx[e4[i]])/4,\
                                        (yy[e1[i]]+yy[e2[i]]+\
                                         yy[e3[i]]+yy[e4[i]])/4,\
                                        tex=i+1, fill="magenta")
        # particle view
        if (self.var6.get() != 0):
            for i in range(0,Npt):
                self.canvas.create_oval(pxx[i]-3,pyy[i]+3,pxx[i]+3,pyy[i]-3, \
                                        outline="grey40")
        # particle fill view
        if (self.var7.get() != 0):
            for i in range(0,Npt):
                self.canvas.create_oval(pxx[i]-3,pyy[i]+3,pxx[i]+3,pyy[i]-3, \
                                        fill = "grey40")
        # particle numbering
        if (self.var8.get() != 0):
            for i in range(0,Npt):
                self.canvas.create_text(pxx[i]-10,pyy[i]+10,text=i+1, \
                                        fill="grey20")
        # header
        if (self.var10.get() != 0):
            self.canvas.create_rectangle(550, 150, 750, 320, fill="white", \
                                         outline="black")
            self.canvas.create_text(640, 180, text = "System info.", \
                                    font="Arial 14")
            self.canvas.create_text(630, 220, text = Nnode, font="Arial 14", \
                                    anchor=E)
            self.canvas.create_text(640, 220, text = "nodes", \
                                    font="Arial 14", anchor=W)
            self.canvas.create_text(630, 250, text = Nel, font="Arial 14", \
                                    anchor=E)
            self.canvas.create_text(640, 250, text = "elements", \
                                    font="Arial 14", anchor=W)
            self.canvas.create_text(630, 280, text = Npt, \
                                    font="Arial 14", anchor=E)
            self.canvas.create_text(640, 280, text = "particles", \
                                    font="Arial 14", anchor=W)
        self.var11 = 0

    def OnCanvasClicked(self,event):
        self.OrgX = event.x
        self.OrgY = event.y
        self.CurrLine = self.canvas.create_rectangle(event.x, event.y, \
                                                     event.x, event.y, \
                                                     outline="cyan")

    def OnCanvasMouseDrag(self,event):
        self.canvas.coords(self.CurrLine, self.OrgX, self.OrgY, \
                           event.x, event.y)

    def OnCanvasMouseUp(self,event):
        self.canvas.delete(CURRENT)
        # Transform coordinate
        dx = abs(self.OrgX - event.x)
        dy = abs(self.OrgY - event.y)
        cx = (self.OrgX + event.x)/2
        cy = (self.OrgY + event.y)/2
        if (float(dx)/refx > float(dy)/refy):
            dx = float(dx)/refx
        else:
            dx = float(dy)/refy
        for i in range (0, Nnode):
            xx[i] = (xx[i] - cx)/dx + refx/2
            yy[i] = (yy[i] - cy)/dx + refy/2
        for i in range (0, Npt):
            pxx[i] = (pxx[i] - cx)/dx + refx/2
            pyy[i] = (pyy[i] - cy)/dx + refy/2
        # Redraw
        self.canvas.delete(ALL)
        if (self.var11 == 0):
            self.redraw()
        else:
            self.indexplot()

    def indexplot(self):
        self.canvas.delete(ALL)

        tk_rgb = ["#000077", "#0000ff", "#3333bb", "#777777", "#bbbb33",
                  "#ffff00", "#ffbb00", "#ff7700", "#ff3300","#ff0000" ,
                  "#ff0000" ]
        # XY results
        if (self.var9.get() == "3"):
            for i in range(0,Nel):
                self.canvas.create_polygon(xx[e1[i]],yy[e1[i]],\
                                           (xx[e2[i]]+xx[e1[i]])/2,\
                                           (yy[e2[i]]+yy[e1[i]])/2,
                                           (xx[e4[i]]+xx[e3[i]]+\
                                            xx[e2[i]]+xx[e1[i]])/4,\
                                           (yy[e4[i]]+yy[e3[i]]+\
                                            yy[e2[i]]+yy[e1[i]])/4,\
                                           (xx[e4[i]]+xx[e1[i]])/2,\
                                           (yy[e4[i]]+yy[e1[i]])/2,\
                                           fill = tk_rgb[ixy[i*4]])
                self.canvas.create_polygon((xx[e2[i]]+xx[e1[i]])/2,\
                                           (yy[e2[i]]+yy[e1[i]])/2,\
                                           xx[e2[i]],yy[e2[i]],\
                                           (xx[e3[i]]+xx[e2[i]])/2,\
                                           (yy[e3[i]]+yy[e2[i]])/2,\
                                           (xx[e4[i]]+xx[e3[i]]+\
                                            xx[e2[i]]+xx[e1[i]])/4,\
                                           (yy[e4[i]]+yy[e3[i]]+\
                                            yy[e2[i]]+yy[e1[i]])/4,\
                                           fill = tk_rgb[ixy[i*4+1]])
                self.canvas.create_polygon((xx[e4[i]]+xx[e3[i]]+\
                                            xx[e2[i]]+xx[e1[i]])/4,\
                                           (yy[e4[i]]+yy[e3[i]]+\
                                            yy[e2[i]]+yy[e1[i]])/4,\
                                           (xx[e3[i]]+xx[e2[i]])/2,\
                                           (yy[e3[i]]+yy[e2[i]])/2,\
                                           xx[e3[i]],yy[e3[i]],\
                                           (xx[e3[i]]+xx[e4[i]])/2,\
                                           (yy[e3[i]]+yy[e4[i]])/2,\
                                           fill = tk_rgb[ixy[i*4+2]])
                self.canvas.create_polygon((xx[e1[i]]+xx[e4[i]])/2,\
                                           (yy[e1[i]]+yy[e4[i]])/2,\
                                           (xx[e4[i]]+xx[e3[i]]+\
                                            xx[e2[i]]+xx[e1[i]])/4,\
                                           (yy[e4[i]]+yy[e3[i]]+\
                                            yy[e2[i]]+yy[e1[i]])/4,\
                                           (xx[e3[i]]+xx[e4[i]])/2,\
                                           (yy[e3[i]]+yy[e4[i]])/2,\
                                           xx[e4[i]],yy[e4[i]],\
                                           fill = tk_rgb[ixy[i*4+3]])
        # YY results
        elif (self.var9.get() == "2"):
            for i in range(0,Nel):
                self.canvas.create_polygon(xx[e1[i]],yy[e1[i]],\
                                           (xx[e2[i]]+xx[e1[i]])/2,\
                                           (yy[e2[i]]+yy[e1[i]])/2,\
                                           (xx[e4[i]]+xx[e3[i]]+\
                                            xx[e2[i]]+xx[e1[i]])/4,\
                                           (yy[e4[i]]+yy[e3[i]]+\
                                            yy[e2[i]]+yy[e1[i]])/4,\
                                           (xx[e4[i]]+xx[e1[i]])/2,\
                                           (yy[e4[i]]+yy[e1[i]])/2,\
                                           fill = tk_rgb[iyy[i*4]])
                self.canvas.create_polygon((xx[e2[i]]+xx[e1[i]])/2,\
                                           (yy[e2[i]]+yy[e1[i]])/2,\
                                           xx[e2[i]],yy[e2[i]],\
                                           (xx[e3[i]]+xx[e2[i]])/2,\
                                           (yy[e3[i]]+yy[e2[i]])/2,\
                                           (xx[e4[i]]+xx[e3[i]]+\
                                            xx[e2[i]]+xx[e1[i]])/4,\
                                           (yy[e4[i]]+yy[e3[i]]+\
                                            yy[e2[i]]+yy[e1[i]])/4,\
                                           fill = tk_rgb[iyy[i*4+1]])
                self.canvas.create_polygon((xx[e4[i]]+xx[e3[i]]+\
                                            xx[e2[i]]+xx[e1[i]])/4,\
                                           (yy[e4[i]]+yy[e3[i]]+\
                                            yy[e2[i]]+yy[e1[i]])/4,\
                                           (xx[e3[i]]+xx[e2[i]])/2,\
                                           (yy[e3[i]]+yy[e2[i]])/2,\
                                           xx[e3[i]],yy[e3[i]],\
                                           (xx[e3[i]]+xx[e4[i]])/2,\
                                           (yy[e3[i]]+yy[e4[i]])/2,\
                                           fill = tk_rgb[iyy[i*4+2]])
                self.canvas.create_polygon((xx[e1[i]]+xx[e4[i]])/2,\
                                           (yy[e1[i]]+yy[e4[i]])/2,\
                                           (xx[e4[i]]+xx[e3[i]]+\
                                            xx[e2[i]]+xx[e1[i]])/4,\
                                           (yy[e4[i]]+yy[e3[i]]+\
                                            yy[e2[i]]+yy[e1[i]])/4,\
                                           (xx[e3[i]]+xx[e4[i]])/2,\
                                           (yy[e3[i]]+yy[e4[i]])/2,\
                                           xx[e4[i]],yy[e4[i]],\
                                           fill = tk_rgb[iyy[i*4+3]])
        # XX results
        else:
            for i in range(0,Nel):
                self.canvas.create_polygon(xx[e1[i]],yy[e1[i]],\
                                           (xx[e2[i]]+xx[e1[i]])/2,\
                                           (yy[e2[i]]+yy[e1[i]])/2,\
                                           (xx[e4[i]]+xx[e3[i]]+\
                                            xx[e2[i]]+xx[e1[i]])/4,\
                                           (yy[e4[i]]+yy[e3[i]]+\
                                            yy[e2[i]]+yy[e1[i]])/4,\
                                           (xx[e4[i]]+xx[e1[i]])/2,\
                                           (yy[e4[i]]+yy[e1[i]])/2,\
                                           fill = tk_rgb[ixx[i*4]])
                self.canvas.create_polygon((xx[e2[i]]+xx[e1[i]])/2,\
                                           (yy[e2[i]]+yy[e1[i]])/2,\
                                           xx[e2[i]],yy[e2[i]],\
                                           (xx[e3[i]]+xx[e2[i]])/2,\
                                           (yy[e3[i]]+yy[e2[i]])/2,\
                                           (xx[e4[i]]+xx[e3[i]]+\
                                            xx[e2[i]]+xx[e1[i]])/4,\
                                           (yy[e4[i]]+yy[e3[i]]+\
                                            yy[e2[i]]+yy[e1[i]])/4,\
                                           fill = tk_rgb[ixx[i*4+1]])
                self.canvas.create_polygon((xx[e4[i]]+xx[e3[i]]+\
                                            xx[e2[i]]+xx[e1[i]])/4,\
                                           (yy[e4[i]]+yy[e3[i]]+\
                                            yy[e2[i]]+yy[e1[i]])/4,\
                                           (xx[e3[i]]+xx[e2[i]])/2,\
                                           (yy[e3[i]]+yy[e2[i]])/2,\
                                           xx[e3[i]],yy[e3[i]],\
                                           (xx[e3[i]]+xx[e4[i]])/2,\
                                           (yy[e3[i]]+yy[e4[i]])/2,\
                                           fill = tk_rgb[ixx[i*4+2]])
                self.canvas.create_polygon((xx[e1[i]]+xx[e4[i]])/2,\
                                           (yy[e1[i]]+yy[e4[i]])/2,\
                                           (xx[e4[i]]+xx[e3[i]]+\
                                            xx[e2[i]]+xx[e1[i]])/4,\
                                           (yy[e4[i]]+yy[e3[i]]+\
                                            yy[e2[i]]+yy[e1[i]])/4,\
                                           (xx[e3[i]]+xx[e4[i]])/2,\
                                           (yy[e3[i]]+yy[e4[i]])/2,\
                                           xx[e4[i]],yy[e4[i]],\
                                           fill = tk_rgb[ixx[i*4+3]])

        for i in range(0,Npt):
            self.canvas.create_oval(pxx[i]-3,pyy[i]+3,pxx[i]+3,pyy[i]-3, \
                                    fill = tk_rgb[ip[i]])
            
        # index of level
        self.canvas.create_rectangle(550, 130, 750, 520, fill="white", \
                                     outline="black")
        self.canvas.create_text(650, 150, text = "index level",font="Arial 14")
        self.canvas.create_text(670, 170, text = "element       particle",\
                                font="Times 12 bold")
        for i in range(0,10):
            self.canvas.create_rectangle(570, i*30+190,
                                         600, (i+1)*30+190, fill=tk_rgb[9-i])
            aaa = '%10.2e' % (imaxx - idx*i)
            self.canvas.create_text(630, i*30+190, text = aaa)
            self.canvas.create_oval(670, i*30+200,
                                         680, i*30+210, fill=tk_rgb[9-i])
            aaa = '%10.2e' % (imax2 - idx2*i)
            self.canvas.create_text(710, i*30+190, text = aaa)
        aaa = '%10.2e' % (iminx)
        self.canvas.create_text(630, 300+190, text = aaa)
        aaa = '%10.2e' % (imin2)
        self.canvas.create_text(710, 300+190, text = aaa)
        self.var11 = 1

    def quit(self):
        root.quit()

root = Tk()
root.title(" HAYATE - visualzation program for MD & FEM coupling")
app = Application(root)
root.mainloop()
root.destroy()
del root
