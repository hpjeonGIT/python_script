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
Keyword    = '*engine*'            # Be careful not to use '*', which will pull all of PI TAGs
Time0     = "2018-nov-01 03:45:00" # To use last 2days: "*-2 Day"  To use last 4 hours"*-4h"
Time1     = "2018-nov-08 13:01:15" # Up to now: "*"
TimeInterp = "5s"
Download_Recorded_Data     = False  # or False : Be careful to use "True". Data Could be very large.  
Download_Interpolated_Data = True
PrintTime_1stTagOnly_Inter = True  # Decide to print time stamp in the first column only or not
### Modify above ^^^^^^^^^^^^^^

def print_csv(TAGSUCCESS, list_all, type_data):
    if type_data == 'int' and PrintTime_1stTagOnly_Inter:
        first_only = True
    else:
        first_only = False
    result_all = []
    columns = []
    for result, pitag, i in zip(list_all, TAGSUCCESS, range(len(list_all))):
        a_list = []; b_list = []
        for event in result:
            a_list.append(event.Timestamp.LocalTime)
            b_list.append(str(event.Value))
        if (first_only and i >0):
            print("Time stamp is skipped at %s"%(pitag))
        else:
            result_all.append(a_list)
            columns.append('time_'+pitag)
        result_all.append(b_list)
        columns.append(pitag)
    #
    df = pd.DataFrame(result_all)
    df = df.transpose()
    df.columns = columns
    return df

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

# Find PI Tags  
All_PIpts = PIPoint.FindPIPoints(myserver,Keyword)
N_All_PIpts = len(list(ALL_PIpts))
print("Number of found PI TAGs = %d"%(N_All_PIpts))
MYPITAG = []
for pitag in all_pipts:
    MYPITAG.append(pitag)
  
#  
## Download PI data as recorded - Different tag results are concatenated in the bottom of CSV
if (Download_Recorded_Data):
    t0 = time.time()
    list_all = []; TAGSUCCEESS = []
    timerange = AFTimeRange(Time0, Time1)
    for pitag, i in zip(MYPITAG, range(len(MYPITAG))):
        try:
            pt= PIPoint.FindPIPoint(myserver,pitag)
            name = pt.Name
            recorded = pt.RecordedValues(timerange,AFBoundaryType.Inside,"",False)
            cv = str(pt.CurrentValue()).lower()
            if (cv not in ['scan off', 'shutdown', 'no data', 'pt created']):
                list_all.append(recorded)
                TAGSUCCESS.append(pitag)
                print('PI TAG %s has been pulled. %d out of %d'%(pitag, i+1, len(MYPITAG)))
            else:
                print('PI TAG %s is not active. %d out of %d'%(pitag, i+1, len(MYPITAG)))
        except:                           
            print('PI TAG %s is not active. %d out of %d'%(pitag, i+1, len(MYPITAG)))
    #
    if (len(list_all) > 0):
        print("Downloaded recorded data. Took %.2f sec"%(time.time() - t0))
        t0 = time.time()
        df = print_csv(TAGSUCCESS, list_all, 'rec')
        tt = time.localtime()
        fname = 'PI_Data_recorded_' + str(tt.tm_mon) + str(tt.tm_mday) + str(tt.tm_hour) + str(tt.tm_min) + '.csv'
        df.to_csv(fname)
        print("Printed recorded data at %s . Took %.2f sec"%(fname, time.time() - t0))
 
## Download PI data as interpolation
if (Download_Interpolated_Data):
    span = AFTimeSpan.Parse(TimeInterp)
    timerange = AFTimeRange(Time0, Time1)            
    t0 = time.time()
    list_all = []
    TAGSUCCESS = []
    for pitag,i in zip(MYPITAG,range(len(MYPITAG))):
        try:
            pt= PIPoint.FindPIPoint(myserver,pitag)
            name = pt.Name
            interpolated = pt.InterpolatedValues(timerange, span, "", False)  
            cv = str(pt.CurrentValue()).lower()
            if (cv not in ['scan off', 'shutdown', 'no data', 'pt created']):
                list_all.append(interpolated)
                TAGSUCCESS.append(pitag)
                print('PI TAG %s has been pulled. %d out of %d'%(pitag, i+1, len(MYPITAG)))
            else:
                print('PI TAG %s is not active. %d out of %d'%(pitag, i+1, len(MYPITAG)))
        except:                           
            print('PI TAG %s is not active. %d out of %d'%(pitag, i+1, len(MYPITAG)))
    #
    # Now we make one big table or dataframe
    if (len(list_all) > 0):
        print("Downloaded recorded data. Took %.2f sec"%(time.time() - t0))
        t0 = time.time()
        df = print_csv(TAGSUCCESS, list_all, 'int')
        tt = time.localtime()
        fname = 'PI_Data_interp_' + str(tt.tm_mon) + str(tt.tm_mday) + str(tt.tm_hour) + str(tt.tm_min) + '.csv'
        df.to_csv(fname)
        print("Printed interpolated data at %s . Took %.2f sec"%(fname, time.time() - t0))
        print("Number of valid PI TAGs = %d. The size of the produced table is %d x %d"%(len(TAGSUCCESS), df.shape[0], df.shape[1]))
        
print("Elapsed time = %.2f sec"%(time.time()-t1))

