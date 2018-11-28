import numpy
import time
import random
import pandas as pd
N = 100000

x = [random.random() for i in range(N)]
y = [random.random() for i in range(N)]
indx = [i for i in range(N)]
df = pd.DataFrame([indx,x,y])
df = df.transpose()
df.columns = ['id','x','y']


# Regular looping
a_list = []
t0 = time.time()
for i in range(len(df)):
    if df.x.iat[i] > 0.5 or df.y.iat[i]> 0.5:
        a_list.append(df.id.iat[i])
print(len(a_list), a_list[0:10], time.time()-t0)
## This takes 2.1 sec

# Pythonic computing
t0 = time.time()
bf = df.id[df.x.gt(0.5)|df.y.gt(0.5)]
print(len(bf), bf[0:10],time.time() - t0)
# This takes 0.0156 sec
