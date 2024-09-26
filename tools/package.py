import subprocess
from pathlib import Path
import sys

CURRENT = Path(__file__).resolve().parent
sys.path.insert(0, str(CURRENT.parent))
from tools.compile_all import main as compile_ui
from tools.translate import generate as generate_ts, compile as compile_ts

import contextlib  # noqa: E402

import platform  # noqa: E402

PYINSTALLER = "pyinstaller" if platform.system() != "Linux" else "venv/bin/pyinstaller"

PREFIX = "" if platform.system() != "Linux" else "venv/bin/"


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
        generate_ts()
        compile_ts()
        compile_ui()
        subprocess.run(f"{PYINSTALLER} entry.py.spec".split(), check=True)


if __name__ == "__main__":
    run_pyinstaller()
