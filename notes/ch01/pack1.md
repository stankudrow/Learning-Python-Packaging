# Быстрое начало

Полдела откачало...

Создаю .python-version - там прописана опорная версия интерпретатора для проекта - это будет Python 3.14. Затем создаю виртуальное окружение и вместо `uv venv --python 3.14`, благодаря [.python-version][pyversion] файлу, достаточно лишь `uv venv`. Именно в виртуальное окружение будут устанавливаться зависимости для корневого проекта, например, пакет [build][build]: `uv pip install build`.

```shell
╰─➤  uv pip list
Package         Version
--------------- -------
build           1.5.0
packaging       26.3
pyproject-hooks 1.2.0
```

Программа [build][build] - это фронтенд, т.е. программа, предоставляющая пользовательский интерфейс для сборки пакетов. Но фронтенд не занимается самой сборкой, но умеет вызывать программу-бэкэнд, которая и умеет собирать пакеты из исходников. Вот поясняющая картинка (взятая без разрешения, естественно) из книги "Publishing Python Packages":

![Python build system](Python-build-system.png)

Затем создаю простой "приветмирный" проект, но с другим интерпретатором: `uv init pack1` (можно с `--python 3.14`, но зачем когда есть [.python-version][pyversion]). А теперь его можно пособирать разными способами и наипростой из них: `uv build pack1` (из директории "ch01"), который создаёт два "обменопригодных" архива (уже в "pack1/dist" директории): колесо (wheel) и архив .tar.gz, который называется source distribution (sdist), который наверное можно коряво перевести как "исходниковый раздаток" (ужас) - ну пусть будет "издаток" если у нас импортозамещение.

Помимо "прямодорожного" `uv build` имеются и другие пути (попробуйте в выводе отыскать название программы-бэкэнд):

- `uvx --from build pyproject-build --installer uv pack1` - использовать команду pyproject-build как инструмент (tool, ведь uvx == uv tool run) из пакета build чтобы собрать проект pack1 посредством установщика uv.
- `python3 -m build --installer=uv pack1` - [здесь](https://build.pypa.io/en/stable/index.html#uv-build) эта команда заявлена как "сущностно равнозначной" (essentially equivalent) команде `uv build`.

А далее собранные архивы можно установить через тот же `pip` (на это он и нужен). Можно установить через колесо:

```shell
╰─➤  uv pip install pack1/dist/pack1-0.1.0-py3-none-any.whl
Resolved 1 package in 3ms
Prepared 1 package in 8ms
Installed 1 package in 1ms
pack1==0.1.0 (from file:///.../Learning-Python-Packaging/pack1/dist/pack1-0.1.0-py3-none-any.whl)
╰─➤  uv pip list
Package         Version
--------------- -------
build           1.5.0
pack1           0.1.0
packaging       26.3
pyproject-hooks 1.2.0
╰─➤  uv pip uninstall pack1
Uninstalled 1 package in 24ms
- pack1==0.1.0 (from file:///.../Learning-Python-Packaging/pack1/dist/pack1-0.1.0-py3-none-any.whl)
```

Можно установить и через .tar.gz:
```shell
╰─➤  uv pip install pack1/dist/pack1-0.1.0.tar.gz
Resolved 1 package in 6ms
      Built pack1 @ file:///.../Learning-Python-Prepared 1 package in 1.12s
Installed 1 package in 1ms
pack1==0.1.0 (from file:///.../Learning-Python-Packaging/pack1/dist/pack1-0.1.0.tar.gz)
╰─➤  python3
Python 3.14.3 (main, Mar  3 2026, 14:59:53) [Clang 21.1.4 ] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import pack1
>>> quit()
╰─➤  uv pip uninstall pack1
Uninstalled 1 package in 5ms
 - pack1==0.1.0 (from file:///.../Learning-Python-Packaging/pack1/dist/pack1-0.1.0.tar.gz)
```

Вот такой "Привет мир" на уровне сборки, распространения и установки пакетов.

Также в pack1 создалась директория "pack1.egg-info" - это артефакт сборки посредством бэкэнда [setuptools][setuptools], к которому uv прибегает когда в проекте на сборку нет файла "pyproject.toml" или же в нём отсутствует раздел "\[build-backend\]". При запуске `uv init pack1`, в директории pack1 создаётся "pyproject.toml" следующего содержания:

```toml
[project]
name = "pack1"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.14"
dependencies = []
```

Но в этом файле нет раздела "\[build-backend\]", а значит, согласно [PEP-517](https://peps.python.org/pep-0517/):

> If the `pyproject.toml` file is absent, or the `build-backend` key is missing, the source tree is not using this specification, and tools should revert to the legacy behaviour of running `setup.py` (either directly, or by implicitly invoking the `setuptools.build_meta:__legacy__` backend).

Т.е. включается проброс к наследному поведению, что и видно с первых строк сборки пакета pack1:

```shell
╰─➤  uvx --from build pyproject-build --installer uv pack1
Installed 3 packages in 4ms
* Creating isolated environment: venv+uv...
  Using external uv from /home/.../.local/bin/uv
* Installing packages in isolated environment:
  - setuptools >= 40.8.0
```

А зачем это так? В давние смутные времена безначалия и вседозволенности, опуская сведения про distutils и прочие бубнопляски с архивами и установочными скриптами, проект [setuptools][setuptools] предложил свой формат яйца (egg) - zip-архив, который содержит исходники и метаданные проекта. Но яйца так и не вкатились в экосистему Python, а колёса вкатились благодаря [PEP-427](https://peps.python.org/pep-0427/) и дальнейшим усилиям по стандартизации сборки и упаковки Python программ (см. [PEP-621](https://peps.python.org/pep-0621/) о внедрении pyproject.toml файла).

[pyversion]: ../../.python-version
[build]: https://pypi.org/project/build/
[setuptools]: https://setuptools.pypa.io/
