# PyUtils

General utilities written in python, so far mostly for data analysis

## MeasurementErrors.py
Defines a `Measurement` class that acts as a regular number. Errors are calculated using Gaussian error propagation, assuming covariances are 0. Includes several functions on measurements

## Fitting.py
Common functions for fitting data, based around [scipy](https://docs.scipy.org/doc/scipy/reference/) fitting

## Launcher.py
Defines a `Launcher` class that can be used to launch multiple jobs in parallel. Could be used for instance, if you want to run `./myExecutable myInput` for several different inputs in parallel. See [Examples](Examples) for examples.