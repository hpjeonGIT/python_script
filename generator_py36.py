def read_row(row):
    if row[0:3] == "end":
        raise StopIteration
    else:
        print(row)
    
def main_read():
    for row in open("ex.txt",'r'):
        yield read_row(row)
    
if __name__ == '__main__':
    mygen = main_read()
    for iter in mygen:
        iter
        
