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

# update of yield for generator from Python 3.6 to 3.7
- A typical while loop for generator in Python 3.6 or older
```
def action():
    while True:
        yield do_something()
```        
- In Python 3.7 or higher, StopIteration will raise a runtime error and this might be modified as:
```
def action():
    while True:
        try:
            yield do_something()
        except StopIteration:
           return
```        
- Ref: https://stackoverflow.com/questions/16465313/how-yield-catches-stopiteration-exception
