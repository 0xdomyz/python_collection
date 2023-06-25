import datetime
from pathlib import Path

here = Path("D:/")

# get all files as a list of dict
files = []
for i in [i for i in here.iterdir() if i.is_file() and i.name.endswith(".mp3")]:
    
    file = {}
    file["name"] = i.name
    file["size"] = i.stat().st_size
    file["created"] = datetime.datetime.fromtimestamp(i.stat().st_ctime)
    file["modified"] = datetime.datetime.fromtimestamp(i.stat().st_mtime)

    files.append(file)
