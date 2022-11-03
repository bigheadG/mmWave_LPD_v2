#=======================================================================
# File Name: lpdv2_ex2_pyqtgraph_xyz_100m.py
#
# Requirement:
# Hardware: BM201-ISK (AWR6843)
# Firmware: LPD_v2 : v4.12.0
#  
# lib: lpdISK 
# plot tools: pyqtgraph 3D
# Plot point cloud(V6) in 3D figure 
# lib: from mmWave import lpdISK_v2
# type: Raw data
# Baud Rate:
#=======================================================================

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np
from mmWave import lpdISK_v2

import serial
from threading import Thread

class CustomTextItem(gl.GLGraphicsItem.GLGraphicsItem):
	def __init__(self, X, Y, Z, text):
		gl.GLGraphicsItem.GLGraphicsItem.__init__(self)
		self.text = text
		self.X = X
		self.Y = Y
		self.Z = Z

	def setGLViewWidget(self, GLViewWidget):
		self.GLViewWidget = GLViewWidget

	def setText(self, text):
		self.text = text
		self.update()

	def setX(self, X):
		self.X = X
		self.update()

	def setY(self, Y):
		self.Y = Y
		self.update()

	def setZ(self, Z):
		self.Z = Z
		self.update()

	def paint(self):
		pass
		#self.GLViewWidget.qglColor(QtCore.Qt.cyan)
		#self.GLViewWidget.renderText(self.X, self.Y, self.Z, self.text)


class Custom3DAxis(gl.GLAxisItem):
	#Class defined to extend 'gl.GLAxisItem'
	def __init__(self, parent, color=(0,0,0,.6)):
		gl.GLAxisItem.__init__(self)
		self.parent = parent
		self.c = color
		
	def add_labels(self):
		#Adds axes labels. 
		x,y,z = self.size()
		#X label
		self.xLabel = CustomTextItem(X=x/2, Y=-y/20, Z=-z/20, text="X")
		self.xLabel.setGLViewWidget(self.parent)
		self.parent.addItem(self.xLabel)
		#Y label
		self.yLabel = CustomTextItem(X=-x/20, Y=y/2, Z=-z/20, text="Y")
		self.yLabel.setGLViewWidget(self.parent)
		self.parent.addItem(self.yLabel)
		#Z label
		self.zLabel = CustomTextItem(X=-x/20, Y=-y/20, Z=z/2, text="Z")
		self.zLabel.setGLViewWidget(self.parent)
		self.parent.addItem(self.zLabel)
		
	def add_tick_values(self, xticks=[], yticks=[], zticks=[]):
		#Adds ticks values. 
		x,y,z = self.size()
		xtpos = np.linspace(0, x, len(xticks))
		ytpos = np.linspace(0, y, len(yticks))
		ztpos = np.linspace(0, z, len(zticks))
		#X label
		for i, xt in enumerate(xticks):
			val = CustomTextItem(X=xtpos[i], Y=0, Z=0, text='{}'.format(xt))
			val.setGLViewWidget(self.parent)
			self.parent.addItem(val)
		#Y label
		for i, yt in enumerate(yticks):
			val = CustomTextItem(X=0, Y=ytpos[i], Z=0, text='{}'.format(yt))
			val.setGLViewWidget(self.parent)
			self.parent.addItem(val)
		#Z label
		for i, zt in enumerate(zticks):
			val = CustomTextItem(X=0, Y=0, Z=ztpos[i], text='{}'.format(zt))
			val.setGLViewWidget(self.parent)
			self.parent.addItem(val)

app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.show()

g = gl.GLGridItem()
g.setSize(x=200,y=200,z=5)
w.addItem(g)

axis = Custom3DAxis(w, color=(0.2,0.2,0.2,1.0))
axis.setSize(x=100, y=100, z=5)
zt = [0,1,2,3,4,5]
xt = [0,20,40,60,80,100]  
axis.add_tick_values(xticks=xt, yticks=xt, zticks=zt)
w.addItem(axis)

#
#use USB-UART
#port = serial.Serial("/dev/ttyUSB0",baudrate = 921600, timeout = 0.5)
#
#for Jetson nano UART port
#port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5) 
#
#for pi 4 UART port
#port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
#
#Drone Object Detect Radar initial 
#port = serial.Serial("/dev/tty.usbmodemGY0052854",baudrate = 921600, timeout = 0.5)
port = serial.Serial("/dev/tty.usbmodemGY0043864",baudrate = 921600, timeout = 0.5)

#for NUC ubuntu 
#port = serial.Serial("/dev/ttyACM1",baudrate = 921600, timeout = 0.5)

radar = lpdISK_v2.LpdISK(port)

v6len = 0
v7len = 0
v8len = 0
v9len = 0

pos1 = np.empty((100,3))
pos2 = np.empty((100,3))
sp1 = gl.GLScatterPlotItem(pos=pos1,color=[1.0,1.0,0.0,1.0],size = 15.0)
sp2 = gl.GLScatterPlotItem(pos=pos2,color=[1.0,0.0,0.0,1.0],size = 20.0)
w.addItem(sp1)
w.addItem(sp2)

def update():
    global sp1,sp2,pos1,pos2
    sp1.setData(pos=pos1)
    sp2.setData(pos=pos2)


t = QtCore.QTimer()
t.timeout.connect(update)
t.start(50)

prev_fn = 0
fn = 0

def radarExec():
	global v6len,v7len,v8len,v9len,pos1,pos2,zOffset,prev_fn,fn
	flag = True
	(dck,v6,v7,v8,v9)  = radar.tlvRead(False)
	fn = radar.hdr.frameNumber
	radar.headerShow() # check sensor information
	
	if prev_fn != fn:
		prev_fn = fn
		v8len = len(v8)
		v6len = len(v6)
		v7len = len(v7)
		v9len = len(v9)
		print("Sensor Data: [v6,v7,v8,v9]:[{:d},{:d},{:d},{:d}]".format(v6len,v7len,v8len,v9len))
		#if v6len != 0 and flag == True:
		flag = False
		
		# v6 struct = [(r,e,a,d,x,y,z),(r,e,a,d,x,y,z),(r,e,a,d,x,y,z)..]
		pos1X = np.empty((len(v6),3))
		for i in range(len(v6)):
			pos1X[i] = (v6[i][4], v6[i][5], v6[i][6])
		pos1 = pos1X
		
		# v7 
		pos2X = np.empty((len(v7),3))
		for i in range(len(v7)):
			pos2X[i] = (v7[i][1], v7[i][2], v7[i][3])
		pos2 = pos2X
		
		flag = True
		
	port.flushInput()
		
		 
def uartThread(name):
	port.flushInput()
	while True:
		radarExec()
					
thread1 = Thread(target = uartThread, args =("UART",))
thread1.setDaemon(True)
thread1.start()

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore,'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
