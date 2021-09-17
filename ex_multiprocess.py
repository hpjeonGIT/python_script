import multiprocessing as mp
import os
import numpy as np
import time
from numpy import linalg as LA

N=1000
M = 10
x=[]
for i in range(M):
    x.append(np.random.rand(N,N))
    
def solve(i):
    print("start ", i)
    w,v = LA.eig(x[i])

#
clist = range(M)
t0=time.time()
for i in  clist:
    solve(i)
print("elapsed time for serial=", time.time()-t0)
#
t0=time.time()
p = mp.Pool(processes=2)
with p:
    p.map(solve, clist, chunksize=5)
print("elapsed time for 2cpus=", time.time()-t0)
