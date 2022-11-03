 # -*- coding: utf-8 -*-
"""
****************************************
version: v1.0 2022/011/03 release
         
         
Long Range People Detect Radar API
****************************************
Use: pyqtgraph to plot

Hardware requirements:
 Batman Kit- 201 LPD mmWave Sensor SDK
 Jetson nano, pi 4 , NUC, PC or MAC
**************
Install Jetson nano: Please reference

https://makerpro.cc/2019/05/the-installation-and-test-of-nvida-jetson-nano/
it will teach you how to install
 
(1)install Jetson nano GPIO
    $sudo pip3 install Jetson.GPIO
    $sudo groupadd -f -r gpio
    
    #please change pi to your account
    $cd practice sudo usermod -a -G gpio pi
    
    $sudo cp /opt/nvidia/jetson-gpio/etc/99-gpio.rules /etc/udev/rules.d/
    
    reboot system and run
    
    $sudo udevadm control --reload-rules && sudo udevadm trigger
(2)install mmWave lib
$sudo pip3 install mmWave
(3) upgarde mmWave lib
$sudo pip3 install mmWave -U

************************************************
raspberry pi 4 UART setting issues reference:
https://www.raspberrypi.org/documentation/configuration/uart.md

************************************************

"""

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

import numpy as np
import serial
#import Jetson.GPIO as GPIO

from mmWave import lpdISK_v2
 
import struct
import sys
from threading import Thread
#from scipy.fftpack import fft
import numpy as np
from scipy import signal
import time

class globalV:
	count = 0
	subFrameN = 0
	def __init__(self, count):
		self.count = count		
			
gv = globalV(0)
#pg win
win = pg.GraphicsWindow()
win.resize(1200,800)
#pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'y')
 
win.setWindowTitle('Long Range People Detect Radar')


# 1) for detected object scatterPlot (spots0,spots2))

w0 = win.addPlot()
w0.setRange(xRange=[-10,10],yRange= [0,200])
w0.setLabel('bottom', 'V6(o) Object Location(spots0)/ V7(S) Cluster Object(spots2)')
w0.setLabel('left', 'Range', 'm')
w0.showGrid(x = True, y = True, alpha = 1.0)

spots0 = []
curveS0 = pg.ScatterPlotItem(size =10, pen=pg.mkPen('w'), pxMode=True)  
w0.addItem(curveS0)

spots2 = []
curveS2 = pg.ScatterPlotItem(size =20, pen=pg.mkPen('w'), pxMode=True)  
w0.addItem(curveS2)


# 2) for detected object Doppler scatterPlot(spots1)

w1 = win.addPlot()
w1.setRange(xRange=[0,40],yRange= [-40,40]) 
w1.showGrid(x = True, y = True, alpha = 1.0)


w1.setLabel('bottom', 'V6 Range (spots1)', '')
w1.setLabel('left'  , 'V6 Doppler', '')


spots1 = []
curveS1 = pg.ScatterPlotItem(size=20, pen=pg.mkPen('g'), pxMode=True)
w1.addItem(curveS1) 



########################################################################
# for V7 TARGET TAG
# ALERT: should be called in update() thread otherwise WARNING on thread issue
textA_old = [pg.TextItem()]
JB_skipFirst = 0
JB_textCount = 0
def jb_vText(w, v1 = None, v2 = None):
	global textA_old, JB_skipFirst, JB_textCount
	global fN
	 
	# (1) clean old target text
	# due to TARGET is NO needed to be removed at first time
	if JB_skipFirst == 0:
		JB_skipFirst = 1  
	else:
		for i in range(len(textA_old)):
			w.removeItem(textA_old[i])
			
	# (2) insert new target text
	textA_old = [] # all cleared before running
	for i in range(len(v1)):
		#
		#        v1    =: ['X'  ,  'Y', 'Z','doppler','peakVal','fN']
		#      index         0      1    2     3        4        5
		#       
		textA = pg.TextItem()
		textA.setFont(QtGui.QFont("consolas", 16))
		textA.setPos(v1[i][0], v1[i][1])
		
		jb_posStr = ' [fN={:},({:.1f},{:.1f}),vy={:.1f}Km/H]'.format(int(v1[i][5]), v1[i][0], v1[i][1], v1[i][3] * 3.6)
			
		textA.setColor(pg.intColor(i, len(v1))) # set the same color with TARGET dot
		textA.setPlainText(jb_posStr)
		w.addItem(textA)
		textA_old.append(textA) # saved into old array
		
	for i in range(len(v2)):
		#
		#        v2    =: ['ccX','ccY','csX','csY',   'fN']
		#      index         0      1    2     3        4        5
		#       
		textA = pg.TextItem()
		textA.setFont(QtGui.QFont("consolas", 16))
		textA.setPos(v2[i][0], v2[i][1])

		jb_posStr = ' [fN={:},({:.1f},{:.1f})]'.format(int(v2[i][4]), v2[i][0], v2[i][1])
			
		textA.setColor(pg.intColor(i, len(v2))) # set the same color with TARGET dot
		textA.setPlainText(jb_posStr)
		w.addItem(textA)
		textA_old.append(textA) # saved into old array
		

########################################################################	


# 
# plot data update 
#
def update():
	global  curveS0,curveS1,curveS2,spots0,spots1,spots2
	curveS0.setData(spots0)  # w0
	curveS1.setData(spots1)  # w1 doppler ok
	curveS2.setData(spots2)  # w0

		

#
#----------timer Update--------------------   
timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(143) #150  80: got(20 Times)   *50ms from uart: 
#------------------------------------------

#use USB-UART
#port = serial.Serial("/dev/ttyUSB0",baudrate = 921600, timeout = 0.5)
#
#for Jetson nano UART port
#port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)
#for pi 4 UART port
#port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
#Mac OS
port = serial.Serial("/dev/tty.usbmodemGY0043864",baudrate = 921600, timeout = 0.5) 

#Medium Range Radar initial 
radar =   lpdISK_v2.LpdISK(port)


radar.sm = False  # set true to check V1...V4 state machine running state. 
 
def parkingBins(v4d = None):
	#    ['X','Y','Z','doppler','peakVal','fN']
	#idx:  0    1   2    3         4        5
    len4 = len(v4d)
    if len4 != 0:
        v4d = np.fft.fftshift(v4d)
        v4d = np.append(v4d,v4d[0])
        x1 = np.linspace(-1,1,len4+2)
        y1 = np.sqrt(1 - x1 * x1) #circle formular
        x_1 = v4d * x1[0:-1]
        x_2 = v4d * x1[1:]
        y_1 = v4d * y1[0:-1]
        y_2 = v4d * y1[1:]
        xal = []
        yal = []
        for i in range(len(x_1)):
            xal.append(x_1[i])
            xal.append(x_2[i])
            yal.append(y_1[i])
            yal.append(y_2[i])
        xal = xal[1:-1]
        yal = yal[1:-1]
        return xal,yal
        
prv_fn = 0
fn = 0
v6_clear = 0
v7_clear = 0
v8_clear = 0
v9_clear = 0

def radarExec():
	global v6len,v7len,v8len,v9len,pxA,pyA,sxA,syA,fn,prv_fn,spots0,spots1,spots2,v6_clear,v7_clear,v8_clear,v9_clear
	
	t0 = time.time()
	(chk,v6,v7,v8,v9) = radar.tlvRead(True) 
	v6len = len(v6);v7len = len(v7);v8len = len(v8);v9len = len(v9)
	
	hdr = radar.getHeader()
	fn = hdr.frameNumber
	
	 
	
	if fn != prv_fn:
		# v6 struct = [(r,e,a,d,x,y,z),(r,e,a,d,x,y,z),(r,e,a,d,x,y,z)..]
		v6_clear+= 1; v7_clear+= 1; v8_clear+= 1;
		if v6len > 0:  
			spots0 = [{'pos': [v6[i][4],v6[i][5]], 'data': 1, 'brush':pg.intColor(i, v6len), 'symbol': 'o', 'size': 10 } for i in range(v6len)]
			spots1 = [{'pos': [v6[i][0],v6[i][3]], 'data': 1, 'brush':pg.intColor(i, v6len), 'symbol': 'o', 'size': 10 } for i in range(v6len)]  #dopplerA
			sxA = []; syA = []
			for i in range(v6len):
				sxA.append(v6[i][4])
				syA.append(v6[i][5])
			v6_clear = 0
		else:
			if v6_clear > 20:
				spots0 = [] 

		if v7len > 0: #v2 struct = (fn,ccX,ccY,csX,csY)
			spots2 = [{'pos': [v7[i][1],v7[i][2]], 'data': 1, 'brush':pg.intColor(i,v7len), 'symbol': 's', 'size': 12 } for i in range(v7len)] 
			v7_clear = 0
		else:
			if v7_clear > 20:
				spots2 = []
				
		prv_fn = fn
		print(f"fn = {fn} state:{chk} [v6={v6len}:v7={v7len}:v8={v8len}:v9={v9len}]")
		
	port.flushInput()
		
		 
def uartThread(name):
	port.flushInput()
	while True:
		radarExec()
					
thread1 = Thread(target = uartThread, args =("UART",))
thread1.setDaemon(True)
thread1.start()

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
	import sys
	if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
		QtGui.QApplication.instance().exec_()
