from pathlib import Path

here = Path("D:/")


def move_startswith_into_a_folder(startswith: str, folder: str, here: Path):
    # start with sth
    res = [f for f in here.iterdir() if f.is_file() and f.name.startswith(startswith)]

    (here / folder).mkdir(exist_ok=True)

    # paste in
    for f in res:
        print(f.name)
        f.rename(here / folder / f.name)


def move_contains_into_a_folder(contains: str, folder: str, here: Path):
    # start with sth
    res = [f for f in here.iterdir() if f.is_file() and f.name.find(contains) != -1]

    (here / folder).mkdir(exist_ok=True)

    # paste in
    for f in res:
        print(f.name)
        f.rename(here / folder / f.name)


# reverse by moving files out of folders
def move_files_out_of_folders(here: Path):
    for i in [i for i in here.iterdir() if i.is_dir()]:
        # i is a folder in here
        for j in [j for j in i.iterdir()]:
            # j is a file or folder in i
            if j.is_dir():
                raise Exception("There is a folder in a folder")
            else:
                print(j)
                j.rename(here / j.name)
        i.rmdir()
