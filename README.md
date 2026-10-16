# 🚀 Enterprise Web Harvester & Data Pipeline

A resilient, production-ready Python web scraping and data pipeline engine. Designed with defensive crawling strategies, exponential backoff retries, rate-limiting compliance, and multi-format data exports (CSV & JSON).

---

## 🌟 Key Features

- **Defensive HTTP Client**: Automatic retry logic with exponential backoff on `429 (Too Many Requests)` and `503 (Service Unavailable)`.
- **Anti-Bot & Rate-Limit Friendly**: Built-in request delays, random jitter, and user-agent rotation.
- **Defensive Parsing**: Resilient CSS/regex selectors handling missing fields and bad HTML gracefully.
- **Multi-Format Export**: Generates both clean **JSON** and **Excel-optimized CSV** (`utf-8-sig`).
- **Data Analytics Summary**: Instant console metric breakdown (total records, availability %, price averages, rating distribution).

---

## 🛠️ Architecture

```
01_python_automation/
├── harvester/
│   ├── __init__.py
│   ├── core.py       # Robust HTTP client, backoff logic & session handling
│   ├── parsers.py    # Abstract parser interface + concrete e-commerce extractor
│   └── storage.py    # Multi-format exporter (JSON/CSV) & executive summary generator
├── main.py           # CLI entry point with configurable flags
└── requirements.txt  # Project dependencies
```

---

## ⚡ Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Scraper
```bash
# Scrape 2 pages (default) with 0.8s polite delay
python main.py

# Scrape 5 pages with 1.5s delay and export only CSV
python main.py --pages 5 --delay 1.5 --format csv
```

### 3. CLI Options
| Argument | Type | Default | Description |
|---|---|---|---|
| `--pages` | int | `2` | Total number of pages to crawl |
| `--delay` | float | `0.8` | Polite pause between HTTP calls (seconds) |
| `--format` | string | `both` | Export format (`json`, `csv`, or `both`) |
| `--output-dir` | string | `output` | Folder where generated files are stored |

---

## 💼 Business Use Cases for Clients
- **E-commerce Monitoring**: Track competitor prices, out-of-stock items, and rating fluctuations.
- **Lead Generation**: Harvest directories, listings, and public contact information.
- **Market Research**: Aggregate market catalogs into structured spreadsheets ready for BI tools.
