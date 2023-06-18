from pathlib import Path

here = Path("D:/")

def move_startswith_into_a_folder(startswith:str, folder:str,here:Path):

    # start with sth
    res = [f for f in here.iterdir() if f.is_file() and f.name.startswith(startswith)]

    (here / folder).mkdir(exist_ok=True)

    # paste in
    for f in res:
        print(f.name)
        f.rename(here / folder / f.name)

def move_contains_into_a_folder(contains:str, folder:str,here:Path):

    # start with sth
    res = [f for f in here.iterdir() if f.is_file() and f.name.find(contains) != -1]

    (here / folder).mkdir(exist_ok=True)

    # paste in
    for f in res:
        print(f.name)
        f.rename(here / folder / f.name)

