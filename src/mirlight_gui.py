#!/usr/bin/env python
# -*- coding: utf-8 -*-
#mirlight by grizz - Witek Firlej http://grizz.pl
# Copyright (C) 2009-2010 Witold Firlej
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>

__author__    = "Witold Firlej (http://grizz.pl)"
__project__      = "mirlight"
__version__   = "d.2010.03.09.2"
__license__   = "GPL"
__copyright__ = "Witold Firlej"

import sys, ConfigParser, serial, time, os, glob
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QWidget, QApplication, QCursor, QInputDialog
from PyQt4.QtCore import Qt, QPoint

from mirlight_form import Ui_MainWindow

class MyForm(QtGui.QMainWindow):
	
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self._Timer = QtCore.QTimer(self)
		self._watchTimer = QtCore.QTimer(self)
		self.connect(self._Timer, QtCore.SIGNAL('timeout()'), self.timer)
		self.connect(self._watchTimer, QtCore.SIGNAL('timeout()'), self.watch)
		QtCore.QObject.connect(self.ui.pushButton,QtCore.SIGNAL("clicked()"), self.startStop)
		QtCore.QObject.connect(self.ui.showFieldsPushButton,QtCore.SIGNAL("clicked()"), self.showFields)
		QtCore.QObject.connect(self.ui.buttonBox,QtCore.SIGNAL("accepted()"), self.saveConfiguration)
		QtCore.QObject.connect(self.ui.buttonBox,QtCore.SIGNAL("rejected()"), self.loadConfiguration)
		QtCore.QObject.connect(self.ui.AutoArrangeCheckBox,QtCore.SIGNAL("clicked()"), self.changePresetsComboBoxEnabled)

		self.setWindowTitle(__project__ + " ver. " + __version__ + " by " + __author__)

		self.ui.AboutVersionLabel.setText("ver. " + __version__)

		self.labels = [self.ui.label, self.ui.label_2, self.ui.label_3, self.ui.label_4, self.ui.label_5, self.ui.label_6, self.ui.label_7, self.ui.label_8]	# fieldlabels
		self.fieldsWidgets = []
		self.blackout = [0,0,0,0,0,0,0,0]


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
			self.sendColors(self.blackout)

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
		colors = []
		for field, x, y, w, h in [(1, fieldsconfig.getint('1', 'x'), fieldsconfig.getint('1', 'y'), fieldsconfig.getint('1', 'w'), fieldsconfig.getint('1', 'h')),
									(2, fieldsconfig.getint('2', 'x'), fieldsconfig.getint('2', 'y'), fieldsconfig.getint('2', 'w'), fieldsconfig.getint('2', 'h')),
									(3, fieldsconfig.getint('3', 'x'), fieldsconfig.getint('3', 'y'), fieldsconfig.getint('3', 'w'), fieldsconfig.getint('3', 'h')),
									(4, fieldsconfig.getint('4', 'x'), fieldsconfig.getint('4', 'y'), fieldsconfig.getint('4', 'w'), fieldsconfig.getint('4', 'h')),
									(5, fieldsconfig.getint('5', 'x'), fieldsconfig.getint('5', 'y'), fieldsconfig.getint('5', 'w'), fieldsconfig.getint('5', 'h')),
									(6, fieldsconfig.getint('6', 'x'), fieldsconfig.getint('6', 'y'), fieldsconfig.getint('6', 'w'), fieldsconfig.getint('6', 'h')),
									(7, fieldsconfig.getint('7', 'x'), fieldsconfig.getint('7', 'y'), fieldsconfig.getint('7', 'w'), fieldsconfig.getint('7', 'h')),
									(8, fieldsconfig.getint('8', 'x'), fieldsconfig.getint('8', 'y'), fieldsconfig.getint('8', 'w'), fieldsconfig.getint('8', 'h'))]:
			color = self.getColor(x, y, w, h)
			colors.append(color)
			self.updateLabel(field, x, y, w, h, color)
		self.sendColors(colors)
		

	def addSum(self, value):
		global sum
		sum += value ##???
		if sum > 255:
			sum -=256


	def sendColors(self, colors):
		kod = chr(128) #kod inicjujacy poczatek standardowej paczki + konfig
		global sum
		sum = 0
		self.addSum(128) #suma kontrolna tj. suma wszystkich wartosci, skrocona do 7 bitow (bajt podzielony przez dwa)
		for color in colors:
			red = float(QtGui.qRed(color))/255
			green = float(QtGui.qGreen(color))/255
			blue = float(QtGui.qBlue(color))/255
			verbose("k: %d" % (colors.index(color)+1), 3)
			verbose("\trgb: %f, %f, %f" % (red, green, blue), 3)
			red = int(red*red*100)
			green = int(green*green*100)
			blue = int(blue*blue*100)
			verbose("\t\trgb: %f, %f, %f" % (red, green, blue), 3)
			kod += chr(red)
			kod += chr(green) 
			kod += chr(blue)
			self.addSum(red)
			self.addSum(green)
			self.addSum(blue)
		kod += chr(sum/2)
		try:
			ser.write(kod)
		except:
			verbose("--\nCannot send to device. Check your configuration!",1)
		time.sleep(0.009) # hack needed by hardware

	def watch(self):
		"""
		Get remote code and perform an action
		"""
		try: 
			temp=ser.read()
			ser.flushInput()
			x=ord(temp)
			command = "echo \'not bind\'" ##XXX debug
			if x == 14: command='smplayer -send-action pause'#works as pause/play
			if x == 59: command='smplayer -send-action pause'#works as pause/play
			if x == 10: command='smplayer -send-action stop'
			if x == 0: command='smplayer -send-action play'
			if x == 16: command='smplayer -send-action increase_volume'
			if x == 17: command='smplayer -send-action decrease_volume'
			if x == 13: command='smplayer -send-action mute' #mute/unmute
			if x == 5: command='smplayer -send-action dec_sub_scale' #decrease subtitles
			if x == 8: command='smplayer -send-action inc_sub_scale' #increase subtitles
			if x == 7: command='smplayer -send-action rewind1' #small jump
			if x == 9: command='smplayer -send-action forward1'
			if x == 4: command='smplayer -send-action rewind2' #medium jump
			if x == 6: command='smplayer -send-action forward2'
			if x == 1: command='smplayer -send-action rewind3'#large jump
			if x == 3: command='smplayer -send-action forward3'
			verbose("%s:\t%s" % (x, command), 2)
			os.system(command)
		except:
			verbose("no remote command", 2)



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


		if  self.ui.showFieldsPushButton.isChecked():
			if (config.get("Fields", "autoarrange") == "on" and self.ui.AutoArrangeCheckBox.checkState() != 2) or (config.get("Fields", "autoarrange") == "off" and self.ui.AutoArrangeCheckBox.checkState() != 0) or (config.getint("Fields", "size") != self.ui.AutoarrangeHorizontalSlider.value()): ###XXX ugly hack
				SAVE = "Save"
				CANCEL = "Cancel"
				message = QtGui.QMessageBox(self)
				message.setText('Save changes before?')
				message.setWindowTitle('Mirlight')
				message.setIcon(QtGui.QMessageBox.Question)
				message.addButton(SAVE, QtGui.QMessageBox.AcceptRole)
				message.addButton(CANCEL, QtGui.QMessageBox.RejectRole)
				message.exec_()
				response = message.clickedButton().text()
				if response == SAVE:
					self.saveConfiguration()
				else:
					self.loadConfiguration()

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
			self.ui.showFieldsPushButton.setText("Hide fields")
			self.ui.AutoArrangeCheckBox.setEnabled(0)
			self.ui.AutoarrangeHorizontalSlider.setEnabled(0)

		elif config.get("Fields", "autoarrange") == "off":
			SAVE = "Save"
			CANCEL = "Cancel"
			presets = ""
			for infile in glob.glob("presets/*.mrl"):
				presets += infile[8:-4] + ", "
			print presets
			(presetName, state) = QtGui.QInputDialog.getText(self, "Mirlight", "Existed names: %s\nEnter a new name (or an old one to overwrite):" % presets, QtGui.QLineEdit.Normal, "preset-")
			if state == True and len(presetName) > 0:
				self.saveFields(presetName)
				verbose("--\nSaved as: %s.mrl" % presetName,1)
			else:
				verbose("--\nPreset not saved",1)
			self.closeFields()
		else:
			self.closeFields()

	def closeFields(self):
		"""
		hide fields preview
		"""
		for widget in self.fieldsWidgets:
			widget.close()
		self.ui.showFieldsPushButton.setText("Show and set fields")

		self.ui.AutoArrangeCheckBox.setEnabled(1)
		self.ui.AutoarrangeHorizontalSlider.setEnabled(1)


	def saveFields(self, name):
		"""
		save fields to conf file
		"""
		for field, widget in zip([1,2,3,4,5,6,7,8], self.fieldsWidgets):
			if not fieldsconfig.has_section(`field`): 			# if there is no section FIELD, create one
				fieldsconfig.add_section(`field`)
			x, y, w, h = widget.getGeometry()
			verbose("Field: %d\tx: %d\ty: %d\tw: %d\th: %d" % (field,x,y,w,h), 1)
			fieldsconfig.set(`field`, "x", x)
			fieldsconfig.set(`field`, "y", y)
			fieldsconfig.set(`field`, "w", w)
			fieldsconfig.set(`field`, "h", h)
		with open('presets/%s.mrl' % name, 'wb') as configfile:
			fieldsconfig.write(configfile)

		config.set("Fields", "preset", name)
		with open('mirlight.conf', 'wb') as configfile:
			config.write(configfile)

		self.loadConfiguration() ##XXX it's bad here! reThink that.


	def listAviablePresets(self):
		"""
		list presets aviable in presets folder
		"""

	def loadPreset(self, preset):
		"""
		load fields preset from file
		"""

	def saveConfiguration(self):
		"""
		save configuration to mirlight.conf file
		"""
		config.set("Timer", "interval", self.ui.TimerHorizontalSlider.value())
		config.set("Port", "number", self.ui.portNumberLineEdit.text())
		if self.ui.AutoArrangeCheckBox.isChecked():
			config.set("Fields", "autoarrange", "on")
		else:
			config.set("Fields", "autoarrange", "off")
		config.set("Fields", "size", self.ui.AutoarrangeHorizontalSlider.value())
		config.set("Fields", "preset", self.ui.PresetsComboBox.currentText())
		with open('mirlight.conf', 'wb') as configfile:
				config.write(configfile)

		self.loadConfiguration() 						# reload after saving


	def loadConfiguration(self):
		"""
		load configuration from mirlight.conf
		"""
		self.checkFiles()
		config.read("mirlight.conf")
		if config.get("Fields", "autoarrange") == "on":
			self.autoArrangeFields()
			fieldsconfig.read("presets/autoarrange.mrl")
		else:
			name = config.get("Fields", "preset", "default")
			fieldsconfig.read("presets/%s.mrl" % name)
			verbose("--\nLoading >>> %s <<< preset" % name, 1)
			verbose("--\nAutoarrange is off", 1)
		try:
			global ser 									##XXX uhh a nasty code...
			port = config.get('Port', 'number')
			if port.isdigit():
				port = int(port)
			ser = serial.Serial(port, 38400, timeout=0)
			verbose("--\nSelected port: %s" % ser.portstr, 1)       # check which port was really used 
		except:
			verbose("--\nError:\tUnable to open port\nCheck your port (com (ttyS)) configuration!", 1)
		
		self._watchTimer.start(300)
		self.ui.portNumberLineEdit.setText(config.get("Port", "number"))
		timerInterval = config.getint("Timer", "interval")
		self.ui.TimerHorizontalSlider.setValue(timerInterval)
		verbose("--\nScan Interval: %d" % timerInterval, 1)
		self.ui.TimerValueLabel.setText(str(timerInterval))
		if config.get("Fields", "autoarrange") == "on":
			self.ui.AutoArrangeCheckBox.setCheckState(2) 				# no "1" that is for no-change
		else:
			self.ui.AutoArrangeCheckBox.setCheckState(0)
		self.changePresetsComboBoxEnabled()
		self.ui.AutoarrangeHorizontalSlider.setValue(config.getint("Fields", "size"))

	def changePresetsComboBoxEnabled(self):
		if self.ui.AutoArrangeCheckBox.checkState() == 2:
			self.ui.PresetsComboBox.setEnabled(0)
			self.ui.AutoarrangeHorizontalSlider.setEnabled(1)
		else:
			self.ui.PresetsComboBox.clear()
			for infile in glob.glob("presets/*.mrl"):
				name = infile[8:-4] 		#cut "presets/" and ".mrl"
				self.ui.PresetsComboBox.addItem(name)
			self.ui.PresetsComboBox.setCurrentIndex(self.ui.PresetsComboBox.findText(config.get("Fields", "preset"))) 	### XXX write what to do on ERRORs !
			self.ui.PresetsComboBox.setEnabled(1)
			self.ui.AutoarrangeHorizontalSlider.setEnabled(0)

	def checkFiles(self):
		"""
		Check if basic conf file exists. If not, create them.
		"""
		if not os.path.exists('mirlight.conf'):
			verbose("Creating mirlight.conf file", 1)
			config.add_section("Fields")
			config.add_section("Timer")
			config.add_section("Port")
			config.set("Fields", "autoarrange", "on")
			config.set("Fields", "size", 5)
			config.set("Timer", "interval", 100)
			config.set("Port", "number", "1")
			with open('mirlight.conf', 'wb') as configfile:
				config.write(configfile)

		if not os.path.exists('presets/'):
			os.mkdir('presets')

		#if not os.path.exists('presets/autoarrange.mrl'): # not need, as autoarrange is set by default in case of the lack of confings
			# ...
		

	def closeEvent(self, closeEvent):
		"""
		blackout and clean screan on close
		"""
		self.startStop() 			# stoping timer prevent from restart lights after blackout
		self.closeFields()
		self.sendColors(self.blackout)

	def autoArrangeFields(self):
		"""
		Auto arrange fields depends on screen resolution and "size" factor from conf file
		"""
		screen = QtGui.QDesktopWidget().screenGeometry()
		sw = screen.width()
		sh = screen.height()
		factor = config.getint("Fields", "size")
		if factor > 10: 										# factor can be between 1 and 10
			factor = 10
		elif factor < 1:
			factor = 1

		verticalWidth = (sw/100)*factor
		verticalHeight = sh/2
		horizontalWidth = sw/3
		horizontalHeight = (sh/100)*factor
		verbose("--\nAuto arranging...", 1)
		verbose("Size factor: \t\t%d" % factor, 1)
		verbose("vertical width: \t%d" % verticalWidth, 1)
		verbose("vertical height: \t%d" % verticalHeight, 1)
		verbose("horizontal width: \t%d" % horizontalWidth, 1)
		verbose("horizontal height: \t%d" % horizontalHeight, 1)


		def writeToConfing(field, x, y, w, h):
			if not fieldsconfig.has_section(`field`): 			# if there is no section FIELD, create one
				fieldsconfig.add_section(`field`)
			fieldsconfig.set(`field`, "x", x)
			fieldsconfig.set(`field`, "y", y)
			fieldsconfig.set(`field`, "w", w)
			fieldsconfig.set(`field`, "h", h)
			with open('presets/autoarrange.mrl', 'wb') as configfile:
				fieldsconfig.write(configfile)

		for field, x, y, w, h in [(1, 0, sh/2, verticalWidth, verticalHeight),\
									(2, 0, 0, verticalWidth, verticalHeight),\
									(3, 0, 0, sw/3, horizontalHeight),\
									(4, sw/3, 0, sw/3, horizontalHeight),\
									(5, (sw/3)*2, 0, sw/3, horizontalHeight),\
									(6, sw-verticalWidth, 0, verticalWidth, verticalHeight),\
									(7, sw-verticalWidth, sh/2, verticalWidth, verticalHeight),\
									(8, sw/4, sh-horizontalHeight, sw/2, horizontalHeight)]:
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
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		
		self.button = QtGui.QPushButton('', self)
		self.button.setGeometry(0, 0, 30, 30)
		self.button.setText(str(field))
		self.button.setFocusPolicy(QtCore.Qt.NoFocus)

		self.label = QtGui.QLabel('Dialog', self)
		self.label.setText("Saved position: " + str(x) + ", " + str(y) + ", " + str(w) + ", " + str(h))
		self.label.move(35, 8)
		self.setToolTip("Click and hold left mouse button to move field \nClick and hold right mouse button to resize field")


		QtCore.QObject.connect(self.button,QtCore.SIGNAL("pressed()"), self.showPos)

	def mousePressEvent(self, event): # moving - thx to salmon http://forum.python.org.pl/index.php?topic=846.msg4359#msg4359
		self.last_pos = QCursor.pos()

	def mouseMoveEvent(self, event):
		buttons = event.buttons()
		new_pos = QCursor.pos()
		offset = new_pos - self.last_pos
		if buttons & Qt.LeftButton:
			self.move(self.pos() + offset)
			self.update()
		elif buttons & Qt.RightButton:
			size = self.size()
			self.resize(size.width() + offset.x(), size.height() + offset.y())
			self.update()
		self.last_pos = QPoint(new_pos)
	
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

def verbose (msg, level):
	try:
		for item in sys.argv:
			if item == "-v" and level == 1:
				print msg
				break
			elif item == "-vv" and level <= 2:
				print msg
				break
			elif item == "-vvv" and level <= 3:
				print msg
				break
	except IndexError:
		pass


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	myapp = MyForm()
	myapp.show()
	config = ConfigParser.ConfigParser()
	fieldsconfig = ConfigParser.ConfigParser()
	ser = "ziaaaf" 														# just an initialization
	sum = 0 															# just an initialization
	verbose("\n\t%s \n\tversion %s \n\tby %s\n" % (__project__, __version__, __author__),1)
	myapp.loadConfiguration()
	sys.exit(app.exec_())
#	ser.close()             # close port ##XXX here?
