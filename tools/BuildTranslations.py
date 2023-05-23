#!/usr/env python
import subprocess
import pathlib
import shutil
import sys
import os


def get_lrelease_command() -> str | None:
    for i in ("lrelease", "lrelease6", "pyside6-lrelease", "pyside5-lrelease"):
        if shutil.which(i) is not None:
            return i
    return None


def main() -> None:
    command = get_lrelease_command()

    if command is None:
        print("lrelease was not found", file=sys.stderr)
        sys.exit(1)

    translation_dir = pathlib.Path(__file__).parent.parent / "jdNBTExplorer" / "translations"
    for i in translation_dir.iterdir():
        if i.suffix == ".ts":
            subprocess.run([command, str(i), "-qm", os.path.join(translation_dir, i.stem + ".qm")])


if __name__ == "__main__":
    main()
