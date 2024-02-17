# example of using pathlib

from pathlib import Path

# Path.cwd() is the current working directory
print(Path.cwd())

# Path.home() is the home directory
print(Path.home())

# Path.home() / "Desktop" is the desktop directory
print(Path.home() / "Desktop")

# Path.home() / "Desktop" / "test.txt" is the test.txt file
print(Path.home() / "Desktop" / "test.txt")

# Path.home() / "Desktop" / "test.txt" is the test.txt file

# iterating through a directory
for file in Path.home().iterdir():
    print(file)

# modify path
p = Path.home() / "Desktop" / "test.txt"
print(p)
p = p.with_suffix(".csv")
print(p)

# opearte on file
p = Path.home() / "Desktop" / "test.txt"
print(p.exists())
print(p.is_file())
print(p.is_dir())

# create a file
p = Path.home() / "Desktop" / "test.txt"
p.touch()

# create a directory
p = Path.home() / "Desktop" / "test"
p.mkdir()

# delete a file
p = Path.home() / "Desktop" / "test.txt"
p.unlink()

# delete a directory
p = Path.home() / "Desktop" / "test"
p.rmdir()

# read a file
p = Path.home() / "Desktop" / "test.txt"
print(p.read_text())

# write a file
p = Path.home() / "Desktop" / "test.txt"
p.write_text("hello world")

# append to a file
p = Path.home() / "Desktop" / "test.txt"
p.write_text("hello world", append=True)

# path of a library
import pandas as pd

print(pd.__file__)
