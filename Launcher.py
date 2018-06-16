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

        self.options = None
        self.jobs = None
        self.niceness = None
        self.nohup = None
        self.nruns = None

    def Parse(self):
        self.options = self.parser.parse_args()
        
        self.jobs = self.options.j
        self.niceness = self.options.n
        self.nohup = self.options.nohup
        self.nruns = self.options.nruns
        
        return None
        
    def Run(self):
        if self.options is None:
            self.Parse()
        
        if self.jobs is not None and (self.jobs < 1 or self.jobs > os.cpu_count()):
            raise ValueError('Number of jobs given not allowed!')
        if self.nruns < 0:
            raise ValueError('Number of runs to do is less than 0!')

        # create temporary file to feed into parallel, it will be deleted at the end
        jobfile = tempfile.NamedTemporaryFile(mode='w+t',newline='\n',delete=False)
        jobname = jobfile.name

        # write commands to temporary file
        for i in range(self.nruns):
            jobfile.write(self.command(i)+'\n')
        jobfile.close()

        # launch jobs
        launcher = ''
        limiter = ''
        if self.nohup:
            launcher += 'nohup '
        if self.jobs is not None:
            limiter = '-j{}'.format(self.jobs)
        launcher += 'nice -n {} parallel {} < {}'.format(self.niceness,limiter,jobname)
        os.system(launcher)

        # remove temporary file
        os.system('rm '+jobname)
        
        return None
