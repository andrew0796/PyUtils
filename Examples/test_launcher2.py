#! /usr/bin/env python3

'''Run several jobs in parallel to calculate pi using monte carlo methods'''

from Launcher import *

import os

def test_launcher2():
    # create the output file
    os.system('touch CalculatePi.txt')
    
    # set command
    command = lambda x: 'python3 CalculatePi.py >> CalculatePi.txt'
    launcher = Launcher(command)

    # parse the arguments
    launcher.Parse()

    # run the launcher
    launcher.Run()

    # get the average of pi from the output file
    pi = 0
    nruns = launcher.nruns
    with open('CalculatePi.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if line != '':
                pi += float(line)
    pi /= nruns

    # print out the results
    print('Calculated pi using a monte carlo method with {} runs'.format(nruns))
    print('pi ~ {}'.format(pi))

    # delete the file created
    os.system('rm CalculatePi.txt')

    return None

if __name__=='__main__':
    test_launcher2()
    
