import os
import pandas as pd
from datetime import datetime

class Storage:
    def __init__(self, db_path):
        self.db_path = db_path

    def save(self, records, export_format, filename=None):
        df = pd.DataFrame(records)
        if df.empty:
            print("No records to save.")
            return

        os.makedirs("data", exist_ok=True)

        if export_format == "csv":
            if not filename:
                date = datetime.utcnow().strftime("%Y-%m-%d")
                filename = f"data/headlines-{date}.csv"
            df.to_csv(filename, index=False)
            print(f"Wrote {len(df)} records to {filename}")

        elif export_format == "parquet":
            filename = filename or self.db_path.replace(".db", ".parquet")
            df.to_parquet(filename, index=False)
            print(f"Wrote {len(df)} records to {filename}")

        elif export_format == "sqlite":
            import sqlite3
            conn = sqlite3.connect(self.db_path)
            df.to_sql("headlines", conn, if_exists="replace", index=False)
            conn.close()
            print(f"Wrote {len(df)} records to {self.db_path}")
