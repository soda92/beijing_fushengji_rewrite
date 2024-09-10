from pathlib import Path
import subprocess

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
    subprocess.run(f"pyside6-uic {str(file)} -o {str(dest_path)}".split(), check=True)


if __name__ == "__main__":
    ui_dir.mkdir(parents=True, exist_ok=True)
    for i in get_ui_files():
        compile(i)
    subprocess.run(
        f"pyside6-rcc {str(CURRENT.parent.joinpath('main.qrc'))} -o {str(CURRENT.parent.joinpath('main_rc.py'))}".split(),
        check=True,
    )
