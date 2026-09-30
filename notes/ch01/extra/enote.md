# Полёт на Jupyter

В [Jypyter](https://jupyter-notebook.readthedocs.io/en/latest/) тетрадке (это не ноутбук, иначе был бы `jupyter laptop` вместо [`jupyter notebook`](https://jupyter-notebook.readthedocs.io/en/latest/notebook.html#starting-the-notebook-server)) [learning_toml.ipynb](./learning_toml.ipynb) описывается работа с [TOML v1.0][toml_docs] в действии (in action). Поскольку в моём окружении Python>=3.11, а именно с этой версии в стандартную библиотеку и подвезли модуль [tomllib](https://docs.python.org/3/library/tomllib.html), то меня не парило "возюкаться" со сторонним решенеим [toml](https://pypi.org/project/toml/). Но всё же я решил засучить рукава и загразянить руки... и почти возрадовался, что всё может быть так легко и просто, как следующий запуск меня обломал:

```jupyter
!pip install toml  # in Jupyter code cell

error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.
    
    If you wish to install a non-Debian-packaged Python package,
    create a virtual environment using python3 -m venv path/to/venv.
    Then use path/to/venv/bin/python and path/to/venv/bin/pip. Make
    sure you have python3-full installed.
    
    If you wish to install a non-Debian packaged Python application,
    it may be easiest to use pipx install xyz, which will manage a
    virtual environment for you. Make sure you have pipx installed.
    
    See /usr/share/doc/python3.12/README.venv for more information.

note: If you believe this is a mistake, please contact your Python installation or OS distribution provider. You can override this, at the risk of breaking your Python installation or OS, by passing --break-system-packages.
hint: See PEP 668 for the detailed specification.
```

Всё правильно, не нужно загрязнять систему, и подробности в [PEP-668](https://peps.python.org/pep-0668/). Hо тогда возникают следующие вопросы:

- как натравить Джупитер на Python из виртуального окружения?
- хватит ли этого чтобы устанавливать нужные допзависимости или нужно будет подготавливать окружение заранее?

Так и возникла потребность в этой заметке.

## Виртуальное ядро

Сначала я создам виртуальное окружение и на этот раз с `Python=~=3.11` - косвенный путь показать, что библиотека tomllib есть в стандартной библиотеке Python: `uv venv --python 3.11`:

```shell
╰─➤  uv venv --python 3.11
Using CPython 3.11.12
Creating virtual environment at: .venv
Activate with: source .venv/bin/activate
```

Затем нужно поставить пакет управления IPython ядрами ([ipykernel](https://pypi.org/project/ipykernel/)s) для Jupyter: `uv pip install ipykernel`. Ядро - это работающий процесс, который умеет исполнять код в ячейках (cells) в Jupyter, хранить состояние между запусками ячеек и т.п. Ядро - это не просто Python, это именно [IPython ядро](https://ipython.readthedocs.io/en/latest/development/how_ipython_works.html#the-ipython-kernel), или скорее даже [IPython сессия](https://ipython.readthedocs.io/en/stable/overview.html). Остаётся зарегистрировать ядро (грубо говоря, Python), причём лишь для моей учётной пользовательской (user) записи, а не на уровне системы: `python3 -m ipykernel install --user --name=ch01_extra --display-name="Chapter01 (Extra)"` - это ядро с (внутренним) именем`ch01_extra` и внешним (отображаемым) именем `Chapter01 (Extra)`, которое и будет видно в Джупитере.

> На самом деле потребуется ещё установить `pip` в виртуальное окружение, чтобы в тетрадке сработала команда `%pip install toml`, а uv по умолчанию не устанавливает pip в виртуальное окружение ибо незачем когда есть собственный `uv pip`. (Едва) Заметно, что команду нужно начинать с процента (%), а не восклицательного знака (!), потому что:

- % - запуск pip для текущего ядра, именно поэтому потребовалось установить pip в текущее виртуальное окружение, потому что uv при создании окружения не устанавливает в него pip по умолчанию (ибо имеет свой `uv pip`);
- ! - запуск через системную оболочку, что приведёт к уже виденной (c'est déjà vu, putain) ошибке.

Подробнее о встроенных волшебных командах в [документации IPython](https://ipython.readthedocs.io/en/stable/interactive/magics.html).

Фух, заметка кончена, но "здесевый" опыт пригодится когда понадобится поиграться с [Cython](https://cython.org/).

## Cсылки

- [IPython docs](https://ipython.readthedocs.io/en/latest/)
- [Jupyter docs](https://docs.jupyter.org/en/latest/)
- [TOML docs][toml_docs]

[toml_docs]: https://toml.io/en/v1.0.0
