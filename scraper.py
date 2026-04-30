import requests
from bs4 import BeautifulSoup
import csv
import time


# -- Config --
BASE_URL = "https://books.toscrape.com/catalogue/"
START_URL = "https://books.toscrape.com/catalogue/page-1.html"


#Fetch Page 
def fetch_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, "html.parser")
    else:
        print(f"Failed to fetch:  {url}")
        return None
    
# -- Scrape Books --
RATING_MAP = {
    "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5
}

def scrape_books(soup):
    books = []
    for book in soup.select("article.product_pod"):
        title  = book.select_one("h3 a")["title"]
        price  = book.select_one("p.price_color").text.strip().replace("Â", "").replace("£", "").strip()
        rating = RATING_MAP.get(book.select_one("p.star-rating")["class"][1], 0)
        books.append({
            "title":  title,
            "price":  float(price),
            "rating": rating
        })
    return books

# -- Scrape All Pages --
def scrape_all_pages():
    all_books = []
    page = 1

    while True:
        url  = f"{BASE_URL}page-{page}.html"
        print(f"Scraping page {page}...")
        soup = fetch_page(url)

        if soup is None:
            break

        page_books = scrape_books(soup)

        if not page_books:
            break

        all_books.extend(page_books)
        page += 1
        time.sleep(1)

    print(f"Done! Scraped {len(all_books)} books total.")
    return all_books


#-- Save to CSV --
def save_to_csv(books):
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "books.csv")
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "price", "rating"])
        writer.writeheader()
        writer.writerows(books)
    print(f"Saved. {len(books)} books to books.csv")


#-- Run -- 
import os
books = scrape_all_pages()
save_to_csv(books)