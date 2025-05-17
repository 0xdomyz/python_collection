from pathlib import Path

# __file__ = "web/scrap_pi/scrap_pi.py"
here = Path(__file__).parent.absolute()

# use selenium
###################################
import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver

word = "jetfighter"

url = f"https://www.pinterest.com.au/search/pins/?q={word}&rs=typed"

driver = webdriver.Firefox()

driver.get(url)

# scroll down to load more images
for i in range(10):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# get the page source
page_source = driver.page_source
# with open("page_source.txt", "w") as f:
#     f.write(page_source)

# get image tags
soup = BeautifulSoup(page_source, "lxml")
images = soup.find_all("img")
print(len(images))

# repack the src, alt attributes into a list of dictionaries
images = [
    {"src": image["src"], "alt": image["alt"]}
    for image in images
    if "src" in image.attrs and "alt" in image.attrs
]

# for each src attribute, parse the url and make a new field for the last part of the url before .jpg
for image in images:
    image_url = image["src"]
    image["filename"] = os.path.basename(image_url)


# get iamges in parallel via aiohttp
import asyncio

from aiohttp import ClientSession


async def fetch(image, session):
    url = image["src"]
    async with session.get(url) as response:
        image["content"] = await response.read()


async def run(images):
    tasks = []
    async with ClientSession() as session:
        for image in images:
            task = asyncio.ensure_future(fetch(image, session))
            tasks.append(task)
        await asyncio.gather(*tasks)


# limit how many aync requests are made at once

loop = asyncio.get_event_loop()
future = asyncio.ensure_future(run(images))
loop.run_until_complete(future)

# save images to a folder
for image in images:
    with open(here / "images" / image["filename"], "wb") as f:
        f.write(image["content"])
