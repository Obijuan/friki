#!/usr/bin/python
# -*- coding: utf-8 -*-

import FreeCAD
import Part

class cube(object):
	"""Primitive Object: a cube"""
	
	def __init__(self, lx = 10):
		self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Cube")
		#--Add property
		self.obj.Proxy = self
		self.obj.ViewObject.Proxy = self
		FreeCAD.ActiveDocument.recompute()
		print ("Cube Init!")

	def translate(self, x, y, z):
		"""Translate the object"""

		#-- Get the translation vector
		v = FreeCAD.Vector(x, y, z)
		self.obj.Placement.Base = v
	
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

