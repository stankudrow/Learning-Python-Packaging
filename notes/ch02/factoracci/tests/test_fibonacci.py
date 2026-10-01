import pytest

from factoracci.fibonacci import (
    fibonacci_iterative_memoized,
    fibonacci_iterative_naive,
    fibonacci_recursive_memoized,
    fibonacci_recursive_naive,
    gen_fibonacci,
)


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
