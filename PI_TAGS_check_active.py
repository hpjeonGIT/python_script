# Ref: https://pisquare.osisoft.com/community/developers-club/pi-net-framework-pi-af-sdk/blog/2017/03/30/python-36-and-afsdk-example#comment-14485
#
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
MYSERVERNAME = 'myPISERVER'

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

# find all pi tags
all_pipts = PIPoint.FindPIPoints(myserver,'*AVG*')
N_all_pipts = len(list(all_pipts))
print("Number of all pi tags = %d\n"%(N_all_pipts))
list_pitags = []
for any in all_pipts:
    list_pitags.append(any.Name)

list_assessment = [] 
list_cv = []
N_inactive = 0; N_active = 0; N_fail = 0
for pitag,i in zip(list_pitags,range(N_all_pipts)):
    pt = PIPoint.FindPIPoint(myserver,pitag)
    try:
        cv = str(pt.CurrentValue())
    except:
        list_assessment.append('Failed'); N_fail += 1
        list_cv.append('fail')
        print('%d %s failed\n'%(i,pitag))
    else:
        cvl = cv.lower()
        if cvl == 'scan off' or cvl == 'shutdown' or cvl == 'no data':
            list_assessment.append('inactive'); N_inactive += 1
            list_cv.append(cv)
        else:
            list_assessment.append('active'); N_active += 1
            list_cv.append(cv)
        print("%d %s %s\n"%(i, pitag,cv))
    
list_df = []
for pitag, status, cv in zip(list_pitags, list_assessment, list_cv):
    list_df.append((pitag, status, cv))


df= pd.DataFrame(list_df)
df.columns = ['pitag','status','CurrentValue']
fname = 'PI_tags_status.csv'
df.to_csv(fname)
print("Printed results to %s. Took %.2f sec\n"%(fname, time.time()-t1))
print("N.fail = %d N.inactive =%d N.active = %d  out of %d\n"%(N_fail, N_inactive, N_active, N_all_pipts))
