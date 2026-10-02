"""Implementations of Fibonacci functions.

References:
    - https://en.wikipedia.org/wiki/Fibonacci_sequence
    - https://en.wikipedia.org/wiki/Recursion
    - https://en.wikipedia.org/wiki/Dynamic_programming
"""

from functools import cache
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator


def fibonacci_recursive_naive(nth: int) -> int:
    """Compute the `nth` Fibonacci number using a naive recursive approach.

    Args:
        nth: The number from the sequence of Fibonacci numbers.

    Raises:
        ValueError: If `nth` is non-positive.

    Returns:
        The `nth` Fibonacci number.
    """
    if nth < 1:
        msg = "n must be a positive integer"
        raise ValueError(msg) from None
    if nth < 3:
        return 1
    return _fibo_rec(nth - 1) + _fibo_rec(nth - 2)


@cache
def _fibo_rec(nth: int) -> int:
    if nth < 3:
        return 1
    return _fibo_rec(nth - 1) + _fibo_rec(nth - 2)


def fibonacci_recursive_memoized(nth: int) -> int:
    """Compute recursively the `nth` Fibonacci number using memoisation.

    Args:
        nth: The number from the sequence of Fibonacci numbers.

    Raises:
        ValueError: If `nth` is non-positive.

    Returns:
        The `nth` Fibonacci number.
    """
    if nth < 1:
        msg = "n must be a positive integer"
        raise ValueError(msg) from None
    return _fibo_rec(nth)


### iterative versions


def fibonacci_iterative_naive(nth: int) -> int:
    """Compute iteratively the `nth` Fibonacci number.

    Args:
        nth: The number from the sequence of Fibonacci numbers.

    Raises:
        ValueError: If `nth` is non-positive.

    Returns:
        The `nth` Fibonacci number.
    """
    if nth < 1:
        msg = "n must be a positive integer"
        raise ValueError(msg) from None
    if nth < 3:
        return 1
    a, b = 1, 1
    for _ in range(2, nth):
        a, b = b, a + b
    return b


_dp: dict[int, int] = {0: 1, 1: 1, 2: 1}


def fibonacci_iterative_memoized(nth: int) -> int:
    """Compute iteratively the `nth` Fibonacci number using memoisation.

    Args:
        nth: The number from the sequence of Fibonacci numbers.

    Raises:
        ValueError: If `nth` is non-positive.

    Returns:
        The `nth` Fibonacci number.
    """
    if nth < 1:
        msg = "n must be a positive integer"
        raise ValueError(msg) from None
    if nth in _dp:
        return _dp[nth]
    last = tuple(_dp)[-1]
    for i in range(last + 1, nth + 1):
        _dp[i] = _dp[i - 1] + _dp[i - 2]
    return _dp[nth]


def gen_fibonacci() -> Generator[int]:
    """Generate Fibonacci numbers using an iterative approach.

    Yields:
        The next Fibonacci number in the sequence.
    """
    a, b = 1, 1
    while True:
        yield a
        a, b = b, a + b
