# Factoracci

Factorials + Fibonacci algorithms.

## Notes

Feel free to look at the following files concerning project cythonisation:

- [setup.py](./setup.py) is recommended for cythonising Python packages yet may be avoided;
- Cython is dealared to be a build-time dependency in the `[build-system]` section (see [pyproject.toml](./pyproject.toml)).

To install this package with Cython optional dependency (extra): `pip install "factoracci[cy]"` (or just `pip install ".[cy]"`).


### Coverage

100% - cool, but this package is not complex, so here this rate is reasonable.

```shell
Name                           Stmts   Miss Branch BrPart    Cover   Missing
----------------------------------------------------------------------------
src/factoracci/factorials.py      41      0     20      0  100.00%
src/factoracci/fibonacci.py       45      0     20      0  100.00%
----------------------------------------------------------------------------
TOTAL                             86      0     40      0  100.00%
Coverage HTML written to dir htmlcov
Required test coverage of 80.0% reached. Total coverage: 100.00%
```

### Benchmarking

Separated outputs.


- Factorial:

```shell
------------------------------- benchmark 'func=<cyfunction factorial at 0x7e5d5c5a8f50>': 3 tests ------------------------------
Name (time in ns)                                   Min                  Mean              StdDev                Median
---------------------------------------------------------------------------------------------------------------------------------
test_factorial_performance[1-factorial]         37.7520 (1.0)         39.7813 (1.0)        6.1978 (1.0)         39.1120 (1.0)
test_factorial_performance[10-factorial]       111.5099 (2.95)       116.1489 (2.92)      11.9838 (1.93)       114.3200 (2.92)
test_factorial_performance[50-factorial]     1,382.5011 (36.62)    1,489.3805 (37.44)    232.5328 (37.52)    1,457.7490 (37.27)
---------------------------------------------------------------------------------------------------------------------------------

---------------------------- benchmark 'func=<function factorial_iterative_memoized at 0x7e5d5c45a610>': 3 tests ----------------------------
Name (time in ns)                                                    Min                Mean             StdDev              Median
---------------------------------------------------------------------------------------------------------------------------------------------
test_factorial_performance[1-factorial_iterative_memoized]       74.3400 (1.0)       77.2657 (1.0)      10.0686 (1.0)       75.9500 (1.0)
test_factorial_performance[10-factorial_iterative_memoized]     149.9939 (2.02)     160.9758 (2.08)     59.0099 (5.86)     159.9983 (2.11)
test_factorial_performance[50-factorial_iterative_memoized]     149.9939 (2.02)     160.6437 (2.08)     93.1882 (9.26)     159.9983 (2.11)
---------------------------------------------------------------------------------------------------------------------------------------------

-------------------------------- benchmark 'func=<function factorial_iterative_naive at 0x7e5d5c45a4b0>': 3 tests -------------------------------
Name (time in ns)                                                   Min                  Mean              StdDev                Median
-------------------------------------------------------------------------------------------------------------------------------------------------
test_factorial_performance[1-factorial_iterative_naive]         57.4100 (1.0)         59.3921 (1.0)        8.9547 (1.0)         58.4100 (1.0)
test_factorial_performance[10-factorial_iterative_naive]       273.2777 (4.76)       284.3016 (4.79)      42.2823 (4.72)       279.9445 (4.79)
test_factorial_performance[50-factorial_iterative_naive]     1,632.9989 (28.44)    1,722.1388 (29.00)    296.1522 (33.07)    1,683.3340 (28.82)
-------------------------------------------------------------------------------------------------------------------------------------------------
```

- Fibonacci:

```shell
--------------------------- benchmark 'func=<cyfunction fibonacci at 0x7e5d5c595440>': 3 tests ---------------------------
Name (time in ns)                                 Min                Mean             StdDev              Median
--------------------------------------------------------------------------------------------------------------------------
test_fibonacci_performance[1-fibonacci]       37.5462 (1.0)       39.4942 (1.0)       6.6515 (1.0)       38.7311 (1.0)
test_fibonacci_performance[10-fibonacci]      75.0400 (2.00)      79.1870 (2.01)     10.6465 (1.60)      77.6500 (2.00)
test_fibonacci_performance[50-fibonacci]     485.9001 (12.94)    508.0487 (12.86)    70.9170 (10.66)    497.4499 (12.84)
--------------------------------------------------------------------------------------------------------------------------

---------------------------- benchmark 'func=<function fibonacci_iterative_memoized at 0x7e5d5c45afb0>': 3 tests ----------------------------
Name (time in ns)                                                    Min                Mean             StdDev              Median
---------------------------------------------------------------------------------------------------------------------------------------------
test_fibonacci_performance[1-fibonacci_iterative_memoized]       74.0400 (1.0)       77.0868 (1.0)      10.2971 (1.0)       75.7400 (1.0)
test_fibonacci_performance[10-fibonacci_iterative_memoized]     149.9939 (2.03)     159.3629 (2.07)     56.0039 (5.44)     159.9983 (2.11)
test_fibonacci_performance[50-fibonacci_iterative_memoized]     149.9939 (2.03)     162.7267 (2.11)     82.4099 (8.00)     159.9983 (2.11)
---------------------------------------------------------------------------------------------------------------------------------------------

----------------------------- benchmark 'func=<function fibonacci_iterative_naive at 0x7e5d5c45ae50>': 3 tests ----------------------------
Name (time in ns)                                                 Min                Mean              StdDev              Median
-------------------------------------------------------------------------------------------------------------------------------------------
test_fibonacci_performance[1-fibonacci_iterative_naive]       57.9100 (1.0)       60.6963 (1.0)       10.3605 (1.0)       59.1100 (1.0)
test_fibonacci_performance[10-fibonacci_iterative_naive]     219.4998 (3.79)     228.8318 (3.77)      38.5376 (3.72)     225.4092 (3.81)
test_fibonacci_performance[50-fibonacci_iterative_naive]     912.1999 (15.75)    947.1745 (15.61)    101.8830 (9.83)     927.2499 (15.69)
-------------------------------------------------------------------------------------------------------------------------------------------
```

```shell
Legend:
  Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
  OPS: Operations Per Second, computed as 1 / Mean
```

Memoisation is powerful! Here (and keep that in mind), Cython-based memoisation beats the naive approach in both cases, yet memosed solution overwhelms even cythonic implementations.
