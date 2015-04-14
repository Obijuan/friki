import sys
FREECADPATH = '/usr/lib/freecad/lib/'
sys.path.append(FREECADPATH)
from pyooml import *
import random

#-- Constants
HEIGHT = 5
MIN = 2

def base(Ml):
    #-- Creates a random base of given height
    l = Ml * random.random()
    b = cube(l, l, HEIGHT, center = True)
    return b


doc = newdoc()

lc = []
b = base(100)
h = HEIGHT

while(b.lx > MIN):
    lc.append(b)
    b = base(b.lx).translate(0, 0, h)
    h += HEIGHT


obj = union(lc)

#-- Export the file
name = "./obj{}-{}.stl".format(int(round(b.lx * 10)),
                               int(round(b.ly * 10)))
obj.export_STL(name)
print("{} generated".format(name))
