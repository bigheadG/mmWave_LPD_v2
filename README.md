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
  This repository contains the Batman Kit- 201(ISK) Sensing mmWave Sensor SDK Device Version:ES2.0 . The sample code below consists of instruction for using the mmWave lib. This mmWave-LPD Python Program will work with Long-Range People Detection based Batman BM201 mmWave Kit solution (BM201-LPD). This Python Program works with a Raspberry Pi 4 and/or NVIDIA Jetson Nano computer with Batman BM201-LPD Kit attached via Kit’s HAT Board; and that the BM201 Kit is an easy-to-use mmWave sensor evaluation kit for tracking multiple people’s movements simultaneously from 1meter ~ 50meter range with a high degree of accuracy suitable for privacy conscious applications; and where the Python Program would detect multiple people movements in a 3-Dimentional Area with ID tag, posX, posY, posZ, velx, vely, velz, accX, accY, accZ parameters, along with Point Clouds with elevation, azimuth, doppler, range, and snr parameters.

# Hardware Sensor:
   Batman BM201-LPD provid two types of data:

        BM201-LPD provids raw data as:

            Point Cloud Spherical(V6): range,elevation,azimuth,doppler,x,y,z
            Target Object (V7): tid,posX,posY,posZ,velX,velYvelZ,accX,accY,accZ,ec[16],g,confidenceLevel
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
