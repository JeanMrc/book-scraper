import requests
from bs4 import BeautifulSoup
import csv
import json
import time
import os

# ─────────────────────────────────────────
# Site Configurations
# ─────────────────────────────────────────
SITES = {
    "books": {
        "start_url": "https://books.toscrape.com/catalogue/page-1.html",
        "pagination": "https://books.toscrape.com/catalogue/page-{page}.html",
        "item_selector": "article.product_pod",
        "fields": {
            "title":  {"selector": "h3 a",          "attr": "title"},
            "price":  {"selector": "p.price_color", "attr": None},
            "rating": {"selector": "p.star-rating", "attr": "class"},
        }
    }
}

# ─────────────────────────────────────────
# Config
# ─────────────────────────────────────────
OUTPUT_FORMAT = "csv"   # "csv" or "json"
MAX_RETRIES   = 3
DELAY         = 1       # seconds between requests

RATING_MAP = {
    "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5
}

# ─────────────────────────────────────────
# Fetch Page
# ─────────────────────────────────────────
def fetch_page(url):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return BeautifulSoup(response.text, "html.parser")
            elif response.status_code == 404:
                return None
            else:
                print(f"  Attempt {attempt}: HTTP {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"  Attempt {attempt}: {e}")
        time.sleep(DELAY * attempt)
    print(f"  Failed after {MAX_RETRIES} attempts: {url}")
    return None

# ─────────────────────────────────────────
# Field Extractor
# ─────────────────────────────────────────
def extract_field(item, field_name, config):
    try:
        el = item.select_one(config["selector"])
        if el is None:
            return None

        if field_name == "price":
            raw = el.text.strip()
            return float(''.join(c for c in raw if c.isdigit() or c == '.'))

        if field_name == "rating":
            word = el["class"][1] if "class" in el.attrs else None
            return RATING_MAP.get(word, 0)

        if config["attr"]:
            return el[config["attr"]].strip()

        return el.text.strip()

    except Exception as e:
        print(f"  Field '{field_name}' extraction error: {e}")
        return None

# ─────────────────────────────────────────
# Scrape Page
# ─────────────────────────────────────────
def scrape_page(soup, site_config):
    items = []
    for item in soup.select(site_config["item_selector"]):
        record = {}
        for field_name, field_config in site_config["fields"].items():
            record[field_name] = extract_field(item, field_name, field_config)
        if any(v is not None for v in record.values()):
            items.append(record)
    return items

# ─────────────────────────────────────────
# Scrape All Pages
# ─────────────────────────────────────────
def scrape_site(site_name, site_config):
    print(f"\n{'='*50}")
    print(f"Scraping: {site_name}")
    print(f"{'='*50}")

    all_items = []
    page = 1

    while True:
        url  = site_config["pagination"].format(page=page)
        print(f"  Page {page}: {url}")
        soup = fetch_page(url)

        if soup is None:
            break

        page_items = scrape_page(soup, site_config)

        if not page_items:
            break

        all_items.extend(page_items)
        print(f"  {len(page_items)} items collected.")
        page += 1
        time.sleep(DELAY)

    print(f"  Total: {len(all_items)} items scraped from {site_name}.")
    return all_items

# ─────────────────────────────────────────
# Save Output
# ─────────────────────────────────────────
def save_output(site_name, items, fmt="csv"):
    if not items:
        print(f"  No data to save for {site_name}.")
        return

    base     = os.path.dirname(os.path.abspath(__file__))
    filename = f"{site_name}_data.{fmt}"
    path     = os.path.join(base, filename)

    if fmt == "json":
        with open(path, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=2, ensure_ascii=False)
    else:
        fieldnames = list(items[0].keys())
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(items)

    print(f"  Saved: {path} ({len(items)} records)")

# ─────────────────────────────────────────
# Main
# ─────────────────────────────────────────
if __name__ == "__main__":
    total = 0
    for site_name, site_config in SITES.items():
        items = scrape_site(site_name, site_config)
        save_output(site_name, items, fmt=OUTPUT_FORMAT)
        total += len(items)

    print(f"\n{'='*50}")
    print(f"Done. {total} total records scraped.")
    print(f"{'='*50}")
