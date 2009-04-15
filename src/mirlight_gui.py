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

		self.labels = [self.ui.label, self.ui.label_2, self.ui.label_3, self.ui.label_4, self.ui.label_5, self.ui.label_6, self.ui.label_7, self.ui.label_8]	# fieldlabels
		self.fieldsWidgets = []

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
		for field, x, y, w, h in [(1, fieldsconfig.getint('1', 'x'), fieldsconfig.getint('1', 'y'), fieldsconfig.getint('1', 'w'), fieldsconfig.getint('1', 'h')),
									(2, fieldsconfig.getint('2', 'x'), fieldsconfig.getint('2', 'y'), fieldsconfig.getint('2', 'w'), fieldsconfig.getint('2', 'h')),
									(3, fieldsconfig.getint('3', 'x'), fieldsconfig.getint('3', 'y'), fieldsconfig.getint('3', 'w'), fieldsconfig.getint('3', 'h')),
									(4, fieldsconfig.getint('4', 'x'), fieldsconfig.getint('4', 'y'), fieldsconfig.getint('4', 'w'), fieldsconfig.getint('4', 'h')),
									(5, fieldsconfig.getint('5', 'x'), fieldsconfig.getint('5', 'y'), fieldsconfig.getint('5', 'w'), fieldsconfig.getint('5', 'h')),
									(6, fieldsconfig.getint('6', 'x'), fieldsconfig.getint('6', 'y'), fieldsconfig.getint('6', 'w'), fieldsconfig.getint('6', 'h')),
									(7, fieldsconfig.getint('7', 'x'), fieldsconfig.getint('7', 'y'), fieldsconfig.getint('7', 'w'), fieldsconfig.getint('7', 'h')),
									(8, fieldsconfig.getint('8', 'x'), fieldsconfig.getint('8', 'y'), fieldsconfig.getint('8', 'w'), fieldsconfig.getint('8', 'h'))]:
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
		return self.labels[field-1]

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
		self.fieldsWidgets = [] ## clear to avoid multiple instances
		self.widget1 = FieldDialog(1)
		self.fieldsWidgets.append(self.widget1)
		self.widget2 = FieldDialog(2)
		self.fieldsWidgets.append(self.widget2)
		self.widget3 = FieldDialog(3)
		self.fieldsWidgets.append(self.widget3)
		self.widget4 = FieldDialog(4)
		self.fieldsWidgets.append(self.widget4)
		self.widget5 = FieldDialog(5)
		self.fieldsWidgets.append(self.widget5)
		self.widget6 = FieldDialog(6)
		self.fieldsWidgets.append(self.widget6)
		self.widget7 = FieldDialog(7)
		self.fieldsWidgets.append(self.widget7)
		self.widget8 = FieldDialog(8)
		self.fieldsWidgets.append(self.widget8)

		for widget in self.fieldsWidgets:
			widget.show()


	def saveFields(self):
		"""
		save fields to conf file
		"""

	def closeEvent(self, closeEvent):
		for widget in self.fieldsWidgets:
			widget.close()


	def autoArrangeFields(self):
		"""
		Auto arrange fields depends on screen resolution and "size" factor from conf file
		"""
		screen = QtGui.QDesktopWidget().screenGeometry()
		sw = screen.width()
		sh = screen.height()
		factor = config.getint("Fields", "size")

		verticalWidth = (sw/100)*factor
		verticalHeight = sh/2
		horizontalWidth = sw/3
		horizontalHeight = (sh/100)*factor

		def writeToConfing(field, x, y, w, h):
			if not fieldsconfig.has_section(`field`): 			# if there is no section FIELD, create one
				fieldsconfig.add_section(`field`)
			fieldsconfig.set(`field`, "x", x)
			fieldsconfig.set(`field`, "y", y)
			fieldsconfig.set(`field`, "w", w)
			fieldsconfig.set(`field`, "h", h)
			with open('presets/autoarrange.mrl', 'wb') as configfile:
				fieldsconfig.write(configfile)

		###TODO do this like in timer()
		for field, x, y, w, h in [(1, 0, sh/2, verticalWidth, verticalHeight),\
									(2, 0, 0, verticalWidth, verticalHeight),\
									(3, 0, 0, sw/3, horizontalHeight),\
									(4, sw/3, 0, sw/3, horizontalHeight),\
									(5, (sw/3)*2, 0, sw/3, horizontalHeight),\
									(6, sw-verticalWidth, 0, verticalWidth, verticalWidth),\
									(7, sw-verticalWidth, sh/2, verticalWidth, verticalHeight),\
									(8, sw-sw/3, sh-horizontalHeight, sw/3, horizontalHeight)]:
			writeToConfing(field, x, y, w, h)

class FieldDialog(QtGui.QWidget):
	def __init__(self, field, parent=None):
		QtGui.QWidget.__init__(self, parent)
		x = fieldsconfig.getint(str(field), 'x')
		y = fieldsconfig.getint(str(field), 'y')
		w = fieldsconfig.getint(str(field), 'w')
		h = fieldsconfig.getint(str(field), 'h')
		self.setGeometry(x, y, w, h)
#		self.setMinimumSize (30, 30)						##XXX do it?
		self.setWindowTitle('Field: ' + str(field))
		
		self.button = QtGui.QPushButton('', self)
		self.button.setGeometry(0, 0, 30, 30)
		self.button.setText(str(field))
		self.button.setFocusPolicy(QtCore.Qt.NoFocus)

		self.label = QtGui.QLabel('Dialog', self)
		self.label.setText("Saved position: " + str(x) + ", " + str(y) + ", " + str(w) + ", " + str(h))
		self.label.move(35, 8)


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

	config = ConfigParser.ConfigParser() 								##TODO create config automatically
	config.read("mirlight.conf")
	fieldsconfig = ConfigParser.ConfigParser()
	if config.get("Fields", "autoarrange") == "on":
		print "Autoarrange fields" ##XXX debug purposes
		myapp.autoArrangeFields()
		fieldsconfig.read("presets/autoarrange.mrl")
	else:
		fieldsconfig.read("presets/default.mrl")
		print "Loading default fields' preset" ##XXX debug purposes

	try:
		ser = serial.Serial(config.getint('Port', 'number'), 9600, timeout=0) ##TODO maybe not int, but string /dev/ttyS01 ?
		print ser.portstr       # check which port was really used ##XXX debug purposes
	except:
		print "Error:\tUnable to open port\nCheck your port (com (ttyS)) configuration!"


	sys.exit(app.exec_())
#	ser.close()             # close port ##XXX here?
