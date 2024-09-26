from pathlib import Path
import subprocess
import platform
import contextlib


@contextlib.contextmanager
def cd(dir: str):
    import os

    cwd = os.getcwd()
    try:
        os.chdir(dir)
        yield
    finally:
        os.chdir(cwd)


PREFIX = "" if platform.system() != "Linux" else "venv/bin/"

LINUX = platform.system() == "Linux"
UCRT = False
if platform.system() == "Windows":
    if Path("C:/msys64/ucrt64").exists():
        UCRT = True

CURRENT = Path(__file__).resolve().parent
form_dir = CURRENT.parent.joinpath("form")
ui_dir = CURRENT.parent.joinpath("ui")


def get_ui_files() -> list[Path]:
    files = form_dir.glob("*.ui")
    return files


def get_dest_path(file: Path) -> Path:
    name = file.stem
    ui_name = f"{name}.py"
    return ui_dir.joinpath(ui_name)


def compile(file: Path):
    dest_path = get_dest_path(file)

    command = "venv/Scripts/pyside6-uic.exe"
    if LINUX:
        command = "venv/bin/pyside6-uic"
    subprocess.run(f"{command} {str(file)} -o {str(dest_path)}".split(), check=True)


def compile_rc():
    command = "venv/Scripts/pyside6-rcc.exe"
    if LINUX:
        command = "venv/bin/pyside6-rcc"
    subprocess.run(
        f"{command} {str(CURRENT.parent.joinpath('main.qrc'))} -o {str(CURRENT.parent.joinpath('main_rc.py'))}".split(),
        check=True,
    )


def compile_forms():
    ui_dir.mkdir(parents=True, exist_ok=True)
    for i in get_ui_files():
        compile(i)

def main():
    compile_forms()
    compile_rc()


if __name__ == "__main__":
    main()
