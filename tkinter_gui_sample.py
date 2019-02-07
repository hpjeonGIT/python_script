import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
import numpy as np
import cv2
from PIL import ImageTk, Image
import pandas as pd
import os
import time
import mysql.connector
from mysql.connector import Error
import datetime
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class AppWin(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = tk.Tk()
        self.master.title('Grumpy GUI v0.1')
        self.master.geometry("1000x800")
        self.init_window()
        self.master.protocol("WM_DELETE_WINDOW", self.quit) 


    def init_window(self):
        self.master.title("Grmpy GUI v0.0")
        self.pack()
        # Configuring menu
        menubar = Menu(self.master)
        self.master.config(menu=menubar)        
        helpmenu = Menu(menubar)
        menubar.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.about)         
        #
        lframe = Frame(self.master, width=500, height=800)
        lframe.grid(row=0,column=0)
        self.IO_log_title = tk.Label(lframe, text = "IO LOG :")
        self.IO_log_title.grid(row=0,column=0)
        self.IO_log = tk.Label(lframe, text = "IO Log is written here"+ datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))
        self.IO_log.grid(row=1,column=0)
        # Configuring button        
        update_button = tk.Button(lframe, text = "Update",
                           command = self.update_ftn)
        update_button.grid(row=2, column=0) 
        # Configuring log 
        self.ERR_log_title = tk.Label(lframe, text = "ERROR Log :")
        self.ERR_log_title.grid(row=3,column=0)
        self.ERR_log = tk.Label(lframe, text = "ERROR Log is written here"+ datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))
        self.ERR_log.grid(row=4,column=0)
        #
        # Image
        try:
            self.raw = Image.open(".\\dog.jpg")
            self.img = ImageTk.PhotoImage(self.raw, master=self.master)
        except IOError:
            self.raw = Image.new("RGB", (300,300), "white")
            self.img = ImageTk.PhotoImage(self.raw, master=self.master)
        self.plot = self.img
        self.imageviewer = tk.Label(lframe, image=self.img)
        self.imageviewer.grid(row=5, column=0)
        rframe = Frame(self.master, width=500, height=800)
        rframe.grid(row=0,column=1)
        self.plotviewer = tk.Canvas(rframe,width=200,height=100, background="white")
        #self.plotviewer = tk.Label(rframe, image=self.plot)
        self.plotviewer.grid(row=0,column=0)
                
    def update_ftn(self):
        # Find the id of newest picture and load it
        self.IO_log.config(text= "button clicked")
        connection = mysql.connector.connect(host='mysql',database='mydata',user='myuser', 
                                     password='mypasswd', use_pure=True)
        if connection.is_connected():
            t0 = time.time()
            db_Info = connection.get_server_info()
            str1 = "Connected to MySQL database... MySQL Server version on "+db_Info + datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
            self.IO_log.config(text=str1)
            cursor = connection.cursor()
            sql_fetch_blob_query = """select * from mydata.keys WHERE project_id = '1234'"""
            cursor.execute(sql_fetch_blob_query)    
            record = cursor.fetchall()
            cursor.close()
            connection.close()
            t1 = time.time(); str1 = "Pulled results. Took %4.1f sec"%(t1-t0) + datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
            self.IO_log.config(text=str1)            
            blob = None
            for row in record:
                if row[2] == 5 and row[3] == 1:
                    blob = row[4]
            if blob == None:
                self.ERR_log.config(text="image not found" +  datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))
            else:
                tmp = np.frombuffer(blob, np.uint8)
                arr = cv2.imdecode(tmp, 0)
                Ylim,Xlim = arr.shape
                # Use arr for section analysis
                # Show image with ROI 
                cimg = cv2.cvtColor(arr,cv2.COLOR_GRAY2BGR)
                #cv2.rectangle(cimg,(0,Ylim-1),(200,200),(255,0,0),1)
                cv2.line(cimg, (0, Ylim-1),   (  0, 200), (255,0,0),2)
                cv2.line(cimg, (50, Ylim-1),  ( 50, 200), (255,0,255),2)
                cv2.line(cimg, (100, Ylim-1), (100, 200), (0,0,255),2)
                cv2.line(cimg, (150, Ylim-1), (150, 200), (0,255,255),2)
                cv2.line(cimg, (200, Ylim-1), (200, 200), (0,255,0),2)
                img = Image.fromarray(cimg)
                self.img = ImageTk.PhotoImage(img, master=self.master)
                self.imageviewer.configure(image=self.img)
                #Plotting section view
                part = arr[200:, 0:200]
                fig = Figure(figsize=(6,6))
                a   = fig.add_subplot(111)
                a.plot(part[:,0],color='red')
                a.plot(part[:,49],color='magenta')
                a.plot(part[:,99],color='blue')
                a.plot(part[:,149],color='cyan')
                a.plot(part[:,199],color='green')
                a.set_ylabel('intensity')
                a.set_xlabel('distance from the top of ROI')
                canvas = FigureCanvasTkAgg(fig, master=self.plotviewer)
                canvas.get_tk_widget().pack()
                canvas.draw()
                #
                #self.plot = ImageTk.PhotoImage(im, master=self.master)
                #self.plotviewer.configure(image=self.plot)
        else:
            self.ERR_log.config(text="Failed to connect to SQL server" + datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))


    def about(self):
        self.log.config(text = 'made by hpjeon'+ datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))
        
def main():
    app = AppWin()
    app.mainloop()
    app.destroy()

if __name__ == '__main__':
    main()
