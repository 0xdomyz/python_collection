# open browser with url
import webbrowser

url = "https://en.wikipedia.org/wiki/Main_Page"
webbrowser.open(url)
# open browser with url and new tab
import webbrowser

url = "https://en.wikipedia.org/wiki/Main_Page"
webbrowser.open_new_tab(url)
# open browser with url and new window
import webbrowser

url = "https://en.wikipedia.org/wiki/Main_Page"
webbrowser.open_new(url)
# open browser with url and new window and set browser
import webbrowser

url = "https://en.wikipedia.org/wiki/Main_Page"
webbrowser.get("firefox").open_new(url)

# write a program to open a browser and search for a keyword on google
import webbrowser

webbrowser.open("https://www.google.com/search?q=python")

# write a url as markdown text
url = "https://en.wikipedia.org/wiki/Main_Page"
print(f"[{url}]({url})")

# write a url as sphinx link
url = "https://en.wikipedia.org/wiki/Main_Page"
print(f"`{url} <{url}>`_")

# write a url as restructured text link
url = "https://en.wikipedia.org/wiki/Main_Page"
print(f"`{url} <{url}>`_")

# write a url as html link
url = "https://en.wikipedia.org/wiki/Main_Page"
print(f" {url} ")

# write a url as markdown link that works in jupyter notebook
url = "https://en.wikipedia.org/wiki/Main_Page"
print(f"[{url}]({url})")

# write a url as markdown link that works in streamlit
url = "https://en.wikipedia.org/wiki/Main_Page"
print(f"[{url}]({url})")
