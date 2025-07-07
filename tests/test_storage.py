import sqlite3
import pandas as pd

conn = sqlite3.connect("data/headlines.db")
df = pd.read_sql("SELECT source, COUNT(*) as count FROM headlines GROUP BY source", conn)
print(df)
conn.close()
