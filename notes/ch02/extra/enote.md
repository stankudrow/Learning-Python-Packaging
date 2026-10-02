# Дополнительно

В директории "extra":

1. `uv venv --python 3.12` и задействование виртуального окружения;
2. `uv pip install ipykernel` - установка пакета управления IPython ядрами;
3. `python3 -m ipykernel install --user --name=ch02_extra --display-name="Chapter02 (Extra)"` - регистрация ядра, которое будет нацелено на Python из виртуального окружения;
4. `uv pip install cython` - установка пакета [Cython](https://cython.org/);
5. `jupyter notebook` - запуск "Jupyter Notebook" сервера.

И вот в ячейке файла [cython.ipynb](./cython.ipynb) я хочу выполнить команду `%load_ext cython` и...да что ж такое:

```
---------------------------------------------------------------------------
ModuleNotFoundError                       Traceback (most recent call last)
Cell In[1], line 1
----> 1 get_ipython().run_line_magic('load_ext', 'Cython')

File ~/Projects/Learning-Python-Packaging/notes/ch02/extra/.venv/lib/python3.12/site-packages/Cython/__init__.py:11, in load_ipython_extension(ip)
      9 def load_ipython_extension(ip: Any) -> None:
     10     """Load the extension in IPython."""
---> 11     from .Build.IpythonMagic import CythonMagics  # pylint: disable=cyclic-import
     12     ip.register_magics(CythonMagics)

File ~/Projects/Learning-Python-Packaging/notes/ch02/extra/.venv/lib/python3.12/site-packages/Cython/Build/IpythonMagic.py:52
     50 import time
     51 import copy
---> 52 import distutils.log
     53 import textwrap
     55 IO_ENCODING = sys.getfilesystemencoding()

ModuleNotFoundError: No module named 'distutils'
```

Потому что модуль [distutils](https://docs.python.org/3.14/library/distutils.html#module-distutils) был удалён в Python 3.12 согласно [PEP 632](https://peps.python.org/pep-0632/). Решение: установить [setuptools](https://setuptools.pypa.io/en/latest/) (`uv pip install setuptools`), потому что он предоставляет замену для `distutils` и умеет подменять его во "внесках" (импортах).
