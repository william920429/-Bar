from PyQt5 import QtCore, QtGui, QtWidgets
import math, random

class _roll():
	def __init__(self, mainWindow):
		self.image = [[], [], []]
		self.led_top = [[], [], []]
		self.led_bot = [[], [], []]
		self.speed = [0, 0, 0]
		self.accleration = [0, 0, 0]
		self.ui = mainWindow.ui
		self.FPS = mainWindow.FPS
		self.mainWindow = mainWindow

		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.roll)
		self.timer.setInterval(1000//self.FPS)

		self.step = 0 #{'0': 停止,1': 加速, '2': 減速}
		self.speed_control_timer = QtCore.QTimer()
		self.speed_control_timer.timeout.connect(self.speed_control)
		#self.speed_control_timer.setInterval(1000//self.FPS)

		self.led_timer = QtCore.QTimer()
		self.led_timer.timeout.connect(self.led)
		self.led_timer.start(1000)

		self.pic_init()
		pass

	
	def start(self):
		if self.timer.isActive() > 0:
			return False
		self.step = 1
		self.finish = []
		self.mainWindow.prize(win = False)
		for i in range(len(self.speed)):
			self.speed[i] = 0
			self.accleration[i] = 100/self.FPS*(random.random() + 1)
			self.finish.append(-1)

		self.speed_control_timer.start(1000)
		self.timer.start()
		return True
		pass

	def speed_control(self):
		#(0, 2000, 3000)
		if self.step == 1:
			for i in range(len(self.speed)):
				self.accleration[i] = -50/self.FPS*(random.random() + 0.5)
			# self.speed_control_timer.start(2000)
			self.speed_control_timer.stop()
			self.step = 2
			
		elif self.step == 2:
			self.speed_control_timer.stop()
			self.timer.stop()
			s = self.name[self.finish[0]] + self.name[self.finish[1]] + self.name[self.finish[2]]
			if s[0] == s[1] and s[1] == s[2] or s == "crc":
				self.mainWindow.log.addItem("恭喜您抽中了{}".format(s))
				self.mainWindow.prize(win = True)
				self.mainWindow.stars.boom()
				self.mainWindow.meow_mp3.play()
			else:
				self.mainWindow.log.addItem("您抽中了{}".format(s))
				# self.mainWindow.stars.boom()################
				# self.mainWindow.meow_mp3.play()
		pass

	def roll(self):
		for i in range(len(self.image)): #row
			self.speed[i] += self.accleration[i]
			for j in range(len(self.image[i])):#index
				if self.finish[i] != -1:
					break
				x, y, w, h = self.image[i][j].geometry().getRect()
				if y + self.speed[i] > self.height*6:
					y += self.speed[i]  - self.height_total
					self.image[i][j].hide()
				else:
					y += self.speed[i]
					self.image[i][j].show()
				if y >= 0 and y < 50 and self.speed[i] > -50 and self.speed[i] < 0 and self.accleration[i] < 0:
					y = 0
					self.image[i][j].setGeometry(x, y, w, h)
					self.speed[i] = 0
					self.accleration[i] = 0
					self.finish[i] = j
					for k in range(len(self.image[i])):
						label = self.image[i][(j + k)%len(self.image[i])]
						label.setGeometry(0, k*h, w, h)
						if label.y() > h:
							label.hide()
						else:
							label.show()
					# print("finished:", i, j)
					break
				else:
					self.image[i][j].setGeometry(x, y, w, h)
			
		if self.finish[0] != -1 and self.finish[1] != -1 and self.finish[2] != -1:
			# print("finished3:", i)
			self.speed_control()
		# if reach and self.accleration[0] < 0:
		
		pass

	def led(self):
		for i in range(len(self.led_top)):
			num = random.randint(0, len(self.led_top[i]) - 1)
			# print(num)
			for j in range(len(self.led_top[i])):
				if j == num:
					self.led_top[i][j].show()
				else:
					self.led_top[i][j].hide()
			num = random.randint(0, len(self.led_bot[i]) - 1)
			# print(num)
			for j in range(len(self.led_bot[i])):
				if j == num:
					self.led_bot[i][j].show()
				else:
					self.led_bot[i][j].hide()

	def pic_init(self):
		self.name = ['h', 's', 'n', 'u', 'c', 'r', 'c']
		self.name.reverse()

		widgets = [self.ui.left_widget, self.ui.mid_widget, self.ui.right_widget]
		width = self.ui.horizontalLayoutWidget.width()//3
		height = self.ui.horizontalLayoutWidget.height()
		pixmap = []
		pixmap.append(QtGui.QPixmap("pic/h.png").scaledToWidth(width))
		pixmap.append(QtGui.QPixmap("pic/s.png").scaledToWidth(width))
		pixmap.append(QtGui.QPixmap("pic/n.png").scaledToWidth(width))
		pixmap.append(QtGui.QPixmap("pic/u.png").scaledToWidth(width))
		pixmap.append(QtGui.QPixmap("pic/c.png").scaledToWidth(width))
		pixmap.append(QtGui.QPixmap("pic/r.png").scaledToWidth(width))
		pixmap.append(pixmap[4])
		pixmap.reverse()
		
		self.height_total = height*len(pixmap)
		self.height = height

		for i in range(len(pixmap)):
			for j in range(len(widgets)):
				label = QtWidgets.QLabel(widgets[j])
				label.setPixmap(pixmap[i])
				label.setGeometry(0, i*height, width, height)
				if label.y() > height:
					label.hide()
				self.image[j].append(label)

		#################################################################

		pixmap = []
		pixmap.append(QtGui.QPixmap("pic/blue top.png").scaledToWidth(width))
		pixmap.append(QtGui.QPixmap("pic/green top.png").scaledToWidth(width))
		pixmap.append(QtGui.QPixmap("pic/purple top.png").scaledToWidth(width))
		pixmap.append(QtGui.QPixmap("pic/red top.png").scaledToWidth(width))
		pixmap.append(QtGui.QPixmap("pic/yellow top.png").scaledToWidth(width))
		
		for i in range(len(pixmap)):
			for j in range(len(widgets)):
				label = QtWidgets.QLabel(widgets[j])
				label.setPixmap(pixmap[i])
				label.setGeometry(0, -107, width, height)
				label.hide()
				self.led_top[j].append(label)

		#################################################################

		pixmap = []
		pixmap.append(QtGui.QPixmap("pic/blue bot.png").scaledToWidth(width))
		pixmap.append(QtGui.QPixmap("pic/green bot.png").scaledToWidth(width))
		pixmap.append(QtGui.QPixmap("pic/purple bot.png").scaledToWidth(width))
		pixmap.append(QtGui.QPixmap("pic/red bot.png").scaledToWidth(width))
		pixmap.append(QtGui.QPixmap("pic/yellow bot.png").scaledToWidth(width))
		
		for i in range(len(pixmap)):
			for j in range(len(widgets)):
				label = QtWidgets.QLabel(widgets[j])
				label.setPixmap(pixmap[i])
				label.setGeometry(0, 108, width, height)
				label.show()
				self.led_bot[j].append(label)
		
		# self.led

		pass
	
