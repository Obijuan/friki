#------------------------------------------------------------------------------
#-- FRIKI:  Freecad, RobotIcs and KInematics
#------------------------------------------------------------------------------
#-- (C) Juan Gonzalez-Gomez (Obijuan)  March - 2015
#------------------------------------------------------------------------------
#-- Releases under the GNU GPL v2
#------------------------------------------------------------------------------

import FreeCAD
import pyooml
import HMatrix

from pyooml import frame, svector
from FreeCAD import Vector

#-- Exercise. Barrientos book. 79. Example. 3.1
def barrientos_pag79_ex3_1():
	#--- Frame 1 and p vector
	frame()
	p = Vector(6, -3, 8)
	svector(p)

	#--- Frame 2. Translated p
	f2 = frame()
	M = HMatrix.Translation(p)
	f2.T = M

	#-- Vector r in the frame 2
	r = Vector(-2, 7, 3)
	sr = svector(r)
	sr.T = M

	#-- Calculate the r0 vector: r refered to frame 1
	r0 = M.multiply(r)
	sr0 = svector(r0).color("yellow")
	print("r0: {}".format(r0))

def barrientos_ex3_2_pag_80():
	#--- Define the transformation
	p = Vector(6, -3, 8)
	T = HMatrix.Translation(p)
	
	#--- Calculate r and its transformation
	r = Vector(4, 4, 11)
	r2 = T.multiply(r)
	
	#--- Draw all the vectors
	vr = svector(r)
	vp = svector(p).translate(r)
	vr2 = svector(r2).color("yellow")
	
	print("r2: {}".format(r2))


if __name__ == "__main__":
	#barrientos_pag79_ex3_1()
	barrientos_ex3_2_pag_80()
	

