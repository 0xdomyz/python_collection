# example of request library
from pprint import pprint

import requests

# wikipeaid home page
url = "https://en.wikipedia.org/wiki/Main_Page"
r = requests.get(url)
pprint(r)
pprint(r.url)
pprint(r.text)
# pprint(r.json())
pprint(r.status_code)
pprint(r.headers)
pprint(r.headers["content-type"])
pprint(r.headers["server"])
pprint(list(r.headers.keys()))

# fred data
key = ""
url = (
    f"https://api.stlouisfed.org/fred/series/observations?series_id=GNPCA&api_key={key}"
)
r = requests.get(url)
pprint(r)

# add header
url = "https://en.wikipedia.org/wiki/Main_Page"
headers = {"user-agent": "my-app/0.0.1"}
r = requests.get(url, headers=headers)
pprint(r)

# add query string
url = "https://en.wikipedia.org/wiki/Main_Page"
params = {"action": "query", "format": "json"}
r = requests.get(url, params=params)
pprint(r)

# session
s = requests.Session()
s.get("https://httpbin.org/cookies/set/sessioncookie/123456789")
r = s.get("https://httpbin.org/cookies")
pprint(r.text)

# post example
url = "https://httpbin.org/post"
payload = {"key1": "value1", "key2": "value2"}
r = requests.post(url, data=payload)
pprint(r.text)

# put example
url = "https://httpbin.org/put"
payload = {"key1": "value1", "key2": "value2"}
r = requests.put(url, data=payload)
pprint(r.text)

# delete example
url = "https://httpbin.org/delete"
payload = {"key1": "value1", "key2": "value2"}
r = requests.delete(url, data=payload)
pprint(r.text)

# head example
url = "https://httpbin.org/get"
r = requests.head(url)
pprint(r.text)

# options example
url = "https://httpbin.org/get"
r = requests.options(url)
pprint(r.text)
