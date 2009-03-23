# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtCore, QtGui

from mirlight_form import Ui_MainWindow

class MyForm(QtGui.QMainWindow):
	state = 1 #1 - waiting for action 2- working
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self._Timer = QtCore.QTimer(self)
		self.connect(self._Timer, QtCore.SIGNAL('timeout()'), self.timer)
		QtCore.QObject.connect(self.ui.pushButton,QtCore.SIGNAL("clicked()"), self.setColor)
	
	def setColor(self):
		if self.state == 1:
			self.ui.label.setText("Bum")
			self.ui.pushButton.setText("Stop!")
			self.state = 2
			self._Timer.start(100)
		else:
			self._Timer.stop()
			self.ui.pushButton.setText("Start!")
			self.state = 1

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


