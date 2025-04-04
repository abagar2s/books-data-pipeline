import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
import psycopg2
from psycopg2 import sql

# Function to scrape book data from the website
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

# Function to check and create the database if it doesn't exist
def create_database_if_not_exists():
    db_user = os.getenv("DB_USER", "postgres")
    db_pass = os.getenv("DB_PASS", "admin")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "bookdb")

    try:
        # Connect to PostgreSQL server (default database can be 'postgres')
        conn = psycopg2.connect(
            dbname="postgres",  # Use 'postgres' database to connect to the server
            user=db_user,
            password=db_pass,
            host=db_host,
            port=db_port
        )
        conn.autocommit = True  # This allows us to create a new database without starting a transaction
        cursor = conn.cursor()

        # Check if the database exists
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        exists = cursor.fetchone()

        if not exists:
            # Create the database if it does not exist
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            print(f"Database '{db_name}' created successfully.")
        else:
            print(f"Database '{db_name}' already exists.")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error while creating database: {e}")
        if conn:
            conn.close()

# Function to save the data to PostgreSQL
def save_to_postgres(df):
    db_user = os.getenv("DB_USER", "postgres")
    db_pass = os.getenv("DB_PASS", "admin")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "bookdb")

    DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    # First, ensure the database exists
    create_database_if_not_exists()

    # Proceed to connect and save data if the database exists
    try:
        engine = create_engine(DATABASE_URL)
        df.to_sql("books_to_scrape_listings", engine, if_exists="append", index=False)
        print("✅ Data saved to PostgreSQL!")
    except OperationalError as e:
        print(f"Error connecting to PostgreSQL: {e}")

# Main execution
if __name__ == "__main__":
    df = scrape_books_to_scrape()  # This is where the error was happening earlier
    
    if not df.empty:
        print(df.head())
        df.to_csv("data/books_to_scrape_listings.csv", index=False)
        save_to_postgres(df)
    else:
        print("⚠️ No data scraped — skipping database save.")
        print("🧪 Check 'data/debug.html' to inspect what was returned.")
