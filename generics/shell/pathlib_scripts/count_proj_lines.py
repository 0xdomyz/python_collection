# python3.11 count_proj_lines.py . "*.py"
# python3.11 count_proj_lines.py . "*"
# python3.11 count_proj_lines.py /home/user/Projects/example/src "*.py"
# python3.11 count_proj_lines.py /home/user/Projects/effective_cpp "*.cpp"

from pathlib import Path
from iter_tree_for_files import iter_tree_for_files
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "path", help="Path to the directory to count lines in", type=Path
    )
    parser.add_argument("pattern", help="Pattern to match", type=str)
    args = parser.parse_args()

    path = args.path
    pattern = args.pattern

    print(f"Counting lines in {path}")
    total = 0

    for p in iter_tree_for_files(path):
        if p.match(pattern):
            try:
                with p.open() as f:
                    l = len(f.readlines())
                    print(f"lines: {l:5}, path: {p}")
                    total += l
            except UnicodeDecodeError:
                print(f"UnicodeDecodeError: {p}")
    print(f"Total lines: {total}")
