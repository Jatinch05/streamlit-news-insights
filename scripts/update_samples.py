#!/usr/bin/env python
import os
import yaml
import asyncio

from src.fetcher import AsyncFetcher

def main():
    cfg = yaml.safe_load(open("config.yaml"))
    fetcher = AsyncFetcher(cfg["sites"], since=None)
    raw_items = asyncio.run(fetcher.fetch_all())

    os.makedirs("samples", exist_ok=True)
    for item in raw_items:
        name = item["site"]
        ext  = "xml" if name.endswith("_rss") else "html"
        path = os.path.join("samples", f"{name}.{ext}")
        with open(path, "w", encoding="utf-8") as f:
            f.write(item["html"])
        print(f"Saved sample: {path}")

if __name__ == "__main__":
    main()
