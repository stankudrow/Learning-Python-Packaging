from contextlib import suppress

import pytest

from factoracci import (
    factorial_iterative_memoized,
    factorial_iterative_naive,
    factorial_recursive_memoized,
    factorial_recursive_naive,
)

_CYTHON_AVAILABLE = False
with suppress(ImportError):
    from factoracci import factorial_cython

    _CYTHON_AVAILABLE = True


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


@pytest.mark.skipif(
    not _CYTHON_AVAILABLE,
    reason="Cython extension not built/importable; skipping Cython-based tests",
)
@pytest.mark.parametrize(
    ("n", "expected"),
    _get_factorial_head(),
)
def test_cython_factorial(n: int, expected: int) -> None:
    assert factorial_cython(n) == expected
