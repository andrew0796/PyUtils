#! /usr/bin/env python3

'''Base class for launching many jobs at the same time, using GNU parallel'''

import os
import argparse
import tempfile

class Launcher :
    '''Base class for launching many jobs at the same time using GNU parallel

    __init__ takes one parameter, command which is a function that takes one parameter (the run number) and outputs a string with the bash command to run
    '''
    def __init__(self, command):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-j",
                                 help="maximum number of jobs to run at once",
                                 type=int)
        self.parser.add_argument("-n",
                                 help="niceness level to run at",
                                 type=int, default=15)
        self.parser.add_argument("--nohup",
                                 help="run within nohup, useful for remote work",
                                 action='store_true')
        self.parser.add_argument("--nruns",
                                 help="number of runs to do",
                                 type=int, default=1)

        self.command = command

    def Run(self):
        options = self.parser.parse_args()
        
        jobs = options.j
        niceness = options.n
        nohup = options.nohup
        nruns = options.nruns
        
        if jobs is not None and (jobs < 1 or jobs > os.cpu_count()):
            raise ValueError('Number of jobs given not allowed!')
        if nruns < 0:
            raise ValueError('Number of runs to do is less than 0!')

        # create temporary file to feed into parallel, it will be deleted at the end
        jobfile = tempfile.NamedTemporaryFile(mode='w+t',newline='\n',delete=False)
        jobname = jobfile.name

        # write commands to temporary file
        for i in range(nruns):
            jobfile.write(self.command(i)+'\n')
        jobfile.close()

        # launch jobs
        launcher = ''
        limiter = ''
        if nohup:
            launcher += 'nohup '
        if jobs is not None:
            limiter = '-j{}'.format(jobs)
        launcher += 'nice -n {} parallel {} < {}'.format(niceness,limiter,jobname)
        os.system(launcher)

        # remove temporary file
        os.system('rm '+jobname)
        
        return None
