from pathlib import Path

CURRENT = Path(__file__).resolve().parent
import sys

sys.path.insert(0, str(CURRENT))


def test():
    import co2

    print(111222)
    print(co2.test2())
