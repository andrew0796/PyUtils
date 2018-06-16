#! /usr/bin/env python3

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

def polyCF(n):
    '''
    n^th order polynomial to be used with scipy.optimize.curve_fit
    y = a[0]+a[1]*x+...+a[n]*x^n
    '''
    def f(x, *a):
        y = 0
        for i in range(n+1):
            y += a[i]*x**i
        return y
    return f

def polyODR(n):
    '''
    n^th order polynomial to be used with scipy.ODR
    y = a[0]+a[1]*x+...+a[n]*x^n
    '''
    def f(B, x):
        y = 0
        for i in range(n+1):
            y += B[i]*x**i
        return y
    return f

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

    f can either be a function (described below) or a string representing one of the built in functions:
       'p{n}'  : nth order polynomial (n>=0), a[0]+a[1]x+...+a[n]x^n
       'gauss' : Gaussian : A*exp(-(x-x0)^2/(2*s^2))+C
    
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
        if type(f) is str:
            if f[0] == 'p' and len(f)>1 and f[1:].isnumeric():
                n = int(f[1:])
                F = polyCF(n)
            elif f == 'gauss':
                F = gaussianCF
            else:
                raise ValueError("The string given doesn't match a built in function")
        else:
            F = f
        params, cov = curve_fit(F, x,y, sigma=dy, p0=guess)
        errors = np.sqrt(np.diag(cov))
    else:
        if guess is None:
            raise ValueError('scipy.odr requires guess be given')

        if type(f) is str:
            if f[0] == 'p' and len(f)>1 and f[1:].isnumeric():
                n = int(f[1:])
                F = polyCF(n)
            elif f == 'gauss':
                F = gaussianODR
            else:
                raise ValueError("The string given doesn't match a built in function")
        else:
            F = f
        model = odr.Model(F)
        data = odr.RealData(x,y, sx=dx, sy=dy)
        myOdr = odr.ODR(data, model, beta0=guess)
        output = myOdr.run()

        params, errors = output.beta, output.sd_beta
    return params, errors

                
