#! /usr/bin/env python3

'''Simple test/example for Launcher.py
Run with `python3 test_launcher.py --nruns 4` to print out the following
    1
   1-1
  1-2-1
 1-3-3-1
1-4-6-4-1
'''

from Launcher import *

import math

def test_launcher():
    '''print out pascal's triangle as a test'''

    # dummy command to initialize with, reset the command later once we've figured out how many rows to do
    command = lambda x: ''
    launcher = Launcher(command)

    # parse command line arguments for launcher to get the number of rows (as nruns)
    launcher.Parse()
    launcher.nruns += 1
    rows = launcher.nruns

    # function to produce rows of pascal's triangle
    def Pascal(row):
        choose = lambda n, k: math.factorial(n)//(math.factorial(k)*math.factorial(n-k))
        s = ' '.join(map(lambda x: str(choose(row, x)), range(row+1)))
        s = ' '*(rows-row)+s
        command = 'echo "{}"'.format(s)
        return command

    # set command to be Pascal
    launcher.command = Pascal

    # run the launcher
    launcher.Run()

    return None

if __name__=='__main__':
    test_launcher()
