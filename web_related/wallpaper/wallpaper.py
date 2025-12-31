"""Download wallpapers via a JSON endpoint with sane defaults and CLI options."""

import argparse
import datetime
import json
import re
import subprocess
from pathlib import Path
from typing import Iterable

import requests
import toml

BASE_PATH = Path(__file__).parent
PICTURES = BASE_PATH / "pictures"
CONFIG_PATH = BASE_PATH / "config.toml"
RUN_DATE = BASE_PATH / "run_date.txt"
TIMEOUT = 15


def load_endpoint() -> str:
    data = toml.load(CONFIG_PATH)
    return data["url"]["url"]


def ensure_dirs() -> None:
    PICTURES.mkdir(exist_ok=True)


def clean_name(url: str) -> str:
    name = url.split("/")[-1]
    return re.sub(r"%[0-9a-fA-F]{2}", " ", name)


def fetch_json(session: requests.Session, url: str) -> list[dict]:
    resp = session.get(url, timeout=TIMEOUT)
    resp.raise_for_status()
    data = resp.json()
    return data if isinstance(data, list) else []


def get_wallpaper(
    session: requests.Session, endpoint: str, date: datetime.date
) -> None:
    day = date.day
    month = date.month
    year = date.year
    url = f"{endpoint}?day={day}&month={month}&year={year}&tags=rating:safe"
    for item in fetch_json(session, url):
        wallpaper_url = item.get("file_url")
        if not wallpaper_url:
            continue
        name = clean_name(wallpaper_url)
        if "censored" in name:
            continue
        resp = session.get(wallpaper_url, timeout=TIMEOUT)
        resp.raise_for_status()
        with open(PICTURES / name, "wb") as f:
            f.write(resp.content)
        print(f"Downloaded {name}")


def open_folder() -> None:
    target = PICTURES.as_posix().replace("/", "\\")
    try:
        subprocess.check_call(["explorer.exe", target])
    except subprocess.CalledProcessError:
        print("Error opening folder")


def save_run_date(date: datetime.date) -> None:
    RUN_DATE.write_text(date.strftime("%Y-%m-%d"))


def get_run_date():
    if not RUN_DATE.exists():
        return None
    return datetime.datetime.strptime(RUN_DATE.read_text(), "%Y-%m-%d").date()


def date_range_weeks(base: datetime.date, weeks: int) -> Iterable[datetime.date]:
    for i in range(weeks + 1):
        yield base - datetime.timedelta(weeks=i)


def use_saved_date_actions(
    session: requests.Session, endpoint: str, date: datetime.date
) -> None:
    prior_date = get_run_date()
    if prior_date is None:
        get_wallpaper(session, endpoint, date)
        save_run_date(date)
        return
    weeks_between = max((date - prior_date).days // 7, 0)
    for dt in date_range_weeks(date, weeks_between):
        get_wallpaper(session, endpoint, dt)
    save_run_date(date)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", type=str, default=None, help="Date yyyy-mm-dd")
    parser.add_argument(
        "--weeks_prior", type=int, default=None, help="Download for N prior weeks"
    )
    parser.add_argument(
        "--use_saved_date",
        action="store_true",
        help="Use the saved run date to compute missing weeks",
    )
    args = parser.parse_args()

    ensure_dirs()
    endpoint = load_endpoint()
    session = requests.Session()
    session.headers.update({"user-agent": "wallpaper-downloader/0.1"})

    date = (
        datetime.date.today()
        if args.date is None
        else datetime.date.fromisoformat(args.date)
    )

    if args.use_saved_date and args.weeks_prior is not None:
        parser.error(
            "--use_saved_date and --weeks_prior cannot be set at the same time"
        )

    if args.use_saved_date:
        use_saved_date_actions(session, endpoint, date)
        open_folder()
        return

    if args.weeks_prior is not None:
        for dt in date_range_weeks(date, args.weeks_prior):
            get_wallpaper(session, endpoint, dt)
        open_folder()
        return

    get_wallpaper(session, endpoint, date)
    open_folder()


if __name__ == "__main__":
    main()
