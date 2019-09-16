"""
Checkstyle script to automatically run Checkstyle on every java source file within
the current working directory (using class-specific options)
"""

import os
import argparse
import subprocess
import urllib.request
import sys
import re
from subprocess import PIPE
from shutil import which

__author__ = "CS 2340 TAs"
__version__ = "1.0"

DESCRIPTION = "Checkstyle script to run checkstyle on every .java file in the CWD"
JAVA_EXTENSION = ".java"
CHECKSTYLE_JAR_NAME = "checkstyle-8.24-all.jar"
CHECKSTYLE_JAR_URL = "https://github.com/checkstyle/checkstyle/releases/download/checkstyle-8.24/checkstyle-8.24-all.jar"
CHECKSTYLE_XML_NAME = "cs2340_checks.xml"
CHECKSTYLE_XML_URL = "https://raw.githubusercontent.com/jazevedo620/cs2340-codestyle/master/src/cs2340_checks.xml"
BASE_PROCESS = ["java", "-jar"]
MULTILINE_COMMENT_REGEX = r"\/\*([\S\s]+?)\*\/"
SINGLELINE_COMMENT_REGEX = r"\/{2,}.+"
STATEMENT_REGEX = r"[^;]+?;"
AFTER_BRACE_REGEX = r"{\s*;"
EMPTY_STATEMENT_REGEX = r"^\s*;"
CHECKSTYLE_OUTPUT_REGEX = r"^\[[A-Z]+\] (.+?):\d+(?::\d+?)?:"
SCORE_FORMAT = """Your code has been rated at {:.2f}/10 [raw score: {:.2f}/10]"""


def main(root=None, verbose=False, strict=False):
    """
    Runs the main checkstyle script and parses/redirects output
    """

    # Verify java is installed
    if which("java") is None:
        print(
            """Java is required to run Checkstyle. Make sure it is installed
and that it exists on your PATH. More instructions are available here:

https://www.java.com/en/download/help/path.xml""")
        return

    # Assemble dependencies
    print()
    jar_path = find_or_download(CHECKSTYLE_JAR_NAME, CHECKSTYLE_JAR_URL)
    xml_path = find_or_download(CHECKSTYLE_XML_NAME, CHECKSTYLE_XML_URL)

    path = os.path.abspath(root) if root is not None else os.getcwd()
    files = find_files(path, JAVA_EXTENSION)

    print("Running Checkstyle on {} files:".format(len(files)))
    # Print each file in verbose mode
    if verbose:
        for file in files:
            print(" - {}".format(file))

    output = run_checkstyle(files, jar_path=jar_path,
                            xml_path=xml_path, strict=strict)
    print()
    print(output)

    # Print score
    score = assemble_score(files, output)
    score_output = SCORE_FORMAT.format(max(score, 0), score)
    print(len(score_output) * "-")
    print(score_output)
    print()


def find_or_download(filename, url):
    """
    Finds a file with the given filename in the same directory as the current
    script or downloads it from the given url if it doesn't exist
    """

    current_dir = os.path.dirname(os.path.realpath(__file__))
    target_path = os.path.join(current_dir, filename)
    exists = os.path.exists(target_path)

    if (exists):
        return target_path

    # Download file
    print("Downloading {}".format(filename))
    urllib.request.urlretrieve(url, target_path, reporthook)
    print()
    return target_path


def assemble_score(files, checkstyle_output):
    """
    Calculates code "score" using the same formula as pylint for consistency:
    https://docs.pylint.org/en/1.6.0/faq.html#pylint-gave-my-code-a-negative-rating-out-of-ten-that-can-t-be-right
    """

    errors = count_errors(checkstyle_output)
    statements = 0
    for filename in files:
        statements = count_statements(filename)

    if statements is 0:
        return 10.0

    return 10.0 - ((float(5 * errors) / statements) * 10)


def count_errors(checkstyle_output):
    """
    Counts total checkstyle errors given the checkstyle stdout
    """

    count = 0
    for line in checkstyle_output.splitlines():
        if line.startswith("["):
            if re.match(CHECKSTYLE_OUTPUT_REGEX, line):
                count += 1

    return count


def count_statements(filename):
    """
    Counts the number of Java statements included in a file
    each semicolon counts as a semicolon as long as it isn't preceded by only
    whitespace or brackets before the previous semicolon
    """

    if not os.path.exists(filename):
        return 0

    count = 0
    with open(filename, "r+") as java_file:
        buffer = ""
        contents = java_file.read()
        contents = re.sub(MULTILINE_COMMENT_REGEX, "", contents)

        for line in contents.splitlines():
            buffer += line
            if ";" in buffer:
                # Remove single-line comments
                buffer = re.sub(SINGLELINE_COMMENT_REGEX, "", buffer)

                # Process buffer
                for match in re.finditer(STATEMENT_REGEX, buffer):
                    statement_candidate = match.group()
                    if not re.search(AFTER_BRACE_REGEX, buffer) and not re.search(EMPTY_STATEMENT_REGEX, buffer):
                        count += 1

                # Clear buffer
                buffer = ""

            if len(buffer) > 1024:
                # Flush buffer
                buffer = buffer[-128:]

    return count


def reporthook(blocknum, blocksize, totalsize):
    """
    Report hook callback for urllib.request.urlretrieve
    Sourced from:
    https://stackoverflow.com/questions/13881092/download-progressbar-for-python-3
    """

    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        s = "\r%5.1f%% %*d / %d" % (
            percent, len(str(totalsize)), readsofar, totalsize)
        sys.stdout.write(s)
        if readsofar >= totalsize:
            sys.stdout.write("\n")
    else:
        sys.stdout.write("read %d\n" % (readsofar,))


def run_checkstyle(files, jar_path=None, xml_path=None, strict=False):
    """
    Runs checkstyle on every file specified using the class-specific
    arguments as well as any additional ones specified

    Parameters:
    files (array(string)): filepaths to java source files

    Named:
    strict (boolean): Whether to run the linter in strict mode
    jar_path (string): The filepath to the checkstyle jar
    xml_path (string): The filepath to the checkstyle config XML file

    Returns:
    the stdout output from checkstyle
    """

    if not files or jar_path is None or xml_path is None:
        return ""

    args = BASE_PROCESS + [jar_path, "-c", xml_path] + files
    result = subprocess.run(args, stdout=PIPE)
    return result.stdout.decode(sys.stdout.encoding)


def find_files(path, extension):
    """
    Gets a list of every file in the given path that has the given file extension
    """

    file_list = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                file_list.append(os.path.join(root, file))

    return file_list


def bootstrap():
    """
    Runs CLI parsing/execution
    """

    # Argument definitions
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("--root", "-r", metavar="path",
                        help="the path to run checkstyle over (defaults to current working directory)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="whether to display additional output")
    parser.add_argument("--all", "-a", "--strict", action="store_true",
                        help="enables all checks (strict mode)")

    # Parse arguments
    parsed_args = parser.parse_args()
    main(root=parsed_args.root, verbose=parsed_args.verbose, strict=parsed_args.all)


# Run script
if __name__ == "__main__":
    bootstrap()
