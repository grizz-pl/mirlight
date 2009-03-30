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
		QtCore.QObject.connect(self.ui.showFieldsPushButton,QtCore.SIGNAL("clicked()"), self.showFields)
		QtCore.QObject.connect(self.ui.saveFieldsPushButton,QtCore.SIGNAL("clicked()"), self.saveFields)

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
		for field, x, y, w, h in [(1, config.getint('1', 'x'), config.getint('1', 'y'), config.getint('1', 'w'), config.getint('1', 'h')),
									(2, config.getint('2', 'x'), config.getint('2', 'y'), config.getint('2', 'w'), config.getint('2', 'h')),
									(3, config.getint('3', 'x'), config.getint('3', 'y'), config.getint('3', 'w'), config.getint('3', 'h')),
									(4, config.getint('4', 'x'), config.getint('4', 'y'), config.getint('4', 'w'), config.getint('4', 'h')),
									(5, config.getint('5', 'x'), config.getint('5', 'y'), config.getint('5', 'w'), config.getint('5', 'h')),
									(6, config.getint('6', 'x'), config.getint('6', 'y'), config.getint('6', 'w'), config.getint('6', 'h')),
									(7, config.getint('7', 'x'), config.getint('7', 'y'), config.getint('7', 'w'), config.getint('7', 'h')),
									(8, config.getint('8', 'x'), config.getint('8', 'y'), config.getint('8', 'w'), config.getint('8', 'h'))]:
			color = self.getColor(x, y, w, h)
			self.sendColor(field, color)
			self.updateLabel(field, x, y, w, h, color)

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
		time.sleep(0.001) ##hack needed by hardware


	def getLabel (self, field):
		"""
		@return label corresponding to field
		"""
		if field == 1: return self.ui.label
		if field == 2: return self.ui.label_2
		if field == 3: return self.ui.label_3
		if field == 4: return self.ui.label_4
		if field == 5: return self.ui.label_5
		if field == 6: return self.ui.label_6
		if field == 7: return self.ui.label_7
		if field == 8: return self.ui.label_8

	def updateLabel (self, field, x, y, w, h, color = 0): # default color is black
		"""
		set label text and color
		"""
		label = self.getLabel(field)
		label.setText(`x` + ", " + `y` + ", " + `w` + ", " + `h`)
		palette = QtGui.QPalette(label.palette())
		palette.setColor(QtGui.QPalette.Window, QtGui.QColor(color))
		label.setPalette(palette)


	def showFields(self):
		"""
		draw fields
		"""
		self.widget1 = FieldDialog(1)
		self.widget1.show()

	def saveFields(self):
		"""
		save fields to conf file
		"""
		x, y, w, h = self.widget1.getGeometry()
		self.ui.label.setText(str(x) + ", " + str(y) + ", " + str(w) + ", " + str(h))

class FieldDialog(QtGui.QWidget):
	def __init__(self, field, parent=None):
		QtGui.QWidget.__init__(self, parent)
		x = config.getint(str(field), 'x')
		y = config.getint(str(field), 'y')
		w = config.getint(str(field), 'w')
		h = config.getint(str(field), 'h')
		self.setGeometry(x, y, w, h)
		self.setWindowTitle('Field: ' + str(field))
		
		self.button = QtGui.QPushButton('', self)
		self.button.setFocusPolicy(QtCore.Qt.NoFocus)

		self.label = QtGui.QLabel('Dialog', self)
		self.label.setText("Saved position: " + str(x) + ", " + str(y) + ", " + str(w) + ", " + str(h))
		self.label.move(0, 50)


		QtCore.QObject.connect(self.button,QtCore.SIGNAL("pressed()"), self.showPos)
	
	def showPos(self):
		x, y, w, h = self.getGeometry()
		self.label.setText(str(x) + ", " + str(y) + ", " + str(w) + ", " + str(h))
	
	def getGeometry(self):
		"""
		get frame geometry
		@return x, y, w, h
		"""
		geometry = self.frameGeometry()
		x = geometry.x()
		y = geometry.y()
		w = geometry.width()
		h = geometry.height()
		return x, y, w, h



if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	myapp = MyForm()
	myapp.show()
	sys.exit(app.exec_())
#	ser.close()             # close port ##XXX here?


