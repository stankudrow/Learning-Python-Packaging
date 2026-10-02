# Factoracci

Factorials + Fibonacci.

## Notes

To build Cython modules:

- [setup.py](./setup.py) is recommended for cythonising Python packages;
- Cython should be a dependency in the `[build-system]` section (see [pyproject.toml](./pyproject.toml)).

To install this package with Cython optional dependency (extra): `pip install factoracci[cy]` (or just `uv pip install ".[cy]"`).
