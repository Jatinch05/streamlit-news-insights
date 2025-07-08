# 📰 News Insights Dashboard

A real-time, sentiment-aware dashboard that scrapes, analyzes, and visualizes news headlines from multiple major sources using asynchronous Python and Streamlit.

---

## 🚀 Features

- **Asynchronous news scraping** using `aiohttp` for fast parallel fetches
- **Multi-source support**: BBC, CNN, TechCrunch, The Guardian (and easily extendable)
- **Sentiment analysis** using `TextBlob`
- **Interactive dashboard** built with `Streamlit`
- **Visualizations**: time trends, sentiment breakdowns, word clouds, and more
- **Data export** in CSV format
- **Daily auto-scraping** via GitHub Actions
- **SQLite storage** for persistent historical data

---

## 📦 Tech Stack

- **Backend**: Python 3.10, `asyncio`, `aiohttp`, `feedparser`
- **Frontend**: Streamlit
- **NLP**: TextBlob (Sentiment), WordCloud
- **Storage**: SQLite, CSV
- **Automation**: GitHub Actions (daily scraping)

---

## 📊 Dashboard Preview

![Dashboard Screenshot]("C:\Users\jatin\OneDrive\Pictures\Screenshots\Screenshot 2025-07-08 184701.png")

---

## 🛠️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/streamlit-news-insights.git
   cd streamlit-news-insights
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the scraper**
   ```bash
   python src/main.py --config config.yaml --export sqlite
   ```

5. **Launch the dashboard**
   ```bash
   streamlit run src/dashboard.py
   ```

---

## ⚙️ GitHub Actions (Auto Scraper)

- Scheduled to run daily at **11 30 AM IST**
- Updates the `headlines.db` file and commits changes to GitHub

---

## 📁 Project Structure

```
├── src/
│   ├── main.py          # Orchestrates fetch, parse, transform, store
│   ├── fetcher.py       # AsyncFetcher class using aiohttp
│   ├── parser.py        # RSS parsers for each source
│   ├── transformer.py   # Cleans and normalizes raw data
│   ├── storage.py       # Stores to SQLite/CSV/Parquet
│   ├── dashboard.py     # Streamlit frontend
├── data/                # Database and CSV exports
├── config.yaml          # Site configs
├── requirements.txt
├── .github/workflows/   # GitHub Actions automation
└── README.md
```

---

## 📌 Future Work

- Add topic classification (e.g., Tech, Politics, Sports)
- Enhance scraping with full-text article parsing
- Upgrade to PostgreSQL for scalable storage


---

## 📄 License

MIT License – feel free to use, modify, and contribute.