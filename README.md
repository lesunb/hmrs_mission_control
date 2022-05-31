[![Build Status](https://www.travis-ci.com/gabrielsr/hmrs_mission_control.svg?branch=master)](https://www.travis-ci.com/gabrielsr/hmrs_mission_control)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/c40a1b3e88c74755be3423074b0b0b45)](https://www.codacy.com/gh/gabrielsr/hmrs_mission_control/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=gabrielsr/hmrs_mission_control&amp;utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/gabrielsr/hmrs_mission_control/branch/master/graph/badge.svg)](https://codecov.io/gh/gabrielsr/hmrs_mission_control)



Heterogeneous Multi-Robots Mission Control
==========================================

## Overview

**Heterogeneous Multi-Robots Mission Control** is an architecture for the development of applications, capable of coordinating multi-robot missions subject to uncertainty in properties of the available robots in the Software Engineering Lab (LES) at University of Brasilia.

**Keywords:** Software architecture, cooperative heterogeneous robots, multi-robots systems, Cyber-physical systems

### License

The source code is released under a [MIT license](LICENSE).

**Authors: Gabriel Rodrigues, Vicente Moraes and Gabriel F P Araujo <br />
Affiliation: [LES](http://les.unb.br//)<br />
Maintainers: [Gabriel Rodrigues](mailto:gabrielsr@gmail.com), [Vicente Moraes](mailto:vicenteromeiromoraes@gmail.com),[Gabriel F P Araujo](mailto:gabriel.fp.araujo@gmail.com)**

**Heterogeneous Multi-Robots Mission Control** is research code, expect that it changes often and any fitness for a particular purpose is disclaimed.


    @article{rodrigues_architecture_2022,
      title = {An Architecture for Mission Coordination of Heterogeneous Robots},
      author = {Rodrigues, Gabriel and Caldas, Ricardo and Araujo, Gabriel and {de Moraes}, Vicente and Rodrigues, Gena{\'i}na and Pelliccione, Patrizio},
      year = {2022},
      month = sep,
      journal = {Journal of Systems and Software},
      volume = {191},
      pages = {111363},
      issn = {01641212},
      doi = {10.1016/j.jss.2022.111363},
      langid = {english}
    }




Environment dependencies
-------------
python 3, pip

Used IDE: vscode, plugin python

macOS aditional dependencies
brew install libmagic

Development
---

Install poetry
------------- 

poetry easy the process of managing python dependencies

PIP
```console
$ pip install poetry
```

Alternatively, macOS brew
```console
$ brew install poetry 
```

Install dependencies
--------------------

Inside the project folder (after clone)

```console
$ poetry install
$ poetry shell
```

Run a Controlled Experiment
------
Inside poetry environment (after poetry shell)

```console
 python evaluation/experiment_gen_lab_samples/experiment_gen.py
```


Test
----

Tests should be put on /tests folder and are executed with the following command.

```console
 $ poetry run pytest -v --cov .
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
$ poetry shell
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
$ poetry install [name]
```

This command will add the dependency to the Pipfile and poetry.lock assuring that the execution can be reproduced in another environment (after dependencies are updated with `poetry install` command )

Add New Dev Dependency
----------------------
Same as previous dependencies, but for development libraries such as the ones used for test.

```console
$ poetry install [name] --dev
```
Note that other systems after pulling updates will need a reexecution of `poetry install --dev`
