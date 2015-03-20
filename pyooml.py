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
		print("Parts sum!!! {} + {}".format(self.obj.Label, other.obj.Label))

		#-- Return the union of the two objects
		return union(self, other)

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
	
	def __init__(self, lx = 10, ly = 10, lz = 10):
		"""Create a primitive cube:
			lx: length in x axis
			ly: length in y axis
			lz: length in z axis"""
		
		#-- Call the parent class constructor first
		super(cube, self).__init__()
		
		#-- Create the Freecad Object
		self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Cube")

		#--Add property
		
		#-- Configure the object for working ok in the Freecad environment	
		self.obj.Proxy = self
		self.obj.ViewObject.Proxy = self
		
		#-- Show the object!
		FreeCAD.ActiveDocument.recompute()
		print ("Cube Init!")
	
	def __str__(self):
		str_id = "cube({}, {}, {}). Label: {}".format(10, 10, 10, self.obj.Label)
		return str_id	
	
	def translate(self, x, y, z):
		"""Translate the object"""

		#-- Get the translation vector
		v = FreeCAD.Vector(x, y, z)
		
		#-- Apply the translation (relative to the current position)
		self.obj.Placement.Base += v

		print("hola")
		return self
	
	def execute(self, obj):
		"""Build the object"""
		obj.Shape = Part.makeBox(10, 10, 10)
		print ("Cube Exetute!")
	
	def getDefaultDisplayMode(self):
		"""VIEWPROVIDER..."""
		print("getDefaultDisplayMode")
		return "Flat Lines"

def test_cube1():
	#-- Place a single cube
	cube()
	
	#-- Place a translated cube
	cube().translate(10, 10, 10)

	
if __name__ == "__main__":
	test_cube1()

