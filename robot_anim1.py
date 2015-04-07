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
from PySide import QtCore
import serial
import glob

from pyooml import frame, svector, cube, cylinder, link, sphere
from FreeCAD import Vector

class robot(object):
	"""Simple robot example"""
	def __init__(self, a1, a2):
		"""Robot constructor"""
		#-- Store the robot angles
		self.a1 = a1
		self.a2 = a2
		
		#-- Create the robot parts
		self.f0 = frame()
		self.f1 = frame()
		self.f2 = frame()
		self.l1 = link(l = 40, w = 6, D = 10).ice(80)
		self.l2 = self.l1.copy()
		self.l2.w = 4
		self.base = sphere(r = 14, angle1 = 0).translate(0, 0, -6).ice(80)
		self.f1_r = svector(self.l1.l, 0., 0.).color("yellow")
		self.f2_r = svector(self.l2.l, 0., 0.).color("yellow")		

		#-- Write labels
		self.f0.label = "Frame-0"
		self.f1.label = "Frame-1"
		self.f2.label = "Frame-2"
		self.l1.label = "Link-1"
		self.l2.label = "Link-2"
		self.base.label = "Base"
		
		#-- Recalculate robot
		self.recalculate()
		
	
	def recalculate(self):
		M1_1 = HMatrix.Roty(self.a1)
		M1_2 = HMatrix.Translation(self.l1.l, 0, 0)
		M2_1 = HMatrix.Roty(self.a2)
		M2_2 = HMatrix.Translation(self.l2.l, 0, 0)
		self.l1.T = M1_1
		self.f1.T = self.l1.T * M1_2
		self.l2.T = self.f1.T * M2_1
		self.f2.T = self.l2.T * M2_2
		
		#-- Frame position vectors
		self.f1_r.T = self.l1.T
		self.f2_r.T = self.l2.T
	
	def pose(self, a1, a2):
		"""Define the robot pose"""
		self.a1 = a1
		self.a2 = a2
		self.recalculate()
	
	def serial_on(self):
		#-- Open serial port
		port="/dev/ttyUSB0"
		self.sp = serial.Serial(port,19200, timeout = 0.2)
		
		#-- Lauch timer
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.update)
		self.timer.start(50)
		print("Launched!")
	
	def serial_off(self):
		self.timer.stop()
	
	def update(self):
		self.sp.write('\n')
		angle = 90 - (90. * float(self.sp.readline()) / 1023.)
		self.a1 = -angle
		self.recalculate()
		print("Angle: {}".format(angle))
	

if __name__ == "__main__":
	r = robot(-60, 70)


    