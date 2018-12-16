import numpy
import time
import random
import pandas as pd
N = 2000000

x = [random.random() for i in range(N)]
y = [random.random() for i in range(N)]
indx = [i for i in range(N)]
random.shuffle(indx)
df = pd.DataFrame([indx,x,y])
df = df.transpose()
df.columns = ['id','x','y']

df.to_csv('sample.dat')

# Regular looping
a_list = []
t0 = time.time()
for i in range(len(df)):
    if df.x.iat[i] > 0.5 or df.y.iat[i]> 0.5:
        a_list.append(df.id.iat[i])
print(len(a_list), a_list[0:10], time.time()-t0)
## This takes 47 sec

# Pythonic computing
t0 = time.time()
bf = df.id[df.x.gt(0.5)|df.y.gt(0.5)]
print(len(bf), bf[0:10],time.time() - t0)
# This takes 0.039 sec
''' Fortran version
program test
  implicit none
  integer::N, i, j
  real:: t1, t2
  real*8:: tmp
  integer,allocatable:: id(:), find(:)
  real*8,allocatable:: x(:), y(:)
  N = 2000000
  allocate(id(N), x(N), y(N), find(N))
  open(unit=10,file='sample.dat')
  read(10,*)
  do i = 1, N
     read(10,*), j, tmp, x(i), y(i)
     id(i) = int(tmp)
  end do
  close(10)
  find(:) = 0
  !
  j = 0
  t1 = secnds (0.0)
  do i =1, N
     if (x(i) > 0.5 .or. y(i) > 0.5) then
        j = j + 1
        find(j) = id(i)
     end if
  end do
  !
  t2 = secnds (t1)
  print*, j, find(1:10), t2 ! took 0.0156 sec
  deallocate(id,x,y, find)
end program test
'''
