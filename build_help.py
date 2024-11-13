from pathlib import Path

files = ["help.html", "help_en.html"]

for file in files:
    r = Path(file).read_text(encoding="utf8")
    dest_file = Path("beijing_fushengji").joinpath(
        Path(file).name.replace(".", "_") + ".py"
    )
    r = 'help = r"""\n' + r + 'r"""'
    dest_file.write_text(r, encoding="utf8")
