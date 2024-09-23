import subprocess
from pathlib import Path

CURRENT = Path(__file__).resolve().parent

import contextlib

import platform

PYINSTALLER = "pyinstaller" if platform.system() != "Linux" else "venv/bin/pyinstaller"

@contextlib.contextmanager
def cd(dir: str):
    import os

    cwd = os.getcwd()
    try:
        os.chdir(dir)
        yield
    finally:
        os.chdir(cwd)


def run_pyinstaller():
    with cd(str(CURRENT.parent)):
        subprocess.run(f"{PYINSTALLER} entry.py.spec".split(), check=True)


if __name__ == "__main__":
    run_pyinstaller()
