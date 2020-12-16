#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 12:51:04 2019

@author: logancooke

Functions for choosing lenses to correct a measured beam profile, using a
two-lens telescope configuration.
"""

import numpy as np
from prettytable import PrettyTable
from scipy.stats import linregress

def beamprofiler(rs, ds):
    '''
    Computes the divergence half-angle of a beam from linear fit to data of beam-radius
    versus distance.

    Parameters:
        rs, ds : Data of the radii "rs" at distances "ds", both numpy arrays with the
            same length. Data must have the same units.
    Returns:
        theta: The divergence half-angle of this beam, in radians.
    '''
    fit = linregress( ds, rs ) #fit line to the x,y data
    theta = np.arctan( fit.slope ) #Extract the half angle from slope [Rad]
    return theta


def telescope( f1, f2, d , ri ):
    '''
    From an input beam radius & half-angle, computes the output through a telescope
    configuration of lenses with focal length f1 & f2, separated by distance d. All
    lengths must have the same units.

    Parameters:
        f1, f2 : Lens focal lengths. May be positive or negative.
        d : Separation between lenses.
        ri : Input beam vector, numpy array, [radius, angle].

    Returns:
        r, theta : Output beam vector, as a numpy array, [radius, angle]. Returns
            the |r| because a negative beam radius is the same as a positive one
            (but the beam went through a focus, thus the inversion).
    '''

    r = ( (f1 - d)/f1 ) * ri[0] + d * ri[1] #radius
    theta = ( (f1 + f2 - d)/( f1 * f2 ) ) * ri[0] + ( (f2 - d)/f2 ) * ri[1] #angle

    return np.array([ abs(r), theta ])

def lensconfigs( f1, f2, dpm=0 ):
    '''
    Compiles an array containing all combinations of focal lengths in the input
    arrays f1 & f2, along with the "ideal" separation distance f1+f2. This excludes
    those with separation distance d=0

    Parameters:
        f1, f2 : Input arrays containing potenital focal lengths to try in a
            telescope configuration. These can be different length arrays, but
            must be in the same units
        dpm : "Distance plus/minus", by default is 0. Represents how far on each side
            of f1+f2 to place lenses. Will try 10 different distances on either side,
            up to the value of dpm, and add them as configurations. So for a given dpm,
            51 distances between f1 + f2 +/- dpm will be generated and added as new
            configurations, representing how one could put the second lens a slightly
            smaller or larger distance away from the f1 + f2 recomendation for
            collimated input; this provides more flexibility for uncollimated inputs.
    Returns:
        configs : Array of possible configurations in form [f1_i, f2_j, d] where d is
            just f1_i + f2j, for all i, j in f1, f2.
    '''
    if dpm != 0:
        ds = np.linspace( -dpm, dpm, num=11, endpoint=True )
    else:
        ds = np.zeros(1)

    configs = np.empty( (0,3) ) #empty row array, with 3 columns
    for f in f1:
        'For each lens in f1...'
        for l in f2:
            'And for each lens in f2...'
            for d in ds:
                'And for each modified separation distance...'
                if f+l+d >= 0.2*f and f+l+d >= 0.2*l:
                    'So long as the lens separation is greater than 20% of f1 & f2'
                    temp = np.array([ f, l, f+l+d ]) #New configuration
                    configs = np.append( configs, [temp], axis=0 ) #Append config.

    return configs

def tryall( ri, configs ):
    '''
    For an input beam profile [radius, angle], and array of lens configurations [f1,
    f2, d] will compute the output beam profile for each configuration in the array.

    Parameters:
        ri : Input beam profile, numpy array, [radius, angle].
        configs : Input list of lens configurations, numpy array, [f1, f2, d].

    Returns:
        rf : List of all output beam profiles, numpy array, [radius, angle].
    '''

    num = len( configs[:,0] ) #number of lens configurations
    rf = np.empty( (0,2) ) #Empty row array, 2 columns

    for i in range(num):
        out = telescope( configs[i,0], configs[i,1], configs[i,2], ri ) #New output
        rf = np.append( rf, [out], axis=0) #Append output

    return rf

def filterall( rf, configs, rmax, themax, rmin=0 ):
    '''
    Specify the maximum allowed beam radius and divergence half-angle, and this
    function will sort through the input set of lens configurations and corresponding
    output beam profiles, and return those that meet specifications.
    
    Parameters:
        rf : List of output beam profiles, numpy array, [radius, angle].
        configs : List of telescope lens configurations, numpy array, [f1, f2, d].
        rmax : Maximum allowed beam radius.
        themax : Maximum allowed divergence half-angle.
        rmin : minimum beam radius, not required. Default is 0.
        
    Returns:
        rf_good : List of output beam profiles which match specifications, numpy array,
            [radius, angle]
        configs_good : List of telescope lens configurations corresponding to the list
            of accepted beam profiles, numpy array, [f1, f2, d].
    '''
    
    num = len( rf[:,0] ) #Number of outputs to filter through
    configs_good = np.empty( (0,3) ) #Empty row array, 3 columns
    rf_good = np.empty( (0,2) ) #Empty row array, 2 columns
    
    for i in range(num):
        'For all output beam-profiles/configurations'
        if (rf[i,0] <= rmax and rf[i,0]>=rmin) and abs(rf[i,1]) <= themax:
            'If the radius & angle are less than desired value'
            configs_good = np.append(configs_good, [configs[i,:]], axis=0) #Keep config.
            rf_good = np.append(rf_good, [rf[i,:]], axis=0) #Keep beam-profile 
            
    return rf_good, configs_good

def beamdoctor( ri, f1s, f2s, rmax, thetamax, dpm=0, rmin=0 ):
    '''
    For a given input beam profile and lists of lenses to try in a telescope 
    configuration, this function will determine all the possible outputs that will
    result in a beam radius and half angle less than a specified amount. Optionally,
    the distances between the lenses can be modified to try configurations within a 
    range specified by "dpm" (see below).
    
    Parameters:
        ri : Input beam profile, numpy array, [radius, angle].
        f1s, f2s : List of lens focal lengths to try, numpy arrays, can be positive or
            negative.
        rmax, thetamax : Maximum allowed output beam radius and half-angle.
        dpm : "Distance plus/minus", by default is 0. Represents how far on each side 
            of f1+f2 to place lenses. So for a given dpm, many distances between 
            f1 + f2 +/- dpm will be added as new configurations, representing how one 
            could put the second lens a slightly smaller or larger distance away 
            from the f1 + f2 recomendation for collimated input; this provides 
            more flexibility for uncollimated inputs.
        rmin : Minimum allowed beam radius, not required. Default is 0.
    '''
    
    #----- Generate Output -----
    telescopes = lensconfigs( f1s, f2s, dpm=dpm ) #Get all configurations
    rfs = tryall( ri, telescopes ) #Get all output beam-profiles
    rfs, telescopes = filterall( rfs, telescopes, rmax, thetamax, rmin=rmin ) #Filter through
    
    #----- Make a Table -----
    t = PrettyTable([ 'Radius [mm]' ,\
                     'Theta [deg]' ,\
                     'f1 [mm]' ,\
                     'f2 [mm]' ,\
                     'd [mm]' ])
        
    num = len(rfs[:,0]) #Number of good beam-profiles/configs.
    for i in range(num):
        'For each good beam-profile/config'
        t.add_row([ '%.3f' %rfs[i,0], '%.3f' %(rfs[i,1]*180/np.pi), \
                   '%d' %telescopes[i,0], \
                   '%d' %telescopes[i,1], \
                   '%d' %telescopes[i,2] ])
    print(t)
