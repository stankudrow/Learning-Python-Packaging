from typing import Callable  # noqa: UP035

import pytest

from factoracci import (
    fibonacci_cython,
    fibonacci_iterative_memoized,
    fibonacci_iterative_naive,
    fibonacci_recursive_memoized,
    fibonacci_recursive_naive,
    gen_fibonacci,
)


@pytest.mark.parametrize(
    "func",
    [
        fibonacci_cython,
        fibonacci_iterative_memoized,
        fibonacci_iterative_naive,
        fibonacci_recursive_memoized,
        fibonacci_recursive_naive,
    ],
)
@pytest.mark.parametrize("n", [0, -1])
def test_invalid_input(func: Callable, n: int) -> None:
    with pytest.raises(ValueError):  # noqa: PT011
        func(n)


def _get_fibonacci_head() -> list[tuple[int, int]]:
    return [
        (1, 1),
        (2, 1),
        (3, 2),
        (4, 3),
        (5, 5),
        (6, 8),
        (7, 13),
        (8, 21),
        (9, 34),
        (10, 55),
    ]


@pytest.mark.parametrize(
    ("nth", "expected"),
    _get_fibonacci_head(),
)
def test_fibonacci_naive(nth: int, expected: int) -> None:
    res_rec = fibonacci_recursive_naive(nth)
    res_iter = fibonacci_iterative_naive(nth)
    assert res_rec == res_iter == expected


@pytest.mark.parametrize(
    ("nth", "expected"),
    _get_fibonacci_head(),
)
def test_memoized_fibonacci(nth: int, expected: int) -> None:
    res1 = fibonacci_recursive_memoized(nth)
    res2 = fibonacci_iterative_memoized(nth)
    assert res1 == res2 == expected


def test_gen_fibonacci() -> None:
    gen = gen_fibonacci()
    for _, expected in _get_fibonacci_head():
        assert next(gen) == expected


@pytest.mark.parametrize(
    ("nth", "expected"),
    _get_fibonacci_head(),
)
def test_cythonic_fibonacci(nth: int, expected: int) -> None:
    assert fibonacci_cython(nth) == expected


@pytest.mark.parametrize(
    "func",
    [fibonacci_iterative_naive, fibonacci_iterative_memoized, fibonacci_cython],
    ids=lambda f: f.__name__,
)
@pytest.mark.parametrize("n", [1, 10, 50])
@pytest.mark.bench
def test_fibonacci_performance(
    func: Callable[[int], int],
    n: int,
    benchmark,  # noqa: ANN001
) -> None:
    result = benchmark(func, n)
    assert result == func(n)
