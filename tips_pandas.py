# Basic
import numpy  as np
import pandas as pd
import time
from datetime import datetime, timedelta

####### Augment non-uniform time grid data into every second table - BEGINS #############
# Preprocessing
# round milliseconds into sec
af = df.copy()
af.timestamp = af.timestamp.dt.round('1S')
# replace 3.0 into 0 (bad) and 5.0 to 1 (good)
af = af.replace(3.0, 0)
af = af.replace(5.0, 1)
print(af.shape)
fig = plt.gcf()
fig.set_size_inches(30,10)
plt.plot(af.timetamp,af.result, "-o")
plt.show()
plt.hist(af.result)
plt.show()

# Generate uniform grid of time stamp
tf = pd.DataFrame(pd.date_range('2018-Nov-19 06:00:00','2018-Nov-19 23:00:00',freq='1S'))
tf.columns = ['timestamp']
# Join two DataFrame
ff = pd.merge_asof(tf, af, on='timestamp')
ff.fillna(0) # Fill NaN with 0
fig = plt.gcf()
fig.set_size_inches(30,10)
plt.plot(ff.timetamp,ff.result, "-o")
plt.show()
plt.hist(ff.result)
plt.show()

####### Augment non-uniform time grid data into every second table - ENDS #############

### Resampling over 1 minute as aggregation - BEGINS ####
ff = ff.set_index(pd.DatetimeIndex(ff['timestamp'])
ff = ff.drop('timestamp'], axis=1)
af = ff.data1.resample('1T').sum()
fig = plt.gcf()
fig.set_size_inches(30,10)
plt.plot(af)
plt.show()
### Resampling over 1 minute as aggregation - ENDS ####

### phase vs mag in FFT - BEGINS ####
y = preprocessing.scale(af)
yf = np.fft.fft(y)
angle = np.angle(yf)*180/np.pi
mag = np.abs(yf)
plt.plot(angle, mag, 'o')
plt.yscale('log')
plt.ylim([1,100000])
plt.title('title')
plt.show()
### phase vs mag in FFT - ENDS ####
