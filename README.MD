#  Book Scraper

A Python web scraper that automatically collects all 1000 books from 
books.toscrape.com across 50 pages and outputs a clean, analysis-ready CSV.

---

##  Features
- Scrapes 50 pages automatically without manual intervention
- Cleans and structures price and rating data
- Outputs analysis-ready CSV — no post-processing needed
- Ethical scraping — 1 second delay between requests
- Gracefully handles missing pages without crashing

---

##  Data Collected
| Column | Type | Example |
|--------|------|---------|
| title  | text | A Light in the Attic |
| price  | float | 51.77 |
| rating | integer | 3 |

---

## Sample Results

| Title | Price  | Rating  |
|-------|-----------|------------|
| A Light in the Attic | 51.77 | 3 |
| Tipping the Velvet | 53.74 | 1 |
| Soumission | 50.10 | 1 |
| Sharp Objects | 47.82 | 4 |

---

##  Built With
- Python 3.13
- Requests — HTTP requests
- BeautifulSoup4 — HTML parsing
- CSV — lightweight data export

---

##  How to Run
1. Clone the repo git clone https://github.com/JeanMrc/book-scraper
2. Install dependencies:
   pip install -r requirements.txt
3. Run the scraper:
   python scraper.py

---

## Ethical Scraping
- books.toscrape.com is a sandbox site built for scraping practice
- 1 second delay between each page request
- No personal data collected — public product data only

---

## Technical Challenges Solved

**1. Text-based star ratings**
Books.toscrape.com returns ratings as words ("One", "Two", "Three") 
instead of numbers. Solved by mapping them to integers using a Python 
dictionary ensuring the CSV is immediately ready for analysis.

**2. Encoding issues**
Price symbols appeared as (Â£) due to character encoding mismatches. 
Solved by stripping invalid characters and converting prices to floats 
for proper numerical sorting in Excel.
