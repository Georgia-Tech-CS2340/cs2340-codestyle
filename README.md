# CS 2340 Codestyle

## 🚀 Getting Started

### Prerequisites

- Docker runtime (i.e. [Docker Desktop](https://www.docker.com/products/docker-desktop))

**TODO** write getting started instructions

## ℹ About

### Rationale

Standardizing code style within group projects is important for a multitude of reasons. Besides making code easier for TA graders to read & comprehend, enforcing consistent code style is beneficial for group members—ensuring all members can read and write code with consistent style/layout.

### Software

Students have the option to use either Python Flask or Java Swing to write their group projects with, so style checkers are provided for each option separately.

#### Python - `pylint`

Python code style is checked using [Pylint](https://www.pylint.org/), which enforces [PEP-8](https://www.python.org/dev/peps/pep-0008/) style guidelines, widely regarded as best style practices in Python.

##### Installation

Once Python/`pip` are installed as a part of installing the required software to develop using Flask, Pylint can be installed by using pip:

```bash
pip install pylint
```

##### Running

To run `pylint` on a python source file(s), the following command can be run:

```bash
pylint source.py [...additional_files.py] --disable=missing-docstring,no-else-return --const-naming-style=any
```

> Note: if the command output sounds like `command not found` or `The term 'pylint' is not recognized as the name of a cmdlet, ...` or `'pylint' is not recognized as an internal or external command`, the alternative syntax below can be used:
>
> ```bash
> python -m pylint source.py [...additional_files.py] --disable=missing-docstring,no-else-return --const-naming-style=any
> ```

**Note that the above command includes specific arguments that disable/modify the behavior of `pylint`. These are designed to make the code style standards for this class less strict, so these arguments will be used when code style is graded.**

##### Running - Script

For your convenience, a python script has been provided that automatically runs `pylint` on every python file in a directory:

**Example run**

(in project root folder that also includes checkstyle.py):
```bash
$ python checkstyle.py

Running pylint on 4 files:
 - /mnt/d/Github/cs2340-codestyle/test/flask/api.py
 - /mnt/d/Github/cs2340-codestyle/test/flask/app.py
 - /mnt/d/Github/cs2340-codestyle/test/flask/models/object.py
 - /mnt/d/Github/cs2340-codestyle/test/flask/models/object_formatted.py

<.. code style reports ...>

 ------------------------------------------------------------------
 Your code has been rated at 3.18/10 (previous run: 3.18/10, +0.00)
```

###### Syntax

```bash
$ python checkstyle.py -h
usage: checkstyle.py [-h] [--root path] [--parallel count] [--verbose] [--all]

Checkstyle script to run pylint on every .py file in the CWD

optional arguments:
  -h, --help            show this help message and exit
  --root path, -r path  the path to run pylint over (defaults to current
                        working directory)
  --parallel count, -p count, -j count
                        the number of parallel processes to split pylint into
  --verbose, -v         whether to display additional output
  --all, -a, --strict   enables all checks (strict mode)
```
