import pandas as pd
import json
import time
import random
from py_essentials import simpleRandom as sr
from datetime import datetime

N=1000000

alist = []

t0 = time.time()
nfail = 0
for i in range(N):    
    lname = sr.randomString(random.randrange(2,5))
    fname = sr.randomString(random.randrange(3,8))
    x = random.random()
    y = random.randrange(1,9)    
    while True:
        try:
            year = random.choice(range(1950, 2001))
            month = random.choice(range(1, 13))
            day = random.choice(range(1, 29))
            xdate = datetime(random.randrange(1950,2011), random.randrange(1,12),random.randrange(1,31))
        except ValueError:
            nfail += 1
        else:
            break
        
    alist.append({'id':i, 'lname':lname, 'fname':fname, 'x':x, 'y':y, 'date_updated': xdate})

print('%.1f sec'%(time.time() - t0))
print(nfail, 'repeated')

df = pd.DataFrame(alist)
df.to_csv('small.csv',index=False)
