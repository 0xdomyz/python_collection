# scrap wallpaper from
import argparse
import datetime
import json
import re
import subprocess
from pathlib import Path

import requests
import toml

path = Path(__file__).parent

# read in toml file
with open(path / "config.toml", "r") as f:
    endpoint = toml.load(f)["url"]["url"]

# get wallpaper
def get_wallpaper(date: datetime.date):
    day = date.day
    month = date.month
    year = date.year
    url = f"{endpoint}?day={day}&month={month}&year={year}&tags=rating:safe"
    response = requests.get(url)
    json_data = json.loads(response.text)

    for i in json_data:
        wallpaper_url = i["file_url"]
        wallpaper_name = wallpaper_url.split("/")[-1]
        # replace % and any 2 numbers with space via regexp
        wallpaper_name = re.sub(r"%[0-9a-fA-F]{2}", " ", wallpaper_name)

        # if has word censored or uncensored in it, skip
        if "censored" in wallpaper_name:
            continue

        wallpaper = requests.get(wallpaper_url)

        with open(path / "pictures" / wallpaper_name, "wb") as f:
            f.write(wallpaper.content)
        print(f"Downloaded {wallpaper_name}")


# open file explorer on pictures folder, on wsl
def open_folder():
    # make windows path \\ instead of /
    txt = (path / "pictures").as_posix().replace("/", "\\")

    try:
        subprocess.check_call(["explorer.exe", txt])
    except subprocess.CalledProcessError:
        print("Error opening folder")


if __name__ == "__main__":
    # use argparse to get day, month, year
    parser = argparse.ArgumentParser()
    parser.add_argument("--day", type=int, default=None)
    parser.add_argument("--month", type=int, default=None)
    parser.add_argument("--year", type=int, default=None)
    args = parser.parse_args()

    if args.day is None or args.month is None or args.year is None:
        date = datetime.date.today()
    else:
        date = datetime.date(args.year, args.month, args.day)

    get_wallpaper(date)
    open_folder()
