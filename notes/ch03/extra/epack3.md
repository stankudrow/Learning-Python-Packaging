# И GUI в придачу

В основной заметки сделано простое CLI эхо-приложение, а в этой, в качестве добавки, будет положен модуль с графическим интерфейсом пользователя (Graphical User Interface, GUI).

Дерево проекта:

```shell
╰─➤  tree
.
├── LICENSE.md
├── pyproject.toml
├── README.md
├── scriptex
│   ├── cli.py
│   ├── gui.py
│   ├── __init__.py
│   ├── __main__.py
│   └── tools
│       ├── echo.py
│       └── __init__.py
└── tests
    └── test_echo.py

4 directories, 10 files
```

На самом деле потребуется мало изменений в донастройке проекта, можете [diff](https://www.man7.org/linux/man-pages/man1/diff.1.html)'ануть pyproject.toml из основного и этого модулей (приводится далее):

```toml
[build-system]
requires = ["setuptools~=84.0"]
build-backend = "setuptools.build_meta"

[project]
name = "scriptex"
version = "0.3.1"
description = "My fancy CLI app with extra GUI"
readme = "README.md"
license = "LicenseRef-Proprietary"
license-files = ["LICEN[CS]E*.md"]
requires-python = "~=3.14.0"
dependencies = [
    "anyio>=4.15.1",
]
keywords = ["python", "packaging", "cli", "async"]
classifiers = [
    "Environment :: Console",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.14",
    "Topic :: Education",
]

[dependency-groups]
lint = [
    "ruff>=0.16.8",
    "ty>=0.0.84",
]
test = [
    "pytest>=9.1.1",
    "pytest-asyncio>=1.4.0",
]

[project.optional-dependencies]  # extras
cli = ["click~=8.5"]
all = ["scriptex[cli,gui]"]
gui = ["pyqt6~=6.11.0"]

[project.scripts]
# `scriptex.cli:main` == `from scriptex.cli import main`
echo-cli = "scriptex.cli:main"
# type `echo-gui` in the shell
echo-gui = "scriptex.gui:main"

[project.gui-scripts]
# To be run as `uv run echoer`
# In case of "ModuleNotFoundError: No module named 'PyQt6'"
# run `uv sync --extra gui` and rerun the target command (above)
echoer = "scriptex.gui:main"
```

В общих чертах вышло нетрудным делом, архивы на ваше употрошение. [Здесь](https://docs.astral.sh/uv/guides/scripts/#using-gui-scripts) можно посмотреть за использование GUI-скриптов в uv. Также мне не приходится возится с "приколюхами" Windows, поэтому тема `gui-scripts`за подробностями в официальную доку.

https://docs.astral.sh/uv/concepts/projects/config/#graphical-user-interfaces

Итоги:

```shell
╰─➤  uv pip install -e ".[all]"
Using Python 3.14.3 environment at: ~/Projects/Learning-Python-Packaging/notes/ch03/.venv
Resolved 8 packages in 240ms
      Built scriptex @ file: ~/Projects/Learning-PPrepared 1 package in 678ms
Uninstalled 1 package in 0.81ms
Installed 1 package in 2ms
 ~ scriptex==0.3.1 (from file:~/Projects/Learning-Python-Packaging/notes/ch03/extra/epack3)
╰─➤  python3 -m scriptex
Echoing 'I am the main (entry) module'
╰─➤  echo-cli -m PyPackaging
Echoing 'PyPackaging'
╰─➤  echo-gui
```

И далее терминал западает пока оконка открыта. Но это запуск через терминал, а можно ещё запустить с использование данных из `[project.gui-scripts]`:

- `uv sync --extra gui` - может потребоваться для установик зависимостей;
- `uv run echoer` - запуск оконки через `uv`.

Вот она такая скромная и даже не сломалась на пустой строке, что приятно:

![Echo-GUI-empty](./echo_gui.png)

**Внимание**: определения в разделе `[project.gui-scripts]` имеет особенность в Windows, которая мне без надобности, но [ссылку](https://docs.astral.sh/uv/concepts/projects/config/#graphical-user-interfaces) оставляю.
