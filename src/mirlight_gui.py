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

config = ConfigParser.ConfigParser() 								##TODO create config automatically
config.read("mirlight.conf")


class MyForm(QtGui.QMainWindow):
	
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self._Timer = QtCore.QTimer(self)
		self.connect(self._Timer, QtCore.SIGNAL('timeout()'), self.timer)
		QtCore.QObject.connect(self.ui.pushButton,QtCore.SIGNAL("clicked()"), self.startStop)
	
	def startStop(self): 											##XXX rename this function!
		"""
		start/stop Timer and change text on Button
		"""
		if self._Timer.isActive() == 0: 							# if timer doesn't work
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
		self.destPixmap = self.originalPixmap.scaled(1, 1)
		self.destImage = self.originalPixmap.toImage()
		value = self.destImage.pixel(1,1)
		return value

	def timer(self):
		"""
		getColor for every field and display it on appropriate label
		"""
			##TODO get it screen resolution independent. Now it's configured for 1920*1200
			##TODO function to set label color and text - almost DONE!
		for label, x, y, w, h in [(self.ui.label, 1, 700, 300, 500), 		\
									(self.ui.label_2, 1, 200, 300, 500), 	\
									(self.ui.label_3, 1, 1, 640, 200), 		\
									(self.ui.label_4, 640, 1, 640, 200), 	\
									(self.ui.label_5, 1280, 1, 640, 200), 	\
									(self.ui.label_6, 1620, 200, 300, 300),	\
									(self.ui.label_7, 1620, 700, 300, 300),	\
									(self.ui.label_8, 300, 1080, 1320, 200)]:
			color = self.getColor(x, y, w, h)
			rgb = str(QtGui.qRed(color)) + ", " + str(QtGui.qGreen(color)) + ", " + str(QtGui.qBlue(color))
			label.setText(str(rgb))
			palette = QtGui.QPalette(label.palette())
			palette.setColor(QtGui.QPalette.Window, QtGui.QColor(color))
			label.setPalette(palette)


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	myapp = MyForm()
	myapp.show()
	sys.exit(app.exec_())


