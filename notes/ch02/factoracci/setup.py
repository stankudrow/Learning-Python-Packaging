from pathlib import Path

from Cython.Build import cythonize  # noqa: F401
from setuptools import Extension, find_packages, setup

# - https://setuptools.pypa.io/en/latest/userguide/ext_modules.html
# - https://setuptools.pypa.io/en/stable/deprecated/distutils/setupscript.html
SRC_DIR = Path("src") / "factoracci"


extensions = [
    Extension(
        name="factoracci._factoracci",
        # paths must bot be absolute, but relative to this "setup.py"
        sources=[str(SRC_DIR / "_factoracci.pyx")],
    )
]

setup(
    name="Factoracci",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    ext_modules=extensions,
)
