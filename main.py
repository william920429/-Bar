from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from Ui.Ui_MainWindow import *
from stars import _stars
from roll import _roll###################
import os, sys, random, math

class MainWindow(QtWidgets.QMainWindow):
	def __init__(self, app, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.app = app

		self.cat_mp3 = QMediaPlayer()
		self.cat_mp3.setMedia(QMediaContent(QtCore.QUrl.fromLocalFile("mp3/NyanCat.mp3")))
		self.cat_mp3.setVolume(100)
		self.cat_mp3.play()

		self.FPS = 60
		self.log = self.ui.log_listWidget

		self.default_prize = 100
		self.ui.prize_num_label.setText(str(self.default_prize))
		
		self.stars = _stars(self, 200, "pic/meow.png")
		self.roll = _roll(self)

		self.ui.log_clear_btn.hide()
		
		self.event_init()
		self.main()

	def prize(self, win = False):
		num = int(self.ui.prize_num_label.text())
		if win:
			self.ui.prize_num_label.setText(str(self.default_prize))
			self.log.addItem("您獲得了 {} 元".format(num))
		else:
			self.ui.prize_num_label.setText(str(num + 10))
		pass
	
	def event_init(self):
		self.ui.pull_btn.clicked.connect(self.event_handle)
		self.installEventFilter(self)
		pass

	def eventFilter(self, obj, event):
		# print(event.type())
		if obj is self and ( event.type() == QtCore.QEvent.KeyPress or event.type() == QtCore.QEvent.KeyRelease ):
			# print(event)
			if event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter, QtCore.Qt.Key_Space):
				self.event_handle()
				return True
		return super().eventFilter(obj, event)

	def keyPressEvent(self, keyEvent):
		self.event_handle()
		# print(keyEvent)
		pass

	def event_handle(self):
		#sender = self.sender()
		#if sender is self.ui.pull_btn or sender is self:
		self.roll.start()
		# self.cat_mp3.play()

		pass	

	def main(self):
		
		pass

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	mainWindow = MainWindow(app)
	mainWindow.show()
	sys.exit(app.exec_())
