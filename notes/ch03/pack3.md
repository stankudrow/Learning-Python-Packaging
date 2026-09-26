# Терминальное эхо

В прошлой заметке выяснилось несколько забавных вещей:

- example - это не то имя, которым стоит называть поставляемый проект, setuptools, например, его исключает из рассмторения (при плоском раскладе точно);
- tests - достойные чтобы включаться по умолчанию в sdist, тогда как в колесе они не сдались по понятным причинам - пользователю нужен уже испытанный (протестированный) код и им нет дела до самостоятельных (и утомительных) проверок;
- документацию читать нужно, даже если тягомотно, ибо не всякая такая, вот пример хорошей -> [Управление проектами (uv)](https://docs.astral.sh/uv/guides/projects/).

В этой заметке я вознамерился набросать простое приложение с интерфейсом командной строки (Commad Line Interface - CLI), а заодно поиграюсь с "повыборными" (опциональными) зависимостями, или extras на забугорском. А ещё это приложение можно будет запускать как скрипт из терминала (не могу сказать за консоль ибо не пользуюсь Windows).

Команда `uv init --app clap` (флаг `--app` необязательный, но пусть) создала скромное деревце:

```shell
╰─➤  tree
├── main.py
├── pyproject.toml
├── README.md
└── uv.lock
```

А теперь надобавляю зависимости проекта:

- основные -> `uv add --active anyio click`;
- необязательные:
  - звено/группа lint -> `uv add --active --group lint ruff ty`;
  - звено/группа test -> `uv add --active --group test pytest pytest-asyncio`.

А теперь пора определить новые вкусности - те самые необязательные зависимости (extras):

```toml
[project.optional-dependencies]  # extras
cli = ["click"]
all = ["clap[cli]"]

[project.scripts]
# `clap.cli:main` == `from clap.cli import main`
clapper = "clap.cli:main"
```

"Повыборные" зависимости (optional dependencies) - такие, которые можно установить вкупе с проектом если их указать при установке. Т.е. `uv pip install -e .` установит лишь проект clap, тогда как `uv pip install -e ".[cli]"` подтянет ещё и click. Ещё определил "доп" (так я решил обозвать extra по-русски - потому что могу) all как "clap\[cli\]" - именно так, а не просто "cli", потому что в этом "противном" случае установщик полез бы на PyPI (как индекс по умолчанию) за пакетом "cli", которого на время составления заметки в PyPI и нет. А впрочем посмотрим и пусть прописано `all = ["cli"]`:

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

Итоговое дерево проекта:

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

**Примечание**: `uv sync --group lint --group test --extra all --active` помогает установить зависимости из указанных групп с учётом "допов" и в задействованное виртуальное окружение (спасибо `--active` за это). И тут словилось следующее:

```shell
Resolved 20 packages in 2ms
warning: Skipping installation of entry points (`project.scripts`) for package `clap` because this project is not packaged; to install entry points, set `tool.uv.package = true` or define a `build-system`
Checked 18 packages in 0.59ms
```

Ну правильно, я забыл определить таблицу (раздел/секцию) `[build-system]` в "pyproject.toml", что было исправлено. С определённом разделом всё поставилось и вот что стало доступно:

```shell
╰─➤  python3 -m clap
Echoing 'I am the main (entry) module'
╰─➤  clapper -m Ye-ye
Echoing 'Ye-ye'
```

Сборка проекта также произошла успешно и я не зря решил заморочиться с подмодулем "tools": при сборке он попал в раздатки (как "издаток", так и колесо) и без необходимости указывать явные пути в "pyproject.toml" - отыскание (discovery) произошло успешно, setuptools взял всё на себя и справился (ну так а что не справиться когда директория-кандидат единственная и там Python файлы). Вывод содержимого "исходникового" архива:

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

Был день, и был вечер, и даже ночь: глава третья. А в дополнительной заметке к этой главе будет показан "впил" ещё и GUI-скрипта.
