# Дополнительные трудности сборки

Усложняю себе жизнь себе же на благо.

## Содержание

- [Снова здарова](#снова-здарова)
- [Данные пакета](#данные-пакета)
- [MANIFEST.in](#manifestin)
- [Итоги](#итоги)

### Снова здарова

Снова создаю пустой проект "expack2" (надо было назвать "epack2", но бой болезненному стремлению к совершенству и выверенности), наполняю его и прорастает такое дерево:

```shell
╰─➤  tree
.
├── expack2
│   └── __init__.py
├── pictures
│   ├── Building-Empty-Python-Packages.png
│   ├── Manifest-in-directives.png
│   ├── Python-build-system.png
│   ├── Python-Venv_maps.png
│   └── Venvs.png
├── pyproject.toml
└── tests
    └── __init__.py

4 directories, 8 files
```

Файл pyproject.toml пока такой:

```toml
[build-system]
requires = ["setuptools ~= 84.0"]  # the frontend should install them automatically
build-backend = "setuptools.build_meta"  # the path to the backend program

[project]
name = "expack2"
version = "0.2.1"
description = "A sample Python extra package v2"
requires-python = "~=3.14.0"
```

Основное отличие, что в теперешнем проекте несколько директорий и вот вопрос: "сумеет ли бэкэнд определить где располагаются исходники, а где так, "непитонячьи" файлы?"

```shell
╰─➤  uv build
Building source distribution...
error: Multiple top-level packages discovered in a flat-layout: ['expack2', 'pictures'].

To avoid accidental inclusion of unwanted files or directories,
setuptools will not proceed with this build.

If you are trying to create a single distribution with multiple packages
on purpose, you should not rely on automatic discovery.
Instead, consider the following options:

1. set up custom discovery (`find` directive with `include` or `exclude`)
2. use a `src-layout`
3. explicitly set `py_modules` or `packages` with a list of names

To find more information, look for "package discovery" on setuptools docs.
error: Failed to build
       `~/Projects/Learning-Python-Packaging/notes/ch02/extra/expack2`
  Caused by: The build backend returned an error
  Caused by: Call to `setuptools.build_meta.build_sdist` failed (exit status:
             1)

hint: Build failures usually indicate a problem with the package or the build environment
```

Не случилось, зато простыня довольно подробная: setuptools просто не знает что включать в сборку, ведь директорий-кандидатов не одна, а уже две - неочевидность. Зато, как хороший сотрудник, не просто критикует, а предлагает решения:

- src расклад (layout) - пока я не хочу к нему прибегать, ибо и плоский (flat) расклад вполне живуч в Python мире, хотя есть противостояние [src-vs-flat](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/), но нет речи - считайте, что есть требование делать именно плоский расклад ибо "потому что".
- раз src-расклад не в чести, остаётся явно указать где искать пакеты и что определяемо в качестве пакетов.

Поэтому в pyproject.toml указываю явно что есть пакеты (он такой один и это не Тинькофф):

```toml
[tool.setuptools]
packages = ["expack2"]
```

При этом не нужно прописывать явный exclude директории "pictures", ибо пакет(ы) уже указаны. Но что если я хочу также поставлять в сборке директорию "pictures"? Пусть она настолько важна, что её стоит включать в архивы. Оказывается, есть несколько способов это сделать и рассмотрим их в отдельных подглавах.

Кстати, эти картинки снова слямзены из книги "Publishing Python Packages" и снова без разрешения: уж хороша книга, а ссылка на неё оставлена в корневом README проекта.

### Данные пакета

Сиречь "package data" на "туманоальбионском". Данные пакета - это непитоновские файлы, которые хранятся внутри Python пакета. Если переместить директорию "pictures" в пакет "expack2", то она уже считается данными пакета. Но для явности укажу какому пакету соотносимы какие данные (излишне это или нет - проверьте сами):

```toml
[tool.setuptools.package-data]
expack2 = ["pictures/*.png"]  # wanna include 'em all
```

В документации setuptools [написано](https://setuptools.pypa.io/en/latest/userguide/datafiles.html#configuration-options), что с версии v61 можно не прописывать `include-package-data = true` в разделе `[tool.setuptools]` ибо такое поведение обеспечивается по умолчанию (но не в случае "setup.py" или "setup.cfg" файлов). [Здесь](https://setuptools.pypa.io/en/latest/userguide/datafiles.html#package-data) поясняется, что при `include-package-data = true`, все непитоновские файлы внутри пакета обнаруживаются и включаются в пакет (есть тонкости и они в доке).

```shell
╰─➤  tree
.
├── expack2
│   ├── __init__.py
│   └── pictures
│       ├── Building-Empty-Python-Packages.png
│       ├── Manifest-in-directives.png
│       ├── Python-build-system.png
│       ├── Python-Venv_maps.png
│       └── Venvs.png
├── pyproject.toml
└── tests
    └── __init__.py

4 directories, 8 files
```

Архивы расположил в директории [dists/v1](./dists/v1_package-data) - исследуйте на здоровье.

Вообще картинки трудно считать данными пакета, если только они не являются ценными "исчерпывающими" времени исполнения (runtime resources): вдруг их нужно выдавать и в этом мулька самой программы, и такое бывает. Пример надуманный, но, например, на моей работе в одном проекте есть CSV-файл, где указаны разновидности коммерческих услуг. По историческим причинам, сведения по услугам хранятся не в БД, а именно в файле на стороне сервиса и таким путём, данные в этом файле являются данными пакета/сервиса.

### MANIFEST.in

Если директория с картинками не предназначена быть данными пакета, а является "хорошо-иметь" побочкой, тогда можно оставить директорию в корне, но "наставить" setuptools включать оную в сборку и для этого как раз и потребуется файл "MANIFEST.in".

```shell
╰─➤  tree
.
├── expack2
│   └── __init__.py
├── MANIFEST.in
├── pictures
│   ├── Building-Empty-Python-Packages.png
│   ├── Manifest-in-directives.png
│   ├── Python-build-system.png
│   ├── Python-Venv_maps.png
│   └── Venvs.png
├── pyproject.toml
└── tests
    └── __init__.py

4 directories, 9 files
```

И здесь сборка показала отличия (доступны в [dists/v2](./dists/v2_manifest)): в тарбол (sdist) картинки попали, а в колесо нет - да что за не так?! Да как раз всё так, ибо файл "MANIFEST.in" - это про наполнение архива с исходниками, а не колеса. Кроме того, картинки теперь не внутри пакета, а значит они не данные пакета, а значит с какого им попадать в раздаток (дистрибутив)? А манифест-файл как раз содержит директивы что включать в архив .tar.gz, а что исключать.

Посему, если важно поставить данные, но они скорее сопутствующие и не обязаны быть в итоговом поставляемом изводе (версии) проекта, то смело пользуйте файл "MANIFEST.in" - он не отожрёт место в хранилище (репозитории).

Вот хорошая картинка (и снова без разрешения):

![MANIFEST.in](./Manifest-in-directives.png)

И не без тонкости: setuptools ищет "MANIFEST.in", а не файл "MANIFEST" без расширения ([ссылка](https://setuptools.pypa.io/en/latest/userguide/miscellaneous.html#using-manifest-in)).

### Итоги

Этих двух способов хватит на эту заметку. Если вкратце, то:

- непитоновские файлы могут и должны использоваться пакетом во время исполнения (runtime) - включайте их внутрь пакета и package-data в помощь;
- если данные сопутствующие, но не прям данные пакета - используйте "MANIFEST.in" и проверяйте их в sdist.
