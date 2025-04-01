import pandas as pd
from etl import ingest
import warnings

def test_scrape_returns_dataframe():
    df = ingest.scrape_listings()
    assert isinstance(df, pd.DataFrame), "Output is not a DataFrame"

    if df.empty:
        warnings.warn("⚠️ WARNING: Scraper returned an empty DataFrame. Possible site block or structure change.")
    else:
        assert set(['title', 'price', 'location', 'link']).issubset(df.columns), "Missing expected columns"
