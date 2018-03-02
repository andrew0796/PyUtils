#! /usr/local/bin/python3

'''
Utilities for fitting data in python
'''

# TODO
#   Add Jacobian support
#   Have built in functions called by strings instead of passed as functions
#   Return a figure of merit, ie chi squared (per DOF) or likelihood or something

import scipy.odr as odr
from scipy.optimize import curve_fit
import numpy as np
import pandas as pd

def linearODR(B, x):
    ''' 
    simple linear model to be used with scipy.ODR
    y = B[0]+B[1]*x
    '''
    return B[0]+B[1]*x

def linearCF(x, b,a):
    '''
    simple linear model to be used with scipy.optimize.curve_fit
    y = a*x+b
    '''
    return a*x+b

def gaussianODR(B, x):
    ''' 
    Gaussian model to be used with scipy.ODR
    y = B[0]*exp(-(x-B[1])^2/(2*B[2]^2)+B[3]
    '''
    return B[0]*np.exp(-np.square(B[1]-x)/(2*np.square(B[2])))+B[3]

def gaussianCF(x, A,x0,s,C):
    '''
    Gaussian model to be used with scipy.optimize.curve_fit
    y = A*exp(-(x-x0)^2/(2*s^2))+C
    '''
    return A*np.exp(-np.square(x-x0)/(2*np.square(s)))+C

def FitData(f, x,y, dx=None,dy=None, guess=None):
    '''
    fit data y to independent variable x with model f (ie f(x)=y)

    for now just return the fitted parameters, and their errors
    
    dx and dy are errors on x and y (look up scipy docs for more)
    guess is a collection (list, array, etc) of guess parameters

    if dx is None:
        scipy.optimize.curve_fit is used
        f must be f(x, p1,p2,...) where p1,p2,... are parameters
        guess is optional
    if dx is given
        scipy.odr is used
        f must be f(p, x) where p is a list of parameters
        guess must be given
    '''

    if dx is None:
        params, cov = curve_fit(f, x,y, sigma=dy, p0=guess)
        errors = np.sqrt(np.diag(cov))
    else:
        if guess is None:
            raise ValueError('scipy.odr requires guess be given')
        
        model = odr.Model(f)
        data = odr.RealData(x,y, sx=dx, sy=dy)
        myOdr = odr.ODR(data, model, beta0=guess)
        output = myOdr.run()

        params, errors = output.beta, output.sd_beta
    return params, errors

                
