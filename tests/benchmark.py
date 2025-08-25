

import time
import asyncio
import aiohttp
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
BASE_URLS = [
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://techcrunch.com/feed/",
    "http://rss.cnn.com/rss/cnn_topstories.rss",
    "https://www.theguardian.com/world/rss",
]


URLS = BASE_URLS * 5


def sync_fetch_all(urls):
    start = time.perf_counter()
    for url in urls:
        r = requests.get(url, timeout=10, headers=headers)
        r.raise_for_status()
    elapsed = time.perf_counter() - start
    return elapsed


async def async_fetch_all(urls, concurrency=10):
    sem = asyncio.Semaphore(concurrency)
    async with aiohttp.ClientSession() as session:
        async def fetch(url):
            async with sem:
                async with session.get(url, timeout=10, headers=headers) as resp:
                    resp.raise_for_status()
                    await resp.read()

        start = time.perf_counter()
        await asyncio.gather(*(fetch(u) for u in urls))
        elapsed = time.perf_counter() - start
    return elapsed

if __name__ == "__main__":
    print(f"Running {len(URLS)} requests total (4 base URLs × 5)…\n")

    sync_time = sync_fetch_all(URLS)
    print(f"Synchronous total time:   {sync_time:.2f}s")

    async_time = asyncio.run(async_fetch_all(URLS, concurrency=10))
    print(f"Asynchronous total time:  {async_time:.2f}s")

    reduction = (sync_time - async_time) / sync_time * 100
    print(f"Speed‑up: ~{reduction:.0f}% faster\n")
