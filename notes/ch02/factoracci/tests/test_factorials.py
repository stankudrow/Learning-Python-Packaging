from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

import pytest

from factoracci import (
    factorial_cython,
    factorial_iterative_memoized,
    factorial_iterative_naive,
    factorial_recursive_memoized,
    factorial_recursive_naive,
)


def _get_factorial_head() -> list[tuple[int, int]]:
    return [
        (0, 1),
        (1, 1),
        (2, 2),
        (3, 6),
        (4, 24),
        (5, 120),
        (6, 720),
        (7, 5040),
        (8, 40320),
        (9, 362880),
        (10, 3628800),
    ]


@pytest.mark.parametrize(
    "func",
    [
        factorial_cython,
        factorial_iterative_memoized,
        factorial_iterative_naive,
        factorial_recursive_memoized,
        factorial_recursive_naive,
    ],
)
def test_invalid_input(func: Callable[[int], int]) -> None:
    with pytest.raises(ValueError):  # noqa: PT011
        func(-1)


@pytest.mark.parametrize(
    ("n", "expected"),
    _get_factorial_head(),
)
def test_naive_factorials(n: int, expected: int) -> None:
    res_iter = factorial_iterative_naive(n)
    res_rec = factorial_recursive_naive(n)
    assert res_iter == res_rec == expected


@pytest.mark.parametrize(
    ("n", "expected"),
    _get_factorial_head(),
)
def test_memoized_factorials(n: int, expected: int) -> None:
    res_iter = factorial_iterative_memoized(n)
    res_rec = factorial_recursive_memoized(n)
    assert res_iter == res_rec == expected


@pytest.mark.parametrize(
    ("n", "expected"),
    _get_factorial_head(),
)
def test_cythonic_factorial(n: int, expected: int) -> None:
    assert factorial_cython(n) == expected


@pytest.mark.parametrize(
    "func",
    [factorial_iterative_naive, factorial_iterative_memoized, factorial_cython],
    ids=lambda f: f.__name__,
)
@pytest.mark.parametrize("n", [1, 10, 50])
@pytest.mark.bench
def test_factorial_performance(
    func: Callable[[int], int],
    n: int,
    benchmark,  # noqa: ANN001
) -> None:
    result = benchmark(func, n)
    assert result == func(n)
