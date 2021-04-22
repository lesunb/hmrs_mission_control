[![Codacy Badge](https://api.codacy.com/project/badge/Grade/b9b2abf80de34584a596147b099f4473)](https://app.codacy.com/gh/gabrielsr/hmrs_mission_control?utm_source=github.com&utm_medium=referral&utm_content=gabrielsr/hmrs_mission_control&utm_campaign=Badge_Grade_Settings)
[![Build Status](https://travis-ci.org/gabrielsr/hmrs_mission_control.svg?branch=master)](https://travis-ci.org/gabrielsr/hmrs_mission_control)
[![codecov](https://codecov.io/gh/gabrielsr/hmrssim/branch/master/graph/badge.svg)](https://codecov.io/gh/gabrielsr/hmrs_mission_control)


Heterogeneous Multi-Robots Mission Control
==========================================

Env Depencies
-------------
python 3, pip

Used IDE: vscode, plugin python

Instal pipenv
------------- 

pipenv easy the process of managing python dependencies

PIP
```console
$ pip install pyenv
```

Alternatively, macOS brew
```console
$ brew install pipenv 
```

Install dependencies
--------------------

Inside the project folder (after clone)

```console
$ pyenv install
$ pip install pipenv
$ pipenv install
$ pipenv shell
(hmrs_mission_control env) % pipenv install --dev
```


Test
----

Tests should be put on /tests folder and are executed with the following command.

```console
 $ pytest -v --cov .
```

Linter
------

```console
 $ flake8 --statistics
```


Run
---

Select the exec shell

```console
$ pipenv shell
```

Then, Execute Simulation

```console
$ python ./run.py
```

Dependency
----------

Add New Dependency
------------------

To add new dependencies use the following command.

```console
$ pipenv install [name]
```

This command will add the dependency to the Pipfile and Pipfile.lock assuring that the execution can be reproduced in another environment (after dependencies are updated with `pipenv install` command )

Add New Dev Dependency
----------------------
Same as previous dependencies, but for development libraries such as the ones used for test.

```console
$ pipenv install [name] --dev
```
Note that other systems after pulling updates will need a reexecution of `pipenv install --dev`
