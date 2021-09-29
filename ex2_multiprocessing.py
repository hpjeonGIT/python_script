import multiprocessing as mp
import os
import numpy as np
import random
import time
from numpy import linalg as LA

N=1000
M =  1000
L = 8
x = []
for i in range(L):
    x.append([])
    
for j in range(L):
    x[j] = []
    for i in range(M):
        tmp = []
        for k in range(N):
            tmp.append(random.random())
        x[j].append( tmp)
    
def diff(i):
    maxx = 0.0
    for j in range(1,M):
        for k in range(N):
            dx = abs(x[i][j][k] - x[i][0][k])
            if dx > maxx:
                maxx = dx
    return maxx

#
t0=time.time()
ans = []
for i in range(L):
    ans.append(diff(i))
print (ans)
print("elapsed time for serial=", time.time()-t0) ## 1.09 sec
#
clist = range(L)
t0=time.time()
p = mp.Pool(processes=2)
with p:
    ans=p.map(diff, clist, chunksize=2)
print(ans)
print("elapsed time for 2cpus=", time.time()-t0) ## 0.73sec
