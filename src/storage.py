# src/storage.py

import os
import asyncio
import aiosqlite
import pandas as pd
from datetime import datetime
from typing import List, Dict

class Storage:
    def __init__(self, db_path: str):
        self.db_path = db_path
        # Ensure the data directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

    def save(self, records: List[Dict], export: str):
        """
        Persist records to the specified storage format.
        export: one of "sqlite", "csv", or "parquet"
        """
        if export == "sqlite":
            # Run the async upsert in the event loop
            asyncio.run(self._save_sqlite(records))
        else:
            # CSV or Parquet via Pandas
            self._save_file(records, export)

    async def _save_sqlite(self, records: List[Dict]):
        # Connect (creates file if not exists)
        async with aiosqlite.connect(self.db_path) as db:
            # Create table if missing
            await db.execute("""
                CREATE TABLE IF NOT EXISTS headlines (
                    source       TEXT,
                    headline     TEXT,
                    url          TEXT PRIMARY KEY,
                    published_at TEXT
                )
            """)
            # Upsert each record
            for rec in records:
                await db.execute("""
                    INSERT INTO headlines(source, headline, url, published_at)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(url) DO UPDATE SET
                      source = excluded.source,
                      headline = excluded.headline,
                      published_at = excluded.published_at
                """, (
                    rec["source"],
                    rec["headline"],
                    rec["url"],
                    rec["published_at"]
                ))
            await db.commit()

    def _save_file(self, records: List[Dict], export: str):
        # Build DataFrame
        df = pd.DataFrame(records)
        # Make sure data/ exists
        out_dir = os.path.dirname(self.db_path)
        os.makedirs(out_dir, exist_ok=True)

        # Filename with date
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
        if export == "csv":
            path = os.path.join(out_dir, f"headlines-{date_str}.csv")
            df.to_csv(path, index=False)
        else:  # parquet
            path = os.path.join(out_dir, f"headlines-{date_str}.parquet")
            df.to_parquet(path, index=False)

        print(f"Wrote {len(df)} records to {path}")
