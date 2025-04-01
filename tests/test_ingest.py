# tests/test_ingest.py

import pandas as pd
from etl import ingest

def test_scrape_returns_dataframe():
    df = ingest.scrape_listings()
    assert isinstance(df, pd.DataFrame), "Output is not a DataFrame"
    assert not df.empty, "DataFrame is empty"
    assert set(['title', 'price', 'location', 'link']).issubset(df.columns), "Missing expected columns"
