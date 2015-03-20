#!/usr/bin/python
# -*- coding: utf-8 -*-

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
		return union(self, other)

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
	
	def __init__(self, part1, part2):
		#-- Call the parent class constructor first
		super(union, self).__init__()
		
		#-- Create the Freecad Object
		doc = FreeCAD.activeDocument()
		self.obj = doc.addObject("Part::MultiFuse","Union")

		#-- Do the union!
		self.obj.Shapes = [part1.obj, part2.obj]

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
	base = cube(b, center = True).translate(0, 0, b.z/2)
	
	final_part = base + cross
	
if __name__ == "__main__":
	#test_cube1()
	#test_L()
	#test_cross()
	test_cross2()

