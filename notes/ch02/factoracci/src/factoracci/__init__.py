from contextlib import suppress

from factoracci.factorials import (
    factorial_iterative_memoized,
    factorial_iterative_naive,
    factorial_recursive_memoized,
    factorial_recursive_naive,
)

__all__ = [
    "factorial_iterative_memoized",
    "factorial_iterative_naive",
    "factorial_recursive_memoized",
    "factorial_recursive_naive",
]

with suppress(ImportError):
    from factoracci._factoracci import factorial as factorial_cython

    __all__ += ["factorial_cython"]
