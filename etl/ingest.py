# etl/ingest.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import random

def scrape_listings():
    url = "https://www.ebay-kleinanzeigen.de/s-immobilien/berlin/c195l3331"
    headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
    }


    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    listings = []

    for item in soup.select("article.aditem"):
        title = item.select_one(".text-module-begin")
        price = item.select_one(".aditem-main--middle--price")
        location = item.select_one(".aditem-main--top--left")
        link = item.select_one("a")["href"]

        listings.append({
            "title": title.get_text(strip=True) if title else None,
            "price": price.get_text(strip=True) if price else None,
            "location": location.get_text(strip=True) if location else None,
            "link": "https://www.ebay-kleinanzeigen.de" + link,
            "date_scraped": datetime.utcnow().isoformat()
        })

    return pd.DataFrame(listings)

if __name__ == "__main__":
    df = scrape_listings()
    print(df.head())
    df.to_csv("data/raw_listings.csv", index=False)
