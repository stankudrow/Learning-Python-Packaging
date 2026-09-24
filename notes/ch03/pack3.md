# Управление файлами сборки

В прошлой заметке было несколько забавных вещей:

- example - это не то имя, которое setuptools, а возможно и другой бэкэнд сборки, готов включать в раздатки;
- зато директория tests рассматривается на включение в издаток, но не колесо - это сложившаяся практика, потому что колесо - это как раз то, что "желает" видеть установщик pip (например), а пользователю зачем испыты если ему/ей нужен сам код.

В этой заметке буду собирать простое приложение с интерфейсом командной строки (Commad Line Interface - CLI), заодно приоткрою завесу с дополнительных зависимостей (extras) и покажу установку приложения с возможностью запуска оного как скрипта.

Команда `uv init --app clap` создала привычное неприхотливое дерево:

```shell
╰─➤  tree
├── main.py
├── pyproject.toml
├── README.md
└── uv.lock
```

Зависимости проекта:

- основные -> `uv add --active anyio click`
- необязательные:
  - звено/группа lint -> `uv add --active --group lint ruff ty`
  - звено/группа test -> `uv add --active --group test pytest pytest-asyncio`

А теперь добавляю новые вкусности:

```toml
[project.optional-dependencies]  # extras
cli = ["click"]
all = ["clap[cli]"]

[project.scripts]
# `clap.cli:main` == `from clap.cli import main`
clapper = "clap.cli:main"
```

"Повыборные" зависимости (optional dependencies) - это что называются "допы" (extras) - зависимости, которые можно установить вкупе с проектом если указать их при установке. Т.е. `uv pip install -e .` установит лишь проект clap, а `uv pip install -e ".[cli]"` подтянет ещё и click. Также я определил зависимости all как "clap\[cli\]" - именно так, а не cli, потому что в этом противном случае искался бы пакет cli, а не сам доп cli в составе повыборных групп. Т.е., если бы all доп был бы определён так - `all = ["cli"]` - то выдалось бы следующее:

```shell
╰─➤  uv pip install -e ".[all]"
Using Python 3.14.3 environment at: ~/Projects/Learning-Python-Packaging/notes/ch03/.venv
  × No solution found when resolving dependencies:
  ╰─▶ Because cli was not found in the package registry and clap[all]==0.0.3 depends on cli, we can conclude that clap[all]==0.0.3 cannot be used.
      And because only clap[all]==0.0.3 is available and you require clap[all], we can conclude that your requirements are unsatisfiable.
```

Ну нет в индексе (PyPI) такого пакета cli (пока ещё, может потом). А с `all = ["clap[cli]"]` всё ставится хорошо:

```shell
╰─➤  uv pip install -e ".[all]"
Using Python 3.14.3 environment at: ~/Projects/Learning-Python-Packaging/notes/ch03/.venv
Resolved 11 packages in 21ms
      Built clap @ file: ~/Projects/Learning-Python-Packaging/notes/ch03/clap                                                                            Prepared 1 package in 1.10s
Installed 1 package in 4ms
 + clap==0.0.3 (from file: ~/Projects/Learning-Python-Packaging/notes/ch03/clap)
```

Итоговое деревце проекта:

```shell
╰─➤  tree
.
├── clap
│   ├── cli.py
│   ├── __init__.py
│   ├── __main__.py
│   └── tools
│       ├── echo.py
│       └── __init__.py
├── LICENSE.md
├── main.py
├── pyproject.toml
├── README.md
├── tests
│   ├── __init__.py
│   └── test_echo.py
└── uv.lock

4 directories, 12 files
```

Примечание: `uv sync --group lint --group test --extra all --active` помогает установить зависимости из указанных групп с учётом допов и в задействованное (active) виртуальное окружение. И тут я словил следующее:

```shell
Resolved 20 packages in 2ms
warning: Skipping installation of entry points (`project.scripts`) for package `clap` because this project is not packaged; to install entry points, set `tool.uv.package = true` or define a `build-system`
Checked 18 packages in 0.59ms
```

Ну правильно, я забыл определить таблицу (раздел/секуию) `[build-system]` в "pyproject.toml". Добавление раздела помогло в установке проекта и вот что стало доступно:

```shell
╰─➤  python3 -m clap
Echoing 'I am the main (entry) module'
╰─➤  clapper -m Ye-ye
Echoing 'Ye-ye'
```

Сборка проекта также произошла успешно и я не зря решил заморочиться с подмодулем "tools": при сборке он попал в раздатки (как издаток, так и колесо) без необходимости указывать явные пути в "pyproject.toml" - отыскание (discovery) произошло успешно.

```shell
╰─➤  tar -tzf dist/clap-0.0.3.tar.gz | tree --fromfile
.
└── clap-0.0.3
    ├── clap
    │   ├── cli.py
    │   ├── __init__.py
    │   ├── __main__.py
    │   └── tools
    │       ├── echo.py
    │       └── __init__.py
    ├── clap.egg-info
    │   ├── dependency_links.txt
    │   ├── entry_points.txt
    │   ├── PKG-INFO
    │   ├── requires.txt
    │   ├── SOURCES.txt
    │   └── top_level.txt
    ├── LICENSE.md
    ├── PKG-INFO
    ├── pyproject.toml
    ├── README.md
    ├── setup.cfg
    └── tests
        └── test_echo.py

6 directories, 17 files
```

Был день, и был вечер: глава третья.

### Ссылки

- [Управление проектами (uv)](https://docs.astral.sh/uv/guides/projects/)
