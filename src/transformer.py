from typing import List, Dict
from dateutil import parser as date_parser

class Transformer:
    def normalize(self, records: List[Dict]) -> List[Dict]:
        """
        Clean, dedupe, and standardize a list of raw parser outputs.
        """
        seen_urls = set()
        out = []

        for rec in records:
            url = rec.get("url")
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)

            raw_ts = rec.get("published_at")
            iso_ts = None
            if raw_ts:
                try:
                    dt = date_parser.parse(raw_ts)
                    iso_ts = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
                except Exception:
                    iso_ts = None

            out.append({
                "source": rec.get("source"),
                "headline": rec.get("headline"),
                "url": url,
                "published_at": iso_ts,
            })

        return out
