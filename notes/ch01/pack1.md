# Азы сборки

## Содержание

- [Предвариловка](#предвариловка)
- [Привет, сборка](#привет-сборка)
- [Итоги](#итоги)
- [Ссылки](#ссылки)

### Предвариловка

В корневой директории заметок уже есть [.python-version](../../.python-version) файл с опорной версией интерпретатора на проект (Python 3.14), которая и пригождается при создании виртуальных окружений уже в конкретных директориях. Так, в директории "notes/ch01" можно [создать виртуальное окружение](https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-and-using-virtual-environments) с определённой на проект изводом (версией) интерпретатора:

```shell
╰─➤  uv venv
Using CPython 3.14.3
Creating virtual environment at: .venv
Activate with: source .venv/bin/activate
╭─X@D ~/Projects/Learning-Python-Packaging/notes/ch01  ‹add-ch03*›
╰─➤  source .venv/bin/activate
(ch01) ╭─X@D ~/Projects/Learning-Python-Packaging/notes/ch01  ‹add-ch03*›
╰─➤
```

Если же потребовалась бы иная версия, например Python 3.12, то использовалась бы команда `uv venv --python 3.12`. Работа с виртуальным окружением - это основа основ, служащее великой цели: отграничению (изоляции). На каждый проект своё виртуальное окружение как отдельная игроплощадка (playground), в котором делать можно что заблагорассудится. Основная польза, что установка или обновление зависимостей в окружении одного проекта не то чтобы не скажутся на других проектах, но и на системе в целом ибо отграничение (изоляция) как раз и задаёт условия непросачиваемости последствий из одной части в другие или всё целое.

Вот и поставлю в (виртуальное) окружение проекта пакет [build][build] - [фронтенд](https://packaging.python.org/en/latest/glossary/#term-Build-Frontend) по установке Python программ:

```shell
╰─➤  uv pip install build
Resolved 3 packages in 517ms
Prepared 2 packages in 99ms
Installed 3 packages in 8ms
 + build==1.6.1
 + packaging==26.3
 + pyproject-hooks==1.3.3
(ch01) ╭─X@D ~/Projects/Learning-Python-Packaging/notes/ch01  ‹add-ch03*›
╰─➤  uv pip list
Package         Version
--------------- -------
build           1.6.1
packaging       26.3
pyproject-hooks 1.3.3
(ch01) ╭─X@D ~/Projects/Learning-Python-Packaging/notes/ch01  ‹add-ch03*›
╰─➤
```

Фронтенд значит, что [build][build] предоставляет пользовательский интерфейс для сборки пакетов, но самой сборкой не занимается, а вызывает программы-[бэкэнды](https://packaging.python.org/en/latest/glossary/#term-Build-Backend), которые как раз и умеют за сборку. Да тот же [pip][pip] является [фронтендом](https://packaging.python.org/en/latest/glossary/#term-Build-Frontend) для установки пакетов.

Поясняющая картинка (взятая без разрешения, естественно) из книги "Publishing Python Packages":

![Python build system](Python-build-system.png)

### Привет, сборка


Время создавать малополезный "приветмирный" проект:

```shell
╰─➤  uv init pack1
Initialized project `pack1` at `~/Projects/Learning-Python-Packaging/notes/ch01/pack1`
(ch01) ╭─X@D ~/Projects/Learning-Python-Packaging/notes/ch01  ‹add-ch03*›
╰─➤  tree pack1
pack1
├── main.py
├── pyproject.toml
└── README.md

1 directory, 3 files
(ch01) ╭─X@D ~/Projects/Learning-Python-Packaging/notes/ch01  ‹add-ch03*›
╰─➤  uv build pack1
Building source distribution...
running egg_info
creating pack1.egg-info
writing pack1.egg-info/PKG-INFO
writing dependency_links to pack1.egg-info/dependency_links.txt
writing top-level names to pack1.egg-info/top_level.txt
writing manifest file 'pack1.egg-info/SOURCES.txt'
reading manifest file 'pack1.egg-info/SOURCES.txt'
writing manifest file 'pack1.egg-info/SOURCES.txt'
running sdist
running egg_info
writing pack1.egg-info/PKG-INFO
writing dependency_links to pack1.egg-info/dependency_links.txt
writing top-level names to pack1.egg-info/top_level.txt
reading manifest file 'pack1.egg-info/SOURCES.txt'
writing manifest file 'pack1.egg-info/SOURCES.txt'
running check
creating pack1-0.1.0
creating pack1-0.1.0/pack1.egg-info
copying files to pack1-0.1.0...
copying README.md -> pack1-0.1.0
copying main.py -> pack1-0.1.0
copying pyproject.toml -> pack1-0.1.0
copying pack1.egg-info/PKG-INFO -> pack1-0.1.0/pack1.egg-info
copying pack1.egg-info/SOURCES.txt -> pack1-0.1.0/pack1.egg-info
copying pack1.egg-info/dependency_links.txt -> pack1-0.1.0/pack1.egg-info
copying pack1.egg-info/top_level.txt -> pack1-0.1.0/pack1.egg-info
Writing pack1-0.1.0/setup.cfg
Creating tar archive
removing 'pack1-0.1.0' (and everything under it)
Building wheel from source distribution...
running egg_info
writing pack1.egg-info/PKG-INFO
writing dependency_links to pack1.egg-info/dependency_links.txt
writing top-level names to pack1.egg-info/top_level.txt
reading manifest file 'pack1.egg-info/SOURCES.txt'
writing manifest file 'pack1.egg-info/SOURCES.txt'
running bdist_wheel
running build
running build_py
creating build/lib
copying main.py -> build/lib
running egg_info
writing pack1.egg-info/PKG-INFO
writing dependency_links to pack1.egg-info/dependency_links.txt
writing top-level names to pack1.egg-info/top_level.txt
reading manifest file 'pack1.egg-info/SOURCES.txt'
writing manifest file 'pack1.egg-info/SOURCES.txt'
installing to build/bdist.linux-x86_64/wheel
running install
running install_lib
creating build/bdist.linux-x86_64/wheel
copying build/lib/main.py -> build/bdist.linux-x86_64/wheel/.
running install_egg_info
Copying pack1.egg-info to build/bdist.linux-x86_64/wheel/./pack1-0.1.0-py3.14.egg-info
running install_scripts
creating build/bdist.linux-x86_64/wheel/pack1-0.1.0.dist-info/WHEEL
creating '~/Projects/Learning-Python-Packaging/notes/ch01/pack1/dist/.tmp-iu7kuoho/pack1-0.1.0-py3-none-any.whl' and adding 'build/bdist.linux-x86_64/wheel' to it
adding 'main.py'
adding 'pack1-0.1.0.dist-info/METADATA'
adding 'pack1-0.1.0.dist-info/WHEEL'
adding 'pack1-0.1.0.dist-info/top_level.txt'
adding 'pack1-0.1.0.dist-info/RECORD'
removing build/bdist.linux-x86_64/wheel
Successfully built pack1/dist/pack1-0.1.0.tar.gz
Successfully built pack1/dist/pack1-0.1.0-py3-none-any.whl
```

Довольно длинная простыня, но её таки можно разобрать и увидеть следующее:

- Cоздана директория "pack1.egg-info" и она наполняется разными файлами - данными по сборке: сведения о пакете (PKG-INFO), исходники (sources) (хотя возможно это именно источники), ссылки на зависмости (dependency links) и т.п.
- На основе данных из "pack1.egg-info" собирается архив [source distribution (sdist)](https://packaging.python.org/en/latest/glossary/#term-Source-Distribution-or-sdist) - архив формата *.tar.gz*, содержащий исходники, метаданные и прочие файлы и которого хватает для установки из исходников. Я хочу (!) переводить **source distribution** как "исходниковый раздаток", а **sdist** как "издаток", чтобы обходиться хоть каким-то но всё же одним словом (моё нововведение и моя хотелка).
- На основе "издатка" собирается архив [built distribution (bdist)](https://packaging.python.org/en/latest/glossary/#term-Built-Distribution), или [колесо (wheel)](https://packaging.python.org/en/latest/glossary/#term-Wheel) - это и архив с расширением *.whl*, и формат распространения (дистрибуции) Python пакетов. Здесь и далее я могу переводить слово "дистрибутив" как "раздаток" - коряво, но меньше писанины.

Помимио "прямодорожной" команды `uv build`, имеются и другие пути по сборке проекта, например:

- `python3 -m build --installer=uv pack1` - запустить модуль "build" с uv в качестве установщика сборочных зависимостей (вместо "умолчанного" pip) - "сущностно равнозначно" команде `uv build` (заявлено [здесь](https://build.pypa.io/en/stable/index.html#uv-build)).
- `uvx --from build pyproject-build --installer uv pack1` - ну здесь вы уже сами, единственно, `pyproject-build` - это команда из пакета build на целевой запуск.


А далее, собранные архивы можно установить с помощью [pip][pip] как из архива с исходниками (.tar.gz), так и из колеса (.whl):

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

В директории "pack1" при сборке помимо создания или наполения поддиректории "dist" также проявляется поддиректория "pack1.egg-info". Она связана с форматом сборки и распространения ["яйцо"/"egg"](https://packaging.python.org/en/latest/glossary/#term-Egg), который ранее использовался бэкэндом [setuptools][setuptools]. А этот бэкэнд используется когда в проекте нет файла "pyproject.toml" или же в нём отсутствует раздел "\[build-backend\]" ([ссылка](https://docs.astral.sh/uv/concepts/projects/config/#build-systems)). При запуске `uv init pack1`, в директории pack1 создаётся такой "pyproject.toml":

```toml
[project]
name = "pack1"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.14"
dependencies = []
```

И это всё и никакого раздела "\[build-backend\]", а значит по [PEP-517](https://peps.python.org/pep-0517/):

> If the `pyproject.toml` file is absent, or the `build-backend` key is missing, the source tree is not using this specification, and tools should revert to the legacy behaviour of running `setup.py` (either directly, or by implicitly invoking the `setuptools.build_meta:__legacy__` backend).

Т.е. включается проброс к наследному (legacy) бэкэнду, что и видно с первых строк сборки пакета "pack1":

```shell
╰─➤  uvx --from build pyproject-build --installer uv pack1
Installed 3 packages in 4ms
* Creating isolated environment: venv+uv...
  Using external uv from /home/.../.local/bin/uv
* Installing packages in isolated environment:
  - setuptools >= 40.8.0
```

Но, нескромный вопрос, а зачем яйца когда есть колёса?! В стародавнесмутные времена, когда [distutils](https://packaging.python.org/en/latest/key_projects/#distutils) ещё был в стандартной библиотеке Python, проект [setuptools][setuptools] предложил свой формат сборки и распроcтранения пакетов - [яйца (eggs)](https://packaging.python.org/en/latest/glossary/#term-Egg). Кому занятно, есть [чуть более подробное чтиво][about_eggs], но в целом яйца так и не вкатились в экосистему Python, а вот колёса вполне да и как раз благодаря [PEP-427](https://peps.python.org/pep-0427/) и дальнейшим усилиям Python сообщества.

Что-то предостаточно для первой главы, но также оставляю дополнительную заметку по формату [TOML](https://toml.io/en/v1.0.0) (без средств обхода сетевых "запоров" в РФ открывается слабо). Формат TOML ("Tom's Obvious, Minimal Language") выбран сообществом Python для описания метаданных проекта в файле **pyproject.toml** (см. [PEP-621](https://peps.python.org/pep-0621/)), нацеленным быть единым источником правды в Python-проекте.

### Итоги

- sdist (архив исходников) - может содержать документацию, испыты (тесты), файлы на компиляцию (и такое может быть) и т.п. Архива хватает чтобы из него собрать (!) и установить пакет.
- wheel (колесо) - это уже собранный архив, который содержит всё нужное и достаточное для установки в систему. А ещё это формат распространения Python-пакетов.

Колесо - вот что в основном и нужно, ибо оно не треубет сборки, но лишь установки. Правда есть тонкость: если для какой-то платформы нет колеса, тогда понадобится издаток (sdist) и pip обычно умеет "скатываться" (fallback) к поиску архива с досборкой и установкой из него. В общем, из-за "предсобранности" (pre-built) колёс установка из них быстрее чем из исходников ([sdists-vs-wheels](https://packaging.python.org/en/latest/tutorials/installing-packages/#source-distributions-vs-wheels)).

### Ссылки

- [Packaging Flow](https://packaging.python.org/en/latest/flow/) - здесь расписано куда подробнее и качественнее.
- [Distribution package vs. import package](https://packaging.python.org/en/latest/discussions/distribution-package-vs-import-package/#distribution-package-vs-import-package)
- [Key Projects (PyPA and non-PyPA)](https://packaging.python.org/en/latest/key_projects/)
- [What about eggs?][about_eggs]

[about_eggs]: https://packaging.python.org/en/latest/discussions/package-formats/#egg-forma
[build]: https://pypi.org/project/build/
[pip]: https://pip.pypa.io/
[setuptools]: https://setuptools.pypa.io/
[uv]: https://docs.astral.sh/uv/
