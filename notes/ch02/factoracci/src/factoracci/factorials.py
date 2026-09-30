"""Implementations of factorial functions.

References:
    - https://en.wikipedia.org/wiki/Factorial
    - https://en.wikipedia.org/wiki/Recursion
    - https://en.wikipedia.org/wiki/Dynamic_programming
"""

from functools import lru_cache


def _fact_rec(n: int) -> int:
    if n < 2:
        return 1
    return n * _fact_rec(n - 1)


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
    return _fact_rec(n)


def factorial_recursive_memoized_top_down(n: int) -> int:
    """Compute the factorial of `n` recursively using memoisation technique.

    Memoisation = caching the results of function calls.
    If the result is already cached, it is returned immediately,
    otherwise the result is computed and stored in the related storage.

    This implementation relies on the top-down approach of dynamic programming (DP).
    Here the "Least Recently Used" (LRU) caching technique is used.

    Args:
        n: The number to compute the factorial of.

    Raises:
        ValueError: If `n` is negative.

    Returns:
        The factorial of `n`.

    References:
        - https://en.wikipedia.org/wiki/Memoization
        - https://en.wikipedia.org/wiki/Cache_replacement_policies#LRU
    """
    # The actual function is memoised and "enclosed" here,
    # because there is no need to cache rubbish values of `n`.
    fact_rec_lru = lru_cache(maxsize=128)(_fact_rec)

    if n < 0:
        msg = "n must be non-negative"
        raise ValueError(msg) from None
    return fact_rec_lru(n)


### Iterative versions


def _fact_iter(n: int) -> int:
    if n < 2:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


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
    return _fact_iter(n)


def factorial_iterative_memoized(n: int) -> int:
    """Compute the factorial of `n` iteratively using memoisation technique.

    Memoisation = caching the results of function calls.
    If the result is already cached, it is returned immediately,
    otherwise the result is computed and stored in the related storage.

    This implementation relies on the "Least Recently Used" (LRU) caching technique.

    Args:
        n: The number to compute the factorial of.

    Raises:
        ValueError: If `n` is negative.

    Returns:
        The factorial of `n`.

    References:
        - https://en.wikipedia.org/wiki/Memoization
        - https://en.wikipedia.org/wiki/Cache_replacement_policies#LRU
    """
    # The actual function is memoised,
    # because there is no need to cache rubbish values of `n`.
    fact_iter_lru = lru_cache(maxsize=128)(_fact_iter)

    if n < 0:
        msg = "n must be non-negative"
        raise ValueError(msg) from None
    return fact_iter_lru(n)
