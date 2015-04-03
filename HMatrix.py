import FreeCAD
import math

def Translation(x, y=None, z=None):
	"""Homogeneous matrix for translation"""

	#-- Function overloading. x is mandatory
	if y == None and z == None:
		#-- the first argument is an App.Vector
		v = x
	else:
		#-- The three components are given
		v = FreeCAD.Vector(x, y, z)

	return  FreeCAD.Matrix(1, 0, 0,  v.x,
                             0, 1, 0, v.y,
                             0, 0, 1, v.z,
                             0, 0, 0, 1)

def Rotx(ang):
	"""Homogeneous Matrix for Rotation about x axis"""
	rad = math.radians(ang)
	return  FreeCAD.Matrix(1, 0,              0,             0,
                           0, math.cos(rad), -math.sin(rad), 0,
                           0, math.sin(rad),  math.cos(rad), 0,
                           0, 0,              0,             1)
