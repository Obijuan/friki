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
import copy
import Draft

class part(object):
	"""Generic objects"""

	version = '0.1'	
	
	def __init__(self, obj):
		
		#-- Configure the object for working ok in the Freecad environment	
		obj.Proxy = self
		obj.ViewObject.Proxy = self
		
		#-- Show the object!
		FreeCAD.ActiveDocument.recompute()
	
	# overload +
	def __add__(self, other):
		"""Union operator"""

		#-- Return the union of the two objects
		return union([self, other])
	
	 #-- Overload - operator
	def __sub__(self, other):
		"""Difference operator"""
		return difference(self, other)
	
	def translate(self, x, y, z):
		"""Translate the object"""
		
		#-- Get the translation vector
		v = FreeCAD.Vector(x, y, z)
		
		#-- Apply the translation (relative to the current position)
		self.obj.Placement.Base += v
	
		return self

	def copy(self):
		"""Return a copy of the object"""

		c = copy.copy(self)
		c.obj = FreeCAD.ActiveDocument.copyObject(self.obj)
		return c

	def clone(self):
		"""Returns a clone of the object"""
		duplicate = copy.copy(self)
		duplicate.obj = Draft.clone(self.obj)
		return duplicate
	
	def getDefaultDisplayMode(self):
		"""VIEWPROVIDER..."""
		#print("getDefaultDisplayMode")
		return "Flat Lines"
	
	
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
	
	def __getstate__(self):
		return None
 
	def __setstate__(self,state):
		return None

class union(part):
	"""Union of objects"""
	
	def __init__(self, items):
		"""items = list of parts to perform union"""
		
		#-- Create the Freecad Object
		self.obj = FreeCAD.activeDocument().addObject("Part::MultiFuse","Union")
		
		#-- Save the list of parts
		self.childs = items
		
		#-- Do the union!
		l = [item.obj for item in self.childs]
		self.obj.Shapes = l
		
		FreeCAD.activeDocument().recompute()
	
	def __str__(self):
		str_id = "[{}] Union:\n".format(self.obj.Label)
		for child in self.childs:
			str_id += "{}".format(child)
		return str_id + '\n'
	
	def copy(self):
		"""Return a copy of the object"""
		
		#-- Create a new union
		lc = [child.copy() for child in self.childs]
		u = union(lc)
		
		#-- Copy the placement
		u.obj.Placement = self.obj.Placement
		
		FreeCAD.activeDocument().recompute()
		
		return u		

class difference(part):
	"""Difference of two parts: base - tool"""
	
	def __init__(self, base, tool):
		"""Perform the difference of base - tool"""
		
		#-- Create the Freecad Object
		doc = FreeCAD.activeDocument()
		self.obj = doc.addObject("Part::Cut","Difference")
		
		#-- Store the childs
		self.op1 = base
		self.op2 = tool
		
		#-- Do the difference!
		self.obj.Base = self.op1.obj
		self.obj.Tool = self.op2.obj	
		
		doc.recompute()

	def __str__(self):
		str_id = "[{}] Difference:\n".format(self.obj.Label)
		str_id += "{}".format(self.op1)
		str_id += "{}".format(self.op2)
		return str_id + '\n'

		doc.recompute()
	
	def copy(self):
		"""Return a copy of the object"""
		
		#-- Create the new difference
		d = difference(self.op1.copy(), self.op2.copy())
		
		#-- Copy the placement
		d.obj.Placement = self.obj.Placement
		
		return d

class cylinder(part):
	"""Primitive Object: a cylinder"""
	
	def __init__(self, r = 5, h = 30, d = None, angle = 360, center = False):
		"""Create a primitive cylinder:
			 r: radius or d: diameter
			 h: height
		"""
		
		#-- Create the Freecad Object
		self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Cylinder")
		self.obj.addProperty("App::PropertyBool", "center","Cylinder","Cylinder centered").center = False
		self.obj.addProperty("App::PropertyLength","r","Cylinder","Radius").r = r
		self.obj.addProperty("App::PropertyLength","h","Cylinder","Height").h = h
		self.obj.addProperty("App::PropertyAngle","angle","Cylinder","Section angle").angle = angle

		#-- Set the cylinder parameters
		if d == None:
			self.obj.r = r
		else:
			self.obj.r = d / 2.
		
		self.obj.h = h
		
		#-- Call the parent class constructor
		super(cylinder, self).__init__(self.obj)
	
	#-- TODO: Add the properties to the main pyooml object!!!!
	
	def execute(self, obj):
		"""Build the object"""
		
		#-- Draw the box, chaging the position depending on the center property
		if obj.center == True:
			off_z = -obj.h.Value / 2.
			b = Part.makeCylinder(obj.r, obj.h, 
                                  FreeCAD.Vector(0,0,off_z), FreeCAD.Vector(0,0,1), obj.angle)
		else:
			b = Part.makeCylinder(obj.r, obj.h, 
                                  FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1), obj.angle)
		
		#-- Asign the shape
		obj.Shape = b


class cube(part):
	"""Primitive Object: a cube"""
	
	def __init__(self, lx, ly = None, lz = None, center = False):
		"""Create a primitive cube:
			lx: length in x axis
			ly: length in y axis
			lz: length in z axis"""
		
		v = self._vector_from_args(lx, ly, lz)

		#-- Create the Freecad Object
		self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Cube")

		#--Add property
		self.obj.addProperty("App::PropertyLength","lx","Cube","Length in x axis").lx = v.x
		self.obj.addProperty("App::PropertyLength","ly","Cube","Length in y axis").ly = v.y
		self.obj.addProperty("App::PropertyLength","lz","Cube","Length in z axis").lz = v.z
		self.obj.addProperty("App::PropertyBool", "center","Cube","Box centered").center = center
		
		#-- Call the parent class constructor
		super(cube, self).__init__(self.obj)
	
	def __str__(self):
		str_id = "[{}] cube({}, {}, {})\n".format(self.obj.Label, self.obj.lx, 
											 	    self.obj.ly, self.obj.lz)
		return str_id		
	
	@property
	def lx(self):
		"""Object length in x axis"""
		return self.obj.lx
	
	@lx.setter
	def lx(self, value):
		"""Attribute: Set the length in x axis"""
		self.obj.lx = value
		FreeCAD.ActiveDocument.recompute()	

	@property
	def ly(self):
		"""Object length in y axis"""
		return self.obj.ly
	
	@ly.setter
	def ly(self, value):
		"""Attribute: Set the length in y axis"""
		self.obj.ly = value
		FreeCAD.ActiveDocument.recompute()
		
	@property
	def lz(self):
		"""Object length in z axis"""
		return self.obj.lz
	
	@lz.setter
	def lz(self, value):
		"""Attribute: Set the length in z axis"""
		self.obj.lz = value
		FreeCAD.ActiveDocument.recompute()
	
	@property	
	def center(self):
		"""How to draw the cube"""
		return self.obj.center
	
	@center.setter
	def center(self, value):
		"""Set the center property"""
		self.obj.center = value
		FreeCAD.ActiveDocument.recompute()
		
	def execute(self, obj):
		"""Build the object"""
		
		#-- Draw the box, chaging the position depending on the center property
		if obj.center == True:
			off = FreeCAD.Vector(-obj.lx.Value/2., -obj.ly.Value/2., -obj.lz.Value/2.)
			b = Part.makeBox(obj.lx, obj.ly, obj.lz, FreeCAD.Vector(off.x,off.y,off.z))
		else:
			b = Part.makeBox(obj.lx, obj.ly, obj.lz)
		
		#-- Asign the shape
		obj.Shape = b






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
	part1 = base - hole1 - hole2

def test_cube_copy():
	#-- The two cubes are equal
	c1 = cube(10, 20, 30)
	c2 = c1.copy()
	
	#-- Translate the copy. It should not affect cube 1
	c2.translate(20, 0, 0)
	
	#-- Change cube 1. It should NOT affect cube 2
	c1.lx = 5
	
	#-- Change cube 2. It should NOT affect cube 1
	c2.lx = 20
	
def test_difference_copy():
	#-- Create an object using differences
	c1 = cube(30, 30, 2, center = True)
	c2 = cube(5,5,20, center = True)
	d1 = c1 - c2
	
	#-- Copy the object
	d2 = d1.copy()
	
	#-- Translate the copy
	d2.translate(50, 0, 0)
	
	#-- Change the inner part of the first object
	c2.lx = 10

def test_difference_3():
	"""Test the difference  a - (b + c +d)"""
	base = cube(40,40,3, center = True)
	drill1 = cube(3,3,10, center = True)
	drill2 = drill1.copy().translate(-10,0,0)
	drill3 = drill1.copy().translate(10,0,0)
	drills = drill1 + drill2 + drill3
	
	mypart = base - drills

def test_union_copy():
	c1 = cube(10,10,10)
	c2 = cube(10,10,10).translate(10,0,0)
	u1 = (c1 + c2).translate(30,0,0)
	
	u2 = u1.copy()
	u2.translate(30, 0, 0)
	c1.ly = 20

def test_difference_4():
	""" Test the difference (a - b) + (c -d)"""
	
	base1 = cube(30,30,5,center = True)
	drill1 = cube(5,5,20, center = True)
	base2 = cube(5,30,30,center = True)
	drill2 = cube(20,5,5, center = True)
	
	part1 = (base1 - drill1) + (base2 - drill2).translate(-15,0,15)

def test_difference_5():
	"""Test the difference (a + b) - (c + d)"""
	
	base1 = cube(30, 30, 5, center = True)
	base2 = cube(20,20,30, center = True).translate(0, 0, 15)
	part1 = base1 + base2
	
	arm1 = cube(10,4, 100, center = True)
	arm2 = cube(4, 10, 100, center = True)
	cross = arm1 + arm2
	final = part1 - cross

def test_mecano_part_1():
	w = 10
	h = 2
	d1 = 10
	d2 = 3
	N = 2
	length = d1 * N
	base = cube(length, w, h, center = True)
	drill1 = cube(d2, d2, 3*h, center = True).translate(-length/2 + d1/2, 0, 0)
	drill2 = drill1.clone().translate(d1, 0, 0)
	part1 = base - drill1 - drill2
		
	
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
	#test_difference_2()
	#test_cube_copy()
	#test_difference_3()
	#test_union_copy()
	#test_difference_4()
	#test_difference_5()
	test_mecano_part_1()


