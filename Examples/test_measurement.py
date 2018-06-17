#! /usr/bin/env python3

'''test MeasurementErrors by analyzing a simple gravity experiment
The experiment measures the time it takes for a theoretical point particle of mass m to fall
We expect that the particle's position as a function of time is y(t)=y(0)-0.5*g*t^2
Thus, the particle hits the ground at t=sqrt(2*y(0)/g) which is what we measure
We then calculate g as g=2*y(0)/t^2

Explicitly calculating out the errors we get dg=g*sqrt((dy0/y0)^2 + (2*dt/t)^2) for each measurement of g
For the average error we get dgAvg=sqrt(1/sum_i(1/dg_i^2))
'''

import MeasurementErrors as me

import math
import random

def test_measurement():
    # experimental parameters
    n = 10    # number of measurements
    dt = 0.05 # [s] uncertainty in timing (1 sigma)
    g = 9.81  # [m/s^2] acceleration due to gravity (expected result)
    y0 = 3.0  # [m] initial height of the particle
    dy = 0.01 # [m] uncertainty in y0 measurement (1 sigma)
    
    # calculate the true time
    tTrue = math.sqrt(2*y0/g) # [s]
    
    # define several time measurements and one height measurement
    times = [me.Measurement(random.gauss(tTrue, dt), dt, units='s', name='trial '+str(i)) for i in range(n)]
    height = me.Measurement(random.gauss(y0, dy), dy, units='m', name='height')
    
    # calculate g for each measurement time
    gravity = [2*height/(t**2) for t in times]

    # calculate the errors in each measurement of g explicitly
    gravityError = [gravity[i].value*math.sqrt( (dy/height.value)**2 + (2*dt/times[i].value)**2 )
                    for i in range(n)]

    # calculate the average of g
    gAvg = me.Average(measurements=gravity, name='gAvg')

    # calculate the average of g explicitly
    gAvgCalc = sum([gravity[i].value/gravityError[i]**2 for i in range(n)])/sum([1/gravityError[i]**2 for i in range(n)])
    gAvgError = math.sqrt( 1/sum([1/gravityError[i]**2 for i in range(n)]) )
    
    # print out results
    print('Performed {} trials to measure g dropping a particle from height {}m'.format(n,y0))
    print('tTrue = {}s'.format(tTrue))
    print('g = {}m/s^2'.format(g))
    print('\n'+'*'*30+'\n  Measurements\n'+'*'*30)
    print(height)
    for t in times:
        print(t)
    print('*'*30+'\n')
    print('\n'+'*'*30+'\n  Results\n'+'*'*30)
    for i in range(n):
        print(gravity[i], '\tExplicitly:',gravity[i].value,'+/-',gravityError[i])
    print('*'*30+'\n')
    print('\n'+'*'*30+'\n  Final Result\n'+'*'*30)
    print(gAvg, '\tExplicitly:',gAvgCalc,'+/-',gAvgError)
    print('*'*30+'\n')

    return None

if __name__=='__main__':
    test_measurement()
    
