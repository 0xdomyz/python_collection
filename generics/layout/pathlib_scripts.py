# create files if not exist in a directory
#############################################
from pathlib import Path

dir = Path() / "example"

for sub_dir in dir.iterdir():
    target = sub_dir / ".gitkeep"
    if not target.exists():
        target.touch()
