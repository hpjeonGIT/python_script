# Ref: https://pisquare.osisoft.com/community/developers-club/pi-net-framework-pi-af-sdk/blog/2017/03/30/python-36-and-afsdk-example#comment-14485
#
import sys
import clr
import time
import pandas as pd
sys.path.append(r'C:\Program Files (x86)\PIPC\AF\PublicAssemblies\4.0')
clr.AddReference('OSIsoft.AFSDK')  
from OSIsoft.AF import *
from OSIsoft.AF.PI import *
from OSIsoft.AF.Asset import *
from OSIsoft.AF.Data import *
from OSIsoft.AF.Time import *
from OSIsoft.AF.UnitsOfMeasure import *
piServers = PIServers()

t1 = time.time()
### Modify below VVVVVVVVVVVVVV
MYSERVERNAME = 'someserver'
Keyword    = '*engine*'
Time0     = "2018-nov-01 03:45:00" # To use last 2days: "*-2 Day"  To use last 4 hours"*-4h"
Time1     = "2018-nov-08 13:01:15" # Up to now: "*"
TimeInterp = "5s"
Download_Recorded_Data     = False  # or False : Be careful to use "True". Data Could be very large.  
Download_Interpolated_Data = True
PrintTime_1stTagOnly_Inter = True  # Decide to print time stamp in the first column only or not
### Modify above ^^^^^^^^^^^^^^

def print_csv(TAGSUCCESS, list_all, type_data):
 


## Find and connect PI server
myserver = None; t0 = time.time()
for server in piServers:
    if server.Name == MYSERVERNAME:
        myserver = server

if myserver == None:
    print("server %s is not found. Stop here\n"%(MYSERVERNAME))
    sys.exit()
else:
    print("server %s is found. took %.2f sec\n"%(MYSERVERNAME, time.time() - t0))
    
## Download PI data as recorded - Different tag results are concatenated in the bottom of CSV
if (Download_Recorded_Data):
    try:
        t0 = time.time()
        list_all = []
        timerange = AFTimeRange(Time0, Time1)
        for pitag in MYPITAG:
            pt= PIPoint.FindPIPoint(myserver,pitag)
            name = pt.Name
            recorded = pt.RecordedValues(timerange,AFBoundaryType.Inside,"",False)
            list_all.append(recorded)
        print("Downloaded recorded data. Took %.2f sec"%(time.time()-t0))
    except:
        print('Something is wrong. An error occured.')
    #    
    if (len(list_all) > 0):
        with open('PI_tag_data_recorded.csv','w') as f:
            for recorded, pitag in zip(list_all,MYPITAG):
                f.write("# %s\n"%(pitag))
                for event in recorded:
                    f.write("%s, %s\n"%(event.Timestamp.LocalTime, str(event.Value)))

 
## Download PI data as interpolation
if (Download_Interpolated_Data):
    span = AFTimeSpan.Parse(TimeInterp)
    timerange = AFTimeRange(Time0, Time1)            
    try:
        t0 = time.time()
        list_all = []
        for pitag in MYPITAG:
            pt= PIPoint.FindPIPoint(myserver,pitag)
            name = pt.Name
            interpolated = pt.InterpolatedValues(timerange, span, "", False)  
            list_all.append(interpolated)
        print("Downloaded interpolated data. Took %.2f sec"%(time.time()-t0))
    except:
        print("Something is wrong. Interpolation data cannot be downloaded.")
    #
    # Now we make one big table or dataframe
    if (len(list_all) > 0):
        columns = []
        for pitag in MYPITAG:
            columns.append('time_'+pitag)
            columns.append(pitag)
        #
        result_all = []
        for interpolated in list_all:
            a_list = [];b_list = []
            for event in interpolated:
                a_list.append(event.Timestamp.LocalTime)
                b_list.append(str(event.Value))
            result_all.append(a_list); result_all.append(b_list)
        #
        df= pd.DataFrame(result_all)
        df = df.transpose()
        df.columns = columns
        df.to_csv('PI_TAG_data_interpol.csv')
        
print("Elapsed time = %.2f sec"%(time.time()-t1))

