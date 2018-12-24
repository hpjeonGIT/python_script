import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
from datetime import datetime,timedelta
import random

def gaussian():
    r=1.0
    while r>= 1.0:
        x = random.random()
        y = random.random()
        v1 = 2.*x - 1.
        v2 = 2.*y - 1.
        r = v1*v1 +v2*v2
    return v1*np.sqrt(-2.*np.log(r)/r)*x*0.1

#
MYPITAG      = "SINUSOID"
TimeInterp   = "1s"                   
Time0        = "2018-Mar-01 06:00:00" 
Time1        = "2018-Mar-01 23:00:00" 
start = datetime.strptime(Time0,"%Y-%b-%d %H:%M:%S")
end   = datetime.strptime(Time1,"%Y-%b-%d %H:%M:%S")
tnow = start
dt  = timedelta(seconds=1)
a_list = []
while (tnow < end):
    if (tnow.minute == 0 and tnow.second < 3 and tnow.hour in [ 10,11,12, 15,16,17,18]):
        signal = 10.0
    else:
        signal = 0.0
    a_list.append((tnow,gaussian()+signal))
    tnow += dt

df = pd.DataFrame(a_list)    
print(df.head())

##
plt.plot_date(df[0],df[1])
plt.gcf().autofmt_xdate()
plt.show()
print(type(df[0][0]),df[0][0])

print(dir(tnow),tnow.hour, tnow.minute, tnow.second)

# Find periodicity
fft = np.fft.fft(df[1])
plt.plot(np.abs(fft))
plt.grid()
plt.show()
tmp = abs(fft)
fft2 = np.fft.ifft(tmp) # autocorrelation
plt.plot(np.abs(fft2))
plt.show()

# Find significant components
for  i in range(len(fft2)):
    x = abs(fft2[i])
    if x > 5:
        print(i, x)
