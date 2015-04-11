import pyooml
import FreeCAD
import math
from pyooml import svector
from FreeCAD import Vector

N = 20
r = 20
ang = -360.0/N
v1 = Vector(r, 0, 0)
vr = Vector(r * math.cos(math.radians(ang)), r * math.sin(math.radians(ang)), 0)
vd = vr - v1

[svector(vd).translate(v1+Vector(4,0,0)).rotz(ang * i).color("red") for i in xrange(N)]

