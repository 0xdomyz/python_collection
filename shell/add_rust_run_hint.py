from pathlib import Path

root = Path("/home/user/Projects/rust_collection/example/")


def iter_dir_and_files(root):
    for path in root.iterdir():
        if path.is_dir():
            yield from iter_dir_and_files(path)
        else:
            yield path


def main():
    for path in iter_dir_and_files(root):
        if path.suffix == ".rs":
            with path.open("r") as f:
                contents = f.read()
            if len(contents) == 0:
                print(path)
                # print(path.name)
                with path.open("w") as f:
                    f.write(f"// rustc {path.name} && ./{path.stem}\n")


if __name__ == "__main__":
    main()
