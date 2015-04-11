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
import math
import HMatrix

class part(object):
	"""Generic objects"""

	version = '0.1'

	#-- Dictionary of colors
	color_dict = {'red'  : (1., 0., 0.),
				  'green': (0., 1., 0.),
				  'blue' : (0., 0., 1.),
				  'darkred' : (0.5, 0., 0.),
				  'darkgreen' : (0., 0.5, 0.),
				  'darkblue'  : (0., 0., 0.5),
				  'yellow'    : (1., 1., 0.0),
				  'darkyellow': (0.5, 0.5, 0.0),
			      'orange'    : (1., 0.6, 0.0),
				  'magenta'   : (1., 0., 1.),
				  'darkmagenta' : (0.5, 0., 0.5),
				  'white'     : (1., 1., 1.),
				  'black'     : (0., 0., 0.),
				  'gray'      : (0.8, 0.8, 0.8),
				 }

	def __init__(self, obj):

		#-- Configure the object for working ok in the Freecad environment
		obj.Proxy = self
		try:
			obj.ViewObject.Proxy = self
		except:
			print("No viewprovider")

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

	def translate(self, x, y=None, z=None):
		"""Translate the object"""

		#-- Get the translation vector
		v = self._vector_from_args(x, y, z)

		#-- Apply the translation (relative to the current position)
		self.obj.Placement.Base += v

		FreeCAD.ActiveDocument.recompute()

		return self

	def rotate(self, v = FreeCAD.Vector(0, 0, 1), ang = 0):
		"""Rotatle the object around the axis given by v, and angle ang (in degrees)
		   Itis a relative transformation"""

		#-- Create the placement
		p = FreeCAD.Placement()
		p.Rotation = FreeCAD.Rotation(v, ang)

		#-- Convert to a Matrix
		M = p.toMatrix()

		#-- Apply the transformation
		self.transform(M)

		return self

	def rotz(self, ang):
		"""Rotate the object about the z axis, a given angle (Relative rotation)"""
		self.rotate(v = FreeCAD.Vector(0, 0, 1), ang = ang)
		return self

	def rotx(self, ang):
		"""Rotate the object about the x axis, a given angle (Relative rotation)"""
		self.rotate(v = FreeCAD.Vector(1, 0, 0), ang = ang)
		return self

	def roty(self, ang):
		"""Rotate the object about the y axis, a given angle (Relative rotation)"""
		self.rotate(v = FreeCAD.Vector(0, 1, 0), ang = ang)
		return self

	def transform(self, matrix):
		"""Apply the transformation given by the homogeneous matrix 4x4
		   The matrix is multiplied by the current transformation
           so, the transformation is relative"""

		#-- Get the current transform matrix
		M = self.obj.Placement.toMatrix()

		#-- Apply the new transformation to the current transform
		self.obj.Placement = FreeCAD.Placement(matrix * M)
		FreeCAD.ActiveDocument.recompute()

	def orientate(self, x, y = None, z = None, vref = FreeCAD.Vector(0,0,1)):
		"""Orientate the object so that the reference vector (vref) is pointing
		   in the same direction thant the given vector (x,y,z)"""
		v = self._vector_from_args(x, y, z)

		#-- Special cases. Null vector. Ignore
		if v.Length == 0:
			return

		#-- Special case: Vector in the z axis, poiting to the negative
		if v.x == 0 and v.y==0 and v.z < 0:
			raxis = App.Vector(1, 0, 0)
		else:
			raxis = vref.cross(v)

		#-- Calculate the rotation angle (in degrees)
		angle = math.degrees(vref.getAngle(v))

		#-- Rotate!
		self.obj.Placement.Rotation = FreeCAD.Rotation(raxis, angle)

		#FreeCAD.ActiveDocument.recompute()
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

	def export_STL(self, filename="unnamed.stl"):
		"""Export the object to STL file"""
		objs = [self.obj]
		import Mesh
		Mesh.export(objs, filename)

	def color(self, r, g = None, b = None):
		"""Set the object color"""

		#-- Check the arguments
		if g == None and b == None:
			#-- First argument is the color name
			try:
				col = part.color_dict[r]
			except:
				col = (0.8, 0.8, 0.8)
		else:
			#-- Arguments are the r, g, b componentes
			col = (float(r), float(g), float(b))

		self.obj.ViewObject.ShapeColor = col
		return self

	def ice(self, level = 50):
		"""Set the transparency level 0 - 100"""
		self.transparency = level
		return self

	def solid(self):
		"""Set the transparency level to 0"""
		self.transparency = 0
		return self

	@property
	def transparency(self):
		"""Read the transparency level 0 - 100"""
		return self.obj.ViewObject.Transparency

	@transparency.setter
	def transparency(self, value):
		"""Set the transparency level 0 - 100"""
		self.obj.ViewObject.Transparency = value

	@property
	def label(self):
		"""Object name"""
		return self.obj.Label

	@label.setter
	def label(self, value):
		"""Object name"""
		self.obj.Label = value

	@property
	def T(self):
		"""Transformation Matrix"""
		return self.obj.Placement.toMatrix()

	@T.setter
	def T(self, value):
		"""Transformation Matrix"""
		self.obj.Placement = FreeCAD.Placement(value)

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
		self.obj.addProperty("App::PropertyBool", "center","Cylinder","Cylinder centered").center = center
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

	@property
	def r(self):
		"""Cylinder radius"""
		return self.obj.r

	@r.setter
	def r(self, value):
		"""Attribute: cylinder radius"""
		self.obj.r = value
		FreeCAD.ActiveDocument.recompute()

	@property
	def h(self):
		"""Cylinder height"""
		return self.obj.h

	@h.setter
	def h(self, value):
		"""Attribute: cylinder height"""
		self.obj.h = value
		FreeCAD.ActiveDocument.recompute()

	@property
	def center(self):
		"""Cylinder centered"""
		return self.obj.center

	@center.setter
	def center(self, value):
		"""Attribute: cylinder centered"""
		self.obj.center = value
		FreeCAD.ActiveDocument.recompute()

	@property
	def angle(self):
		"""Cylinder angle"""
		return self.obj.angle

	@angle.setter
	def angle(self, value):
		"""Attribute: cylinder angle"""
		self.obj.angle = value
		FreeCAD.ActiveDocument.recompute()

	@property
	def d(self):
		"""Cylinder diameter"""
		return self.obj.r * 2.

	@d.setter
	def d(self, value):
		"""Attribute: cylinder diameter"""
		self.obj.r = value / 2.
		FreeCAD.ActiveDocument.recompute()

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

class sphere(part):
	"""Primitive object: a sphere"""

	def __init__(self, r, angle1 = -90):
		"""Create a primitive sphere of given r radius"""

		#-- Create the Freecad Object
		self.obj = FreeCAD.ActiveDocument.addObject("Part::Sphere","Sphere","Sphere")

		#-- Asign the attrributes
		self.r = r
		self.angle1 = angle1

		FreeCAD.activeDocument().recompute()
		return

	@property
	def r(self):
		"""Object radius"""
		return self.obj.Radius

	@r.setter
	def r(self, value):
		"""Object radius"""
		self.obj.Radius = value
		FreeCAD.ActiveDocument.recompute()

	@property
	def angle1(self):
		"""Sphere angle1"""
		return self.obj.Angle1

	@angle1.setter
	def angle1(self, value):
		"""Sphere angle1"""
		self.obj.Angle1 = value
		FreeCAD.ActiveDocument.recompute()

class svector(part):
	"""Solid Vector class"""
	def __init__(self, x, y = None, z = None, l = 0):
		"""Create a solid vector. From the origin to the point (x,y,z)
           or in that direction but with length l"""

		#-- Calculate the vector
		v = self._vector_from_args(x, y, z)

		#-- Create the Freecad Object
		self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Vector")

		#--Add properties
		self.obj.addProperty("App::PropertyVector","v","Vector","Vector coordinates").v = v
		self.obj.addProperty("App::PropertyLength","l","Length","Vector Length").l = l
		self.obj.addProperty("App::PropertyLength","arrow_l","Arrow","Head arrow Length").arrow_l = 2
		self.obj.addProperty("App::PropertyLength","d","Diameter","Vector diameter").d = 0.5

		#-- Call the parent class constructor
		super(svector, self).__init__(self.obj)

		#-- Default display mode
		self.obj.ViewObject.DisplayMode = 'Shaded'

	@property
	def v(self):
		"""Vector coordinates"""
		return self.obj.v

	@v.setter
	def v(self, value):
		"""Object radius"""
		self.obj.v = value
		FreeCAD.ActiveDocument.recompute()

	@property
	def l(self):
		"""Vector Length"""
		return self.obj.l

	@l.setter
	def l(self, value):
		"""Vector Length"""
		self.obj.l = value
		FreeCAD.ActiveDocument.recompute()

	@property
	def arrow_l(self):
		"""Head arrow length"""
		return self.obj.arrow_l

	@arrow_l.setter
	def arrow_l(self, value):
		"""Head arrow legnth"""
		self.obj.arrow_l = value
		FreeCAD.ActiveDocument.recompute()

	@property
	def d(self):
		"""Vector diameter"""
		return self.obj.d

	@d.setter
	def d(self, value):
		"""Vector diameter"""
		self.obj.d = value
		FreeCAD.ActiveDocument.recompute()

	def copy(self):
		"""Copy the vector"""
		#-- Call the parent class copy method
		vc = super(svector, self).copy()

		#-- Set the default display mode
		vc.obj.ViewObject.DisplayMode = 'Shaded'

		return vc

	def execute(self, obj):
		"""Build the object"""

		#-- When length l is given, a vector with length = l and
		#-- orientation v is created
		if obj.l == 0:
			l = obj.v.Length
		else:
			l = obj.l.Value

		#-- Correct the length
		if (l < obj.arrow_l):
			arrow_l = l/2.
		else:
			arrow_l = obj.arrow_l.Value

		#--- Create the base vector
		base_vect = FreeCAD.Vector(obj.v)
		base_vect.Length = l - arrow_l

		#-- Build the object
		vectz = Part.makeCylinder(obj.d / 2.0, base_vect.Length,
							    Vector(0,0,0), obj.v)
		base = Part.makeSphere(obj.d / 2.0)
		arrow = Part.makeCone(obj.d/2. + 2/3. * obj.d, 0.05, arrow_l,
							  base_vect, base_vect)

		#-- Create the union of all the parts
		u = vectz.fuse(base)
		u = u.fuse(arrow)

		#-- Asign the shape
		obj.Shape = u

class frame(part):
	"""Frame object"""
	def __init__(self, l = 10):
		"""Create a frame. l is the vector's length"""

		#-- Store the vector length
		self.l = l

		#-- Create the Freecad Object
		self.obj = FreeCAD.ActiveDocument.addObject("Part::Compound","Frame")

		#-- Build the frame
		self.x_axis = svector(1, 0, 0, l = l).color("red")
		self.x_axis.label = "X axis"

		self.y_axis = svector(0, 1, 0, l = l).color("green")
		self.y_axis.label = "Y axis"

		self.z_axis = svector(0, 0, 1, l = l).color("blue")
		self.z_axis.label = "Z axis"

		self.origin = sphere(r = 0.5)
		self.origin.label = "Origin"

		#-- Creat the compound object
		self.obj.Links = [self.x_axis.obj, self.y_axis.obj, self.z_axis.obj,
						  self.origin.obj]

		#-- Default display mode
		self.obj.ViewObject.DisplayMode = 'Shaded'

		FreeCAD.activeDocument().recompute()
		return

class point(part):
	"""Solid point object"""

	def __init__(self, x, y = None, z = None, r = 0.5):
		"""Create a point"""

		#-- Store the position vector
		self.pos = self._vector_from_args(x, y, z)

		#-- Create the Freecad Object
		self.obj = FreeCAD.ActiveDocument.addObject("Part::Sphere","Point","Point")

		#-- Asign the radius
		self.r = r

		#-- Place the point on the given coordinates
		self.translate(self.pos)

		#-- Default display mode
		self.obj.ViewObject.DisplayMode = 'Shaded'

		FreeCAD.activeDocument().recompute()
		return

	@property
	def r(self):
		"""Object radius"""
		return self.obj.Radius

	@r.setter
	def r(self, value):
		"""Object radius"""
		self.obj.Radius = value
		FreeCAD.ActiveDocument.recompute()

class link(part):
	"""Link object"""

	def __init__(self, l, D, w):
		"""Parameters:
			l: distance between centers
			D: Diameter of the rounded edges
			w: thickness
		"""

		#-- Create the FreeCAD object
		self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Link")

		#--Add properties
		self.obj.addProperty("App::PropertyLength","l","Length","Link Length").l = l
		self.obj.addProperty("App::PropertyLength","D","Diameter","Edge diameter").D = D
		self.obj.addProperty("App::PropertyLength","w","Width","Link thickness").w = w

		#-- Call the parent class constructor
		super(link, self).__init__(self.obj)
		return

	@property
	def l(self):
		"""Link length"""
		return self.obj.l

	@l.setter
	def l(self, value):
		"""Link length"""
		self.obj.l = value
		FreeCAD.ActiveDocument.recompute()

	@property
	def D(self):
		"""Link edges diameter"""
		return self.obj.D

	@D.setter
	def D(self, value):
		"""Link edges diameter"""
		self.obj.D = value
		FreeCAD.ActiveDocument.recompute()

	@property
	def w(self):
		"""Link thickness"""
		return self.obj.w

	@w.setter
	def w(self, value):
		"""Link thickness"""
		self.obj.w = value
		FreeCAD.ActiveDocument.recompute()

	def execute(self, obj):
		"""Build the object"""
		body = Part.makeBox(obj.l, obj.w, obj.D,
							FreeCAD.Vector(0, -obj.w/2., -obj.D/2.))

		edge_o = Part.makeCylinder(obj.D/2., obj.w,
							FreeCAD.Vector(0, -obj.w/2., 0),  FreeCAD.Vector(0, 1, 0))

		edge_l = Part.makeCylinder(obj.D/2., obj.w,
							FreeCAD.Vector(obj.l, -obj.w/2., 0), FreeCAD.Vector(0, 1, 0))
		u = body.fuse(edge_o)
		u = u.fuse(edge_l)
		u = u.removeSplitter()

		#-- Asign the shape
		obj.Shape = u

#--- Aux functions for testing
def newdoc():
	"""Create a new Freecad document"""
	return FreeCAD.newDocument("Example")

#---------------------------  Examples ------------------------------------
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

def test_T_1():
	"""Testing the .T property"""
	c = cube(10, 10, 10)
	c.rotz(45).rotx(30).translate(20, 0, 0).roty(40)

	#-- Create a new cubo
	c1 = cube(30, 30, 2)

	#-- Assign the same transformation
	c1.T = c.T

def test_spheres_1():
	"""Testing spheres: draw them in a sinusoidal path"""
	r = 0.5
	N = 20
	[sphere(r = r).translate(2 * r * i, 0, 10*r * math.sin(2*math.pi*i/N))
     for i in range(N)]

from FreeCAD import Vector

def test_vector_0():
	frame();
	sv = svector(10, 10, 0)

def test_vector_1():
	print("Test")
	v1 = Vector(10, 0, 0)
	v2 = Vector(0, 10, 0)
	v3 = Vector(0, 0, 10)

	sv1 = svector(v1)
	sv2 = svector(v2)
	sv3 = svector(v3)
	sv4 = svector(v1 + v2)

	sv5 = svector(v1).translate(v2)
	sv6 = svector(v2).translate(v1)

#---------------------------
"""
class Line:
    def __init__(self, obj):
         '''"App two point properties" '''
         obj.addProperty("App::PropertyVector","p1","Line","Start point")
         obj.addProperty("App::PropertyVector","p2","Line","End point").p2=FreeCAD.Vector(100,0,0)
         obj.Proxy = self

    def execute(self, fp):
        '''"Print a short message when doing a recomputation, this method is mandatory" '''
        fp.Shape = Part.makeLine(fp.p1,fp.p2)

class ViewProviderLine:
   def __init__(self, obj):
      ''' Set this object to the proxy object of the actual view provider '''
      obj.Proxy = self

   def getDefaultDisplayMode(self):
      ''' Return the name of the default display mode. It must be defined in getDisplayModes. '''
      return "Flat Lines"
"""


#----------- Examples from the friki library
def test_friki_1():
	v = Vector(10,10,10)
	p = point(20, 20,20)
	f1 = frame()
	f2 = frame().translate(20,0,0)

def test_friki_3():
	frame()
	cube(10, 10, 10).ice(80)

	v1 = Vector(10, 10, 10)
	v2 = Vector(10, 10, 0)
	v3 = Vector(0, 0, 10)
	svector(v1).color("yellow")
	svector(v2)
	svector(v3).translate(v2)

def test_friki_4():
	#-- Ref system 1
	frame()
	r1 = Vector(20, 20, 20)
	sv1 = svector(r1).color("yellow")

	#-- Ref system 2
	sv2 = svector(10,10,4).translate(r1)
	f2 = frame().translate(r1)

def test_friki5():
	#-- Frame 1
	frame(l = 20)
	v1 = Vector(20, 20, 20)
	v1p = Vector(v1.x, v1.y, 0)
	svector(v1).color("yellow")
	svector(v1p).color("black")

	#-- Fram 2
	frame(l=20).translate(v1)
	v2 = Vector(30, 0, 10)
	svector(v2).translate(v1)
	svector(v2.x, v2.y, 0).color("black").translate(v1p)

	#-- Frame in the robot end
	frame(l = 20).translate(v1).translate(v2)

def test_friki6():
	#-- Frame 1
	frame()

	#-- Frame 2
	f2 = frame()

	#-- Homogeneours matrices
	M = HMatrix.Translation(20, 0, 0)
	N = HMatrix.Rotx(30)

	#-- Apply a transformation matrix to the frame 2
	f2.T = M * N

def test_link_1():
	f0 = frame()
	l1 = link(l = 40, w = 5, D = 10)
	l2 = l1.copy()
	l2.roty(30)
	l2.translate(40, 0, 0)

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
	#test_mecano_part_1()
	#test_T_1()
	#test_spheres_1()
	#test_vector_0()
	#test_vector_1()
	#test_friki_1()
	#test_friki_3()
	#test_friki_4()
	#test_friki5()
	#test_friki6()
	test_link_1()
