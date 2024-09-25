import subprocess
import pathlib

PREFIX = ""
if pathlib.Path("venv/bin/python").exists():
    PREFIX += "venv/bin"
elif pathlib.Path("venv/Scripts/python.exe").exists():
    PREFIX += "venv/Scripts"


def run(command):
    subprocess.run(f"{PREFIX}/{command}".split(), check=True)


run("pyside6-lupdate form/net_cafe.ui console/mainwindow.py -ts translation_zh_CN.ts")
run("pyside6-linguist translation_zh_CN.ts")
run("pyside6-lrelease translation_zh_CN.ts")
