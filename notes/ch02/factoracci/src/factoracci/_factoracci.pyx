# cython: language_level=3

cimport cython


@cython.overflowcheck(True)
def factorial(int n):
    if n < 0:
        msg = f"{n} < 0"
        raise ValueError(msg) from None
    if n < 2:
        return 1
    cdef int i
    cdef object f = 1
    for i in range(2, n + 1):
        f *= i
    return f
