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
   git clone https://github.com/JeanMrc/book-scraper
```

2. Install dependencies
```bash
   pip install -r requirements.txt
```

3. Run the scraper
```bash
   python scraper.py
```

---

## Configuration

To scrape a different site, add a new entry to the `SITES` dictionary in
`scraper.py`:

```python
SITES = {
    "your_site": {
        "start_url": "https://example.com/page-1/",
        "pagination": "https://example.com/page-{page}/",
        "item_selector": "div.item",
        "fields": {
            "title": {"selector": "h2.title", "attr": None},
            "price": {"selector": "span.price", "attr": None},
        }
    }
}
```

To switch output format, change `OUTPUT_FORMAT` at the top of `scraper.py`:

```python
OUTPUT_FORMAT = "json"  # or "csv"
```

---

## Ethical Scraping

- books.toscrape.com is a sandbox site built for scraping practice
- 1 second delay between each page request
- Exponential backoff on failed requests — 3 attempts before stopping
- No personal data collected — public product data only

---

## Technical Challenges Solved

**1. Text-based star ratings**
books.toscrape.com returns ratings as words ("One", "Two", "Three") instead
of numbers. Solved by mapping them to integers via a dictionary, ensuring the
output is immediately ready for analysis without post-processing.

**2. Encoding issues**
Price symbols appeared as (Â£) due to character encoding mismatches. Solved
by stripping all non-numeric characters and converting to float, making the
data reliable across all environments.

**3. Retry logic**
Network failures previously caused the scraper to stop silently. Solved with
exponential backoff — retrying up to 3 times with increasing wait times before
giving up on a page.
