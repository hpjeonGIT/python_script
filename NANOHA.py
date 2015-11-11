#! /usr/bin/python
#
# Mesh and particle generator for
# MD & FEM coupling simulation
#-----------------------------------------------
#              NANOHA
#-----------------------------------------------
# Byoungseon Jeon, LANL, T-12
# 12/30/05
#
#

from Tkinter import *
import array
import math

Nref = 100000
# Node coordinate
nodex = array.array("f", range(Nref))
nodey = array.array("f", range(Nref))
# Temporary node coordinate
tx = array.array("f", range(Nref))
ty = array.array("f", range(Nref))
# Element storage
el = array.array("i", range(Nref))
hy = array.array("i", range(Nref))
# Particle coordinate
px = array.array("f", range(Nref))
py = array.array("f", range(Nref))
# Temporary particle coordinate
qx = array.array("f", range(Nref))
qy = array.array("f", range(Nref))
# Equivalence set
il = array.array("i", range(1000))
ih = array.array("i", range(1000))

#output = open("nanoha.inp", 'w')
refx = 800
refy = 800
maxx = float(refx)
maxy = float(refy)
minx = 0.0
miny = 0.0

#
# Visualization
#
class Application:

    def __init__(self, master):
        self.canvas = Canvas(master,bg="white",width=refx, height=refy)
        self.master = master
        frame = Frame(master)
        self.refine_mode = IntVar()
        self.button_click = IntVar()
        self.zoom_state = 0
        self.current = 0,0, 0,0, 0,0, 0,0
        self.Nnode = 0
        self.Nel = 0
        self.Npt = 0
        self.Npair = 0
        self.null = 0

        self.entry1 = DoubleVar()
        self.entry2 = DoubleVar()
        self.entry3 = DoubleVar()
        self.entry4 = DoubleVar()
        self.entry5 = DoubleVar()
        self.entry6 = DoubleVar()
        self.entry7 = DoubleVar()
        self.entry8 = DoubleVar()
        self.mesh_size = DoubleVar()
        self.equi_limit = DoubleVar()
        self.part_density= DoubleVar()

        # border around frame
        spacerFrame = Frame(frame,borderwidth=10)
        centerFrame = Frame(spacerFrame)
        lleftColumn = Frame(centerFrame)
        leftColumn = Frame(centerFrame)
        rightColumn = Frame(centerFrame)
        self.radio = Frame(spacerFrame)

        # Mouse control
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.release)

        # Canvas
        self.canvas.config()
        self.canvas.pack(side=RIGHT, fill=BOTH, expand=1)

        # NSWE
        self.canvas.create_line(50,refy-100, 50, refy-50)
        self.canvas.create_line(50,refy-100, 25, refy-75)
        self.canvas.create_line(75,refy-75, 25, refy-75)
        self.canvas.create_text(80,refy-75, text="E")
        self.canvas.create_text(20,refy-75, text="W")
        self.canvas.create_text(50,refy-105, text="N")
        self.canvas.create_text(50,refy-45, text="S")

##################### Quad button ############################################

        # Label as a header
        Label(spacerFrame, text="GEOMETRY", font = "Times 12 bold", relief = \
              RIDGE, pady=2).pack(side=TOP, fill=X)
        Label(leftColumn, text=" x ", pady=2).pack(side=TOP, fill=X)
        Label(rightColumn, text=" y ", pady=2).pack(side=TOP, fill=X)
        Label(lleftColumn, text=" \ ").pack(side=TOP, fill=X)

        Label(lleftColumn, text=" 1.").pack(side=TOP, fill=X)
        self.entry1.set(100.0)
        Entry(leftColumn, textvariable = self.entry1, \
              width=10).pack(side=TOP, fill=X)
        self.entry2.set(100.0)
        Entry(rightColumn, textvariable = self.entry2, \
              width=10).pack(side=TOP, fill=X)
        Label(lleftColumn, text=" 2.").pack(side=TOP, fill=X)
        self.entry3.set(500.0)
        Entry(leftColumn, textvariable = self.entry3, \
              width=10).pack(side=TOP, fill=X)
        self.entry4.set(100.0)
        Entry(rightColumn, textvariable = self.entry4, \
              width=10).pack(side=TOP, fill=X)
        Label(lleftColumn, text=" 3.").pack(side=TOP, fill=X)
        self.entry5.set(500.0)
        Entry(leftColumn, textvariable = self.entry5, \
              width=10).pack(side=TOP, fill=X)
        self.entry6.set(500.0)
        Entry(rightColumn, textvariable = self.entry6, \
              width=10).pack(side=TOP, fill=X)

        Label(lleftColumn, text=" 4.").pack(side=TOP, fill=X)
        self.entry7.set(100.0)
        Entry(leftColumn, textvariable = self.entry7, \
              width=10).pack(side=TOP, fill=X)
        self.entry8.set(500.0)
        Entry (rightColumn, textvariable = self.entry8, \
               width=10).pack(side=TOP, fill=X)
        lleftColumn.pack(side=LEFT, expand=YES, fill=Y)
        leftColumn.pack(side=LEFT, expand=YES, fill=BOTH)
        rightColumn.pack(side=LEFT, expand=YES, fill=BOTH)
        centerFrame.pack(side=TOP, expand=NO, fill=BOTH)

        # quad button
        Button(spacerFrame, text = "Quad", fg="blue",  activebackground = \
               "grey60", command = self.quad).pack(side=TOP,fill=X)
        # delete button
        Button(spacerFrame, text = "Delete --> click", fg="blue",  \
               activebackground = "grey60", command = \
               self.delete).pack(side=TOP,fill=X)

##################### Mesh button #############################################

        Label(spacerFrame, text="MESH", font = "Times 12 bold", relief = \
              RIDGE, pady=2).pack(side=TOP, fill=X)
        
        center1Frame = Frame(spacerFrame)
        left1Column = Frame(center1Frame)
        right1Column = Frame(center1Frame)
        # mesh button
        Label(left1Column, text="density").pack(side=TOP, fill=X)
        self.mesh_size.set(10.0)
        Entry(right1Column, textvariable = self.mesh_size).pack(side=TOP, \
                                                                fill=X)
        left1Column.pack(side=LEFT, expand=YES, fill=Y)
        right1Column.pack(side=LEFT, expand=YES, fill=BOTH)
        center1Frame.pack(side=TOP, expand=NO, fill=BOTH)
        
        Button(spacerFrame, text = "Mesh --> click", fg="blue",  \
               activebackground = "grey60", command = \
               self.mesh).pack(side=TOP,fill=X)

        # refine button
        MODES = [ ("LT",1), ("RT",2), ("LB",3), ("RB",4) ]
        self.refine_mode.set(1)
        for text, mode in MODES:
            b = Radiobutton(self.radio, text=text, variable = \
                            self.refine_mode, value=mode)
            b.pack(side=LEFT, padx=1, pady=1, fill=BOTH)
        self.radio.pack(side=TOP, fill=X)
        self.button_click.set(0)
        Button(spacerFrame, text = "Refine --> click", fg="blue",  \
               activebackground = "grey60", command = \
               self.refine).pack(side=TOP,fill=X)

        center2Frame = Frame(spacerFrame)
        left2Column = Frame(center2Frame)
        right2Column = Frame(center2Frame)
        # equivalence button
        Label(left2Column, text="limit").pack(side=TOP, fill=X)
        self.equi_limit.set(0.1)
        Entry(right2Column, textvariable = self.equi_limit).pack(side=TOP, \
                                                                 fill=X)
        left2Column.pack(side=LEFT, expand=YES, fill=Y)
        right2Column.pack(side=LEFT, expand=YES, fill=BOTH)
        center2Frame.pack(side=TOP, expand=NO, fill=BOTH)
        
        Button(spacerFrame, text = "Equivalence", fg="blue", activebackground \
               = "grey60", command = self.equiv).pack(side=TOP,fill=X)

##################### Particle button #########################################

        Label(spacerFrame, text="PARTICLE", font = "Times 12 bold", relief = \
              RIDGE, pady=2).pack(side=TOP, fill=X)

        center3Frame = Frame(spacerFrame)
        left3Column = Frame(center3Frame)
        right3Column = Frame(center3Frame)
        # particle button
        Label(left3Column, text="density").pack(side=TOP, fill=X)
        self.part_density.set(10.0)
        Entry(right3Column, textvariable = self.part_density).pack(side=TOP, \
                                                                   fill=X)
        left3Column.pack(side=LEFT, expand=YES, fill=Y)
        right3Column.pack(side=LEFT, expand=YES, fill=BOTH)
        center3Frame.pack(side=TOP, expand=NO, fill=BOTH)
        
        Button(spacerFrame, text = "Particle --> click", fg="blue",  \
               activebackground = "grey60", command = \
               self.particle).pack(side=TOP,fill=X)
        Button(spacerFrame, text = "Delete --> click", fg="blue",  \
               activebackground = "grey60", command = \
               self.ptremove).pack(side=TOP,fill=X)
        
##################### View buton ##############################################

        Label(spacerFrame, text="VIEW", font = "Times 12 bold", relief = \
              RIDGE, pady=2).pack(side=TOP, fill=X)

        # reset button
        Button(spacerFrame, text = "Reset", fg="blue",  activebackground = \
               "grey60", command = self.reset).pack(side=TOP,fill=X)
        # zoom in button
        Button(spacerFrame, text = "Zoom In --> drag", fg="blue",  \
               activebackground = "grey60", command = \
               self.zoomin).pack(side=TOP,fill=X)

##################### Final buton #############################################

        Label(spacerFrame, text="FINAL", font = "Times 12 bold", relief = \
              RIDGE, pady=2).pack(side=TOP, fill=X)

        # renumber button
        Button(spacerFrame, text = "Particle in mesh --> click", fg="blue", \
               activebackground = "grey60", command = \
               self.pair).pack(side=TOP,fill=X)
        # export button
        Button(spacerFrame, text = "Export", fg="blue",  activebackground = \
               "grey60", command = self.export).pack(side=TOP,fill=X)


##################### System button ###########################################

        # Quit button
        Button(spacerFrame, text = "Quit", fg="blue",  activebackground = \
               "grey60", command = self.quit).pack(side=BOTTOM,fill=X)
        # Info button
        Button(spacerFrame, text = "Info.", fg="blue",  activebackground = \
               "grey60", command = self.showInfo).pack(side=BOTTOM,fill=X)
        # postscript button
        Button(spacerFrame, text = "Postscript", fg="blue",  \
               activebackground = "grey60", command = \
               self.post).pack(side=BOTTOM,fill=X)
        Label(spacerFrame, text="etc.", font = "Times 12 bold", relief = \
              RIDGE, pady=2).pack(side=BOTTOM, fill=X)

        # Frame packing
        spacerFrame.pack(side=TOP,expand=YES,fill=BOTH)
        frame.pack(expand=YES, fill=BOTH)

    def showInfo(self):
        toplevel = Toplevel(self.master, bg="white")
        toplevel.transient(self.master)
        toplevel.title("Information on program")
        Label(toplevel, text= \
              " Preprocessing tool for MD and FEM coupling anlysis ", \
              fg="blue",bg="white").pack(pady=20)
        Label(toplevel, text="Written by Byoungseon Jeon",fg="navy",\
              bg="white").pack(pady=20)
        Label(toplevel, text="UC.Davis Applied Science",fg="blue",\
              bg="white").pack()
        Label(toplevel, text="and",fg="blue",bg="white").pack()
        Label(toplevel, text="LANL T-12",fg="blue",bg="white").pack()
        Button(toplevel, text="Close", fg="blue",  activebackground = \
               "grey60", command=toplevel.withdraw).pack(pady=30)

    def click(self, event):
        self.current = self.canvas.coords(CURRENT)
        if (self.button_click == 2):
            self.canvas.delete(CURRENT)
        self.OrgX = event.x
        self.OrgY = event.y
        self.CurrLine = self.canvas.create_rectangle(event.x, event.y, \
                                                     event.x, event.y, \
                                                     outline="cyan")

    def drag(self,event):
        self.var3 = 1
        self.canvas.coords(self.CurrLine, self.OrgX, self.OrgY, \
                           event.x, event.y)

    def release(self, event):
        self.canvas.delete(self.CurrLine)
        # Mesh
        if (self.button_click == 0):
            self.meshgenerate()
        # Refine
        elif (self.button_click == 1):
            self.transient()
        # particle
        elif (self.button_click == 3):
            self.particlegenerate()
        # zoom in
        elif (self.button_click == 4):
            self.magnify(event)
        # particle remove
        elif (self.button_click == 5):
            self.ptdelete()
        # pair
        elif (self.button_click == 6):
            self.include()

    def meshgenerate(self):
        pos = self.current
        x1 = pos[0]
        y1 = maxy - pos[1]
        x2 = pos[2]
        y2 = maxy - pos[3]
        x3 = pos[4]
        y3 = maxy - pos[5]
        x4 = pos[6]
        y4 = maxy - pos[7]
        dd = self.mesh_size.get()
        dx1 = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        dx2 = math.sqrt((x2-x3)**2 + (y2-y3)**2)
        dx3 = math.sqrt((x3-x4)**2 + (y3-y4)**2)
        dx4 = math.sqrt((x4-x1)**2 + (y4-y1)**2)
        nx = int(min(dx1/dd, dx3/dd))
        ny = int(min(dx2/dd, dx4/dd))
        if (nx <1 ):
            nx = 1
        if (ny <1) :
            ny = 1
        tx[0] = x1
        ty[0] = y1
        tx[ny+1] = x2
        ty[ny+1] = y2

        for i in range (1, ny+1):
            tx[i] = tx[0] + i*(x4-x1)/float(ny)
            ty[i] = ty[0] + i*(y4-y1)/float(ny)
            tx[i+ny+1] = tx[ny+1] + i*(x3-x2)/float(ny)
            ty[i+ny+1] = ty[ny+1] + i*(y3-y2)/float(ny)

        node_init = self.Nnode
        for i in range (0, ny+1):
            for j in range (0, nx+1):
                nodex[self.Nnode] = tx[i] + j*(tx[i+ny+1]-tx[i])/float(nx)
                nodey[self.Nnode] = ty[i] + j*(ty[i+ny+1]-ty[i])/float(nx)
                self.Nnode = self.Nnode + 1
        el_init = self.Nel
        for i in range(0, ny):
            for j in range (0, nx):
                el[self.Nel] = node_init + j + i*(nx+1)
                el[self.Nel+1] = node_init + j + i*(nx+1) + 1
                el[self.Nel+2] = node_init + j + (i+1)*(nx+1) + 1
                el[self.Nel+3] = node_init + j + (i+1)*(nx+1)
                self.Nel = self.Nel + 4

        for i in range(0, ny):
            for j  in range(0, nx):
                x1 = nodex[el[el_init]]
                y1 = maxy - nodey[el[el_init]]
                x2 = nodex[el[el_init+1]]
                y2 = maxy - nodey[el[el_init+1]]
                x3 = nodex[el[el_init+2]]
                y3 = maxy - nodey[el[el_init+2]]
                x4 = nodex[el[el_init+3]]
                y4 = maxy - nodey[el[el_init+3]]
                el_init = el_init+4
                self.canvas.create_polygon(x1,y1,x2,y2,x3,y3,x4,y4, \
                                           fill="green", outline="black")

    def particlegenerate(self):
        pos = self.current
        x1 = pos[0]
        y1 = maxy - pos[1]
        x2 = pos[2]
        y2 = maxy - pos[3]
        x3 = pos[4]
        y3 = maxy - pos[5]
        x4 = pos[6]
        y4 = maxy - pos[7]
        dd = float(self.part_density.get())
        dx1 = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        dx2 = math.sqrt((x2-x3)**2 + (y2-y3)**2)
        dx3 = math.sqrt((x3-x4)**2 + (y3-y4)**2)
        dx4 = math.sqrt((x4-x1)**2 + (y4-y1)**2)
        nx = int(min(dx1/dd, dx3/dd))
        dx1 = max(float(dx1/nx), float(dx3/nx))
        ny = int(min(dx2/dd, dx4/dd))
        dx2 = max(float(dx2/ny), float(dx4/ny))
        if (nx <1 ):
            nx = 1
        if (ny <1) :
            ny = 1
        tx[0] = x1
        ty[0] = y1
        tx[ny] = x2
        ty[ny] = y2

        for i in range (1, ny):
            tx[i] = tx[0] + i*(x4-x1)/float(ny)
            ty[i] = ty[0] + i*(y4-y1)/float(ny)
            tx[i+ny] = tx[ny] + i*(x3-x2)/float(ny)
            ty[i+ny] = ty[ny] + i*(y3-y2)/float(ny)

        npt_init = self.Npt
        for i in range (0, ny):
            for j in range (0, nx):
                px[self.Npt] = tx[i] + j*(tx[i+ny]-tx[i])/float(nx) + 0.5*dx1
                py[self.Npt] = ty[i] + j*(ty[i+ny]-ty[i])/float(nx) + 0.5*dx2
                self.Npt = self.Npt + 1
        for i in range(0, ny):
            for j  in range(0, nx):
                x1 = px[npt_init]-3
                y1 = maxy - py[npt_init]+3
                x2 = px[npt_init]+3
                y2 = maxy - py[npt_init]-3
                npt_init = npt_init + 1
                self.canvas.create_oval(x1,y1,x2,y2, outline="grey40")

    def transient(self):
        pos = self.current
        x1 = pos[0]
        y1 = maxy - pos[1]
        x2 = pos[2]
        y2 = maxy - pos[3]
        x3 = pos[4]
        y3 = maxy - pos[5]
        x4 = pos[6]
        y4 = maxy - pos[7]
        dx = self.equi_limit.get()
        cxx = (x1+x2+x3+x4)/4.
        cyy = (y1+y2+y3+y4)/4.
        self.null = self.null + 1
        i = 0
        if (self.zoom_state ==0):
            for j in range (0, (self.Nel+1)/4):
                if (el[i] > -1):
                    x1 = nodex[el[i]]
                    y1 = nodey[el[i]]
                    x2 = nodex[el[i+1]]
                    y2 = nodey[el[i+1]]
                    x3 = nodex[el[i+2]]
                    y3 = nodey[el[i+2]]
                    x4 = nodex[el[i+3]]
                    y4 = nodey[el[i+3]]
                    cx = (x1+x2+x3+x4)/4.
                    cy = (y1+y2+y3+y4)/4.
                    if ( ((cxx-cx)**2 + (cyy - cy)**2) < dx ):
                        n1 = el[i]
                        n2 = el[i+1]
                        n3 = el[i+2]
                        n4 = el[i+3]
                        el[i]   = -1
                        el[i+1] = -1
                        el[i+2] = -1
                        el[i+3] = -1
                i = i + 4
            x1 = nodex[n1]
            x2 = nodex[n2]
            x3 = nodex[n3]
            x4 = nodex[n4]
            y1 = nodey[n1]
            y2 = nodey[n2]
            y3 = nodey[n3]
            y4 = nodey[n4]
        else:
            for j in range (0, (self.Nel+1)/4):
                if (el[i] > -1):
                    x1 = tx[el[i]]
                    y1 = maxy - ty[el[i]]
                    x2 = tx[el[i+1]]
                    y2 = maxy - ty[el[i+1]]
                    x3 = tx[el[i+2]]
                    y3 = maxy - ty[el[i+2]]
                    x4 = tx[el[i+3]]
                    y4 = maxy - ty[el[i+3]]
                    cx = (x1+x2+x3+x4)/4.
                    cy = (y1+y2+y3+y4)/4.
                    if ( ((cxx-cx)**2 + (cyy - cy)**2) < dx ):
                        n1 = el[i]
                        n2 = el[i+1]
                        n3 = el[i+2]
                        n4 = el[i+3]
                        el[i]   = -1
                        el[i+1] = -1
                        el[i+2] = -1
                        el[i+3] = -1
                i = i + 4
            x1 = tx[n1]
            x2 = tx[n2]
            x3 = tx[n3]
            x4 = tx[n4]
            y1 = maxy - ty[n1]
            y2 = maxy - ty[n2]
            y3 = maxy - ty[n3]
            y4 = maxy - ty[n4]

        # Right-Bottom
        if(self.refine_mode.get() == 4):
            x5 = (x4+x3)/2.
            y5 = (y4+y3)/2.
            x6 = (x1+x4)/2.
            y6 = (y1+y4)/2.
            x7 = (x1+x2+x3+x4)/4.
            y7 = (y1+y2+y3+y4)/4.
        # Left-Bottom
        elif(self.refine_mode.get() == 3):
            x5 = (x4+x3)/2.
            y5 = (y4+y3)/2.
            x6 = (x2+x3)/2.
            y6 = (y2+y3)/2.
            x7 = (x1+x2+x3+x4)/4.
            y7 = (y1+y2+y3+y4)/4.
        # Right-Top
        elif(self.refine_mode.get() == 2):
            x5 = (x1+x2)/2.
            y5 = (y1+y2)/2.
            x6 = (x1+x4)/2.
            y6 = (y1+y4)/2.
            x7 = (x1+x2+x3+x4)/4.
            y7 = (y1+y2+y3+y4)/4.
        # Default Left-Top
        else:
            x5 = (x1+x2)/2.
            y5 = (y1+y2)/2.
            x6 = (x2+x3)/2.
            y6 = (y2+y3)/2.
            x7 = (x1+x2+x3+x4)/4.
            y7 = (y1+y2+y3+y4)/4.

        if (self.zoom_state ==0):
            Nnode_init = self.Nnode
            nodex[Nnode_init]     = x5
            nodex[Nnode_init + 1] = x6
            nodex[Nnode_init + 2] = x7
            nodey[Nnode_init]     = y5
            nodey[Nnode_init + 1] = y6
            nodey[Nnode_init + 2] = y7
        else:
            Nnode_init = self.Nnode
            tx[Nnode_init]     = x5
            tx[Nnode_init + 1] = x6
            tx[Nnode_init + 2] = x7
            ty[Nnode_init]     = maxy - y5
            ty[Nnode_init + 1] = maxy - y6
            ty[Nnode_init + 2] = maxy - y7

            nodex[Nnode_init]     = (x5 - refx/2)*self.dx + self.cx
            nodex[Nnode_init + 1] = (x6 - refx/2)*self.dx + self.cx
            nodex[Nnode_init + 2] = (x7 - refx/2)*self.dx + self.cx
            nodey[Nnode_init]     = (y5 - refy/2)*self.dx - self.cy + refy
            nodey[Nnode_init + 1] = (y6 - refy/2)*self.dx - self.cy + refy
            nodey[Nnode_init + 2] = (y7 - refy/2)*self.dx - self.cy + refy

        Nel_init = self.Nel

        # Right-Bottom
        if(self.refine_mode.get() == 4):
            el[Nel_init]   = n1
            el[Nel_init+1] = n2 
            el[Nel_init+2] = Nnode_init + 2
            el[Nel_init+3] = Nnode_init + 1
            
            el[Nel_init+4] = Nnode_init + 2
            el[Nel_init+5] = n2
            el[Nel_init+6] = n3
            el[Nel_init+7] = Nnode_init
            
            el[Nel_init+8] = Nnode_init + 1
            el[Nel_init+9] = Nnode_init + 2
            el[Nel_init+10]= Nnode_init
            el[Nel_init+11]= n4

        # Left-Bottom
        elif(self.refine_mode.get() == 3):
            el[Nel_init]   = n1
            el[Nel_init+1] = Nnode_init + 2
            el[Nel_init+2] = Nnode_init
            el[Nel_init+3] = n4
            
            el[Nel_init+4] = n1 
            el[Nel_init+5] = n2
            el[Nel_init+6] = Nnode_init + 1
            el[Nel_init+7] = Nnode_init + 2
            
            el[Nel_init+8] = Nnode_init + 2
            el[Nel_init+9] = Nnode_init + 1
            el[Nel_init+10]= n3
            el[Nel_init+11]= Nnode_init

        # Right-Top
        elif(self.refine_mode.get() == 2):
            el[Nel_init]   = n1
            el[Nel_init+1] = Nnode_init 
            el[Nel_init+2] = Nnode_init + 2
            el[Nel_init+3] = Nnode_init + 1
            
            el[Nel_init+4] = Nnode_init 
            el[Nel_init+5] = n2
            el[Nel_init+6] = n3
            el[Nel_init+7] = Nnode_init + 2
            
            el[Nel_init+8] = Nnode_init + 1
            el[Nel_init+9] = Nnode_init + 2
            el[Nel_init+10]= n3
            el[Nel_init+11]= n4

        # Default Left-Top
        else:
            el[Nel_init]   = n1
            el[Nel_init+1] = Nnode_init 
            el[Nel_init+2] = Nnode_init + 2
            el[Nel_init+3] = n4
            
            el[Nel_init+4] = Nnode_init 
            el[Nel_init+5] = n2
            el[Nel_init+6] = Nnode_init + 1
            el[Nel_init+7] = Nnode_init + 2
            
            el[Nel_init+8] = Nnode_init + 2
            el[Nel_init+9] = Nnode_init + 1
            el[Nel_init+10]= n3
            el[Nel_init+11]= n4
 
        self.canvas.delete(CURRENT)

        self.Nel = self.Nel + 12
        self.Nnode = self.Nnode + 3
        if (self.zoom_state ==0):
            for i in range(0, 3):
                x1 = nodex[el[Nel_init]]
                y1 = maxy - nodey[el[Nel_init]]
                x2 = nodex[el[Nel_init+1]]
                y2 = maxy - nodey[el[Nel_init+1]]
                x3 = nodex[el[Nel_init+2]]
                y3 = maxy - nodey[el[Nel_init+2]]
                x4 = nodex[el[Nel_init+3]]
                y4 = maxy - nodey[el[Nel_init+3]]
                Nel_init = Nel_init+4
                self.canvas.create_polygon(x1,y1,x2,y2,x3,y3,x4,y4, \
                                           fill="green", outline="black")
        else:
            for i in range(0, 3):
                x1 = tx[el[Nel_init]]
                y1 = ty[el[Nel_init]]
                x2 = tx[el[Nel_init+1]]
                y2 = ty[el[Nel_init+1]]
                x3 = tx[el[Nel_init+2]]
                y3 = ty[el[Nel_init+2]]
                x4 = tx[el[Nel_init+3]]
                y4 = ty[el[Nel_init+3]]
                Nel_init = Nel_init+4
                self.canvas.create_polygon(x1,y1,x2,y2,x3,y3,x4,y4, \
                                           fill="green", outline="black")

    def magnify(self, event):
        self.zoom_state = 1
        # Transform coordinate
        dx = abs(self.OrgX - event.x)
        dy = abs(self.OrgY - event.y)
        cx = (self.OrgX + event.x)/2
        cy = (self.OrgY + event.y)/2
        if (float(dx)/refx > float(dy)/refy):
            dx = float(dx)/refx
        else:
            dx = float(dy)/refy
        for i in range (0, self.Nnode):
            tx[i] = (nodex[i] - cx)/dx + refx/2
            ty[i] = (refy - nodey[i] - cy)/dx + refy/2
        for i in range (0, self.Npt):
            qx[i] = (px[i] - cx)/dx + refx/2
            qy[i] = (refy - py[i] - cy)/dx + refy/2
        self.dx = dx
        self.cx = cx
        self.cy = cy
        # Redraw
        self.canvas.delete(ALL)
        i = 0
        for j in range (0, (self.Nel+1)/4):
            if (el[i] > -1):
                x1 = tx[el[i]]
                y1 = ty[el[i]]
                x2 = tx[el[i+1]]
                y2 = ty[el[i+1]]
                x3 = tx[el[i+2]]
                y3 = ty[el[i+2]]
                x4 = tx[el[i+3]]
                y4 = ty[el[i+3]]
                self.canvas.create_polygon(x1,y1,x2,y2,x3,y3,x4,y4, \
                                           fill="green", outline="black")
            i = i + 4
        for i in range (0, self.Npt):
            x1 = qx[i]-8
            y1 = qy[i]+8
            x2 = qx[i]+8
            y2 = qy[i]-8
            self.canvas.create_oval(x1,y1,x2,y2, fill="grey40")

    def reset(self):
        self.canvas.delete(ALL)
        self.zoom_state = 0
        i = 0
        for j in range (0, (self.Nel+1)/4):
            if (el[i] > -1):
                x1 = nodex[el[i]]
                y1 = refy - nodey[el[i]]
                x2 = nodex[el[i+1]]
                y2 = refy - nodey[el[i+1]]
                x3 = nodex[el[i+2]]
                y3 = refy - nodey[el[i+2]]
                x4 = nodex[el[i+3]]
                y4 = refy - nodey[el[i+3]]
                self.canvas.create_polygon(x1,y1,x2,y2,x3,y3,x4,y4, \
                                           fill="green", outline="black")
            i = i + 4
        for i in range (0, self.Npt):
            x1 = px[i]-3
            y1 = refy - py[i]+3
            x2 = px[i]+3
            y2 = refy - py[i]-3
            self.canvas.create_oval(x1,y1,x2,y2, outline="grey40")

    def mesh(self):
        self.button_click = 0

    def refine(self):
        self.button_click = 1

    def delete(self):
        self.button_click = 2

    def particle(self):
        self.button_click = 3

    def ptremove(self):
        self.button_click = 5

    def pair(self):
        self.button_click = 6

    def zoomin(self):
        self.button_click = 4
        for i in range (0, self.Nnode):
            tx[i] = nodex[i]
            ty[i] = nodey[i]
        for i in range (0, self.Npt):
            qx[i] = px[i]
            qy[i] = py[i]

    def quad(self):
        x1 = self.entry1.get()
        y1 = self.entry2.get()
        x2 = self.entry3.get()
        y2 = self.entry4.get()
        x3 = self.entry5.get()
        y3 = self.entry6.get()
        x4 = self.entry7.get()
        y4 = self.entry8.get()

        y1 = refy - y1
        y2 = refy - y2
        y3 = refy - y3
        y4 = refy - y4

        quad1 = self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4, \
                                           fill="", outline="black")

    def post(self):
        self.canvas.postscript(file="bbb.ps")
        self.canvas.create_rectangle(98, 448, 352, 402, fill="cyan", \
                                     outline="black")
        self.canvas.create_text(150, 425, text = \
                                "\"bbb.ps\" has been produced" , anchor=W)

    def equiv(self):
        # find coincident sets
        print 'Equivalence and renumbering gets started'
        k = 0
        dx = self.equi_limit.get()
        for i in range (0, self.Nnode-1):
            x1 = nodex[i]
            y1 = nodey[i]
            for j in range (i+1, self.Nnode):
                x2 = nodex[j]
                y2 = nodey[j]
                if ((x1-x2)**2 + (y1-y2)**2 < dx):
                    il[k] = i
                    ih[k] = j
                    k = k + 1
        # Sort descending order
        for i in range (0, k-1):
            for j in range (i, k):
                if (ih[i] < ih[j]):
                    it = ih[j]
                    ih[j] = ih[i]
                    ih[i] = it
                    it = il[j]
                    il[j] = il[i]
                    il[i] = it
        # Re-allocation of nodes for elements
        for j in range (0, k):
            print 'coincident node =', ih[j]
            for i in range (0, (self.Nel+1)/4):
                if (el[i*4] > -1):
                    if (el[i*4] == ih[j]):
                        el[i*4] = il[j]
                    elif (el[i*4] > ih[j]):
                        el[i*4] = el[i*4] - 1
                    if (el[i*4+1] == ih[j]):
                        el[i*4+1] = il[j]
                    elif (el[i*4+1] > ih[j]):
                        el[i*4+1] = el[i*4+1] - 1
                    if (el[i*4+2] == ih[j]):
                        el[i*4+2] = il[j]
                    elif (el[i*4+2] > ih[j]):
                        el[i*4+2] = el[i*4+2] - 1
                    if (el[i*4+3] == ih[j]):
                        el[i*4+3] = il[j]
                    elif (el[i*4+3] > ih[j]):
                        el[i*4+3] = el[i*4+3] - 1
            for i in range (ih[j], self.Nnode-j-1):
                nodex[i] = nodex[i+1]
                nodey[i] = nodey[i+1]
        self.Nnode = self.Nnode - k
        if (self.zoom_state ==0):
            for i in range (0, k):
                x1 = nodex[il[i]] - 5
                y1 = maxy - nodey[il[i]] + 5
                x2 = nodex[il[i]] + 5
                y2 = maxy - nodey[il[i]] - 5
                self.canvas.create_oval(x1,y1,x2,y2, outline="yellow")
        else:
            for i in range(0, k):
                x1 = tx[il[i]] - 5
                y1 = ty[il[i]] + 5
                x2 = tx[il[i]] + 5
                y2 = ty[il[i]] - 5
                self.canvas.create_oval(x1,y1,x2,y2, outline="yellow")

        print 'Equivalence and renumbering is over'

    def ptdelete(self):
        pos = self.current
        x1 = pos[0]
        y1 = maxy - pos[1]
        x2 = pos[2]
        y2 = maxy - pos[3]
        cxx = (x1+x2)/2.
        cyy = (y1+y2)/2.
        dx = self.equi_limit.get()
        i = 0
        nsum = 0
        if (self.zoom_state ==0):
            for i in range (0, self.Npt):
                    cx = px[i]
                    cy = py[i]
                    if ( ((cxx-cx)**2 + (cyy - cy)**2) < dx ):
                        self.canvas.create_oval(pos[0],pos[1],pos[2],pos[3],
                                                outline="red")
                        for j in range(i, self.Npt-1):
                            px[j] = px[j+1]
                            py[j] = py[j+1]
                        nsum = nsum + 1
        else:
            for i in range (0, self.Npt):
                    cx = qx[i]
                    cy = maxy - qy[i]
                    if ( ((cxx-cx)**2 + (cyy - cy)**2) < dx ):
                        self.canvas.create_oval(pos[0],pos[1],pos[2],pos[3],
                                                outline="red")
                        for j in range(i, self.Npt-1):
                            px[j] = px[j+1]
                            py[j] = py[j+1]
                            qx[j] = qx[j+1]
                            qy[j] = qy[j+1]
                        nsum = nsum + 1
        self.Npt = self.Npt - nsum
        
    def include(self):
        pos = self.current
        x1 = pos[0]
        y1 = maxy - pos[1]
        x2 = pos[2]
        y2 = maxy - pos[3]
        x3 = pos[4]
        y3 = maxy - pos[5]
        x4 = pos[6]
        y4 = maxy - pos[7]
        dx = self.equi_limit.get()
        cxx = (x1+x2+x3+x4)/4.
        cyy = (y1+y2+y3+y4)/4.
        i = 0
        if (self.zoom_state == 0):
            for j in range (0, (self.Nel+1)/4):
                if (el[i] > -1):
                    x1 = nodex[el[i]]
                    y1 = nodey[el[i]]
                    x2 = nodex[el[i+1]]
                    y2 = nodey[el[i+1]]
                    x3 = nodex[el[i+2]]
                    y3 = nodey[el[i+2]]
                    x4 = nodex[el[i+3]]
                    y4 = nodey[el[i+3]]
                    cx = (x1+x2+x3+x4)/4.
                    cy = (y1+y2+y3+y4)/4.
                    if ( ((cxx-cx)**2 + (cyy - cy)**2) < dx ):
                        n1 = el[i]
                        n2 = el[i+1]
                        n3 = el[i+2]
                        n4 = el[i+3]
                        hy[self.Npair] = i/4+1
                        self.Npair = self.Npair + 1

                i = i + 4
            x1 = nodex[n1]
            x2 = nodex[n2]
            x3 = nodex[n3]
            x4 = nodex[n4]
            y1 = nodey[n1]
            y2 = nodey[n2]
            y3 = nodey[n3]
            y4 = nodey[n4]
        else:
            for j in range (0, (self.Nel+1)/4):
                if (el[i] > -1):
                    x1 = tx[el[i]]
                    y1 = maxy - ty[el[i]]
                    x2 = tx[el[i+1]]
                    y2 = maxy - ty[el[i+1]]
                    x3 = tx[el[i+2]]
                    y3 = maxy - ty[el[i+2]]
                    x4 = tx[el[i+3]]
                    y4 = maxy - ty[el[i+3]]
                    cx = (x1+x2+x3+x4)/4.
                    cy = (y1+y2+y3+y4)/4.
                    if ( ((cxx-cx)**2 + (cyy - cy)**2) < dx ):
                        n1 = el[i]
                        n2 = el[i+1]
                        n3 = el[i+2]
                        n4 = el[i+3]
                        hy[self.Npair] = i/4+1
                        self.Npair = self.Npair + 1
                i = i + 4
            x1 = tx[n1]
            x2 = tx[n2]
            x3 = tx[n3]
            x4 = tx[n4]
            y1 = maxy - ty[n1]
            y2 = maxy - ty[n2]
            y3 = maxy - ty[n3]
            y4 = maxy - ty[n4]
        
        if (self.zoom_state ==0):
            Npt_init = self.Npt
            px[Npt_init] = x1 + (x2-x1)/4.
            px[Npt_init+1] = x2 - (x2-x1)/4.
            px[Npt_init+2] = x3 - (x3-x4)/4.
            px[Npt_init+3] = x4 + (x3-x4)/4.
            py[Npt_init]   = y1 + (y4-y1)/4.
            py[Npt_init+1] = y2 + (y3-y2)/4.
            py[Npt_init+2] = y3 - (y3-y2)/4.
            py[Npt_init+3] = y4 - (y4-y1)/4.
            self.Npt = self.Npt + 4
            for i in range(0,4):
                x1 = px[Npt_init+i]-3
                y1 = maxy - py[Npt_init+i]+3
                x2 = px[Npt_init+i]+3
                y2 = maxy - py[Npt_init+i]-3
                self.canvas.create_oval(x1,y1,x2,y2, outline="magenta")
        else:
            Npt_init = self.Npt
            qx[Npt_init]   = x1 + (x2-x1)/4.
            qx[Npt_init+1] = x2 - (x2-x1)/4.
            qx[Npt_init+2] = x3 - (x3-x4)/4.
            qx[Npt_init+3] = x4 + (x3-x4)/4.
            qy[Npt_init]   = y1 + (y4-y1)/4.
            qy[Npt_init+1] = y2 + (y3-y2)/4.
            qy[Npt_init+2] = y3 - (y3-y2)/4.
            qy[Npt_init+3] = y4 - (y4-y1)/4.
            px[Npt_init]   = (x1 + (x2-x1)/4. - refx/2)*self.dx + self.cx
            px[Npt_init+1] = (x2 - (x2-x1)/4. - refx/2)*self.dx + self.cx
            px[Npt_init+2] = (x3 - (x3-x4)/4. - refx/2)*self.dx + self.cx
            px[Npt_init+3] = (x4 + (x3-x4)/4. - refx/2)*self.dx + self.cx
            py[Npt_init]   = (y1 + (y4-y1)/4. - refy/2)*self.dx - self.cy+refy
            py[Npt_init+1] = (y2 + (y3-y2)/4. - refy/2)*self.dx - self.cy+refy
            py[Npt_init+2] = (y3 - (y3-y2)/4. - refy/2)*self.dx - self.cy+refy
            py[Npt_init+3] = (y4 - (y4-y1)/4. - refy/2)*self.dx - self.cy+refy
            self.Npt = self.Npt + 4
            for i in range(0,4):
                x1 = qx[Npt_init+i]-3
                y1 = maxy - qy[Npt_init+i]+3
                x2 = qx[Npt_init+i]+3
                y2 = maxy - qy[Npt_init+i]-3
                self.canvas.create_oval(x1,y1,x2,y2, outline="magenta")

        hy[self.Npair]   = Npt_init
        hy[self.Npair+1] = Npt_init+1
        hy[self.Npair+2] = Npt_init+2
        hy[self.Npair+3] = Npt_init+3
        self.Npair = self.Npair + 4
            
    def export(self):
        output = open ("FEM_MD.dat",'w')
	print >> output, "# Hybrid model for FEM and MD coupling"
        print >> output, "# time max, dump, dt"
	print >> output, "100.  10.  1."
        print >> output, "# Node data"
        print >> output, self.Nnode
        for i in range (0, self.Nnode):
            print >> output, i+1, nodex[i], nodey[i]
        print >> output, "# Element data"
        print >> output, (self.Nel+1)/4 - self.null
        j = 1
        for i in range (0, (self.Nel+1)/4):
            if ( el[i*4] > -1):
                print >> output, j, el[i*4]+1, el[i*4+1]+1, el[i*4+2]+1, \
                      el[i*4+3]+1
                j = j + 1
        print >> output, "# Particle data"
        print >> output, self.Npt
        j = 1
        for i in range (0, self.Npt):
            print >> output, j, px[i], py[i] ,  " 1 "
            j = j + 1
        print >> output, "# Particle-mesh pair (node/particle)"
        print >> output, (self.Npair+1)/5
        j = 0
        for i in range (0, (self.Npair+1)/5):
            print >> output, hy[j]-self.null, \
                  hy[j+1]+1, hy[j+2]+1, hy[j+3]+1, hy[j+4]+1
            j = j + 5
        output.close()
        self.canvas.create_rectangle(98, 448, 352, 402, fill="cyan", \
                                     outline="black")
        self.canvas.create_text(150, 425, text = \
                                "\"FEM_MD.dat\" has been produced" , anchor=W)

    def quit(self):
        root.quit()

root = Tk()
root.title(" NANOHA - Modeling program for MD & FEM coupling")

app = Application(root)
root.mainloop()
root.destroy()
del root
