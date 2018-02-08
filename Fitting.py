#! /usr/local/bin/python3

'''
Utilities for fitting data in python
'''

import scipy.odr as odr
from scipy.optimize import curve_fit
import numpy as np
import pandas as pd

def linear(B, x):
    ''' simple linear model '''
    return B[0]+B[1]*x

def FitData(f, x,y, dx=None,dy=None, guess=None):
    '''
    fit data y to independent variable x with model f (ie f(x)=y)
    
    for now just return the fitted parameters, and their errors
    in the future I'd like to also return some figure of merit, for instance chi squared

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

                
