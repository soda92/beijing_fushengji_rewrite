from pathlib import Path
import glob

CURRENT = Path(__file__).resolve().parent


def get_ui_files() -> list[Path]:
    files = glob.glob("**/*.ui", recursive=True, root_dir=str(CURRENT))
    files_fullpath = [
        CURRENT.joinpath(i) for i in files
    ]
    return files_fullpath

if __name__ == "__main__":
    pass
