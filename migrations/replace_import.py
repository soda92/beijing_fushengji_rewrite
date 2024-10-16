from pathlib import Path

CURRENT = Path(__file__).resolve().parent
widgets_dir = CURRENT.parent.joinpath("widgets")


def get_replacement(lines):
    if "\r\n" in lines:
        lines = lines.split("\r\n")
    else:
        lines = lines.split("\n")

    import re

    def is_import(line):
        return re.match(" *import (.*)", line) is not None

    def get_import(line):
        return re.findall("import (.*)", line)[0]

    def is_call(module, line):
        return "=" in line and module in line

    target = []

    def write_block(module, line):
        nonlocal target
        t = line.replace(module, f'load("{module}")')
        target.append(t)

    i = 0
    while i < len(lines):
        v = lines[i]
        v = v.replace('\n', '')
        if is_import(v):
            f = get_import(v)
            if is_call(f, lines[i + 1]):
                write_block(f, lines[i + 1])
                i += 2
                continue
            elif is_call(f, lines[i + 2]):
                write_block(f, lines[i + 2])
                i += 3
                continue
            elif is_call(f, lines[i + 3]):
                write_block(f, lines[i + 3])
                i += 4
                continue
        target.append(v)
        i += 1
    return target


def read_file():
    sources = widgets_dir.glob("*.py")

    for file in sources:
        lines = file.read_text(encoding='utf-8')
        replaced = '\n'.join(get_replacement(lines))
        file.write_text(replaced, encoding='utf-8')


def test1():
    test_str = """
        import ui.bank

        importlib.reload(ui.bank)
        self.ui = ui.bank.Ui_Bank()
        """

    target = """
        self.ui = load("ui.bank").Ui_Bank()
        """

    print(get_replacement(test_str))
    print("\n".join(get_replacement(test_str)))
    print(target)
    print("\n".join(get_replacement(test_str)) == target)

    test_str2 = """
        import ui.bank

        self.ui = ui.bank.Ui_Bank()
        """

    target2 = """
        self.ui = load("ui.bank").Ui_Bank()
        """
    print(get_replacement(test_str2))
    print("\n".join(get_replacement(test_str2)))
    print(target2)
    print("\n".join(get_replacement(test_str2)) == target2)


if __name__ == "__main__":
    test1()
    read_file()
