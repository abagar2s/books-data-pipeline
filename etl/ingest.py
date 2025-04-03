import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine

def scrape_books_to_scrape():
    url = "https://books.toscrape.com"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
    }

    proxies = None  # Optional: if you want to use proxies, update this line accordingly

    response = requests.get(url, headers=headers, proxies=proxies, timeout=15, verify=True)
    
    # Debug: Save response for inspection
    with open("data/debug.html", "w", encoding="utf-8") as f:
        f.write(response.text)

    soup = BeautifulSoup(response.text, "html.parser")
    
    listings = []

    # Parsing the listings from the page
    for item in soup.find_all("article", class_="product_pod"):
        title = item.find("h3").find("a")["title"] if item.find("h3") else None
        price = item.find("p", class_="price_color").get_text(strip=True) if item.find("p", class_="price_color") else None
        availability = item.find("p", class_="instock availability").get_text(strip=True) if item.find("p", class_="instock availability") else None
        link = item.find("h3").find("a")["href"] if item.find("h3").find("a") else None
        full_link = url + link if link else None

        listings.append({
            "title": title,
            "price": price,
            "availability": availability,
            "link": full_link,
            "date_scraped": datetime.utcnow().isoformat()
        })

    print(f"🔍 Scraped {len(listings)} books.")
    return pd.DataFrame(listings)

# Function to save the scraped data to PostgreSQL
def save_to_postgres(df):
    db_user = os.getenv("DB_USER", "postgres")
    db_pass = os.getenv("DB_PASS", "admin")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "realestate")

    DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(DATABASE_URL)

    df.to_sql("books_to_scrape_listings", engine, if_exists="append", index=False)
    print("✅ Data saved to PostgreSQL!")

# Main execution
if __name__ == "__main__":
    df = scrape_books_to_scrape()  # This is where the error was happening earlier
    print(df.head())

    df.to_csv("data/books_to_scrape_listings.csv", index=False)

    if not df.empty:
        save_to_postgres(df)
    else:
        print("⚠️ No data scraped — skipping database save.")
        print("🧪 Check 'data/debug.html' to inspect what was returned.")
