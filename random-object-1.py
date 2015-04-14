import sys
FREECADPATH = '/usr/lib/freecad/lib/'
sys.path.append(FREECADPATH)
from pyooml import *
import random

doc = newdoc()

#-- Random list
ranl = [40 * random.random() for i in xrange(5)]
lc = [cube(10, y + 1, 10).translate(10 * i, 0, 0) for i,y in enumerate(ranl)]
obj = union(lc)

#-- Export the file
name = "./obj{}-{}-{}.stl".format(int(round(ranl[0])),
                                   int(round(ranl[1])),
                                   int(round(ranl[2])))
obj.export_STL(name)
print("{} generated".format(name))
