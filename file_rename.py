#! /usr/bin/python
#


from shutil import move

x = 2.34

for i in range (0,87):
    y = x - i*0.02
    file = "%3.2f"  % (y)
    file = file + 'ns.bin'
    z = y + 0.02
    file2 = "%3.2f"  % (z)
    file2 = file2 + 'ns.bin'
    print file, "->", file2
    move(file, file2)
                
