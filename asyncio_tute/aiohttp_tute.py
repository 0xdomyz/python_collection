import asyncio

import aiohttp
from aiohttp import ClientSession


async def fetch_html(url: str, session: ClientSession, **kwargs) -> str:
    """GET request wrapper to fetch page HTML.

    kwargs are passed to `session.request()`.
    """

    print("fetching: ", url)
    resp = await session.request(method="GET", url=url, **kwargs)
    resp.raise_for_status()
    html = await resp.text()
    print("fetched: ", url)
    return html


async def fetch(res, url: str, session: ClientSession, **kwargs) -> str:
    """GET request wrapper to fetch page HTML.

    kwargs are passed to `session.request()`.
    """

    try:
        html = await fetch_html(url=url, session=session, **kwargs)
    except (
        aiohttp.ClientError,
        aiohttp.http_exceptions.HttpProcessingError,
    ) as e:
        print(e)
    except Exception as e:
        print(e)

    res.append(html)


async def main():
    urls = ["https://www.google.com", "https://www.yahoo.com"]

    res = []

    async with ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(fetch(res, url, session))
        await asyncio.gather(*tasks)

    return res


if __name__ == "__main__":
    res = asyncio.run(main())
    res[0][:500]
    res[1][:500]
