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
        self.parser.add_argument("--bar",
                                 help="display parallel progress bar",
                                 action='store_true')
        self.parser.add_argument("--delay",
                                 help="amount of delay between starting jobs",
                                 type=float)
        self.parser.add_argument("--dry_run",
                                 help="print out each command to be run, but do not run anything",
                                 action='store_true')
        self.parser.add_argument("--parallel_args",
                                 help="additional arguments to pass to parallel",
                                 type=str)

        self.command = command

        self.options = None
        self.jobs = None
        self.niceness = None
        self.nohup = None
        self.nruns = None
        self.bar = None
        self.delay = None
        self.dryRun = None
        self.parallelArgs = None

    def Parse(self):
        self.options = self.parser.parse_args()
        
        self.jobs = self.options.j
        self.niceness = self.options.n
        self.nohup = self.options.nohup
        self.nruns = self.options.nruns
        self.bar = self.options.bar
        self.delay = self.options.delay
        self.dryRun = self.options.dry_run
        self.parallelArgs = self.options.parallel_args
        
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
        additionalArgs = ''
        if self.nohup:
            launcher += 'nohup '
        if self.jobs is not None:
            limiter = '-j{}'.format(self.jobs)
        if self.bar:
            additionalArgs += '--bar '
        if self.delay is not None:
            additionalArgs += '--delay {} '.format(self.delay)
        if self.dryRun:
            additionalArgs += '--dry-run '
        if self.parallelArgs is not None:
            additionalArgs += self.parallelArgs
        launcher += 'parallel --nice {} {} {} < {}'.format(self.niceness,additionalArgs,limiter,jobname)
        print(launcher)
        os.system(launcher)

        # remove temporary file
        os.system('rm '+jobname)
        
        return None
