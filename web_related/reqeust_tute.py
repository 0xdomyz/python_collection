"""Requests examples with safe defaults (timeouts, headers, sessions)."""

from pprint import pprint

import requests

TIMEOUT = 10
HEADERS = {"user-agent": "python-requests-example/0.1"}


def get_text(url: str, params=None):
    resp = requests.get(url, headers=HEADERS, params=params, timeout=TIMEOUT)
    resp.raise_for_status()
    print(f"GET {resp.url} -> {resp.status_code}")
    return resp.text[:300]


def get_json(url: str, params=None):
    resp = requests.get(url, headers=HEADERS, params=params, timeout=TIMEOUT)
    resp.raise_for_status()
    print(f"GET {resp.url} -> {resp.status_code}")
    return resp.json()


def post_form(url: str, data: dict):
    resp = requests.post(url, headers=HEADERS, data=data, timeout=TIMEOUT)
    resp.raise_for_status()
    print(f"POST {resp.url} -> {resp.status_code}")
    return resp.json()


def session_with_cookies():
    with requests.Session() as s:
        s.headers.update(HEADERS)
        s.get(
            "https://httpbin.org/cookies/set/sessioncookie/123456789", timeout=TIMEOUT
        )
        resp = s.get("https://httpbin.org/cookies", timeout=TIMEOUT)
        resp.raise_for_status()
        print("Session cookies:", resp.json())


def main():
    pprint(get_text("https://en.wikipedia.org/wiki/Main_Page"))

    pprint(
        get_json(
            "https://httpbin.org/get",
            params={"action": "query", "format": "json"},
        )
    )

    pprint(post_form("https://httpbin.org/post", data={"key1": "value1"}))

    session_with_cookies()

    fred_url = "https://api.stlouisfed.org/fred/series/observations"
    fred_params = {"series_id": "GNPCA", "api_key": "demo", "file_type": "json"}
    try:
        fred = get_json(fred_url, params=fred_params)
        print("FRED example keys:", list(fred.keys())[:5])
    except requests.HTTPError as exc:
        print("FRED request failed (supply a real API key)", exc)


if __name__ == "__main__":
    main()
