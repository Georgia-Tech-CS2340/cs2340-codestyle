# CS 2340 Codestyle

> Collection of scripts/configuration files used for running static code analysis tools for both Java & Python. Made for instructional use in CS 2340 at Georgia Tech in Fall 2019.

## 📜 Rationale

Standardizing code style within group projects is important for a multitude of reasons. Besides making code easier for TA graders to read & comprehend, enforcing consistent code style is beneficial for group members—ensuring all members can read and write code with consistent style/layout.

## 🚀 Getting Started

Each code-checking script is written using [Python 3.5+](https://www.python.org/downloads/), which must be installed and added to the `PATH` before any script is run.

In Fall 2019 CS2340, students have the option to use either Python Flask or Java Swing to write their group projects with, so style checkers are provided for each option separately.

### 🐍 Python - `pylint`

Python code style is checked using [Pylint](https://www.pylint.org/), which enforces [PEP-8](https://www.python.org/dev/peps/pep-0008/) style guidelines, widely regarded as best style practices in Python.

#### 📚 Features

- Finds all `.py` files in the given path and runs `pylint` on them
- Includes class-specific check disables and configures `pylint`
- Checks for `pylint` being installed

#### 💿 Installation

Once Python/`pip` are installed as a part of installing the required software to develop using Flask, Pylint can be installed by using pip:

```shell
pip install pylint
```

#### ⁉ Syntax

```shell
$ python run_pylint.py -h
usage: run_pylint.py [-h] [--root path] [--parallel count] [--verbose] [--all]

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

#### 🏃 Example Run

```shell
$ python run_pylint.py --root ./flask -v

Running pylint on 4 files:
 - /mnt/d/Github/cs2340-codestyle/flask/api.py
 - /mnt/d/Github/cs2340-codestyle/flask/app.py
 - /mnt/d/Github/cs2340-codestyle/flask/models/object.py
 - /mnt/d/Github/cs2340-codestyle/flask/models/object_formatted.py

************* Module object
 models/object.py:9: convention (C0326, bad-whitespace, ) Exactly one space required after :
         if name in objects.keys():    return objects[name], 200
                                  ^
 models/object.py:18: convention (C0326, bad-whitespace, ) Exactly one space required around assignment
                 objects[name]=args.get('value')
                              ^
 models/object.py:5: convention (C0103, invalid-name, formatMessage) Function name "formatMessage" doesn't conform to snake_case naming style
 models/object.py:15: convention (C0321, multiple-statements, Object.post) More than one statement on a single line

---------------------------------------------------------------------------------------
Your code has been rated at 8.79/10 [raw score: 8.79/10] (previous run: 3.48/10, +5.30)
```

### ☕ Java - Checkstyle

Java code style is checked using [Checkstyle](https://checkstyle.org/) using a custom-created configuration file based off of the one used in CS 1332, Data Structures & Algorithms.

#### 📚 Features

- Finds all `.java` files in the given path and runs Checkstyle on them
- Searches for and downloads the checkstyle JAR and CS 2340 configuration file automatically
- Adds the checkstyle JAR to the `.gitignore` file, or creates a new one
- Checks for Java being installed
- Calculates code quality score using error count and overall statement count
  - Scans Java code and counts number of statements

#### 💿 Installation

Python must be installed & added to the `PATH` to run the script. Instructions are available [here](https://geek-university.com/python/add-python-to-the-windows-path/). Additionally, Java must be installed and added to the `PATH`.

#### ⁉ Syntax

```shell
$ python run_checkstyle.py -h
usage: run_checkstyle.py [-h] [--root path] [--verbose]

Checkstyle script to run checkstyle on every .java file in the CWD

optional arguments:
  -h, --help            show this help message and exit
  --root path, -r path  the path to run checkstyle over (defaults to current
                        directory)
  --verbose, -v         whether to display additional output
```

#### 🏃 Example Run

```shell
$ python run_checkstyle.py --root ./swing -v

Downloading cs2340_checks.xml
100.0% 4873 / 4873

Downloading checkstyle-8.41-all.jar
100.0% 11625142 / 11625142

> Note: The checkstyle jar has been downloaded and automatically added to your gitignore.
        This change should be checked into version control.

Running Checkstyle on 4 files:
 - /mnt/d/Github/cs2340-codestyle/swing/Application.java
 - /mnt/d/Github/cs2340-codestyle/swing/CalculatorWindow.java
 - /mnt/d/Github/cs2340-codestyle/swing/CalculatorWindowFormattingTest.java
 - /mnt/d/Github/cs2340-codestyle/swing/SpringUtilities.java

Starting audit...
[WARN] /mnt/d/Github/cs2340-codestyle/swing/CalculatorWindowFormattingTest.java:52: Abbreviation in name 'CONSTRUCT_LAYOUT' must contain no more than '4' consecutive capital letters. [AbbreviationAsWordInName]
[WARN] /mnt/d/Github/cs2340-codestyle/swing/CalculatorWindowFormattingTest.java:52:22: Name 'CONSTRUCT_LAYOUT' must match pattern '^[a-z][a-zA-Z0-9]*$'. [MethodName]
[WARN] /mnt/d/Github/cs2340-codestyle/swing/CalculatorWindowFormattingTest.java:52:39: '(' is preceded with whitespace. [MethodParamPad]
[WARN] /mnt/d/Github/cs2340-codestyle/swing/CalculatorWindowFormattingTest.java:55: Line is longer than 100 characters (found 119). [LineLength]
Audit done.

--------------------------------------------------------
Your code has been rated at 7.88/10 [raw score: 7.88/10]
```
