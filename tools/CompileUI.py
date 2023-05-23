#!/usr/bin/env python
import subprocess
import pathlib
import shutil
import sys


def main():
    if shutil.which("pyuic6") is None:
        print("pyuic6 was not found", file=sys.stderr)
        sys.exit(1)

    program_dir = pathlib.Path(__file__).parent.parent / "jdNbtExplorer"
    compiled_dir = program_dir / "ui_compiled"
    source_dir = program_dir / "ui"

    try:
        shutil.rmtree(compiled_dir)
    except FileNotFoundError:
        pass

    compiled_dir.mkdir()
    (compiled_dir / "__init__.py").touch()

    for i in source_dir.iterdir():
        if i.suffix != ".ui":
            continue

        subprocess.run(["pyuic6", str(i), "-o", str(compiled_dir / f"{i.stem}.py")], check=True)


if __name__ == "__main__":
    main()
