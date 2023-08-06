import os
from contextlib import contextmanager
import re
import unicodedata
from functools import wraps
import asyncio
import subprocess
import shlex
import psutil

SUPERSCRIPT_REGEX = re.compile(r"\^([+|-]?\d+)")

MYSTRAN_VERSION_REGEX = re.compile(
    "MYSTRAN\s+[V|v]ersion\s+(?P<version>.*?)\s+(?P<date>(\w+\s+){3})"
)


def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()


def get_mystran_version():
    cmd = os.environ["MYSTRAN_BIN"]
    proc = subprocess.Popen(
        shlex.split(cmd), stderr=subprocess.STDOUT, stdout=subprocess.PIPE
    )
    try:
        proc.wait(timeout=0.1)
    except subprocess.TimeoutExpired:
        kill(proc.pid)
    lines = proc.stdout.read().decode().split("\n")
    for line in lines:
        line = line.strip()
        if line.startswith("MYSTRAN Version"):
            match = MYSTRAN_VERSION_REGEX.match(line)
            version, date, *a = match.groups()
            mystran_attrs = {
                "version": version.strip(),
                "date": date.strip().replace(" ", "-"),
            }
            return mystran_attrs


def slugify(txt):

    """
    Slugify a unicode string.

    >>> slugify("Héllo Wörld-LCID#2")
    'hello_world_lcid2'
    >>> slugify("mystran-test-cases.BAR.no_offset.test_bar_06.ini")
    'bar_no_offset_test_bar_06_ini'
    """
    txt = unicodedata.normalize("NFKD", txt)
    txt = txt.replace("mystran-test-cases.", "")
    txt = txt.replace("mystran-test-cases" + os.sep, "")
    txt = txt.replace(os.sep, ".")
    txt = txt.replace(".", "_")
    txt = re.sub(r"[^\w\s-]", "", txt).strip().lower()
    return re.sub(r"[-\s]+", "_", txt)


@contextmanager
def working_directory(path):
    """
    A context manager which changes the working directory to the given
    path, and then changes it back to its previous value on exit.
    Usage:
    > # Do something in original directory
    > with working_directory('/my/new/path'):
    >     # Do something in new directory
    > # Back to old directory
    """

    prev_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
