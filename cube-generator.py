import sys
FREECADPATH = '/usr/lib/freecad/lib/'
sys.path.append(FREECADPATH)
from pyooml import *


doc = newdoc()
c = cube(10,10,10)
c.export_STL("./cubo.stl")
