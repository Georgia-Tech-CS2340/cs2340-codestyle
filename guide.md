# Python / `pylint`

# Java /  Checkstyle

For Java, [Checkstyle](https://checkstyle.org/) is used, which is a static code analysis tool that helps programmers write Java code that adheres to a coding standard. For this class, *the coding standard is provided* in the form of a Checkstyle configuration file (more details below). There are a few ways of running checkstyle, each of which are detailed below.

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
|   ├── Application.java
|   ├── CalculatorWindow.java
|   ├── SpringUtilities.java
|   └── CalculatorWindowFormatingTest.java
└── run_checkstyle.py
```

then I can run checkstyle on every `.java` file in the project directory:

```bash
~/project/ $ python run_checkstyle.py
```

This will output something like the following:

```bash
Downloading checkstyle-8.24-all.jar
100.1% 11632640 / 11625142

> Note:

Running Checkstyle on 4 files:
 - ~/cs2340-codestyle/swing/Application.java
 - ~/cs2340-codestyle/swing/CalculatorWindow.java
 - ~/cs2340-codestyle/swing/CalculatorWindowFormattingTest.java
 - ~/cs2340-codestyle/swing/SpringUtilities.java

Starting audit...
[WARN] ~/cs2340-codestyle/swing/CalculatorWindowFormattingTest.java:29:43: ',' is preceded with whitespace. [NoWhitespaceBefore]
[WARN] ~/cs2340-codestyle/swing/CalculatorWindowFormattingTest.java:41:44: '{' is not preceded with whitespace. [WhitespaceAround]
... more errors
Audit done.

--------------------------------------------------------
Your code has been rated at 1.13/10 [raw score: 1.13/10]
```

## Running Checkstyle Directly

### Prerequisites

- Java installed and on the `PATH` [(tutorial)](https://www.java.com/en/download/help/path.xml)
- [checkstyle jar](https://github.com/checkstyle/checkstyle/releases/download/checkstyle-8.24/checkstyle-8.24-all.jar) downloaded and in the same directory as your code
- [configuration file](https://raw.githubusercontent.com/jazevedo620/cs2340-codestyle/master/cs2340_checks.xml) downloaded and in the same directory as your code

> **Note:** the given configuration file has only been tested with the latest version of Checkstyle as of writing this (8.24), so it might break with older versions

### Running

Once the required files are present, run the following command, adding each file to the end as necessary:

```bash
java -jar checkstyle-8.24-all.jar -c cs2340_checks.xm file1.java file2.java
```

The program should output something similar to the following, where each violation of Checkstyle is listed, along with it's filename, line number, and column number (where applicable).:

```
$ java -jar checkstyle-8.24-all.jar -c cs2340_checks.xml Application.java CalculatorWindowFormattingTest.java
Starting audit...
[WARN] cs2340-codestyle\swing\CalculatorWindowFormattingTest.java:29:43: ',' is preceded with whitespace. [NoWhitespaceBefore]
[WARN] cs2340-codestyle\swing\CalculatorWindowFormattingTest.java:41:44: '{' is not preceded with whitespace. [WhitespaceAround]
[WARN] cs2340-codestyle\swing\CalculatorWindowFormattingTest.java:52: Abbreviation in name 'CONSTRUCT_LAYOUT' must contain no more than '4' consecutive capital letters. [AbbreviationAsWordInName]
Audit done.
```
