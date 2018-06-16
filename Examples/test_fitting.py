#! /usr/bin/env python3

'''test Fitting.py by generating data according to a Gaussian and fitting it'''

import Fitting

import matplotlib.pyplot as plt
import numpy as np

def test_fitting():
    # parameters for the Gaussian
    mean = 4.5
    sigma = 1.2
    A = 6.7
    C = 0.2

    # number of data points and range
    n = 1000
    xMin = -2
    xMax = 12
    
    # truth data
    xTrue = np.linspace(xMin, xMax, n)
    yTrue = Fitting.gaussianCF(xTrue, A,mean,sigma,C)

    # sample data
    noiseSD = 0.2
    x = xTrue + np.random.normal(0,noiseSD,n)
    y = yTrue + np.random.normal(0,noiseSD,n)

    # make a crude guess based on the random data
    guess = [0,0,0,0]
    guess[0] = max(y)-min(y)
    guess[1] = np.mean(x)
    guess[2] = np.std(x)
    guess[3] = min(y)
    
    # fit the data
    params,errors = Fitting.FitData('gauss', x,y, noiseSD*np.ones(n), noiseSD*np.ones(n), guess)
    paramsTrue,errorsTrue = Fitting.FitData('gauss', xTrue,yTrue, guess=guess)

    # plot the data
    plt.figure('test_fitting')
    plt.subplot(121)
    plt.title('Fitting Truth Data')
    plt.plot(xTrue,yTrue, label='Truth Data')
    plt.plot(xTrue,Fitting.gaussianODR(paramsTrue,xTrue), label='Fitted Data')
    plt.legend(loc=0)
    plt.subplot(122)
    plt.title('Fitting Noisy Data')
    plt.plot(x,y,'.', label='Noisy Data')
    plt.plot(x,Fitting.gaussianODR(params,x), label='Fitted Data')
    plt.plot(xTrue,yTrue, label='Truth Data')
    plt.legend(loc=0)
    plt.show()
        
    # print out the results
    print('Generated {} test points for a Gaussian'.format(n))
    print('True parameters:')
    print('Amplitude = {}\nMean = {}\nStandard Deviation = {}\nConstant = {}\n'.format(A,mean,sigma,C))
    print('Fit to truth data:')
    print('Amplitude = {0}+/-{4}\nMean = {1}+/-{5}\nStandard Deviation = {2}+/-{6}\nConstant = {3}+/-{7}\n'.format(*paramsTrue, *errorsTrue))
    print('Fit to noisy data:')
    print('Amplitude = {0}+/-{4}\nMean = {1}+/-{5}\nStandard Deviation = {2}+/-{6}\nConstant = {3}+/-{7}'.format(*params, *errors))

    return None

if __name__=='__main__':
    test_fitting()
