"""
Checkstyle script to automatically run Checkstyle on every java source file within
the current working directory (using class-specific options)
"""

import os
import argparse
import urllib.request
import sys
import re
import subprocess
from subprocess import PIPE
from shutil import which

__author__ = "CS 2340 TAs"
__version__ = "1.0"

DESCRIPTION = "Checkstyle script to run checkstyle on every .java file in the CWD"
JAVA_EXTENSION = ".java"
BASE_PROCESS = ["java", "-jar"]
CHECKSTYLE_JAR_NAME = "checkstyle-8.24-all.jar"
CHECKSTYLE_JAR_URL = "https://github.com/checkstyle/checkstyle/releases/download/checkstyle-8.24/checkstyle-8.24-all.jar" # pylint: disable=line-too-long
CHECKSTYLE_JAR_GITIGNORE = "checkstyle-*.jar"
CHECKSTYLE_JAR_PATTERN = "checkstyle-.*\.jar"
CHECKSTYLE_XML_NAME = "cs2340_checks.xml"
CHECKSTYLE_XML_URL = "https://raw.githubusercontent.com/jazevedo620/cs2340-codestyle/master/cs2340_checks.xml" # pylint: disable=line-too-long

# Scoring
MULTILINE_COMMENT_REGEX = r"\/\*([\S\s]+?)\*\/"
SINGLELINE_COMMENT_REGEX = r"\/{2,}.+"
STATEMENT_REGEX = r"[^;]+?;"
AFTER_BRACE_REGEX = r"{\s*;"
EMPTY_STATEMENT_REGEX = r"^\s*;"
CHECKSTYLE_OUTPUT_REGEX = r"^\[[A-Z]+\] (.+?):\d+(?::\d+?)?:"
ERROR_TEXT_REGEX = r"CheckstyleException: Exception was thrown while processing .+\.java"
SCORE_FORMAT = """Your code has been rated at {:.2f}/10 [raw score: {:.2f}/10]"""

# Gitignore analysis
GIT_REPO_COMMAND = ["git", "rev-parse", "--show-toplevel"]
GIT_REPO_FAILED_SUBSTRING = "fatal: not a git repository"
GITIGNORE = ".gitignore"
IGNORED_FILE_COMMAND = ["git", "status", "--ignored", "--short"]
IGNORED_FILE_REGEX = "^!! (.+)$"

# Patterns
NO_JAVA_TEXT = """
Java is required to run Checkstyle. Make sure it is installed
and that it exists on your PATH. More instructions are available here:

https://www.java.com/en/download/help/path.xml"""
ADDED_GITIGNORE_TEXT = """
> Note: The checkstyle jar has been downloaded and a gitignore has automatically been created
        for you at the project root. This file should be checked into version control.
""".lstrip()
MODIFIED_GITIGNORE_TEXT = """
> Note: The checkstyle jar has been downloaded and automatically added to your gitignore.
        This change should be checked into version control.
""".lstrip()


def main(root=None, verbose=False):
    """
    Runs the main checkstyle script and parses/redirects output
    """

    # Verify java is installed
    if which("java") is None:
        print(NO_JAVA_TEXT)
        return

    # Assemble dependencies
    print()
    xml_path, _ = find_or_download(CHECKSTYLE_XML_NAME, CHECKSTYLE_XML_URL)
    jar_path, jar_downloaded = find_or_download(CHECKSTYLE_JAR_NAME, CHECKSTYLE_JAR_URL)
    if jar_downloaded:
        result, mode = add_to_gitignore(jar_path)
        if result:
            print(ADDED_GITIGNORE_TEXT if mode == "add" else MODIFIED_GITIGNORE_TEXT)

    path = os.path.abspath(root) if root is not None else os.getcwd()
    files = find_files(path, JAVA_EXTENSION)

    print("Running Checkstyle on {} files:".format(len(files)))
    # Print each file in verbose mode
    if verbose:
        for file in files:
            print(" - {}".format(file))

    output = run_checkstyle(files, jar_path=jar_path, xml_path=xml_path)
    print()
    print(output)

    # Print score
    score = 0 if re.search(ERROR_TEXT_REGEX, output) else assemble_score(files, output)
    score_output = SCORE_FORMAT.format(max(score, 0), score)
    print(len(score_output) * "-")
    print(score_output)
    print()


def add_to_gitignore(filename):
    """
    Adds the given file to the gitignore if applicable/necessary
    """

    if which("git") is None:
        return False, ""

    repo_relative_folder = os.path.dirname(filename)
    result = subprocess.run(GIT_REPO_COMMAND, stdout=PIPE, cwd=repo_relative_folder)
    repo_root = result.stdout.decode(sys.stdout.encoding).strip()

    if GIT_REPO_FAILED_SUBSTRING in repo_root:
        return False, ""

    # Clean path
    repo_root = os.path.normpath(repo_root)

    # Find .gitignore file if it exists by walking down the tree
    gitignore_path = find_gitignore(repo_root, repo_relative_folder)

    # Do nothing
    if is_ignored(CHECKSTYLE_JAR_PATTERN, cwd=repo_relative_folder):
        return False, ""

    if gitignore_path is None:
        # Create gitignore file at project root
        with open(os.path.join(repo_root, GITIGNORE), "w") as gitignore:
            gitignore.write(CHECKSTYLE_JAR_GITIGNORE + "\n")
        return True, "add"

    # Append to existing
    with open(gitignore_path, "a") as gitignore:
        gitignore.write(CHECKSTYLE_JAR_GITIGNORE + "\n")
    return True, "modify"


def find_gitignore(repo_root, top_folder):
    """
    Finds the first .gitignore file starting at the top_folder and walking up
    the tree until the repo_root is found, or None if not found
    """

    repo_root = os.path.normpath(repo_root)
    current_path = os.path.normpath(top_folder)
    while len(current_path) >= len(repo_root):
        gitignore_path = os.path.join(current_path, GITIGNORE)
        if os.path.exists(gitignore_path):
            return gitignore_path

        current_path = os.path.dirname(current_path)

    return None


def is_ignored(regex, cwd=None):
    """
    Determines whether the given file is ignored in its containing git repository
    """

    result = subprocess.run(IGNORED_FILE_COMMAND, stdout=PIPE, cwd=cwd)
    output = result.stdout.decode(sys.stdout.encoding)
    for line in output.splitlines():
        match = re.search(IGNORED_FILE_REGEX, line)
        if match:
            line_filename = match.group(1)
            if re.search(regex, line_filename):
                return True

    return False


def find_or_download(filename, url):
    """
    Finds a file with the given filename in the same directory as the current
    script or downloads it from the given url if it doesn't exist
    """

    current_dir = os.path.dirname(os.path.realpath(__file__))
    target_path = os.path.join(current_dir, filename)
    exists = os.path.exists(target_path)

    if exists:
        return target_path, False

    # Download file
    print("Downloading {}".format(filename))
    urllib.request.urlretrieve(url, target_path, reporthook)
    print()
    return target_path, True


def assemble_score(files, checkstyle_output):
    """
    Calculates code "score" using the same formula as pylint for consistency:
    https://docs.pylint.org/en/1.6.0/faq.html#pylint-gave-my-code-a-negative-rating-out-of-ten-that-can-t-be-right
    """  # pylint: disable=line-too-long

    errors = count_errors(checkstyle_output)
    statements = 0
    for filename in files:
        statements += count_statements(filename)

    if statements == 0:
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
        contents = java_file.read()
        contents = re.sub(MULTILINE_COMMENT_REGEX, "", contents)
        contents = re.sub(SINGLELINE_COMMENT_REGEX, "", contents)
        for match in re.finditer(STATEMENT_REGEX, contents):
            statement_candidate = match.group()
            if not re.search(AFTER_BRACE_REGEX, statement_candidate) and not re.search(
                    EMPTY_STATEMENT_REGEX, statement_candidate):
                count += 1

    return count


def reporthook(blocknum, blocksize, totalsize):
    """
    Report hook callback for urllib.request.urlretrieve
    Sourced from:
    https://stackoverflow.com/questions/13881092/download-progressbar-for-python-3
    """

    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = min(readsofar * 1e2 / totalsize, 1e2)
        progress = "\r{:5.1f}% {:d} / {:d}".format(percent, min(totalsize, readsofar), totalsize)
        sys.stdout.write(progress)
        if readsofar >= totalsize:
            sys.stdout.write("\n")
    else:
        sys.stdout.write("read %d\n" % (readsofar,))


def run_checkstyle(files, jar_path=None, xml_path=None):
    """
    Runs checkstyle on every file specified using the class-specific
    arguments as well as any additional ones specified

    Parameters:
    files (array(string)): filepaths to java source files

    Named:
    jar_path (string): The filepath to the checkstyle jar
    xml_path (string): The filepath to the checkstyle config XML file

    Returns:
    the stdout output from checkstyle
    """

    if not files or jar_path is None or xml_path is None:
        return ""

    args = BASE_PROCESS + [jar_path, "-c", xml_path] + files
    result = subprocess.run(args, stdout=PIPE, stderr=PIPE)
    return result.stdout.decode(sys.stdout.encoding) + result.stderr.decode(sys.stderr.encoding)


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
                        help="the path to run checkstyle over (defaults to current directory)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="whether to display additional output")

    # Parse arguments
    parsed_args = parser.parse_args()
    main(root=parsed_args.root, verbose=parsed_args.verbose)


# Run script
if __name__ == "__main__":
    bootstrap()
