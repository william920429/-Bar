from PyQt5 import QtCore, QtGui, QtWidgets
import math, random

class _stars():
	def __init__(self, mainWindow, total, pic):
		self.mainWindow = mainWindow
		self.ui = mainWindow.ui
		self.stars = set()
		self.stars_not_using = set()

		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.update)

		self.pic_init(total, pic)
		pass

	def boom(self):
		#self.stars, self.stars_not_using = self.stars_not_using, self.stars
		i = 0
		for star in self.stars:
			x, y, w, h = star.geometry().getRect()
			x = 170 + 230*(i % 3)
			if i >= 2:
				i = 0
			else:
				i += 1
			y = 380
			star.setGeometry(x, y, w, h)
			v = 7000/self.mainWindow.FPS*random.random()
			theta = 2*math.pi*random.random()
			star.vx = v*math.cos(theta)
			star.vy = v*math.sin(theta)
			star.ax = 0
			star.ay = 7/self.mainWindow.FPS
			star.show()
		self.timer.start(1000//self.mainWindow.FPS)
		pass

	def update(self):
		x, y, Max_x, Max_y= self.mainWindow.geometry().getRect()
		temp = []
		for star in self.stars:
			x, y, w, h = star.geometry().getRect()
			if x + w < 0 or x >= Max_x or y + h < 0 or y >= Max_y:
				star.hide()
				self.stars_not_using.add(star)
				temp.append(star)
			else:
				x += star.vx
				y += star.vy
				star.vx += star.ax
				star.vy += star.ay
				star.setGeometry(x, y, w, h)
		for star in temp:
			self.stars.remove(star)
		if len(self.stars) == 0:
			self.timer.stop()
			self.stars, self.stars_not_using = self.stars_not_using, self.stars
	
	def pic_init(self, total, pic):
		img = QtGui.QPixmap(pic).scaledToWidth(100)
		s = img.size()
		w = s.width()
		h = s.height()
		for i in range(total):
			label = QtWidgets.QLabel(self.mainWindow)
			label.setPixmap(img)
			label.vx = 0
			label.vy = 0
			label.setGeometry(0, 0, w, h)
			label.hide()
			self.stars.add(label)
