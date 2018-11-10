# ref: https://pisquare.osisoft.com/community/developers-club/pi-net-framework-pi-af-sdk/blog/2017/03/30/python-36-and-afsdk-example#comment-14485
import sys
import clr
sys.path.append(r'C:\Program Files (x86)\PIPC\AF\PublicAssemblies\4.0')
clr.AddReference('OSIsoft.AFSDK')  
from OSIsoft.AF import *
from OSIsoft.AF.PI import *
from OSIsoft.AF.Asset import *
from OSIsoft.AF.Data import *
from OSIsoft.AF.Time import *
from OSIsoft.AF.UnitsOfMeasure import *
piServers = PIServers()

MYSERVERNAME = 'some_server'
MYPITAG      = 'sinusoid'
TIMECOND     = "*-2 Day" #"*-4h"
for server in piServers:
	if server.Name == MYSERVERNAME:
		print("server found")
		myserver = server

pt= PIPoint.FindPIPoint(myserver,MYPITAG)
name = pt.Name
timerange = AFTimeRange(TIMECOND,"*")

recorded = pt.RecordedValues(timerange,AFBoundaryType.Inside,"",False)

with open('PI_tag_data.csv','w') as f:
	for event in recorded:
		if type(event.Value) == float:
			f.write("%s, %.4e\n"%(event.Timestamp.LocalTime, event.Value))
		elif type(event.Value) == int:	
			f.write("%s, %d\n"%(event.Timestamp.LocalTime, event.Value))
		else:	
			f.write("%s, %s\n"%(event.Timestamp.LocalTime, str(event.Value)))

