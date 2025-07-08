import asyncio
import aiohttp
from typing import List, Dict, Any

class AsyncFetcher:
    def __init__(self, sites: List[Dict[str, Any]], since: str = None):
        self.sites = sites
        self.since = since
        self.semaphore = asyncio.Semaphore(10)
        self.session = None

    async def _fetch_site(self, site: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Fetch the HTML for a single site respecting the rate limit and concurrency.
        Returns a list of raw items with site name and HTML content.
        """
        async with self.semaphore:
            async with self.session.get(site['url'], timeout=10) as resp:
                resp.raise_for_status()
                data = await resp.text()
                return [{'site': site['name'], 'data': data}]

    async def fetch_all(self) -> List[Dict[str, Any]]:
        """
        Dispatch concurrent fetches for all configured sites and handle exceptions.
        """
        async with aiohttp.ClientSession() as session:
            self.session = session
            tasks = [self._fetch_site(site) for site in self.sites]
            results = await asyncio.gather(*tasks, return_exceptions=True)

        items = []
        for result in results:
            if isinstance(result, Exception):
                print(f"Fetch error: {result}")
            else:
                items.extend(result)
        return items