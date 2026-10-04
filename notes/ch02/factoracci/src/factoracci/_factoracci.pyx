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


def fibonacci(int nth):
    if nth < 1:
        msg = "n must be a positive integer"
        raise ValueError(msg) from None
    if nth < 3:
        return 1
    cdef object a = 1, b = 1
    for _ in range(2, nth):
        a, b = b, a + b
    return b
