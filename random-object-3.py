import sys
FREECADPATH = '/usr/lib/freecad/lib/'
sys.path.append(FREECADPATH)
from pyooml import *
import random


#-- Number of drills to perform
N = 20

#-- Max drill radius
RMAX = 5

#-- Base Max side
SIDE_MAX = 60

doc = newdoc()

#--- Base object
base = cube(SIDE_MAX, SIDE_MAX, 4)

#-- INitially the object is the base without drills
obj = base

#-- Random drill
for i in range(N):
    r = RMAX * random.random()
    x,y = (SIDE_MAX * random.random(), SIDE_MAX * random.random())
    cyl = cylinder(r = r, h = 20, center = True).translate(x,y,0)
    obj = obj - cyl




#-- Export the file
name = "./obj{}-{}.stl".format(int(round(x * 10)),
                               int(round(y * 10)))
obj.export_STL(name)
print("{} generated".format(name))
