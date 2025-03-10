from pathlib import Path
import subprocess
import platform
import contextlib
import argparse


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
PROJ = CURRENT.parent.joinpath("beijing_fushengji")
ROOT = CURRENT.parent
import sys

sys.path.insert(0, str(ROOT))


form_dir = ROOT.joinpath("form")
ui_dir = PROJ.joinpath("ui")

RC_FILE = ROOT.joinpath("main.qrc")


def get_ui_files() -> list[Path]:
    files = form_dir.glob("*.ui")
    return list(files)


def get_dest_path(file: Path) -> Path:
    name = file.stem
    ui_name = f"{name}.py"
    return ui_dir.joinpath(ui_name)


def compile(file: Path):
    dest_path = get_dest_path(file)

    command = ".venv/Scripts/pyside6-uic.exe"
    if LINUX:
        command = "venv/bin/pyside6-uic"
    subprocess.run(f"{command} {file} -o {str(dest_path)}".split(), check=True)

    content = dest_path.read_text(encoding="utf8")
    dest_path.write_text(
        content.replace("import main_rc", "import beijing_fushengji.main_rc"),
        encoding="utf8",
    )


def compile_rc(file: Path = RC_FILE):
    command = ".venv/Scripts/pyside6-rcc.exe"
    if LINUX:
        command = "venv/bin/pyside6-rcc"

    out_file = PROJ.joinpath(f"{file.stem}_rc.py")
    subprocess.run(
        f"{command} {str(file)} -o {str(out_file)}".split(),
        check=True,
    )


def compile_forms():
    ui_dir.mkdir(parents=True, exist_ok=True)
    for i in get_ui_files():
        compile(i)


def get_mtimes(files):
    import os

    mtimes = []

    for file in files:
        mtimes.append(os.path.getmtime(str(file)))
    return mtimes


def compare(files, mtimes, last_mtimes):
    changed_files = []
    for i, v in enumerate(mtimes):
        if last_mtimes[i] != v:
            changed_files.append(files[i])
    return changed_files


def compile2(file: Path):
    print(f"file changed: {file}")
    if file.suffix == ".ui":
        compile(file)
    elif file.suffix == ".rc":
        compile_rc(file)
    elif file.suffix == ".ts":
        from tools.translate import compile as translate_compile

        translate_compile()
        # compile_rc(RC_FILE)


def get_all_files():
    files = get_ui_files()
    files.append(RC_FILE)
    widgets_files = list(PROJ.joinpath("widgets").glob("*.py"))
    files.extend(widgets_files)
    files.append(ROOT.joinpath("translation_zh_CN.ts"))
    return files


def build_help():
    files = ["help.html", "help_en.html"]

    for file in files:
        r = Path(__file__).parent.joinpath(file).read_text(encoding="utf8")
        dest_file = PROJ.joinpath(file.replace(".", "_") + ".py")
        r = 'help = r"""\n' + r + 'r"""'
        dest_file.write_text(r, encoding="utf8")


def main():
    compile_forms()
    from translate import compile
    compile()
    compile_rc(RC_FILE)
    build_help()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--watch", action="store_true", default=False)
    args = parser.parse_args()
    main()
    if args.watch:
        files = get_all_files()
        last_mtimes = get_mtimes(files)

        while True:
            mtimes = get_mtimes(files)
            diff_files = compare(files, mtimes, last_mtimes)
            for file in diff_files:
                compile2(file)
            last_mtimes = mtimes

            if len(diff_files) > 0:
                ui_dir.joinpath("_reload").write_text("")

            import time

            time.sleep(1)
