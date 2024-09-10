import tempfile
import sys
import os
import subprocess
from pathlib import Path

CURRENT = Path(__file__).resolve().parent

sys.path.insert(0, str(CURRENT.parent.parent))
from beijing_fushengji_rewrite.compile_all import get_ui_files


def test_get_ui():
    _fd, file = tempfile.mkstemp()
    with open(file, "w") as f:
        print(get_ui_files(), file=f)
    subprocess.run(f"code.cmd {file}".split(), check=True)
