from argparse import ArgumentParser, RawTextHelpFormatter
from pathlib import Path
from typing import Iterable


# returns iterator of all files in root, recursively
def iter_dir_and_files(root: Path) -> Iterable[Path]:
    for path in root.iterdir():
        if path.is_dir():
            yield from iter_dir_and_files(path)
        else:
            yield path


def process_file(file: Path, payload: str, modify: bool):
    with file.open() as f:
        lines = f.readlines()

    if len(lines) == 0:
        print(f"writing to {file!s}, it was an empty file")
        lines.insert(
            0,
            payload,
        )
    elif modify and lines[0].startswith(payload[:20]):
        print(f"writing to {file!s}, only on first line")
        lines[0] = payload
    else:
        pass

    with file.open("w") as f:
        f.writelines(lines)


def add_compile_and_run_comment(location: Path, suffix: str, template: str):
    for file in iter_dir_and_files(location):
        if file.suffix == suffix:
            payload = template.format(file.stem)
            process_file(
                file=file,
                payload=payload,
                modify=True,
            )


def mass_touch(file_with_names: Path, suffix: str):
    with file_with_names.open() as f:
        names = f.readlines()

    for name in names:
        name = f"{name.strip()}{suffix}"
        target = file_with_names.parent / name
        if not target.exists():
            if not target.parent.exists():
                print(f"creating {target.parent!s}")
                target.parent.mkdir(parents=True)
            print(f"touching {target!s}")
            target.touch()


if __name__ == "__main__":
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        "--touch", action="store_true",
        help="mass touch files from spec file in spec file location"
    )
    parser.add_argument("location", type=Path, help="location of the files")
    parser.add_argument(
        "--lang", type=str, default="cpp", 
        help="language of the files, can be cpp, py or rs, default is cpp")

    parser.description = """
    Add compile and run comment to all files in location recursively.
    Also can touch files from spec file in spec file location, often used prior to
    adding compile and run comment.
    """

    # add example usages to parser to be shown with -h
    parser.epilog = """
    Example usages:
    
    # add compile and run comment
    python add_compile_and_run_comment.py /home/user/Projects/cpp_collection/the_cpp_book/intro/contain_algo
    python3 add_compile_and_run_comment.py /home/user/Projects/fluent_python/. --lang py

    # touch mode
    python add_compile_and_run_comment.py --touch test_acrc/test.txt
    python3 add_compile_and_run_comment.py --touch /home/user/Projects/fluent_python/config.txt --lang py
    """

    args = parser.parse_args()

    # decide on suffix and template based on language
    if args.lang == "cpp":
        template = "// g++ {0}.cpp -o {0} && ./{0}\n"
        suffix = ".cpp"
    elif args.lang == "py":
        template = "# python3 {0}.py\n"
        suffix = ".py"
    elif args.lang == "rs":
        template = "// rustc {0}.rs && ./{0}\n"
        suffix = ".rs"
    else:
        raise ValueError(f"unknown language {args.lang}")

    # actions
    if args.touch:
        mass_touch(
            file_with_names=args.location,
            suffix=suffix,
        )
    else:
        add_compile_and_run_comment(
            location=args.location,
            suffix=suffix,
            template=template,
        )
