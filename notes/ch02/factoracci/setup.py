from pathlib import Path

from Cython.Build import cythonize
from setuptools import Extension, find_packages, setup

# __file__ == this file !
ROOT = Path(__file__).parent

SRC_DIR = ROOT / "src" / "factoracci"


extensions = [
    Extension(
        name="factoracci._factoracci",
        # paths must bot be absolute, but relative to this "setup.py"
        sources=[str(p.relative_to(ROOT)) for p in [SRC_DIR / "_factoracci.pyx"]],
    )
]

setup(
    name="Factoracci",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    ext_modules=cythonize(
        extensions,
        compiler_directives={"language_level": 3},
    ),
)
