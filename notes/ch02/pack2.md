# Cборка с ничего

Не забываю про `uv venv` и создаю директорию `pack2` (естественно она пустая) и запуск `uv build pack2` даёт:

```shell
╰─➤  mkdir pack2
(ch02) ╭─X@D ~/Projects/Learning-Python-Packaging/notes/ch02  ‹add-ch03*›
╰─➤  uv build pack2
Building source distribution...
error: Failed to build `~/Projects/Learning-Python-Packaging/notes/ch02/pack2`
  Caused by: ~/Projects/Learning-Python-Packaging/notes/ch02/pack2 does not appear to be a Python project, as neither `pyproject.toml` nor `setup.py` are present in
             the directory
```

Хорошо есть подсказка что нужно сделать, поэтому создаю (пока что пустосодержательный) файл "pyproject.toml" (ибо [PEP-621][pep621]) в директории "pack2".

```shell
─➤  uv build pack2
Building source distribution...
warning: `~/Projects/Learning-Python-Packaging/notes/ch02/pack2` does not appear to be a Python project, as the `pyproject.toml` does not include a `[build-system]` table, and neither `setup.py` nor `setup.cfg` are present in the directory
running egg_info
...
warning: sdist: standard file not found: should have one of README, README.rst, README.txt, README.md

running check
warning: check: missing required meta-data: name

...
Building wheel from source distribution...
running egg_info
...

Successfully built pack2/dist/unknown-0.0.0.tar.gz
Successfully built pack2/dist/unknown-0.0.0-py3-none-any.whl
```

Хорошо, добавлю README.md и накину в pyproject.toml раздел:

```toml
[build-system]
requires = ["setuptools ~= 84.0"]  # the frontend should install them automatically
build-backend = "setuptools.build_meta"  # the path to the backend program

[project]
name = "example"
```

```shell
╰─➤  uv build pack2
Building source distribution...
error: Failed to build `~/Projects/Learning-Python-Packaging/notes/ch02/pack2`
  Caused by: Failed to parse: `pack2/pyproject.toml`
  Caused by: TOML parse error at line 5, column 1
      |
    5 | [project]
      | ^^^^^^^^^
    `pyproject.toml` is using the `[project]` table, but the required `project.version` field is neither set nor present in the `project.dynamic` list
```

Добавлю версию в явном виде: `version = "0.0.2"`. На этот раз сборка идёт успешно. Но всё равно пока содержимое далеко от того, что есть в настоящих проектах, поэтому добавлю ещё надданных (метаданных):

```toml
[project]
name = "example"
version = "0.0.2"
authors = [
    { name = "Author Name", email = "author@example.com" },
]
maintainers = [
    { name = "Maintainer Name", email = "maintainer@example.com" },
]
description = "A sample Python package v2"
requires-python = "~=3.14"
readme = "README.md"
keywords = ["building", "python", "packages"]
# https://pypi.org/classifiers/
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: Free For Home Use",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.14",
    "Topic :: Education",
]
dependencies = []
```

И вывод стал отзывчивее:

```shell
╰─➤  uv build pack2 --no-cache
Building source distribution...
/tmp/.tmpgOKvOh/builds-v0/.tmpKQ3f9e/lib/python3.14/site-packages/setuptools/config/_apply_pyprojecttoml.py:61: SetuptoolsDeprecationWarning: License classifiers are deprecated.
!!

        ********************************************************************************
        Please consider removing the following classifiers in favor of a SPDX license expression:

        License :: Free For Home Use

        See https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#license for details.
        ********************************************************************************

!!
```
Столько ругани из-за `License :: Free For Home Use` - закомменчу чтоб не мозолило. А теперь желаю добавить pytest](https://docs.pytest.org/)
чтобы запускать испыты (тесты) к проекту.

```shell
╰─➤  cd pack2
(ch02) ╭─X@D ~/Projects/Learning-Python-Packaging/notes/ch02/pack2  ‹add-ch03*›
╰─➤  uv add --group test pytest
warning: `VIRTUAL_ENV=~/Projects/Learning-Python-Packaging/notes/ch02/.venv` does not match the project environment path `.venv` and will be ignored; use `--active` to target the active environment instead
warning: The `requires-python` specifier (`~=3.14`) in `example` uses the tilde specifier (`~=`) without a patch version. This will be interpreted as `>=3.14, <4`. Did you mean `~=3.14.0` to constrain the version as `>=3.14.0, <3.15`? We recommend only using the tilde specifier with a patch version to avoid ambiguity.
Using CPython 3.14.3
Creating virtual environment at: .venv
Resolved 7 packages in 276ms
      Built example @ file:///.../Projects/Learning-Python-Packaging/notes/ch02/pack2                                                                        Prepared 1 package in 1.28s
Installed 6 packages in 14ms
 + example==0.0.2 (from file:///.../Projects/Learning-Python-Packaging/notes/ch02/pack2)
 + iniconfig==2.3.0
 + packaging==26.3
 + pluggy==1.6.0
 + pygments==2.21.0
 + pytest==9.1.1
```

Ага, уже uv хочет определённости с версией интерпретатора, ладно, снабжу и заплаточную (patch) версию. Но что за "выскочка" про `--active`? А потому что директория виртуального окружения создана в
"ch02", а `uv add` запускался из "pack2", а uv при добавлении зависимости создаёт такую же директорию ".venv" уже в "pack02" и происходит "непонятка": действующее окружение по пути к родительской диреткории, а ставится в окружение по текущему пути. Вот чтобы установка шла в родительскую директорию и не было создания директории виртуального окружения в текущей и требуется флаг `--active`.

Ладно, с этим вроде решено, теперь создаю директорию "example", в ней простую функцию, а также директорию "tests" уже на уровне "example". Получаю простое деревце проекта.

```shell
╰─➤  tree
.
├── example
│   ├── __init__.py
│   └── module.py
├── pyproject.toml
├── README.md
├── tests
│   ├── __init__.py
│   └── test_module.py
└── uv.lock

3 directories, 7 files
```

Вот это всё "господарство" и нужно собрать: `uv build` - и вытянуть архивы наружу да исследовать их содержимое.

```shell
╰─➤  tar -tzf dist/example-0.0.2.tar.gz | tree --fromfile
.
└── example-0.0.2
    ├── example.egg-info
    │   ├── dependency_links.txt
    │   ├── PKG-INFO
    │   ├── SOURCES.txt
    │   └── top_level.txt
    ├── PKG-INFO
    ├── pyproject.toml
    ├── README.md
    ├── setup.cfg
    └── tests
        └── test_module.py

4 directories, 9 files
```

Видно, что испыты (директория "tests") включены в "издаток" (sdist), а вот самих исходников-то и нет! Как же так?! Голову сломать, но ответ
в официальной документации: [Package Discovery and Namespace Packages](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#flat-layout). Я же использую "плоский расклад" (flat layout), а setuptools при обнаружении (auto-discovery) файлов по умолчанию исключает некоторые директории, в частности
["example"](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#setuptools.discovery.FlatLayoutPackageFinder.DEFAULT_EXCLUDE) - вот это подстава и прям так сразу, а я думал да что же такое, но хороший урок: читайте доку и осторожнее с "ходячими" именами. Получается, что нужно явно прописать обнаружение модуля
example в "pyproject.toml`". Итого:

```toml
[build-system]
requires = ["setuptools ~= 84.0"]  # the frontend should install them automatically
build-backend = "setuptools.build_meta"  # the path to the backend program

[project]
name = "example"
version = "0.0.2"
authors = [
    { name = "Author Name", email = "author@example.com" },
]
maintainers = [
    { name = "Maintainer Name", email = "maintainer@example.com" },
]
description = "A sample Python package v2"
requires-python = "~=3.14.0"
readme = "README.md"
keywords = ["building", "python", "packages"]
# https://pypi.org/classifiers/
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    # SetuptoolsDeprecationWarning: License classifiers are deprecated.
    # "License :: Free For Home Use",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.14",
    "Topic :: Education",
]
dependencies = []

[dependency-groups]
test = [
    "pytest>=9.1.1",
]

[tool.setuptools.packages.find]
# The name "example" is a special one for the package.
# Setuptools excludes it by default for a flat-layout packages.
# https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#setuptools.discovery.FlatLayoutPackageFinder.DEFAULT_EXCLUDE
include = ["example*"]
```

Итоги:

- испыты попадают в sdist, но не в wheel - это нормально. У setuptools есть правила какие файлы включаются в "распред" (дистрибутив) и указаны они [здесь](https://setuptools.pypa.io/en/latest/userguide/miscellaneous.html).
- важно читать доку, в следующий раз выберу какое-нибудь "незаядлое" имя для проекта, чтобы меньше головомойки и матов при доискивании причин (даже нейронка не сразу просекла "что это было").

Оставляю архивы, из которых вполне можно восстановить исходное строение проекта, а тажке обновил заметку по TOML из первой главы.
