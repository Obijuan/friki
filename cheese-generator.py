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
SIDE_MAX = 83

doc = newdoc()

#--- Base object
base = cylinder(r = SIDE_MAX, h = 4, angle = 45)

#-- INitially the object is the base without drills
obj = base

id = ""

#-- Random drill
for i in range(N):
    r = RMAX * random.random()
    x = SIDE_MAX * random.random()
    y = x * random.random()
    cyl = cylinder(r = r, h = 20, center = True).translate(x,y,0)
    obj = obj - cyl
    id = id + "{}{}{}".format(
                              int(round(x * 10)),
                              int(round(y * 10)),
                              int(round(r * 10)))

id = id[:15]

#-- Export the file
name = "./cheese-id-{}.stl".format(id)

obj.export_STL(name)
print("{} generated".format(name))
