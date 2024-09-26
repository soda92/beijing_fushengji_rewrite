import subprocess
import pathlib
import contextlib
from pathlib import Path

CURRENT = Path(__file__).resolve().parent


@contextlib.contextmanager
def cd(dir: str):
    import os

    cwd = os.getcwd()
    try:
        os.chdir(dir)
        yield
    finally:
        os.chdir(cwd)


PREFIX = ""
if pathlib.Path("venv/bin/python").exists():
    PREFIX += "venv/bin/"
elif pathlib.Path("venv/Scripts/python.exe").exists():
    PREFIX += "venv/Scripts/"


def run(command):
    subprocess.run(f"{PREFIX}{command}".split(), check=True)


def get_files(folder: str, ext: str):
    with cd(str(CURRENT.parent)):
        files1 = pathlib.Path(folder).glob(f"*.{ext}")
        files1 = [f"{folder}/{x.name}" for x in files1]
        return files1


def generate():
    all_files = []
    all_files.extend(get_files("form", "ui"))
    all_files.extend(get_files("widgets", "py"))
    all_files.extend(get_files("console", "py"))

    with cd(str(CURRENT.parent)):
        run(f"pyside6-lupdate {' '.join(all_files)} -ts translation_zh_CN.ts")


def translate():
    with cd(str(CURRENT.parent)):
        run("pyside6-linguist translation_zh_CN.ts")


def compile():
    with cd(str(CURRENT.parent)):
        run("pyside6-lrelease translation_zh_CN.ts")


if __name__ == "__main__":
    generate()
    translate()
    compile()
