#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 12:26:21 2019

@author: logancooke

Script to call BeamDoctorFunctions.py for choosing a two-lens telescope configuration
for correcting laser beam profiles, based on measured profiles and lens-stock.

Required Packages:
    colorama : conda install -c anaconda colorama
    prettytable : conda install -c conda-forge prettytable
"""

#Misc libraries
import numpy as np
import BeamDoctorFunctions as BDF

#------------------------------ Constants ------------------------------
#Thorlabs Cylindrical Lens stock focal lengths [mm]
cylvex = [ 50, 75, 100, 150, 200, 250, 300, 400, 500, 1000] #Convex
cylcave = [ -50, -75, -100, -150, -200, -400, -1000] #Concave

#convert to other angle units by multiplication
radians = np.pi/180 #To radians
degrees = 180/np.pi #To degrees

#------------------------------ Trials ------------------------------
#--- Input Data ---
d = np.linspace( 0, 1000, num=25 ) #distances measured [mm]
th = 1 * radians #beam half-angle [Rad]
r = d*np.tan(th) #Beam-radii at measured distances [mm]
theta = BDF.beamprofiler( r, d ) #Fit divergence angle [Rad]

r_in = np.array([ 2, theta ]) #Input beam profile [radius, half-angle]

#--- Compute Configurations ---
rmax = 3 #Maximum tolerable beam radius
thetamax = 1.5*radians #Maximum tolerable beam divergence
BDF.beamdoctor(r_in, cylvex, cylcave, rmax, thetamax, dpm=200)






