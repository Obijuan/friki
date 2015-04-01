#------------------------------------------------------------------------------
#-- FRIKI:  Freecad, RobotIcs and KInematics
#------------------------------------------------------------------------------
#-- (C) Juan Gonzalez-Gomez (Obijuan)  March - 2015
#------------------------------------------------------------------------------
#-- Releases under the GNU GPL v2
#------------------------------------------------------------------------------

import FreeCAD
import Part
import math


#-- Draw a vector in the z axis
#--- MIGRATED TO PYOOOML
def vectorz(l = 10, l_arrow = 2, d = 0.5, mark = False, show = True):
	"""Draw a vector in the z axis. Parameters:
		 l : Lenght
         l_arrow: arrow length
		 d : vector diameter
	"""

	#-- Correct the length
	if (l < l_arrow):
		l_arrow = l/2

	vectz = Part.makeCylinder(d / 2.0, l - l_arrow)
	base = Part.makeSphere(d / 2.0)
	arrow = Part.makeCone(d/2. + 2/3. * d, 0.05, l_arrow)
	arrow.Placement.Base.z = l - l_arrow

	#-- Create the union of all the parts
	union = vectz.fuse(base)
	union = union.fuse(arrow)

	#-- Return de vector z
	return union

#-- MIGRATED TO PYOOML
def orientate(part, v, vref = FreeCAD.Vector(0, 0, 1)):

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

	#-- Rotate vectz!
	part.Placement.Rotation = FreeCAD.Rotation(raxis, angle)

#-- Change the color to blue
def blue(part):
	part.ViewObject.ShapeColor = (0.0, 0.00, 1.00)

def red(part):
	part.ViewObject.ShapeColor = (1.0, 0.0, 0.0)

def green(part):
	part.ViewObject.ShapeColor = (0.0, 1.0, 0.0)

def gray(part):
	part.ViewObject.ShapeColor = (0.80,0.80,0.80)

def ice(obj, trans = 50):
	obj.ViewObject.Transparency = trans

def yellow(obj):
	obj.ViewObject.ShapeColor = (1.0, 1.0, 0.0)

#-- MIGRATED TO PYOOML
def vector(x, y = None, z = None, l = None):

	#-- Function overloading. x is mandatory
	if y == None and z == None:
		#-- the first argument is an App.Vector
		v = x
	else:
		#-- The three components are given
		v = FreeCAD.Vector(x, y, z)

	#-- When length l is given, a vector with length = l and
	#-- orientation (x,y,z) is created
	if l == None:
		l = v.Length

	#-- Vector on the z axis
	vectz = vectorz(l = l)
	vref = FreeCAD.Vector(0, 0, 1)

	#------ Orientate vectz on the v direction
	#-- Calculate the rotation axis
	orientate(vectz, v)

	#-- Add the vector to the current document
	doc = FreeCAD.ActiveDocument
	vec = doc.addObject("Part::Feature","Vector")
	vec.Shape = vectz
	doc.recompute()

	#-- Change the vector visual properties
	vo = vec.ViewObject
	vo.DisplayMode="Shaded"

	return vec

def frame(l = 10):

	#-- Create the axes vectors with different colors
	x_axis = vector(1, 0, 0, l = l)
	x_axis.Label = "X_axis"
	red(x_axis)
	y_axis = vector(0, 1, 0, l = l)
	y_axis.Label = "Y_axis"
	green(y_axis)
	z_axis = vector(0, 0, 1, l = l)
	z_axis.Label = "Z_axis"
	blue(z_axis)

	#-- Origin
	doc = FreeCAD.ActiveDocument
	origin = doc.addObject("Part::Sphere","Origin")
	origin.Radius = 0.5

	#-- Make a compound
	f = doc.addObject("Part::Compound","Frame")
	f.Links = [x_axis, y_axis, z_axis, origin]
	f.ViewObject.DisplayMode = "Shaded"

	doc.recompute()
	return f

def point(x, y = None, z = None, d = 1.0):

	#-- Function overloading. x is mandatory
		#-- the first argument is an App.Vector
	if y == None and z == None:
		v = x
	else:
		#-- The three components are given
		v = FreeCAD.Vector(x, y, z)

	#-- The point is a sphere
	pp = Part.makeSphere(d / 2.0)

	#-- Add the point to the current document
	doc = FreeCAD.ActiveDocument
	p = doc.addObject("Part::Compound","Point")

	#-- Set the shape
	p.Shape = pp

	#-- Set the placement
	p.Placement.Base = v


	p.ViewObject.DisplayMode = "Shaded"
	doc.recompute()

	return p

#-- MIGRATED TO PYOOML
def cube(lx = 10, ly = 10, lz = 10, center = False):
	print("Cube: {}, center =  {}".format([lx, ly, lz], center))

	#-- Add the cube to the current document
	doc = FreeCAD.ActiveDocument
	c = doc.addObject("Part::Box","Box")

	#-- Set the dimensions
	c.Length = lx
	c.Width = ly
	c.Height = lz

	#-- Set the pos
	if center == True:
		c.Placement.Base = FreeCAD.Vector(-lx / 2., -ly / 2., -lz / 2.)

	doc.recompute()
	return c

#--- MIGRATED TO PYOOML
def cylinder(r = 5, h = 10, center = True):
	doc = FreeCAD.ActiveDocument
	c = doc.addObject("Part::Cylinder","Cylinder")

	#-- Set the dimensions
	c.Radius = r
	c.Height = h
	c.Angle = 360.0

	#-- Set the pos
	if center == True:
		c.Placement.Base.z = -h/2.

	doc.recompute()
	return c

#-- MIGRATED TO PYOOML
def difference(obj1, obj2):
	doc = FreeCAD.ActiveDocument
	cut = doc.addObject("Part::Cut","Cut")
	doc.Cut.Base = obj1
	doc.Cut.Tool = obj2
	##obj1.Visibility = False
	##obj2.Visibility = False
	doc.recompute()
	return cut

#-- MIGRATED TO PYOOML
def translate(obj1, x, y = None, z = None):

	#-- Function overloading. x is mandatory
	if y == None and z == None:
		#-- the first argument is an App.Vector
		v = x
	else:
		#-- The three components are given
		v = FreeCAD.Vector(x, y, z)

	obj1.Placement.Base = FreeCAD.Vector(v)

#--- MIGRATED TO PYOOML
def transform(obj, matrix):
	#-- Get the current transform matrix
	M = obj.Placement.toMatrix()

	#-- Apply the new transformation to the current transform
	obj.Placement = FreeCAD.Placement(matrix * M)

def matrix_translate(x, y=None, z=None):
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
def matrix_rotx(ang):
	rad = math.radians(ang)
	return  FreeCAD.Matrix(1,  0,               0,            0,
                             0, math.cos(rad), -math.sin(rad),  0,
                             0, math.sin(rad),  math.cos(rad), 0,
                             0,  0,               0,            1)

def test3():
	frame()
	ice(cube(10, 10, 10))
	v1 = FreeCAD.Vector(10, 10, 10)
	v2 = FreeCAD.Vector(10, 10, 0)
	v3 = FreeCAD.Vector(0, 0, 10)
	yellow(vector(v1))
	vector(v2)
	translate(vector(v3), v2)

def test4():
	r1 = FreeCAD.Vector(20,20,20)
	r2 = FreeCAD.Vector(10,10,4)
	translate(vector(r2), r1)
	yellow(vector(r1))
	frame()
	f = frame()

	translate(f, r1)

def test5():
	v1 = FreeCAD.Vector(20, 20, 20)
	l1 = v1.Length
	v2 = FreeCAD.Vector(30, 0, 10)
	l2 = v2.Length
	frame(l = 20)

	#-- Projections of the link vector on the z=0 plane
	v1p = FreeCAD.Vector(v1.x, v1.y, 0)
	v2p = FreeCAD.Vector(v2.x, v2.y, 0)

	#-- Draw link vector 1
	yellow(vector(v1))

	#-- Draw link2
	translate(frame(l = 20), v1)
	translate( vector(v2), v1)

	#-- Frame in the robot end
	translate( frame(l = 20), v1+v2)

	#-- Draw the proyections (to see the robot better)
	vector(v1p)
	translate(vector(v2p), v1p)

def test6():
	frame()
	f = frame()
	M = matrix_translate(20, 0, 0)
	N = matrix_rotx(30)
	T = M * N
	transform(f, T)


#-- Exercise. Barrientos book. 79. Example. 3.1
def barrientos_pag79_ex3_1():
	frame()
	p = FreeCAD.Vector(6, -3, 8)
	vector(p)
	f1 = frame()
	M = matrix_translate(p)
	transform(f1,M)

	r = FreeCAD.Vector(-2, 7, 3)
	transform(vector(r), M)

	r0 = M.multiply(r)
	yellow(vector(r0))
	print("r0: {}".format(r0))

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

def test_line():
	a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Line")
	Line(a)
	ViewProviderLine(a.ViewObject)
	App.ActiveDocument.recompute()


if __name__ == "__main__":
	print ("Hola!")
	#barrientos_pag79_ex3_1()
	#test_line()
	#a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Generic")
	#Generic(a)
	#ViewProviderGeneric(a.ViewObject)
	#App.ActiveDocument.recompute()

#---- Doc
# http://www.freecadweb.org/wiki/index.php?title=Scripted_objects
