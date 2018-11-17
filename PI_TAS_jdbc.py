import time
import pandas as pd
import jaydebeapi as jdbapi
import getpass
from datetime import datetime,timedelta
user = getpass.getuser()
password = getpass.getpass("Please enter your Windows Password:")
# Enter windows password
#
MYPITAG      = "SINUSOID"
TimeInterp   = "1s"                   
Time0        = "2018-Mar-01 01:00:00" 
Time1        = "2018-Nov-01 01:00:01" 
start = datetime.strptime(Time0,"%Y-%b-%d %H:%M:%S")
end   = datetime.strptime(Time1,"%Y-%b-%d %H:%M:%S")
Nsplit = 32
diff = (end  - start ) / Nsplit
list_start = []; list_end = []
for i in range(Nsplit):
    ts = (start+diff*i).strftime("%Y-%b-%d %H:%M:%S")
    te = (start + diff*(i+1) - timedelta(seconds=1)).strftime("%Y-%b-%d %H:%M:%S")
    list_start.append(ts)
    list_end.append(te)
#
df = pd.DataFrame()
conn = jdbapi.connect("com.osisoft.jdbc.Driver",
    "jdbc:pioledb://server_ip.ac.kr/Data Source=server_name;Integrated Security=SSPI",
    {'user':user, 'password':password, 'ProtocolOrder': "Https/Soap:5461,NetTcp:5462", 'TrustedConnection':"False"})
t0 = time.time()
for ts,te in zip(list_start, list_end):
    sql = "SELECT time, value FROM [piarchive]..[piinterp2]  \
        WHERE tag = '%s' AND time BETWEEN '%s' AND '%s' AND timestep= '%s'"%(MYPITAG,ts,te,TimeInterp)
    bf = pd.read_sql_query(sql,conn) 
    df = pd.concat([df,bf]) # keeps concatenating to df
print(df.shape)
print("elapsedtime = %.1f"%(time.time() - t0))
conn.close()

