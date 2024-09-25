import subprocess
import pathlib

PREFIX = ""
if pathlib.Path("venv/bin/python").exists():
    PREFIX += "venv/bin"
elif pathlib.Path("venv/Scripts/python.exe").exists():
    PREFIX += "venv/Scripts"


def run(command):
    subprocess.run(f"{PREFIX}/{command}".split(), check=True)

files1 = pathlib.Path("form").glob("*.ui")
files1 = [f"form/{x.name}" for x in files1]

files2 = pathlib.Path("widgets").glob("*.py")
files2 = [f"widgets/{x.name}" for x in files2]

files3 = pathlib.Path("console").glob("*.py")
files3 = [f"console/{x.name}" for x in files3]

all_files = []
all_files.extend(files1)
all_files.extend(files2)
all_files.extend(files3)

run(f"pyside6-lupdate {' '.join(all_files)} -ts translation_zh_CN.ts")
run("pyside6-linguist translation_zh_CN.ts")
run("pyside6-lrelease translation_zh_CN.ts")
