# mmWave_LPD_v2
![Platform](https://img.shields.io/badge/Raspberry-Pi3-orange.svg)&nbsp;
![Platform](https://img.shields.io/badge/Raspberry-Pi4-orange.svg)&nbsp;
![Platform](https://img.shields.io/badge/ubuntu-NCU-orange.svg)&nbsp;
![Platform](https://img.shields.io/badge/Win-OS-blue)&nbsp;
![Platform](https://img.shields.io/badge/Mac-OS-lightgrey)&nbsp;
![Platform](https://img.shields.io/badge/Jeson-Nano-green.svg)&nbsp;
![Language](https://img.shields.io/badge/python-%3E3.7%20-green.svg)&nbsp;
![License](http://img.shields.io/badge/license-MIT-green.svg?style=flat)

# 🚧  Under Construction 🚧 

mmWave Long Range People Detection
  This repository contains the Batman Kit- 201(ISK) Sensing mmWave Sensor SDK Device Version:ES2.0 . The sample code below consists of instruction for using the mmWave lib. This mmWave-LPD Python Program will work with Long-Range People Detection based Batman BM201 mmWave Kit solution (BM201-LPD). This Python Program works with a Raspberry Pi 4 and/or NVIDIA Jetson Nano computer with Batman BM201-LPD Kit attached via Kit’s HAT Board; and that the BM201 Kit is an easy-to-use mmWave sensor evaluation kit for tracking multiple people’s movements simultaneously from 1meter ~ 50meter range with a high degree of accuracy suitable for privacy conscious applications; and where the Python Program would detect multiple people movements in a 3-Dimentional Area with ID tag, posX, posY, posZ, velX, velY, velZ, accX, accY, accZ parameters, along with Point Clouds with  range, elevation, azimuth and  doppler(readxyz) parameters.

# Hardware Sensor:

     Firmware version: i4.12.0
  
     BM201-LPD provids raw data as:

        Point Cloud Spherical(V6): range,elevation,azimuth,doppler,x,y,z (readxyz)
        Target Object (V7): tid,posX,posY,posZ,velX,velY,velZ,accX,accY,accZ,ec[16],g,confidenceLevel
        Target Index (V8): tid and status
        Point Cloud Side Info (V9): snr,noise
            
   
   
# Installing

Library install for Python

    $sudo pip install mmWave
    $sudo pip3 install mmWave

Library update:

    $sudo pip install mmWave -U
    $sudo pip3 install mmWave -U

Examples:
    
    lpdv2_ex1_pyqtgraph_xy.py  # plot point clouds in 2D and range/doppler 
    lpdv2_ex2_pyqtgraph_xyz_100m.py # show detected point cloud in 3D

If Run demo program can not find any Raw data output:
      Please set UART to R/W mode: 
      
      pi 3
      $ls -l /dev/ttyS0
      $sudo chmod +777 /dev/ttyS0
      
      pi 2 
      $ls -l /dev/ttyS0
      $sudo chmod +777 /dev/ttyAMA0
      
      jetson
      $ls -l /dev/ttyTHS1
      $sudo chmod +777 /dev/ttyTHS1
      
 # import lib

    from mmWave import lpdISK_v2

  ### raspberry pi 4 use ttyS0
    port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
 
  ### Jetson Nano use ttyTHS1
      port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)
    and please modify: 
    
  ### use USB-UART
    port = serial.Serial("/dev/ttyUSB0",baudrate = 921600, timeout = 0.5)
 
  ### Mac OS use tty.usbmodemxxxx
    port = serial.Serial("/dev/tty.usbmodemGY0052854",baudrate = 921600, timeout = 0.5)
  
  ### ubuntu NUC
    port = serial.Serial("/dev/ttyACM1",baudrate = 921600, timeout = 0.5)

## define

    radar = lpdISK_v2.LpdISK(port)

## Header:

    class header:
        version = 0
        totalPacketLen = 0
        platform = 0
        frameNumber = 0
        timeCpuCycles = 0
        numDetectedObj = 0
        numTLVs = 0
        subFrameNumber = 0

# Data Structure:    
    (dck,v6,v7,v8) = radar.tlvRead(False)
    
    Type V6: (Point Cloud) (readxyz)
        range:    float   #Range in meters
        
        elv:      float   #Elevation in radians, Elevation angle in degrees in the range[-90,90], where positive angle 
                          #represents abpve the sensor and negative below the sensor
                          
        azimuth:  float   #Azimuth in radians  Azimuth angle in degrees in the range [-90,90], where
                          #positive angle represents the right hand side as viewed from the sensor towards the scene and
                          #negtive angle represents left hand side.
                          
        doppler:  float   #Doppler in m/s, Doppler velocity estimate in m/s. Positive velocity means target is moving away 
                          #from the sensor and negative velocity means target is moving towards the sensor.     
       
        sx : point position x
        sy : point position y
        sz : point position z
        
    Type v7: (Target List)
        tid:  int       #Target ID
        posX: float     #Target position in X, m
        posY: float     #Target position in Y, m
        posZ: float     #Target position in Z, m
        velX: float     #Target velocity in X, m/s
        velY: float     #Target velocity in Y, m/s
        velZ: float     #Target velocity in Z, m/s
        accX: float     #Target velocity in X, m/s2 
        accY: float     #Target velocity in Y, m/s2
        accZ: float     #Target velocity in Z, m/s2
        ec[16]: float   #Tracking error covariance matrix, 
                        [4x4] in range/azimuth/elevation/doppler coordinates
        g: float        #Gating function gain
        confidenceLevel: float #Confidence Level  
    
    Type V8: (Target Index)
        Each Target List consists of an array of target IDs, A targetID at index i is the target to which point i 
        of the previous frame's point cloud was associated. Valid IDs range from 0-249
        
        tragetID: Int #Track ID
        {targetID0,targetID1,.....targetIDn}
        
        Other Target ID values:
        253:Point not associated, SNR to weak
        254:Point not associated, located outside boundary of interest
        255:Point not associated, considered as noise
     
     Type V9: (Side Information)
        [(snr,noise),....]
        snr:    Int  #CFAR cell to side noise ratio in dB expressed in 0.1 steps of dB
        noise:  Int  #CFAR noise level of the side of the detected cell in dB expressed in 0.1 steps of dB 
     
          
        

   
   # Function call: 
        
        (dck,v6,v7,v8,v9) = radar.tlvRead(False)
        dck : True  : data avaliable
              False : data invalid
        v6: point cloud of array
        v7: target object of array
        v8: target id of array
        v9: Side information
        return dck,v6,v7,v8,v9
      
        getHeader()
        headerShow()
        
    
   
