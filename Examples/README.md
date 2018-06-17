# Examples

Basic tests/examples, not extensive in any way

## `test_launcher.py`
Simple test/example for `Launcher.py`
Print out Pascal's triangle for a given number of rows
In a terminal window run `python3 test_launcher.py --nruns=<n>` to print out the first `n` rows of Pascal's triangle

## `test_launcher2.py`
Simple test/example for `Launcher.py`
Calculate pi using a simple monte carlo method defined in `CalculatePi.py`
In a terminal window run `python3 test_launcher2.py --nruns <n> -j <jobs>` to calculate pi with`n` runs in parallel on `jobs` processors

## `test_fitting.py`
Simple test/example for `Fitting.py`
Fit a Gaussian to sample data. Plot and print out the results
In a terminal window run `python3 test_fitting.py`

## `test_measurement.py`
Simple test/example for `MeasurementErrors.py`
Generate data for a simple experiment to measure gravity. Calculate acceleration due to gravity from several measurements and print out the results. Also explicitly calculates the error in each calculation to validate the results.

## `test_general.py`
Simple test/example for `General.py`
Not yet completed