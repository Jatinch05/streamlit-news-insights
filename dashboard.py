import streamlit as st
import pandas as pd
import subprocess
import os
import sys
import glob
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import StringIO
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Set layout
st.set_page_config(page_title="News Dashboard", layout="wide")

# Auto-refresh every 10 minutes
st_autorefresh(interval=10 * 60 * 1000, key="refresh")

st.title("News Headlines Dashboard")

# --- UTILS ---

def fetch_latest_news():
    try:
        subprocess.run([
            sys.executable, "src/main.py", "--config", "config.yaml", "--export", "sqlite"
        ], check=True)

        st.success("Fetched latest news! Please reload the dashboard.")
    except subprocess.CalledProcessError as e:
        st.error(f"Fetch failed: {e}")

@st.cache_data(ttl=60)
def load_data(path):
    if os.path.exists(path) and os.path.getsize(path) == 0:
        os.remove(path)
        st.warning("Removed empty data file. Please re-run the scraper.")
        st.stop()
    try:
        df = pd.read_csv(path, parse_dates=["published_at"])
        if df.empty:
            st.warning("CSV exists but contains no records.")
            st.stop()
        return df
    except pd.errors.EmptyDataError:
        st.warning("The data file is empty or malformed.")
        st.stop()

# --- Sentiment Interpretation ---
def interpret_sentiment(score):
    if score <= -0.5:
        return "Very Negative"
    elif score < -0.1:
        return "Negative"
    elif score <= 0.1:
        return "Neutral"
    elif score < 0.5:
        return "Positive"
    else:
        return "Very Positive"

# --- Manual Refresh ---
if st.button("Fetch Latest News"):
    fetch_latest_news()
    st.cache_data.clear()
    st.rerun()

# --- Load Data ---
import sqlite3

def load_data_sqlite(db_path):
    if not os.path.exists(db_path):
        st.warning("Database not found. Please fetch the latest news first.")
        st.stop()
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql("SELECT * FROM headlines", conn, parse_dates=["published_at"])
        conn.close()
        return df
    except Exception as e:
        st.error(f"Failed to load database: {e}")
        st.stop()

data_path = os.path.join("data", "headlines.db")
df = load_data_sqlite(data_path)

df["published_at"] = pd.to_datetime(df["published_at"], errors="coerce")
df = df.dropna(subset=["published_at"])
st.caption(f"Loaded: `{data_path}`")

# --- Filters ---
st.sidebar.header("Filters")

min_date = df["published_at"].dt.date.min()
max_date = df["published_at"].dt.date.max()
st.caption(f"Data available from **{min_date}** to **{max_date}**")

sources = st.sidebar.multiselect(
    "Filter by source", options=df["source"].unique(), default=df["source"].unique()
)

date_range = st.sidebar.date_input(
    "Date range",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

query = st.sidebar.text_input("Search in headlines", "")

# --- Apply Filters ---
mask = (
    df["source"].isin(sources) &
    df["published_at"].dt.date.between(*date_range)
)
filtered = df.loc[mask]

if query:
    filtered = filtered[filtered["headline"].str.contains(query, case=False, na=False)]

if filtered.empty:
    st.warning("No articles match the current filters.")
    st.stop()

# --- Enrich with sentiment and hour ---
filtered["sentiment"] = filtered["headline"].apply(lambda h: TextBlob(h).sentiment.polarity)
filtered["hour"] = filtered["published_at"].dt.hour
filtered["headline_link"] = filtered.apply(
    lambda row: f"[{row['headline']}]({row['url']})", axis=1
)

# --- Summary Stats ---
st.subheader("Summary")
col1, col2, col3 = st.columns(3)

avg_sentiment = filtered["sentiment"].mean()
sentiment_label = interpret_sentiment(avg_sentiment)

col1.metric("Total Articles", len(filtered))
col2.metric("Avg Sentiment", f"{avg_sentiment:.2f}", sentiment_label)
col3.metric("Sources", ", ".join(filtered["source"].unique()))

# --- Export filtered results ---
csv_buffer = StringIO()
filtered.to_csv(csv_buffer, index=False)
st.download_button(
    label="Download Filtered Headlines",
    data=csv_buffer.getvalue(),
    file_name=f"filtered_{datetime.utcnow().strftime('%Y%m%d_%H%M')}.csv",
    mime="text/csv"
)

# --- Visualizations ---
st.subheader("Articles Over Time")
ts = filtered.groupby(filtered["published_at"].dt.date).size()
st.line_chart(ts)

st.subheader("Articles by Hour of Day")
hourly = filtered.groupby("hour").size()
st.bar_chart(hourly)

st.subheader("Sentiment by Source")
sent_chart = filtered.groupby("source")["sentiment"].mean()
st.bar_chart(sent_chart)

st.subheader("Articles per Source")
st.dataframe(
    filtered["source"]
    .value_counts()
    .reset_index()
    .rename(columns={"index": "source", "source": "Count"})
)

# --- Word Cloud ---
st.subheader("Most Common Words")
from collections import Counter
import re
text = " ".join(filtered["headline"].dropna().tolist())
wordcloud = WordCloud(width=800, height=300, background_color='black').generate(text)
fig, ax = plt.subplots(figsize=(10, 4))
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")
st.pyplot(fig)

# --- Headline Table ---
st.subheader("Latest Headlines")
st.dataframe(
    filtered.sort_values("published_at", ascending=False)[
        ["published_at", "source", "headline_link"]
    ].rename(columns={"headline_link": "headline"}),
    use_container_width=True,
    height=500
)
