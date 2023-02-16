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


def save_run_date(date: datetime.date):
    with open(path / "run_date.txt", "w") as f:
        f.write(date.strftime("%Y-%m-%d"))


def get_run_date():
    file = path / "run_date.txt"
    if not file.exists():
        return None
    else:
        with open(file, "r") as f:
            date = f.read()
        return datetime.datetime.strptime(date, "%Y-%m-%d").date()


def save_date_actions(date: datetime.date):
    prior_date = get_run_date()

    if prior_date is None:
        get_wallpaper(date)
        save_run_date(date)
    else:
        # get wallpapers for all weeks between saved date and current date
        dates = [
            date - datetime.timedelta(weeks=i)
            for i in range((date - prior_date).days // 7 + 1)
        ]
        for date in dates:
            get_wallpaper(date)
        save_run_date(date)


if __name__ == "__main__":
    # use argparse to get day, month, year
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--date", type=str, default=None, help="Date (yyyy-mm-dd) to get wallpaper from"
    )
    # optional argument to extend date range
    parser.add_argument(
        "--weeks_prior", type=int, default=None, help="Number of weeks to extend range"
    )
    # optional argument to save date to file and use saved date to get weeks prior
    parser.add_argument(
        "--save_date",
        action="store_true",
        help="Save date to file to auto use weeks prior, weeks prior must not be set",
    )

    # make sure weeks prior is not set if save date is set
    args = parser.parse_args()
    if args.save_date and args.weeks_prior is not None:
        parser.error("--save_date and --weeks_prior cannot be set at the same time")

    # if date is not set, use today's date
    if args.date is None:
        date = datetime.date.today()
    else:
        year, month, day = args.date.split("-")
        date = datetime.date(int(year), int(month), int(day))

    # vanilla run, get wallpaper for date
    if args.weeks_prior is None and not args.save_date:
        get_wallpaper(date)
        open_folder()
        exit()

    # if weeks prior is set, get wallpapers for that many weeks prior
    if args.weeks_prior is not None:
        # list of dates
        dates = [
            date - datetime.timedelta(weeks=i) for i in range(args.weeks_prior + 1)
        ]
        for date in dates:
            get_wallpaper(date)
        open_folder()
        exit()

    # if save date is set, do save date actions
    if args.save_date:
        save_date_actions(date)
        open_folder()
        exit()
