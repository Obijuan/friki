import pyooml
import FreeCAD
import math
from pyooml import svector
from FreeCAD import Vector

N = 20
r = 20
ang = 360.0/N
v1 = Vector(r, 0, 0)
vr = Vector(r * math.cos(math.radians(ang)), r * math.sin(math.radians(ang)), 0)
vd = vr - v1

l = [svector(vd).translate(v1+Vector(4,0,0)).rotz(ang * i).color("red") for i in xrange(N)]
field = union(l)
cable = cylinder(r = 15, h = 50, center = True).color("green")
iv = svector((0,0,1), l = 150).translate(0,0,-150/2.).color("blue")
iv.d = 5
iv.arrow_l = 20
