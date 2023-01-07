import os
import urllib.request
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# __file__ = "web/scrap_pi.py"
here = Path(__file__).parent.absolute()


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

# use selenium to get the page source
from selenium import webdriver

url = "https://www.pinterest.com.au/search/pins/?q=jetfighter&rs=typed"

driver = webdriver.Firefox()

driver.get(url)

# get the page source
page_source = driver.page_source

# write to a file
with open("page_source.txt", "w") as f:
    f.write(page_source)
