[![Build Status](https://www.travis-ci.com/gabrielsr/hmrs_mission_control.svg?branch=master)](https://www.travis-ci.com/gabrielsr/hmrs_mission_control)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/c40a1b3e88c74755be3423074b0b0b45)](https://www.codacy.com/gh/gabrielsr/hmrs_mission_control/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=gabrielsr/hmrs_mission_control&amp;utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/gabrielsr/hmrs_mission_control/branch/master/graph/badge.svg)](https://codecov.io/gh/gabrielsr/hmrs_mission_control)



Heterogeneous Multi-Robots Mission Control
==========================================

Env Depencies
-------------
python 3, pip

Used IDE: vscode, plugin python

macOS aditional dependencies
brew install libmagic

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
