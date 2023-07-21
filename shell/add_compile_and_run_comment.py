from argparse import ArgumentParser
from pathlib import Path


def add_compile_and_run_comment(location: str):

    for file in Path(location).iterdir():
        if file.suffix == ".cpp":
            with file.open() as f:
                lines = f.readlines()

            payload = (
                f"// Compile and run: g++ {file.stem}.cpp "
                f"-o {file.stem} && ./{file.stem}\n"
            )

            if len(lines) == 0:
                lines.insert(
                    0,
                    payload,
                )
            elif lines[0].startswith("// Compile and run"):
                lines[0] = payload
            else:
                continue

            with file.open("w") as f:
                print(f"writing to {file!s}")
                f.writelines(lines)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("location", type=str, help="location of the files")

    # add example usages to parser to be shown with -h
    parser.epilog = """
    example usages:
    python3.9 add_compile_and_run_comment.py /home/user/Projects/cpp_collection/the_cpp_book/intro/contain_algo
    """

    args = parser.parse_args()
    add_compile_and_run_comment(args.location)