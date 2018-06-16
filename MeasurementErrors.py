#! /usr/local/bin/python3

'''
Utilities for calculating measurement errors in Python
Based on Gaussian Error propagation

See https://en.wikipedia.org/wiki/Propagation_of_uncertainty for more

Assumes variables are uncorrellated, ie covariances are 0

Defines a Measurement class that more or less works like a normal number, operations +,-,*,/ are all allowed with both other Measurements and normal numbers

Includes common functions on Measurements, and arbitrary functions
'''

__name__ = "measurementerrors"

import math
import warnings
import configparser as cp
from sys import float_info # to get machine epsilon
import os

# read the config file
configFile = os.path.dirname(os.path.realpath(__file__))+'/config.ini'
config = cp.ConfigParser()
config.read(configFile)
if 'measurementPrintModes' not in config:
    raise Exception('measurementPrintMode not in configuration file')

class Measurement:
    ''' Measurement class '''
    __doc__ = "Measurement Class"
    __module__ = "MeasurementErrors"
    
    def __init__(self, value,error, name=None,units=None, printMode='default'):
        self.value = value
        self.error = error

        if name is not None:
            self.name = name
        else:
            self.name = 'Measurement'
        if units is not None:
            self.units = units
        else:
            self.units = 'arb'

        if printMode not in config['measurementPrintModes']:
            warnings.warn('given printMode not in config file, setting to default')
            self.printMode = 'default'
        else:
            self.printMode = printMode
        self._printStr = config['measurementPrintModes'][self.printMode]
        
    def __add__(self, other):
        ''' add two values based on Gaussian error propagation '''
        if isinstance(other, Measurement):
            if other.units != self.units:
                warnings.warn('Units do not match up for addition', Warning)
            newValue = self.value+other.value
            newError = math.hypot(self.error, other.error)
            return Measurement(newValue, newError, name=self.name+'+'+other.name, units=self.units)
        else:
            warnings.warn('Adding a measurement to a normal number', Warning)
            newValue = self.value+other
            newError = self.error
            return Measurement(newValue, newError, name=self.name+'+constant', units=self.units)

    def __radd__(self, other):
        ''' add two values based on Gaussian error propagation '''
        return self.__add__(other)

    def __neg__(self):
        ''' return the negative of the measurement '''
        return Measurement(-self.value,self.error,self.name,self.units)
    
    def __sub__(self, other):
        ''' subtract two values based on Gaussian error propagation '''
        return self.__add__(-other)

    def __rsub__(self, other):
        ''' subtract two values based on Gaussian error propagation '''
        temp = Measurement(-self.value, self.error, self.name, self.units)
        return temp+other
    
    def __mul__(self, other):
        ''' multiply two values based on Gaussian error propagation '''
        if isinstance(other, Measurement):
            newValue = self.value*other.value
            newError = newValue*math.hypot(self.error/self.value, other.error/other.value)
            return Measurement(newValue,newError, name=self.name+'*'+other.name, units=self.units+'*'+other.units)
        else:
            newValue = self.value*other
            newError = self.error*other
            return Measurement(newValue,newError, self.name,self.units)
    def __rmul__(self, other):
        ''' multiply two values based on Gaussian error propagation '''
        return self.__mul__(other)

    def __truediv__(self, other):
        ''' divide two values based on Gaussian error propagation '''
        if isinstance(other, Measurement):
            if other.value == 0:
                raise ZeroDivisionError('Tried to divide by zero')
            newValue = self.value/other.value
            newError = newValue*math.hypot(self.error/self.value, other.error/other.value)
            newName = self.name+'/'+other.name
            newUnits = self.units+'/'+other.units
            return Measurement(newValue,newError,newName,newUnits)
        else:
            if other == 0:
                raise ZeroDivisionError('Tried to divide by zero')
            newValue = self.value/other
            newError = self.error/other
            return Measurement(newValue,newError,self.name,self.units)
        
    def __rtruediv__(self, other):
        ''' divide two values based on Gaussian error propagation '''
        if self.value == 0:
            raise ZeroDivisionError('Tried to divide by zero')
        
        if isinstance(other, Measurement):
            newValue = other.value/self.value
            newError = newValue*math.hypot(self.error/self.value, other.error/other.value)
            newName = other.name+'/'+self.name
            newUnits = other.units+'/'+self.units
            return Measurement(newValue,newError,newName,newUnits)
        else:
            newValue = other/self.value
            newError = other*self.error/self.value**2
            newName = '1/'+self.name
            newUnits = '1/('+self.units+')'
            return Measurement(newValue,newError,newName,newUnits)

    def __pow__(self, p):
        ''' take a power based on Gaussian error propagation '''
        newValue = self.value**p
        newError = abs(p)*(self.value)**(p-1)*self.error

        newName = '('+self.name+')^({})'.format(p)
        newUnits = '('+self.units+')^({})'.format(p)
        return Measurement(newValue,newError,newName,newUnits)

    def SetPrintMode(self, mode):
        ''' set the print mode '''
        if mode not in config['measurementPrintModes']:
            print('Given printMode not in config file, printMode not set')
            print('Possible modes are:')
            for i in config['measurementPrintModes']:
                print('\t',i)
            print('You can define a new mode in config.ini')
        else:
            self.printMode = mode
            self._printStr = config['measurementPrintModes'][self.printMode]

    def __str__(self):
        if self.error > self.value:
            scale = 10**math.floor(math.log10(abs(self.value)))
            tempValue = self.value/scale
            tempError = self.error/scale
            value = round(tempValue)*scale
            error = round(tempError)*scale
            nDigitsError = len(str(error))
        else:
            nDigits = -math.floor(math.log10(self.error))
            nDigitsError = nDigits+int(config['measurement']['errorDigits'])-1
            if nDigits <= 0:
                value = int(round(self.value))
            else:
                value = round(self.value, nDigits)
            if nDigitsError <= 0:
                error = int(round(self.error))
            else:
                error = round(self.error, nDigitsError)
            
        if self.printMode == 'latexSI':
            error = error*10**(-math.floor(math.log10(error)))
            if nDigitsError <= 0:
                error = str(error).replace('.','')[:math.floor(math.log10(self.error))+1]
            else:
                nDigitsCfg = int(config['measurement']['errorDigits'])
                error = str(error).replace('.','')[:nDigitsCfg]
        return self._printStr.format(value,error,self.name,self.units)
    
    def __repr__(self):
        return self.__str__()
    

#############################################################################
# Functions
#############################################################################

def Average(values=None,errors=None, measurements=None, name='avg'):
    ''' compute the average of several measurements '''

    if measurements is not None:
        units = measurements[0].units
        
        value = 0
        norm = 0 # normalization factor
        for m in measurements:
            value += m.value/(m.error**2)
            norm += 1/(m.error**2)
            
            if m.units != units:
                warnings.warn('Taking the average of measurements with different units', Warning)
        avg = value/norm
        error = (1/norm)**0.5
        
        return Measurement(avg,error,name,units)

    elif values is not None:
        if errors is not None:
            value = 0
            norm = 0
            for i in range(len(values)):
                value += values[i]/errors[i]**2
                norm += 1/errors[i]**2
            avg = value/norm
            error = (1/norm)**0.5
            return Measurement(avg,error,name)
        return Measurement(sum(values)/len(values),0,name)

    else:
        print('no data was actually given to Average')
        return None

def ArbFunc(m, f, df=None, units=None, fName=None):
    ''' 
    return the arbitrary function applied to m, if the derivative is not given it is estimated 

    m is the measurement of interest
    f is a function that takes the value of m
    df is the derivative of f (optional)

    unless given, it's assumed that the units returned are arbitrary
    unless given, the name is assumed to be f(m.name), otherwise it's fName(m.name)
    '''

    if df is None:
        # estimate df at m
        e = float_info.epsilon
        h = math.sqrt(e)*m.value
        df = lambda x: (f(x+h)-f(x-h))/(2*h)
    if fName is None:
        fName = 'f'
    
    value = f(m.value)
    error = abs(df(m.value)*m.error)
    name = fName+'('+m.name+')'
    units = units

    return Measurement(value,error,name,units)
    

################################
# Common functions for ArbFunc

def sin(m):
    ''' return the sine of measurement m '''
    f = math.sin
    df = math.cos
    fName = 'sin'
    return ArbFunc(m, f,df, fName=fName)

def cos(m):
    ''' return the cosine of measurement m '''
    f = math.cos
    df =math.sin
    fName = 'cos'
    return ArbFunc(m, f,df, fName=fName)

def tan(m):
    ''' return the tangent of measurement m '''
    f = math.tan
    df = lambda x: 1/(math.cos(x))**2
    fName = 'tan'
    return ArbFunc(m, f,df, fName=fName)

def exp(m):
    ''' return the exponential (base e) of measurement m '''
    f = math.exp
    df = math.exp
    fName = 'exp'
    return ArbFunc(m, f,df, fName=fName)

def log(m, base=math.e):
    ''' return the log of measurement m, default base e '''
    if base == math.e:
        f = math.log
        df = lambda x: 1/x
        fName = 'ln'
        return ArbFunc(m, f,df, fName=fName)
    f = lambda x: math.log(x, base)
    df = lambda x: abs(1/(x*math.log(base)))
    fName = 'log_{}'.format(base)
    return ArbFunc(m, f,df, fName=fName)
    
def pow(m, p):
    ''' return m to the power of p '''
    f = lambda x: x**p
    df = lambda x: p*x**(p-1)
    fName = 'pow_{}'.format(p)
    return ArbFunc(m, f,df, fName=fName)
