import sys
import pyansys
if len(sys.argv) < 2:
    print("Enter rst file name with the command: python3 rst2VTK.py file.rst")
    sys.exit()

infile = sys.argv[1]
outfile = infile + '.vtk'
result = pyansys.ResultReader('file.rst')
grid = result.grid.copy()
# check binary_reader.py at source code of pyansys
for i in range(result.nsets):
    _, val = result.NodalSolution(i)
    grid.point_arrays['NodalSolution{:03d}'.format(i)] = val
    nodenum = result.grid.point_arrays['ansys_node_num']
    _, stress = result.NodalStress(i)
    grid.point_arrays['NodalStress{:03d}'.format(i)] = stress

grid.save(outfile)

#pyansys fromPyPI is required.
#If pyansys is built from source code, cython module is necessary
