#!/usr/bin/python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
#- PYOOML.  Python Object Oriented Mechanics Library
#-------------------------------------------------------------------------
#  (C)  Juan Gonzalez-Gomez (Obijuan)  March-2015
#  (C)  Alberto Valero
#--------------------------------------------------------------------------
#-  Released under de GPL v2 License
#---------------------------------------------------------------------------


import FreeCAD
import Part

class part(object):
	"""Generic objects"""
	
	def __init__(self):
		print("new part")
	
	# overload +
	def __add__(self, other):
		"""Union operator"""
		
		print("Union {} + {}".format(self.obj.Label, other.obj.Label))

		#-- Return the union of the two objects
		return union([self, other])
	
	 #-- Overload - operator
	def __sub__(self, other):
		print("Difference")
		return difference(self, other)
	
	def translate(self, x, y, z):
		"""Translate the object"""
		
		#-- Get the translation vector
		v = FreeCAD.Vector(x, y, z)
		
		#-- Apply the translation (relative to the current position)
		self.obj.Placement.Base += v
	
		print("hola")
		return self
	
	def _vector_from_args(self, x, y, z):
		"""Utility function. It returns a vector with the x,y,z components"""
		
		#-- Function overloading. x is mandatory
		if y == None and z == None:
			#-- the first argument is an App.Vector
			v = x
		else:
			#-- The three components are given
			v = FreeCAD.Vector(x, y, z)

		#-- Return the vector
		return v

class union(part):
	"""Union of objects"""
	
	def __init__(self, items):
		"""items = list of parts to perform union"""

		#-- Call the parent class constructor first
		super(union, self).__init__()
		
		#-- Create the Freecad Object
		doc = FreeCAD.activeDocument()
		self.obj = doc.addObject("Part::MultiFuse","Union")

		#-- Do the union!
		l = [item.obj for item in items]
		self.obj.Shapes = l

		doc.recompute()
		print("Union!")

class difference(part):
	"""Difference of two parts: base - tool"""
	
	def __init__(self, base, tool):
		"""Perform the difference of base - tool"""
		
		#-- Call the parent class constructor first
		super(difference, self).__init__()
		
		#-- Create the Freecad Object
		doc = FreeCAD.activeDocument()
		self.obj = doc.addObject("Part::Cut","Difference")

		#-- Do the difference!
		self.obj.Base = base.obj
		self.obj.Tool = tool.obj

		doc.recompute()
		print("Union!")

class cube(part):
	"""Primitive Object: a cube"""
	
	def __init__(self, lx, ly = None, lz = None, center = False):
		"""Create a primitive cube:
			lx: length in x axis
			ly: length in y axis
			lz: length in z axis"""
		
		#-- Call the parent class constructor first
		super(cube, self).__init__()
		
		v = self._vector_from_args(lx, ly, lz)

		#-- Create the Freecad Object
		self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Cube")

		#--Add property
		self.obj.addProperty("App::PropertyLength","lx","Cube","Length in x axis").lx = v.x
		self.obj.addProperty("App::PropertyLength","ly","Cube","Length in y axis").ly = v.y
		self.obj.addProperty("App::PropertyLength","lz","Cube","Length in z axis").lz = v.z

		#-- Set the pos
		if center == True:
			self.obj.Placement.Base = FreeCAD.Vector(-v.x / 2., -v.y / 2., -v.z / 2.)

		#-- Configure the object for working ok in the Freecad environment	
		self.obj.Proxy = self
		self.obj.ViewObject.Proxy = self
		
		#-- Show the object!
		FreeCAD.ActiveDocument.recompute()
		print ("Cube Init!")
	
	def __str__(self):
		str_id = "cube({}, {}, {}). Label: {}".format(self.obj.lx, self.obj.ly, 
												      self.obj.lz, self.obj.Label)
		return str_id
	
	@property
	def lx(self):
		"""Object length in x axis"""
		print("Accesing lx...")
		return self.obj.lx
	
	@lx.setter
	def lx(self, value):
		"""Attribute: Set the length in x axis"""
		self.obj.lx = value
		FreeCAD.ActiveDocument.recompute()	

	@property
	def ly(self):
		"""Object length in y axis"""
		print("Accesing ly...")
		return self.obj.ly
	
	@ly.setter
	def ly(self, value):
		"""Attribute: Set the length in y axis"""
		self.obj.ly = value
		FreeCAD.ActiveDocument.recompute()
		
	@property
	def lz(self):
		"""Object length in z axis"""
		print("Accesing lz...")
		return self.obj.lz
	
	@lz.setter
	def lz(self, value):
		"""Attribute: Set the length in z axis"""
		self.obj.lz = value
		FreeCAD.ActiveDocument.recompute()	
		
	def execute(self, obj):
		"""Build the object"""
		
		obj.Shape = Part.makeBox(obj.lx, obj.ly, obj.lz)
		print ("Cube Execute!")
	
	def getDefaultDisplayMode(self):
		"""VIEWPROVIDER..."""
		print("getDefaultDisplayMode")
		return "Flat Lines"

def test_cube1():
	#-- Place a single cube
	cube()
	
	#-- Place a translated cube
	cube().translate(10, 10, 10)

def test_L():
	c1 = cube(40, 10, 10)
	c2 = cube(10, 40, 10)
	l = c1 + c2

def test_cross():
	c1 = cube(40, 10, 10, center = True)
	c2 = cube(10, 40, 10, center = True)
	cross = c1 + c2

def test_cross2():
	s1 = FreeCAD.Vector(40, 10, 10)
	s2 = FreeCAD.Vector(10, 40, 10)
	cross = cube(s1, center = True) + cube(s2, center = True)

	#-- Base
	b = s1 + s2
	base = cube(b, center = True).translate(0, 0, -b.z/2)
	
	final_part = base + cross

def test_multiple_unions_1():
	v = FreeCAD.Vector(10, 10, 10)
	c1 = cube(v)
	c2 = cube(v).translate(v.x, 0, 0)
	c3 = cube(v).translate(2 * v.x, 0, 0)
	c4 = cube(v).translate(3 * v.x, 0, 0)
	part = c1 + c2 + c3 + c4

def test_multiple_unions_2():
	v = FreeCAD.Vector(10, 10, 10)
	l = [cube(v).translate(i * v.x, i, 0) for i in range(10) ]
	part = union(l)

def test_stairs():
	v = FreeCAD.Vector(10, 40, 4)
	l = [cube(v.x, v.y, v.z * i).translate(i * v.x, 0, 0) for i in range(1,10)]
	union(l)

def test_stairs_2D():
	v = FreeCAD.Vector(100, 100, 4)
	l = [cube(v.x - 10*i, v.y - 10*i, v.z).translate(0, 0, v.z * i) for i in range(10)]
	union(l)

import math
	
def cube_sine_1():
	v = FreeCAD.Vector(10, 80, 10)
	A = 20
	N = 20
	k = 2
	z0 = 10
	phi_ini = math.pi / 2
	l = [cube(v.x, v.y, A * math.sin(2 * math.pi * i / N - phi_ini) + A + z0).translate(v.x * i, 0, 0) for i in range(k * N)]
	union(l)

def cube_sine_2():
	v = FreeCAD.Vector(5, 5, 5)
	A = 10
	N = 10
	k = 1
	z0 = 5
	phi_ini = math.pi / 2
	z = [A * math.sin(2 * math.pi * i / N - phi_ini) + A + z0 for i in range(k * N)]
	l = [cube(v.x, v.y, zx + zy).translate(v.x * i, v.y * j, 0) 
          for i, zx in enumerate(z) for j, zy in enumerate(z)]
	part = union(l)
	return part

def cube_sine_3():
	p1 = cube_sine_2()
	c =cube(50, 50, 50)
	c.translate(0,0,10)
	p2 = c - p1
	

def test_difference_1():
	c1 = cube(30, 30, 2, center = True)
	c2 = cube(5,5,20, center = True)
	d = c1 - c2

def test_difference_2():
	w = 10
	h = 3
	d1 = 10
	d2 = 3
	N = 2
	length = d1 * N
	base = cube(length, w, h, center = True)
	hole1 = cube(d2, d2, 3*h, center = True).translate(-length/2 + d1/2, 0, 0)
	hole2 = cube(d2, d2, 3*h, center = True).translate(-length/2 + d1/2 + d1, 0, 0)
	part = base - hole1 - hole2
	
	
if __name__ == "__main__":
	#test_cube1()
	#test_L()
	#test_cross()
	#test_cross2()
	#test_multiple_unions_1()
	#test_multiple_unions_2()
	#test_stairs()
	#test_stairs_2D()
	#cube_sine_1()
	#cube_sine_2()
	#cube_sine_3()
	#test_difference_1()
	test_difference_2()



