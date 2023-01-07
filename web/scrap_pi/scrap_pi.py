from pathlib import Path

# __file__ = "web/scrap_pi/scrap_pi.py"
here = Path(__file__).parent.absolute()

# via requests
###################
import os
import urllib.request

import requests
from bs4 import BeautifulSoup

url = "https://www.pinterest.com/search/pins/?q=food&rs=typed&term_meta[]=food%7Ctyped"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}


def scrap_pinterest(url):
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    # layout structure of the soup object, write to a file
    with open("soup.txt", "w") as f:
        f.write(soup.prettify())

    images = soup.find_all("jpg")
    for image in images:
        image_url = image["src"]
        # get image
        urllib.request.urlretrieve(image_url, os.path.basename(image_url))


scrap_pinterest(url)


# use selenium
###################################
import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver

url = "https://www.pinterest.com.au/search/pins/?q=jetfighter&rs=typed"

driver = webdriver.Firefox()

driver.get(url)

# scroll down to load more images
for i in range(10):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# get the page source
page_source = driver.page_source

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


async def fetch(url, session):
    async with session.get(url) as response:
        return await response.read()


async def run(urls):
    tasks = []
    async with ClientSession() as session:
        for url in urls:
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
        return responses


# limit how many aync requests are made at once

loop = asyncio.get_event_loop()
future = asyncio.ensure_future(run(image_urls))
responses = loop.run_until_complete(future)

# save images to a folder
for i, response in enumerate(responses):
    with open(here / "images" / f"image_{i}.jpg", "wb") as f:
        f.write(response)

# write to a file
with open("page_source.txt", "w") as f:
    f.write(page_source)
