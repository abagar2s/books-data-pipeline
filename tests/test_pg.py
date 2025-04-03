# test_connection.py
from sqlalchemy import create_engine

try:
    engine = create_engine("postgresql+psycopg2://postgres:admin@127.0.0.1:5432/realestate")
    conn = engine.connect()
    print("✅ Successfully connected to the database!")
except Exception as e:
    print("❌ Failed to connect:", e)
