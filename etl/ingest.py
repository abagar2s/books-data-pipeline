# ingest.py

import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import BookListing
from utils import add_missing_columns_if_needed, create_database_if_not_exists

def scrape_books_to_scrape():
    url = "https://books.toscrape.com"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
    }

    proxies = None  # Optional: if you want to use proxies, update this line accordingly

    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=15, verify=True)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of failure
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    listings = []

    # Parsing the listings from the page
    for item in soup.find_all("article", class_="product_pod"):
        title = item.find("h3").find("a")["title"] if item.find("h3") else None
        price = item.find("p", class_="price_color").get_text(strip=True) if item.find("p", class_="price_color") else None
        availability = item.find("p", class_="instock availability").get_text(strip=True) if item.find("p", class_="instock availability") else None
        link = item.find("h3").find("a")["href"] if item.find("h3").find("a") else None
        full_link = url + "/" + link if link else None

        # Scrape additional data
        rating = item.find("p", class_="star-rating")["class"][1] if item.find("p", class_="star-rating") else None
        image_url = item.find("img")["src"] if item.find("img") else None

        # Scraping category from the book's detail page
        category = None
        book_page = requests.get(full_link, headers=headers, proxies=proxies, verify=True)
        book_soup = BeautifulSoup(book_page.text, "html.parser")
        breadcrumb = book_soup.find("ul", class_="breadcrumb")
        breadcrumb_items = breadcrumb.find_all("li")
        if len(breadcrumb_items) > 2:
            category = breadcrumb_items[2].find("a").get_text(strip=True)

        listings.append({
            "title": title,
            "price": price,
            "availability": availability,
            "link": full_link,
            "rating": rating,
            "image_url": image_url,
            "category": category,
            "date_scraped": datetime.utcnow().isoformat()
        })

    print(f"🔍 Scraped {len(listings)} books.")
    return pd.DataFrame(listings)

def save_to_postgres(df):
    db_user = "postgres"
    db_pass = "admin"
    db_host = "localhost"
    db_port = "5432"
    db_name = "bookdb"

    DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    # Create the SQLAlchemy engine and session
    engine = create_engine(DATABASE_URL, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    # First, ensure the database and table are set up correctly
    create_database_if_not_exists()
    add_missing_columns_if_needed(engine)

    # Convert the dataframe to BookListing objects
    for index, row in df.iterrows():
        book = BookListing(
            title=row['title'],
            price=row['price'],
            availability=row['availability'],
            link=row['link'],
            rating=row['rating'],
            image_url=row['image_url'],
            category=row['category'],
            date_scraped=row['date_scraped']
        )
        session.add(book)

    try:
        session.commit()
        print("✅ Data saved to PostgreSQL!")
    except Exception as e:
        session.rollback()
        print(f"Error saving data: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    df = scrape_books_to_scrape()  # This is where the error was happening earlier
    if not df.empty:
        print(df.head())
        df.to_csv("data/books_to_scrape_listings.csv", index=False)
        save_to_postgres(df)
    else:
        print("⚠️ No data scraped — skipping database save.")
        print("🧪 Check 'data/debug.html' to inspect what was returned.")
