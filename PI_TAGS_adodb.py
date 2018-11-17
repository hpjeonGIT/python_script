from __future__ import print_function
from datetime import datetime, timedelta
from sys import exit, path
import adodbapi
import pandas as pd


## OLEDB Enterprise
conn_str = "Provider=PIOLEDBENT.1;Integrated Security=SSPI;Persist Security Info=False;Initial Catalog=ODI-AF;Data Source=oledbentserver"
db = adodbapi.connect(conn_str,timeout=1000)
cur = db.cursor()
sql = """SELECT *
FROM [OSIDemo Pump Condition Based Maintenance].[Asset].[Category]"""
cur.execute(sql)
result = cur.fetchall()
for any in result:
    print(any)
#    
db.close()


### OLEDB Provider
conn_str = "Provider=PIOLEDB.1;Integrated Security=SSPI;Persist Security Info=False;Initial Catalog=ODI-AF;Data Source=oledbserver"
db = adodbapi.connect(conn_str,timeout=1000)
cur = db.cursor()
sql = """SELECT *
FROM [piarchive]..[piinterp2]
WHERE tag = 'sinusoid'
	AND time BETWEEN '*-12h' AND '*'"""
cur.execute(sql)
result = cur.fetchall()
for any in result:
    print(any)
   
db.close()

### Store results as pandas DataFrame
conn_str = "Provider=PIOLEDB.1;Integrated Security=SSPI;Persist Security Info=False;Initial Catalog=ODI-AF;Data Source=oledbserver"
db = adodbapi.connect(conn_str,timeout=1000)
cur = db.cursor()
sql = """SELECT tag, time, value
FROM [piarchive]..[piinterp2]
WHERE tag = 'SINUSOIDS' 
	AND time BETWEEN '*-1h' AND '*' AND timestep= '10m'"""
df = pd.read_sql_query(sql,db)
print(df.shape, df)
db.close()

