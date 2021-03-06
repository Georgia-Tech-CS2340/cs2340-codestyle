---
title: "2340 Checkstyle Guide"
author: 2340 TAs
date: February 17th 2021
output: pdf_document
---

# Java /  Checkstyle

For Java, [Checkstyle](https://checkstyle.org/) is used, which is a static code analysis tool that helps programmers write Java code that adheres to a coding standard. For this class, *the coding standard is provided* in the form of a Checkstyle configuration file. It can be [downloaded directly from github](https://raw.githubusercontent.com/Georgia-Tech-CS2340/cs2340-codestyle/master/cs2340_checks.xml), and is based off of the one used in CS 1332, Data Structures & Algorithms. **It is important that you run this configuration file on Checkstyle 8.41.** More details on each check can be found in the [official Checkstyle documentation](https://checkstyle.sourceforge.io/checks.html).

In addition, there are some examples of compliant/noncompliant example code provided:

- [`CalculatorWindow.java` (non-compiliant)](https://github.com/Georgia-Tech-CS2340/cs2340-codestyle/blob/master/swing/CalculatorWindow.java) - example Swing application with poor formatting
- [`CalculatorWindowFormatted.java` (compliant)](https://github.com/Georgia-Tech-CS2340/cs2340-codestyle/blob/master/swing/CalculatorWindowFormatted.java) - same as above, plus it passes all Checkstyle checks

As with pylint, there are a few different ways of running Checkstyle, each of which are detailed below.

## Running Checkstyle with Script *(Recommended)*

A utility script was developed by the CS 2340 TAs to make running Checkstyle on your projects easier.

### Prerequisites

- Java installed and on the `PATH` [(tutorial)](https://www.java.com/en/download/help/path.xml)
- Python **3** installed and on the `PATH` [(tutorial for Windows here)](https://geek-university.com/python/add-python-to-the-windows-path/)
- [Checkstyle script](https://raw.githubusercontent.com/Georgia-Tech-CS2340/cs2340-codestyle/master/run_checkstyle.py) downloaded

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
100.0% 4 KB / 4 KB

Downloading checkstyle-8.41-all.jar
100.0% 11352 KB / 11352 KB

> Note: The checkstyle jar has been downloaded and a gitignore has automatically been created
        for you at the project root. This file should be checked into version control.

Running Checkstyle on 3 files (run with -v to view files):

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

#### Running over another directory

To run the script on a directory other than the current working directory, specify a relative or absolute path using `--root path/to/folder`:

```shell
python run_checkstyle.py --root path/to/folder
```

## Running Checkstyle Directly

### Prerequisites

- Java installed and on the `PATH` [(tutorial)](https://www.java.com/en/download/help/path.xml)
- [checkstyle jar](https://github.com/checkstyle/checkstyle/releases/download/checkstyle-8.41/checkstyle-8.41-all.jar) (version 8.41) downloaded and in the same directory as your code
- [configuration file](https://raw.githubusercontent.com/Georgia-Tech-CS2340/cs2340-codestyle/master/cs2340_checks.xml) downloaded and in the same directory as your code

> **Note:** the given configuration file has only been tested with the latest version of Checkstyle as of writing this (8.41), so it might break with older versions

### Running

Once the required files are present, run the following command, adding each file to the end as necessary:

```shell
java -jar checkstyle-8.41-all.jar -c cs2340_checks.xm file1.java file2.java
```

The program should output something similar to the following, where each violation of Checkstyle is listed, along with its filename, line number, and column number (where applicable):

```shell
$ java -jar checkstyle-8.41-all.jar -c cs2340_checks.xml Application.java CalculatorWindow.java
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

> **Warning**: It is not sufficient to show the IDE checkstyle results during a demo. To receive credit for the checkstyle portion, the official script must be run during the demo and the TAs must see the output. These instructions are provided for your convenience.

Plugins are available for Checkstyle for a variety of different editors/IDEs. Some of the more popular ones are listed below:

- [Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=shengchen.vscode-checkstyle) - vscode plugin runs checkstyle automatically
  - Make sure to follow the instructions at the link to set the `cs2340_checks.xml` as the Checkstyle configuration file
- [Eclipse](https://checkstyle.org/eclipse-cs/#!/) - Checkstyle integration into Eclipse
- [IntelliJ IDEA](https://plugins.jetbrains.com/plugin/1065-checkstyle-idea) - JetBrains plugin that adds Checkstyle side pane for real-time and on-demand Checkstyle running
  - **Make sure to set the Checkstyle version to 8.41 in the Checkstyle settings** (you may need to update your plugin to see this option appear)

> **Note**: it is recommended to run Checkstyle via the script/directly at least once before submitting each milestone to make sure all errors are caught.
