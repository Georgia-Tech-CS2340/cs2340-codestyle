"""
Checkstyle script to automatically run pylint on every python source file within
the current working directory (using class-specific options)
"""

# Dependency check
try:
    # pylint: disable=unused-import
    import pylint
except ImportError:
    print(
        """Error, Module pylint is required
********************************
It can be installed by running:

  pip install pylint
""")
    import sys
    sys.exit()

import os
import re
import sys
import datetime
import argparse
import platform
import warnings
from pylint import epylint as lint

__author__ = "CS 2340 TAs"
__version__ = "1.0"

DESCRIPTION = "Checkstyle script to run pylint on every .py file in the CWD"
DISABLED_CHECKS = ["missing-docstring",
                   "no-else-return", "import-error", "no-self-use"]
BASE_OPTIONS = "--const-naming-style=any"
PYTHON_EXTENSION = ".py"
SCORE_REGEX = r"-+\s+Your code has been rated at (-?[0-9\.]+)\/10( \(previous run: -?[0-9\.]+\/10, [-+][0-9\.]+\))?"
SCORE_FORMAT = """Your code has been rated at {:.2f}/10 [raw score: {:.2f}/10]"""


def main(root=None, verbose=False, process_count=None, strict=False):
    """
    Runs the main pylint script and parses/redirects output
    """

    args = []
    if process_count is not None:
        args.append("-j {}".format(process_count))

    try:
        path = os.path.abspath(root) if root is not None else os.getcwd()
        # Filter out the current script
        current_script = os.path.basename(__file__)
        files = [f for f in find_files(
            path, PYTHON_EXTENSION) if not f.endswith(current_script)]

        print()
        print("Running pylint on {} files:".format(len(files)))
        # Print each file in verbose mode
        if verbose:
            for file in files:
                print(" - {}".format(file))

        output = run_linter(files, " ".join(args), strict=strict)
        print()
        print(re.sub(SCORE_REGEX, "", output).rstrip())
        print()

        # Print score
        match = re.search(SCORE_REGEX, output)
        if match:
            score = float(match.group(1))
            score_output = SCORE_FORMAT.format(max(score, 0), score)

            # Add previous score addendum if it exists
            if match.group(2) is not None:
                score_output += match.group(2)

            print(len(score_output) * "-")
            print(score_output)
            print()

    except Exception as e:
        print_crash_info(e)


def run_linter(files, args, strict=False):
    """
    Runs pylint on every file specified using the class-specific
    arguments as well as any additional ones specified

    Parameters:
    files (array(string)): filepaths to python source files
    args (string): CLI arguments

    Named:
    strict (boolean): Whether to run the linter in strict mode

    Returns:
    the stdout output from pylint
    """

    if not files:
        return ""

    command = "{} {}".format(" ".join(files), get_options(args, strict=strict))
    try:
        (pylint_stdout, _) = lint.py_run(command, return_std=True)
        return pylint_stdout.getvalue()
    except:
        return ""



def find_files(path, extension):
    """
    Gets a list of every file in the given path that has the given file extension
    """

    try:
        file_list = []
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(extension):
                    file_list.append(os.path.join(root, file))
    except:
        return []

    return file_list


def get_options(additional_options, strict=False):
    """
    Formats the options string

    Named:
    strict (boolean): Whether to run the linter in strict mode

    Parameters:
    additional_options (string): additional arguments passed to the CLI to append
    """

    if strict:
        return additional_options

    return "--disable={} {} {}".format(",".join(DISABLED_CHECKS), BASE_OPTIONS, additional_options)

def print_crash_info(e):
    """
    Prints system/error information in the case of an unexpected crash
    """
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    print("An unexpected error has ocurred in the pylint script")
    print("===================================================================")
    print("Please make a private post on Piazza with the following information")
    print(e)
    print("===================================================================")
    print("Time: {}".format(str(datetime.datetime.now())))
    print("Script: run_pylint.py")
    print("Python version: {} => {}".format(sys.version, sys.version_info))
    print("Platform: {}".format(sys.platform))
    print("Architecture: {}".format(platform.architecture()))
    print("Distribution: {}".format(platform.dist()))
    print("Processor: {}".format(platform.processor()))
    print("System: {}".format(platform.system()))
    print("uname: {}".format(platform.uname()))
    print("CPU Count: {}".format(os.cpu_count()))
    print("===================================================================")

def bootstrap():
    """
    Runs CLI parsing/execution
    """

    # Argument definitions
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("--root", "-r", metavar="path",
                        help="the path to run pylint over (defaults to current working directory)")
    parser.add_argument("--parallel", "-p", "-j", metavar="count",
                        help="the number of parallel processes to split pylint into")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="whether to display additional output")
    parser.add_argument("--all", "-a", "--strict", action="store_true",
                        help="enables all checks (strict mode)")

    # Parse arguments
    parsed_args = parser.parse_args()
    main(root=parsed_args.root, process_count=parsed_args.parallel,
         verbose=parsed_args.verbose, strict=parsed_args.all)


# Run script
if __name__ == "__main__":
    bootstrap()
