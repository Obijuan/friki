from pyooml import *

doc = newdoc()
c = cube(10,10,10)
c.export_STL("./cubo.stl")
