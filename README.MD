# Book Scraper

A configurable Python web scraper that extracts structured data from paginated
websites and outputs clean, analysis-ready CSV or JSON files.

Built and tested against books.toscrape.com — scraping all 1000 books across
50 pages with automatic pagination, retry logic, and multi-site support.

---

## Features

- Multi-site support — configure any paginated website via the SITES dictionary
- Automatic pagination — scrapes all pages until no more data is found
- Retry logic — retries failed requests up to 3 times with exponential backoff
- Flexible output — exports to CSV or JSON
- Data integrity — deduplicates and cleans price and rating data automatically
- Ethical scraping — 1 second delay between requests, respects server load

---

## Data Collected

| Column | Type    | Example              |
|--------|---------|----------------------|
| title  | text    | A Light in the Attic |
| price  | float   | 51.77                |
| rating | integer | 3                    |

---

## Sample Output

| Title                | Price | Rating |
|----------------------|-------|--------|
| A Light in the Attic | 51.77 | 3      |
| Tipping the Velvet   | 53.74 | 1      |
| Soumission           | 50.10 | 1      |
| Sharp Objects        | 47.82 | 4      |

---

## Built With

- Python 3.13
- Requests — HTTP requests
- BeautifulSoup4 — HTML parsing
- CSV / JSON — data export

---

## How to Run

1. Clone the repo
```bash
