#! /usr/bin/python
from shutil import move

x = 10.0

for i in range (1,78):
    
    file = "%3.3i"  % (i)
    file = 'res' + file + '.bin'
    x = x + 0.02
    file2 = "%4.2f"  % (x)
    file2 = file2 + 'ns.bin'
    print file, "->", file2
    move(file, file2)
