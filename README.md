# python_script
- The code has some issues and may have bugs. Use it at your own risk.

# testing generator
- Raising StopIteration in Python <= 3.6 will halt or close generator but in Python >=3.7, this will raise Runtime Error
- Reading ex.txt:
```
#header
abc
1 2 3
xyz
4 5 6
end
#header
again
11 22 33
end
```
- We may stop when `end` keyword is found
- In generator_py36.py, finding `end` will rais StopIteration and it works OK in Python/3.6 but crashes in 3.7
- generator_py37.py shows how to use close() function for the generator
