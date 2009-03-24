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

config = ConfigParser.ConfigParser()
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
	
	def setColor(self):
		if self.state == 1:
			self.ui.label.setText("Bum") ##XXX testing purposes only
			self.ui.pushButton.setText("Stop!")
			self.state = 2 ##XXX ugly hack
			self._Timer.start(config.getint('Timer', 'interval'))
		else:
			self._Timer.stop()
			self.ui.pushButton.setText("Start!")
			self.state = 1 ##XXX ugly hack

	def timer(self):
		self.originalPixmap = QtGui.QPixmap.grabWindow(QtGui.QApplication.desktop().winId(), 100, 100, 1, 1)
		self.ui.label.setPixmap(self.originalPixmap.scaled(self.ui.label.size()))
		
		self.originalPixmap = QtGui.QPixmap.grabWindow(QtGui.QApplication.desktop().winId(), 1111, 100, 1, 1)
		self.ui.label_2.setPixmap(self.originalPixmap.scaled(self.ui.label.size()))
		
		self.originalPixmap = QtGui.QPixmap.grabWindow(QtGui.QApplication.desktop().winId(), 566, 848, 1, 1)
		self.ui.label_3.setPixmap(self.originalPixmap.scaled(self.ui.label.size()))
		
		self.originalPixmap = QtGui.QPixmap.grabWindow(QtGui.QApplication.desktop().winId(), 999, 664, 1, 1)
		self.ui.label_4.setPixmap(self.originalPixmap.scaled(self.ui.label.size()))
		
		self.originalPixmap = QtGui.QPixmap.grabWindow(QtGui.QApplication.desktop().winId(), 122, 15, 1, 1)
		self.ui.label_5.setPixmap(self.originalPixmap.scaled(self.ui.label.size()))
		
		self.originalPixmap = QtGui.QPixmap.grabWindow(QtGui.QApplication.desktop().winId(), 11, 1111, 1, 1)
		self.ui.label_6.setPixmap(self.originalPixmap.scaled(self.ui.label.size()))

		self.originalPixmap = QtGui.QPixmap.grabWindow(QtGui.QApplication.desktop().winId(), 122, 100, 1, 1)
		self.ui.label_7.setPixmap(self.originalPixmap.scaled(self.ui.label.size()))

		self.originalPixmap = QtGui.QPixmap.grabWindow(QtGui.QApplication.desktop().winId(), 887, 100, 1, 1)
		self.ui.label_8.setPixmap(self.originalPixmap.scaled(self.ui.label.size()))

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	myapp = MyForm()
	myapp.show()
	sys.exit(app.exec_())


