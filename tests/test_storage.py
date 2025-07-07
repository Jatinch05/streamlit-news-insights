# tests/test_storage.py

import pandas as pd

def test_csv():
    df = pd.read_csv("data/headlines-2025-07-02.csv", parse_dates=["published_at"])
    print(df["source"].value_counts())
    print(df[df["source"] == "bbc"].sort_values("published_at", ascending=False).head())

if __name__ == "__main__":
    test_csv()
