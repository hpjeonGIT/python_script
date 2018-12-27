import time
import random
N = 5000*1

x = [ 2*i for i in range(N)]
y = [ 3*i for i in range(N)]
random.shuffle(x)
random.shuffle(y)
c_list = []
# brute force - NxN
t0 = time.time()
for a in x:
    for b in y:
        if a==b:
            c_list.append(a)

print(len(x), len(y), len(c_list), time.time() - t0)
# 1,5 and 6.9 sec for 5000 and 10000

# linear
t0 = time.time()
x.sort()
y.sort()
c_list = []; idx = 0; idy = 0
while(idx < len(x) and idy < len(y)):
    if x[idx] == y[idy]:
        c_list.append(x[idx])
        idx += 1
        idy += 1
    elif x[idx] > y[idy]:
        idy += 1
    else:
        idx += 1

print(len(x), len(y), len(c_list), time.time() - t0)
# 0.0048 and 0.0127 sec for 5000 and 10000
