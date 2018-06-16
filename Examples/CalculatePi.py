#! /usr/bin/env python3

import math
import random

def CalculatePi(samples=1000):
    # number of samples inside a circle or radius 1
    inside = 0

    # sample random points in a 1x1 box and count the points inside the unit circle
    for i in range(samples):
        x = 2*random.random()-1
        y = 2*random.random()-1
        r = math.hypot(x,y)
        
        if r < 1:
            inside += 1

    # calculate pi
    pi = 4*inside/samples
    return pi

if __name__=='__main__':
    pi = CalculatePi()
    print(pi)
