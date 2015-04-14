import sys
FREECADPATH = '/usr/lib/freecad/lib/'
sys.path.append(FREECADPATH)
from pyooml import *
import random

#-- Min. thickness
MIN = 2

#-- Determine the cube maximum dimensions
xmax, ymax, zmax = (60, 60, 60)

#-- Generate the random dimensions
lx = xmax * random.random()
ly = ymax * random.random()
lz = ymax * random.random()

#-- Limit the smallest trickness
if lx < MIN:
    lx = MIN

if ly < MIN:
    ly = MIN

if lz < MIN:
    lx = MIN

#-- Generate the cube
doc = newdoc()
c = cube(lx, ly, lz)


#-- Export the file
name = "./cubo{}-{}-{}.stl".format(int(round(lx)),
                                   int(round(ly)),
                                   int(round(lz)))
c.export_STL(name)
print("{} generated".format(name))
