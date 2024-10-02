import time
from pathlib import Path

CURRENT = Path(__file__).resolve().parent
import sys

sys.path.insert(0, str(CURRENT))
import importlib
import component

for _i in range(100):
    importlib.reload(component)
    component.test()
    time.sleep(3)
