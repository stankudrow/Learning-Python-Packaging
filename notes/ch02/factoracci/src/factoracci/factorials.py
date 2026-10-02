"""Implementations of factorial functions.

References:
    - https://en.wikipedia.org/wiki/Factorial
    - https://en.wikipedia.org/wiki/Recursion
    - https://en.wikipedia.org/wiki/Dynamic_programming
"""

from functools import cache


def factorial_recursive_naive(n: int) -> int:
    """Compute the factorial of `n` using a naive recursive approach.

    Args:
        n: The number to compute the factorial of.

    Raises:
        ValueError: If `n` is negative.

    Returns:
        The factorial of `n`.
    """
    if n < 0:
        msg = "n must be non-negative"
        raise ValueError(msg) from None
    if n < 2:
        return 1
    return n * factorial_recursive_naive(n - 1)


@cache
def _fact_rec_memo(n: int) -> int:
    if n < 2:
        return 1
    return n * _fact_rec_memo(n - 1)


def factorial_recursive_memoized(n: int) -> int:
    """Compute the factorial of `n` recursively using memoisation.

    Args:
        n: The number to compute the factorial of.

    Raises:
        ValueError: If `n` is negative.

    Returns:
        The factorial of `n`.
    """
    if n < 0:
        msg = "n must be non-negative"
        raise ValueError(msg) from None
    return _fact_rec_memo(n)


### Iterative versions


def factorial_iterative_naive(n: int) -> int:
    """Compute the factorial of `n` using a naive iterative approach.

    Args:
        n: The number to compute the factorial of.

    Raises:
        ValueError: If `n` is negative.

    Returns:
        The factorial of `n`.
    """
    if n < 0:
        msg = "n must be non-negative"
        raise ValueError(msg) from None
    if n < 2:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


_dp: dict[int, int] = {0: 1, 1: 1, 2: 2}


def factorial_iterative_memoized(n: int) -> int:
    """Compute the factorial of `n` iteratively using memoisation.

    Args:
        n: The number to compute the factorial of.

    Raises:
        ValueError: If `n` is negative.

    Returns:
        The factorial of `n`.
    """
    if n < 0:
        msg = "n must be non-negative"
        raise ValueError(msg) from None
    if n in _dp:
        return _dp[n]
    start = len(_dp) - 1
    result = _dp[start]
    for i in range(start + 1, n + 1):
        result *= i
        _dp[i] = result
    return result
