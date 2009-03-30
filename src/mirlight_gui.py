#!/usr/bin/env python
# -*- coding: utf-8 -*-
#mirlight ver. 0.25 by grizz - Witek Firlej http://grizz.pl

__author__    = "Witold Firlej (http://grizz.pl)"
__version__   = "0.25"
__license__   = "GPLv2"
__copyright__ = "Witold Firlej"

import sys, ConfigParser, serial, time
from PyQt4 import QtCore, QtGui

from mirlight_form import Ui_MainWindow

config = ConfigParser.ConfigParser() 								##TODO create config automatically
config.read("mirlight.conf")

ser = serial.Serial(config.getint('Port', 'number'), 9600, timeout=0) ##TODO maybe not int, but string /dev/ttyS01 ?
print ser.portstr       # check which port was really used ##XXX debug purposes


class MyForm(QtGui.QMainWindow):
	
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self._Timer = QtCore.QTimer(self)
		self.connect(self._Timer, QtCore.SIGNAL('timeout()'), self.timer)
		QtCore.QObject.connect(self.ui.pushButton,QtCore.SIGNAL("clicked()"), self.startStop)
	
	def startStop(self): 											
		"""
		start/stop Timer and change text on Button
		"""
		if not self._Timer.isActive(): 							# if timer doesn't work
			self.ui.pushButton.setText("Stop!")
			self._Timer.start(config.getint('Timer', 'interval'))
		else:
			self._Timer.stop()
			self.ui.pushButton.setText("Start!")

	def getColor(self, px, py, w, h ):
		"""
		Grab specific field and resize it to receive average color of field
		
		@return a color value
		"""
		self.originalPixmap = QtGui.QPixmap.grabWindow(QtGui.QApplication.desktop().winId(), px, py, w, h)
		self.destPixmap = self.originalPixmap.scaled(1, 1, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
		self.destImage = self.destPixmap.toImage()
		value = self.destImage.pixel(0,0)
		return value

	def timer(self):
		"""
		getColor for every field and display it on appropriate label
		"""
			##TODO get it screen resolution independent. Now it's configured for 1920*1200
			##TODO function to set label color and text - split, move, replace label with field
		for field, label, x, y, w, h in [(1, self.ui.label, 0, 600, 30, 600), 		\
									(2, self.ui.label_2, 0, 0, 30, 600), 	\
									(3, self.ui.label_3, 0, 0, 640, 30), 		\
									(4, self.ui.label_4, 640, 0, 640, 30), 	\
									(5, self.ui.label_5, 1280, 0, 640, 30), 	\
									(6, self.ui.label_6, 1890, 0, 30, 600),	\
									(7, self.ui.label_7, 1890, 600, 30, 600),	\
									(8, self.ui.label_8, 550, 1170, 820, 30)]:
			color = self.getColor(x, y, w, h)
			self.sendColor(field, color)
			rgb = str(QtGui.qRed(color)) + ", " + str(QtGui.qGreen(color)) + ", " + str(QtGui.qBlue(color)) 	##TODO move it to standalone function
			label.setText(str(rgb))
			palette = QtGui.QPalette(label.palette())
			palette.setColor(QtGui.QPalette.Window, QtGui.QColor(color))
			label.setPalette(palette)

	def sendColor(self, field, color):
		"""
		send field and color value to port
		"""
		#if ser.isOpen(): ##XXX needed?
		red = QtGui.qRed(color)
		green = QtGui.qGreen(color)
		blue = QtGui.qBlue(color)
		value = 16*field + red*10/256+1
		ser.write(chr(value))
		value = 16*(green*10/256+1)+(blue*10/256+1)
		ser.write(chr(value))
		time.sleep(0.001)

#	def updateLabel (self, label, color): ##TODO move here instructions from timer()
#		"""
#		change label color, and text
#		"""





if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	myapp = MyForm()
	myapp.show()
	sys.exit(app.exec_())
#	ser.close()             # close port ##XXX here?


