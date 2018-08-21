# for python2
import Tkinter as tk
from Tkinter import *
from tkFileDialog import askopenfilename
from PIL import ImageTk, Image
import numpy as np

class AppWin(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = tk.Tk()
        self.master.title('Sample GUI')
        self.master.geometry("500x500")
        self.init_window()

    def init_window(self):
        self.master.title("GUI")
        self.pack()
        # Configuring menu
        menubar = Menu(self.master)
        self.master.config(menu=menubar)        
        filemenu = Menu(menubar,tearoff=0)
        filemenu.add_command(label="Open",command=self.openfile)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        #
        presetmenu = Menu(menubar)
        menubar.add_cascade(label="Preset", menu=presetmenu)
        presetmenu.add_command(label="Load", command=self.load_preset)         
        #
        helpmenu = Menu(menubar)
        menubar.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.about)         
        #
        label_val1 = tk.Label(self.master, text="val1=")
        label_val1.grid(row=0,column=0)
        self.var1 = tk.IntVar()
        self.scale1 = tk.Scale(self.master, from_=0, to=255, 
                               variable = self.var1)
        self.scale1.grid(row=0, column=1)
        #
        label_val2 = tk.Label(self.master, text="val2=")
        label_val2.grid(row=0,column=2)
        self.var2 = tk.IntVar()
        self.scale2 = tk.Scale(self.master, from_=0, to=255, 
                               variable = self.var2)
        self.scale2.grid(row=0, column=3)
        button = tk.Button(self.master, text = "Transform",
                           command = self.transForm)
        button.grid(row=1, column=1) 
        self.label = tk.Label(self.master, textvariable=self.var1)
        self.label.grid(row=2, column=1) #pack()
        self.log_title = tk.Label(self.master, text = "Log :")
        self.log_title.grid(row=3,column=0)
        self.log = tk.Label(self.master, text = "")
        self.log.grid(row=3,column=1, columnspan=3)
        #
        # Image
        self.Img = Image.new("RGB", (300,300), "white")
        self.img = ImageTk.PhotoImage(self.Img, master=self.master)
        self.imageviewer = tk.Label(self.master, image=self.img)
        self.imageviewer.grid(row=4, column=0, columnspan=4)
        

    def openfile(self):
        filepath = askopenfilename()
        try:
            self.Img = Image.open(filepath)
            w,h = self.Img.size
            if w > 300 or h > 300:
                tmp = w if w > h else h
                nw = int(300*w/tmp)
                nh = int(300*h/tmp)
                self.Img = self.Img.resize((nw,nh), Image.ANTIALIAS)
            self.img = ImageTk.PhotoImage(self.Img, master=self.master)
            self.log.config(text = 'Image loaded')
            self.imageviewer.configure(image=self.img)
        except IOError:
            print("Invalid Image")
            self.log.config(text = 'Invalid image')
            
    def getValue(self):
        result = "Value is " + str(self.var1.get())
        print('result is %d\n'%( self.scale1.get()))
        self.label.config(text=result)

    def transForm(self):
        s1 = self.scale1.get()
        s2 = self.scale2.get()
        tmp = np.array(self.Img)
        tmp[:,:,0] += s1
        tmp[:,0,:] += s2
        self.Img = Image.fromarray(tmp)
        self.img = ImageTk.PhotoImage(self.Img, master=self.master)
        self.log.config(text = 'Image transformed')
        self.imageviewer.configure(image=self.img)

    def load_preset(self):
        filepath = askopenfilename()
        try:
            f = open(filepath)
            tmp = f.read(); line = tmp.split('\n'); word = line[1].split(' ')
            self.val1 = int(word[0]); self.val2 = int(word[1])
            self.setScale()
        except IOError:
            print("Invalid preset")
            self.log.config(text = 'Invalid image')
            
    def setScale(self):
        self.scale1.set(self.val1)
        self.scale2.set(self.val2)
    
    def about(self):
        self.log.config(text = 'made by jeonb')
        
def main():
    app = AppWin()
    app.mainloop()
    app.destroy()

if __name__ == '__main__':
    main()
