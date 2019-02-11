# Grumpy v0.1 by jeoonb@corning
# 02/07/2019
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
##
import sys
import clr
import time
import pandas as pd
sys.path.append(r'C:\Program Files (x86)\PIPC\AF\PublicAssemblies\4.0')
clr.AddReference('OSIsoft.AFSDK')  
from OSIsoft.AF                import *
from OSIsoft.AF.PI             import *
from OSIsoft.AF.Asset          import *
from OSIsoft.AF.Data           import *
from OSIsoft.AF.Time           import *
from OSIsoft.AF.UnitsOfMeasure import *
piServers = PIServers()
t1 = time.time()
### Modify below VVVVVVVVVVVVVV
MYSERVERNAME = 'some_osisoft_piserver'
MYPITAG      = ["sometag1","sometag2"]
Time0        = "*-1h" #"2018-Nov-01 03:45:00" 
Time1        = "*" #"2018-Nov-05 03:45:15" 
TimeInterp   = "1s"                   # 1h: for every hour, 1m: for every min
### Modify above ^^^^^^^^^^^^^^
myserver = None; t0 = time.time()
for server in piServers:
    if server.Name == MYSERVERNAME:
        myserver = server

if myserver == None:
    print("server %s is not found. Stop here\n"%(MYSERVERNAME))
    sys.exit()
else:
    print("server %s is found. took %.2f sec\n"%(MYSERVERNAME, time.time() - t0))

def make_df(TAGSUCCESS, list_all):
    columns = ['timestamp']
    for pitag in TAGSUCCESS:
        columns.append(pitag)
    #
    result_all = []
    for recorded in list_all:
        a_list = [];b_list = []
        for event in recorded:
            a_list.append(str(event.Timestamp.LocalTime))
            b_list.append(event.Value)
        if (len(result_all) ==0):
            result_all.append(a_list); 
        result_all.append(b_list)
    #
    df= pd.DataFrame(result_all)
    df = df.transpose()
    df.columns = columns
    return df

class AppWin(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = tk.Tk()
        self.master.title('Grumpy GUI v0.3')
        self.master.geometry("1000x850")
        self.init_window()
        self.master.protocol("WM_DELETE_WINDOW", self.quit) 
        self.widget = None
        self.widget2 = None


    def init_window(self):
        self.master.title("Grumpy GUI v0.3")
        self.pack()
        # Configuring menu
        menubar = Menu(self.master)
        self.master.config(menu=menubar)        
        helpmenu = Menu(menubar)
        menubar.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.about)         
        #
        lframe = Frame(self.master, width=500, height=400)
        lframe.grid(row=0,column=0)
        # Configuring button        
        subframe = Frame(lframe, width=500, height=400)
        subframe.grid(row=1,column=0)
        update_button = tk.Button(subframe, text = "Update IMG",
                           command = self.update_ftn)
        update_button.grid(row=1, column=0) 
        pi_button = tk.Button(subframe, text = "Update PI",
                           command = self.update_PI)
        pi_button.grid(row=1, column=1) 
        quit_button = tk.Button(subframe, text = "Quit",
                           command = self.quit)
        quit_button.grid(row=1, column=2) 
        
        ## radio button
        self.PI_condition = tk.Label(subframe, text = "PI condition:")
        self.PI_condition.grid(row=2,column=0)
        self.piT0 = tk.StringVar(self.master); self.piT0.set("*-1h")
        a = tk.Radiobutton(subframe, text='-1h', variable=self.piT0, value="*-1h")
        a.select()
        a.grid(row=2,column=1)
        b = tk.Radiobutton(subframe, text='-2h', variable=self.piT0, value="*-2h")
        b.deselect()
        b.grid(row=2,column=2)
        c = tk.Radiobutton(subframe, text='-3h', variable=self.piT0, value="*-3h")
        c.deselect()
        c.grid(row=2,column=3)
        
        
        # Configuring log 
        self.IO_log_title = tk.Label(lframe, text = "IO LOG :")
        self.IO_log_title.grid(row=2,column=0)
        self.IO_log = tk.Label(lframe, text = "IO Log is written here:"+ datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))
        self.IO_log.grid(row=3,column=0)
        self.ERR_log_title = tk.Label(lframe, text = "ERROR Log :")
        self.ERR_log_title.grid(row=4,column=0)
        self.ERR_log = tk.Label(lframe, text = "ERROR Log is written here:"+ datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))
        self.ERR_log.grid(row=5,column=0)
        #
        # Image
        try:
            self.raw = Image.open(".\\cat.jpg")
            self.img = ImageTk.PhotoImage(self.raw, master=self.master)
        except IOError:
            self.raw = Image.new("RGB", (500,300), "white")
            self.img = ImageTk.PhotoImage(self.raw, master=self.master)
        self.plot = self.img
        self.imageviewer = tk.Label(lframe, image=self.img)
        self.imageviewer.grid(row=6, column=0)
        self.pack()
        rframe = Frame(self.master, width=500, height=1000)
        rframe.grid(row=0,column=1)
        self.plotviewer = tk.Canvas(rframe,width=600,height=400, background="white")
        self.plotviewer.grid(row=0,column=0)
        self.PI_log_title = tk.Label(rframe, text = "PI LOG :")
        self.PI_log_title.grid(row=1,column=0)
        self.PI_log = tk.Label(rframe, text = "PI Log is written here:"+ datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))
        self.PI_log.grid(row=2,column=0)
        self.PIplot = tk.Canvas(rframe,width=600,height=400, background="white")
        self.PIplot.grid(row=3,column=0)
                
    def update_ftn(self):
        #
        # Update of Trident image
        # Find the id of newest picture and load it
        self.IO_log.config(text= "button clicked")
        connection = mysql.connector.connect(host='msqlserver',database='myDB',user='read_only_user', 
                                     password='12345!@#$%', use_pure=True)
        if connection.is_connected():
            t0 = time.time()
            db_Info = connection.get_server_info()
            str1 = "Connected to MySQL database... MySQL Server version on "+db_Info + ":"+datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
            self.IO_log.config(text=str1)
            cursor = connection.cursor()
            sql_fetch_blob_query = """select * from trident.item order by timestamp_utc DESC limit 1"""
            cursor.execute(sql_fetch_blob_query)    
            record = cursor.fetchall()
            recent_id = str(record[0][0])
            sql_fetch_blob_query = """select * from trident.image WHERE item_id = %s  AND camera_id = '5' AND image_type_id='1' """ % recent_id
            cursor.execute(sql_fetch_blob_query)    
            record = cursor.fetchall()
            cursor.close()
            connection.close()
            t1 = time.time(); str1 = "Pulled results of %s. Took %4.1f sec"%(recent_id, t1-t0) + ":"+datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
            self.IO_log.config(text=str1)            
            blob = None
            for row in record:
                if row[2] == 5 and row[3] == 1:
                    blob = row[4]
            if blob == None:
                self.ERR_log.config(text="image not found:" +  datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))
            else:
                if self.widget:
                    self.widget.destroy()
                #  
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
                fig = Figure(figsize=(6,4))
                a   = fig.add_subplot(111)
                a.plot(part[:,0],color='red')
                a.plot(part[:,49],color='magenta')
                a.plot(part[:,99],color='blue')
                a.plot(part[:,149],color='cyan')
                a.plot(part[:,199],color='green')
                a.set_ylabel('intensity')
                a.set_xlabel('distance from the top of ROI')
                canvas = FigureCanvasTkAgg(fig, master=self.plotviewer)
                self.widget = canvas.get_tk_widget()
                self.widget.pack()
                canvas.draw()
        else:
            self.ERR_log.config(text="Failed to connect to SQL server:" + datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))

    def update_PI(self):
        #
        # PI data plot
        span = AFTimeSpan.Parse(TimeInterp)
        t0 = str(self.piT0.get())
        print(t0)
        timerange = AFTimeRange(t0, Time1)            
        list_all = []; TAGSUCCESS = []
        for pitag in MYPITAG:
            pt= PIPoint.FindPIPoint(myserver,pitag)
            name = pt.Name
            interpolated = pt.InterpolatedValues(timerange, span, "", False)  
            list_all.append(interpolated); TAGSUCCESS.append(pitag)
        if (len(list_all) > 0):
            if self.widget2:
                self.widget2.destroy()

            self.PI_log.config(text="Downloaded PI data:" + datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))
            df = make_df(TAGSUCCESS, list_all)
            df.timestamp = pd.to_datetime(df.timestamp)
            fig = Figure(figsize=(6,4))
            b   = fig.add_subplot(111)
            for pitag in MYPITAG:
                b.plot_date(df.timestamp,df[pitag],'-',label=pitag)                
            b.set_xlabel('time')
            b.legend(loc='upper right')
            picanvas = FigureCanvasTkAgg(fig, master=self.PIplot)
            self.widget2 = picanvas.get_tk_widget()
            self.widget2.pack()
            picanvas.draw()
        else:
            self.PI_log.config(text="Couldn't pull PI data:" + datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))

    def about(self):
        self.log.config(text = 'made by jeonb:'+ datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))
        
def main():
    app = AppWin()
    app.mainloop()
    app.destroy()

if __name__ == '__main__':
    main()
