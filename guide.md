# Python / `pylint`

For Python, [Pylint](https://www.pylint.org/) is used, which is a static code analysis tool and linter for Python that ensures code is idiomatic and follows Python best practices such as [PEP-8](https://www.python.org/dev/peps/pep-0008/). It is also used to check code for errors and can help prevent difficult-to-find runtime bugs. In this class, **we have disabled certain pylint checks to make the checks less strict**. If desired, these checks can be re-enabled to check for all pylint categories (more details below). There are a few different ways of running pylint, each of which are detailed below.

## Running `pylint` with Script *(Recommended)*

A utility script was developed by the CS 2340 TAs to make running pylint on your projects easier.

### Prerequisites

- Python installed and on the `PATH` [(tutorial on Canvas... complete the "Installing Python" section)](https://gatech.instructure.com/files/7339157/download?download_frd=1)
- [Pylint script](https://raw.githubusercontent.com/jazevedo620/cs2340-codestyle/master/run_pylint.py) downloaded
- `pylint` installed using `pip`:
  - `python -m pip install pylint`


### Running

The `run_pylint.py` script supports running pylint over every python file in a directory. For example, if my project structure is as follows:

```
project/
├── src/
│   ├── models/
│   │   └── object.py
│   ├── api.py
│   └── app.py
└── run_pylint.py
```

then I can run `pylint` on every `.py` file in the project directory (except for the script):

```shell
python run_pylint.py
```

This will output something like the following:

```shell
~/project/ $ python run_pylint.py

Running pylint on 3 files:

************* Module object
 src/models/object.py:9: convention (C0326, bad-whitespace, ) Exactly one space required after :
         if name in objects.keys():    return objects[name], 200
                                  ^
 src/models/object.py:18: convention (C0326, bad-whitespace, ) Exactly one space required around assignment
                 objects[name]=args.get('value')
                              ^
 src/models/object.py:5: convention (C0103, invalid-name, formatMessage) Function name "formatMessage" doesn't conform to snake_case naming style
 src/models/object.py:9: convention (C0321, multiple-statements, Object.get) More than one statement on a single line

---------------------------------------------------------------------------------------
Your code has been rated at 8.10/10 [raw score: 8.10/10] (previous run: 8.10/10, +0.00)
```

The score given at the bottom is a metric of overall code quality, and is computed using the following formula where `e` is the number of pylint errors, `w` is the number of pylint warnings/conventions/refactors, and `n` is the number of Python statements in the scanned code:

![S(e,n)=10-10((5e + w)/n)](https://i.imgur.com/Qrgc6Mp.png)

#### Running with all checks enabled

To run with all checks, add `--all` to the end of the command used to run pylint:

```shell
python run_pylint.py --all
```

This will likely result in a lower score than without all checks enabled, but **this score will not be used when grading. Only the score that is a result of the standard run will be used**.

## Running `pylint` Directly

### Prerequisites

- Python installed and on the `PATH` [(tutorial on Canvas... complete the "Installing Python" section)](https://gatech.instructure.com/files/7339157/download?download_frd=1)
- `pylint` installed using `pip`:
  - `python -m pip install pylint`

### Running

Once the required files are present, run the following command, adding each file to the end as necessary:

```shell
python -m pylint --disable=C0111,R1705,E0401,R0201 file1.py file2.py
```

The program should output something similar to the following, where pylint error is listed, along with it's filename, line number, and column number (where applicable).:

```shell
$ python -m pylint --disable=C0111,R1705,E0401,R0201 api.py app.py models/object.py
 ************* Module object
 models/object.py:9: convention (C0326, bad-whitespace, ) Exactly one space required after :
         if name in objects.keys():    return objects[name], 200
                                  ^
 models/object.py:18: convention (C0326, bad-whitespace, ) Exactly one space required around assignment
                 objects[name]=args.get('value')
                              ^
 models/object.py:5: convention (C0103, invalid-name, formatMessage) Function name "formatMessage" doesn't conform to snake_case naming style
 models/object.py:9: convention (C0321, multiple-statements, Object.get) More than one statement on a single line

---------------------------------------------------------------------------------------
Your code has been rated at 8.10/10 [raw score: 8.10/10] (previous run: 8.10/10, +0.00)
```

Overall, this method is more complex and requires using platform-specific ways of finding every python file in a directory to run pylint on. For those reasons, we recommend using the `run_pylint.py` script as detailed above.

#### Running with all checks enabled

To run with all checks, remove the `--disable=...` flag from the command:

```shell
python -m pylint file1.py file2.py
```

## Running via IDE/Editor Plugins

Plugins are available for `pylint` for a variety of different editors/IDEs. Some of the more popular ones are listed below:

- [PyCharm](https://plugins.jetbrains.com/plugin/11084-pylint) - pylint plugin that creates editor inspections for pylint checks
- [Visual Studio Code](https://code.visualstudio.com/docs/python/linting) - vscode plugin that runs pylint automatically
  - Make sure to set the following setting to replicate the specific checks used for this class:
  - `"python.linting.pylintArgs": ["--disable=C0111,R1705,E0401,R0201"]`
- [Atom](https://atom.io/packages/linter-pylint) - pylint plugin that leverages the Atom linters API to visualize errors in code
- [Emacs](https://docs.pylint.org/en/1.6.0/ide-integration.html#using-pylint-thru-flymake-in-emacs) - integration via `flymake`

> **Note**: it is recommended to run `pylint` via the script/directly at least once before submitting each milestone to make sure all errors are caught.

---

# Java /  Checkstyle

For Java, [Checkstyle](https://checkstyle.org/) is used, which is a static code analysis tool that helps programmers write Java code that adheres to a coding standard. For this class, *the coding standard is provided* in the form of a Checkstyle configuration file (more details below). As with pylint, there are a few ways of running Checkstyle, each of which are detailed below.

## Running Checkstyle with Script *(Recommended)*

A utility script was developed by the CS 2340 TAs to make running Checkstyle on your projects easier.

### Prerequisites

- Java installed and on the `PATH` [(tutorial)](https://www.java.com/en/download/help/path.xml)
- Python installed and on the `PATH` [(tutorial on Canvas... complete the "Installing Python" section)](https://gatech.instructure.com/files/7339157/download?download_frd=1)
- [Checkstyle script](https://raw.githubusercontent.com/jazevedo620/cs2340-codestyle/master/run_checkstyle.py) downloaded

### Running

The `run_checkstyle.py` script supports running checkstyle over every java file in a directory. For example, if my project structure is as follows:

```
project/
├── src/
│   ├── Application.java
│   ├── SpringUtilities.java
│   └── CalculatorWindow.java
└── run_checkstyle.py
```

then I can run checkstyle on every `.java` file in the project directory:

```shell
python run_checkstyle.py
```

This will output something like the following:

```shell
~/project/ $ python run_checkstyle.py

Downloading cs2340_checks.xml
100.0% 4873 / 4873

Downloading checkstyle-8.24-all.jar
100.0% 11625142 / 11625142

> Note: The checkstyle jar has been downloaded and a gitignore has automatically been created
        for you at the project root. This file should be checked into version control.

Running Checkstyle on 3 files:

Starting audit...
[WARN] ~/project/src/CalculatorWindow.java:29:43: ',' is preceded with whitespace. [NoWhitespaceBefore]
[WARN] ~/project/src/CalculatorWindow.java:41:44: '{' is not preceded with whitespace. [WhitespaceAround]
[WARN] ~/project/src/CalculatorWindow.java:52:22: Name 'CONSTRUCT_LAYOUT' must match pattern '^[a-z][a-zA-Z0-9]*$'. [MethodName]
[WARN] ~/project/src/CalculatorWindow.java:55: Line is longer than 100 characters (found 119). [LineLength]
... other errors ...
Audit done.

--------------------------------------------------------
Your code has been rated at 6.73/10 [raw score: 6.73/10]
```

As is shown in the example output, the script will automatically download the checkstyle jar and the code style XML config file and place them in the same folder as the `run_checkstyle.py` script.

> **Note** After this is run, the script will also modify or create a new `.gitignore` file that includes a rule for git to ignore the checkstyle jar file. This means that the jar will not appear to git in the working tree and cannot be staged/committed. **You should commit this file**, as it is considered bad practice to include compiled binaries/jars in git repositories.

The score given at the bottom is a metric of overall code quality, and is computed using the following formula where `e` is the number of Checkstyle errors/warnings and `n` is the number of Java statements in the scanned code:

![S(e,n)=10(1-(5e/n))](https://i.imgur.com/cqRVxbc.png)

## Running Checkstyle Directly

### Prerequisites

- Java installed and on the `PATH` [(tutorial)](https://www.java.com/en/download/help/path.xml)
- [checkstyle jar](https://github.com/checkstyle/checkstyle/releases/download/checkstyle-8.24/checkstyle-8.24-all.jar) downloaded and in the same directory as your code
- [configuration file](https://raw.githubusercontent.com/jazevedo620/cs2340-codestyle/master/cs2340_checks.xml) downloaded and in the same directory as your code

> **Note:** the given configuration file has only been tested with the latest version of Checkstyle as of writing this (8.24), so it might break with older versions

### Running

Once the required files are present, run the following command, adding each file to the end as necessary:

```shell
java -jar checkstyle-8.24-all.jar -c cs2340_checks.xm file1.java file2.java
```

The program should output something similar to the following, where each violation of Checkstyle is listed, along with it's filename, line number, and column number (where applicable).:

```shell
$ java -jar checkstyle-8.24-all.jar -c cs2340_checks.xml Application.java CalculatorWindow.java
Starting audit...
[WARN] ~/project/src/CalculatorWindow.java:29:43: ',' is preceded with whitespace. [NoWhitespaceBefore]
[WARN] ~/project/src/CalculatorWindow.java:41:44: '{' is not preceded with whitespace. [WhitespaceAround]
[WARN] ~/project/src/CalculatorWindow.java:52:22: Name 'CONSTRUCT_LAYOUT' must match pattern '^[a-z][a-zA-Z0-9]*$'. [MethodName]
[WARN] ~/project/src/CalculatorWindow.java:55: Line is longer than 100 characters (found 119). [LineLength]
... other errors ...
Audit done.
```

Overall, this method is more complex and requires using platform-specific ways of finding every java file in a directory to run Checkstyle on. For those reasons, we recommend using the `run_checkstyle.py` script as detailed above.

## Running via IDE/Editor Plugins

Plugins are available for Checkstyle for a variety of different editors/IDEs. Some of the more popular ones are listed below:

- [Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=shengchen.vscode-checkstyle) - vscode plugin runs checkstyle automatically
  - Make sure to follow the instructions at the link to set the `cs2340_checks.xml` as the Checkstyle configuration file
- [Eclipse](https://checkstyle.org/eclipse-cs/#!/) - Checkstyle integration into Eclipse
- [IntelliJ IDEA](https://plugins.jetbrains.com/plugin/1065-checkstyle-idea) - JetBrains plugin that adds Checkstyle side pane for realtime and on-demand Checkstyle running

> **Note**: it is recommended to run Checkstyle via the script/directly at least once before submitting each milestone to make sure all errors are caught.
