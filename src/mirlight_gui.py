#!/usr/bin/env python
# -*- coding: utf-8 -*-
#mirlight ver. 0.01 by grizz - Witek Firlej http://grizz.pl

__author__    = "Witold Firlej (http://grizz.pl)"
__version__   = "0.01"
__license__   = "GPLv2"
__copyright__ = "Witold Firlej"

import sys, ConfigParser
from PyQt4 import QtCore, QtGui

from mirlight_form import Ui_MainWindow

config = ConfigParser.ConfigParser() ##TODO create config automatically
config.read("mirlight.conf")


class MyForm(QtGui.QMainWindow):
	state = 1 #1 - waiting for action 2- working ##XXX ugly hack
	
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self._Timer = QtCore.QTimer(self)
		self.connect(self._Timer, QtCore.SIGNAL('timeout()'), self.timer)
		QtCore.QObject.connect(self.ui.pushButton,QtCore.SIGNAL("clicked()"), self.setColor)
	
	def setColor(self): ##XXX rename this function!
		if self.state == 1:
			self.ui.label.setText("Bum") ##XXX testing purposes only
			self.ui.pushButton.setText("Stop!")
			self.state = 2 ##XXX ugly hack
			self._Timer.start(config.getint('Timer', 'interval'))
		else:
			self._Timer.stop()
			self.ui.pushButton.setText("Start!")
			self.state = 1 ##XXX ugly hack

	def getColor(self, px, py, w, h, step = 1):
		self.originalPixmap = QtGui.QPixmap.grabWindow(QtGui.QApplication.desktop().winId(), px, py, w, h)
		self.destPixmap = self.originalPixmap.scaled(1, 1)
		self.destImage = self.originalPixmap.toImage()
		value = self.destImage.pixel(1,1)
		return value

	def timer(self):
			##TODO get it screen resolution independent. Now it's configured for 1920*1200
			##TODO function to set label color and text
		color = self.getColor(1, 700, 300, 500) #1
		self.ui.label.setText(str(color))
		print color
		palette = QtGui.QPalette(self.ui.label.palette())
		palette.setColor(QtGui.QPalette.Window, QtGui.QColor(color))
		self.ui.label.setPalette(palette)

		color = self.getColor(1, 200, 300, 500) #2
		self.ui.label_2.setText(str(color))
		print color
		palette = QtGui.QPalette(self.ui.label_2.palette())
		palette.setColor(QtGui.QPalette.Window, QtGui.QColor(color))
		self.ui.label_2.setPalette(palette)

		color =  self.getColor(1, 1, 640, 200) #3
		self.ui.label_3.setText(str(color))
		print color
		palette = QtGui.QPalette(self.ui.label_3.palette())
		palette.setColor(QtGui.QPalette.Window, QtGui.QColor(color))
		self.ui.label_3.setPalette(palette)

		color =  self.getColor(640, 1, 640, 200) #4
		self.ui.label_4.setText(str(color))
		print color
		palette = QtGui.QPalette(self.ui.label_4.palette())
		palette.setColor(QtGui.QPalette.Window, QtGui.QColor(color))
		self.ui.label_4.setPalette(palette)

		color =  self.getColor(1280, 1, 640, 200) #5
		self.ui.label_5.setText(str(color))
		print color
		palette = QtGui.QPalette(self.ui.label_5.palette())
		palette.setColor(QtGui.QPalette.Window, QtGui.QColor(color))
		self.ui.label_5.setPalette(palette)

		color =  self.getColor(1620, 200, 300, 300) #6
		self.ui.label_6.setText(str(color))
		print color
		palette = QtGui.QPalette(self.ui.label_6.palette())
		palette.setColor(QtGui.QPalette.Window, QtGui.QColor(color))
		self.ui.label_6.setPalette(palette)

		color =  self.getColor(1620, 700, 300, 300) #7
		self.ui.label_7.setText(str(color))
		print color
		palette = QtGui.QPalette(self.ui.label_7.palette())
		palette.setColor(QtGui.QPalette.Window, QtGui.QColor(color))
		self.ui.label_7.setPalette(palette)

		color =  self.getColor(300, 1080, 1320, 200) #8
		self.ui.label_8.setText(str(color))
		print color
		palette = QtGui.QPalette(self.ui.label_8.palette())
		palette.setColor(QtGui.QPalette.Window, QtGui.QColor(color))
		self.ui.label_8.setPalette(palette)



if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	myapp = MyForm()
	myapp.show()
	sys.exit(app.exec_())


