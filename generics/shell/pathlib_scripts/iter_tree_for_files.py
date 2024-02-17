from pathlib import Path
from typing import Iterable


def iter_tree_for_files(path: Path) -> Iterable[Path]:
    """
    Examples
    ---------
    ::

        for p in iter_tree_for_files(here / "tree_test"):
            print(p)
    """
    for p in path.iterdir():
        if p.is_dir():
            yield from iter_tree_for_files(p)
        else:
            yield p


if __name__ == "__main__":
    here = Path(__file__).parent

    # make test tree
    (here / "tree_test").mkdir(parents=True, exist_ok=True)
    (here / "tree_test" / "a").mkdir(parents=True, exist_ok=True)
    (here / "tree_test" / "b.file").touch()
    (here / "tree_test" / "a" / "c.file").touch()
    (here / "tree_test" / "a" / "d").mkdir(parents=True, exist_ok=True)
    (here / "tree_test" / "a" / "d" / "e.file").touch()

    # test
    for p in iter_tree_for_files(here / "tree_test"):
        print(p)
