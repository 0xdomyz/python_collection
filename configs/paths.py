import os
from pathlib import Path
from glob import glob
import sys


if __name__ == "__main__":
    f = __file__

    p = Path(f).parent

    Path(__file__).parents[2]

    ap = p.resolve().as_posix()
    ap

    for i in p.iterdir():
        print(i)

    for i in p.iterdir():
        if i.is_dir():
            print(i)

    (p / "files").resolve()

    (p / "files").exists()

    (p / "file").exists()

    with open(p / "config.yaml") as f:
        print(f)

    for i in p.glob("*.py"):
        print(i)

    for i in p.glob("*/*.py"):
        print(i)

    for i in p.glob("**/*.yaml"):
        print(i)

    p.home()

    (p.home() / ".dwopt").resolve()

    p.home().joinpath(".dwopt").resolve()

    [i for i in p.glob("*.yaml")]

    [i for i in p.glob("*ta.yaml")]

    q = p.joinpath("paths.py")
    aq = q.resolve().as_posix()
    aq

    q.stem

    q.suffix

    q.name

    q.with_name("read_env.py")

    os.path.abspath("")

    os.path.abspath("../configs/config.yaml")

    os.path.dirname(aq)

    with open(os.path.join(ap, "config.yaml")) as f:
        print(f)

    glob(ap + "/**/*.yaml")

    sys.path

    sys.path.insert(0, p)

    path = Path(__file__).parent / "config.yaml"
    print(path)
