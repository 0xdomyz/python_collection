"""Small helpers to open URLs in a browser and render link snippets."""

import argparse
import webbrowser
from typing import Optional

DEFAULT_URL = "https://en.wikipedia.org/wiki/Main_Page"


def open_default(url: str = DEFAULT_URL) -> None:
    webbrowser.open(url)


def open_tab(url: str = DEFAULT_URL) -> None:
    webbrowser.open_new_tab(url)


def open_window(url: str = DEFAULT_URL) -> None:
    webbrowser.open_new(url)


def open_with_browser(browser: str, url: str = DEFAULT_URL) -> None:
    # Example: "firefox", "chrome", "safari" depending on OS
    webbrowser.get(browser).open_new(url)


def make_links(url: str = DEFAULT_URL) -> dict[str, str]:
    """Return common link formats for docs/notebooks."""
    return {
        "markdown": f"[{url}]({url})",
        "sphinx": f"`{url} <{url}>`_",
        "rst": f"`{url} <{url}>`_",
        "html": f'<a href="{url}">{url}</a>',
    }


def search_google(keyword: str) -> str:
    return f"https://www.google.com/search?q={keyword}"


def main(action: str, url: Optional[str], browser: Optional[str], keyword: str) -> None:
    target = url or DEFAULT_URL
    if action == "open":
        open_default(target)
    elif action == "tab":
        open_tab(target)
    elif action == "window":
        open_window(target)
    elif action == "browser" and browser:
        open_with_browser(browser, target)

    if keyword:
        webbrowser.open(search_google(keyword))

    links = make_links(target)
    for name, text in links.items():
        print(f"{name}: {text}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--action", choices=["open", "tab", "window", "browser"], default="open"
    )
    parser.add_argument("--url", help="URL to open")
    parser.add_argument("--browser", help="Browser name for webbrowser.get()")
    parser.add_argument(
        "--keyword", default="", help="Optional Google keyword to search"
    )
    args = parser.parse_args()

    main(action=args.action, url=args.url, browser=args.browser, keyword=args.keyword)
