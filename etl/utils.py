# utils.py

from sqlalchemy import inspect
from sqlalchemy.exc import ProgrammingError
from sqlalchemy import create_engine
from models import Base, BookListing

def add_missing_columns_if_needed(engine):
    # Reflect the table schema from the database
    inspector = inspect(engine)
    
    # Get the columns of the table
    existing_columns = [col["name"] for col in inspector.get_columns("books_to_scrape_listings")]
    
    # Check and add missing columns
    with engine.connect() as connection:
        if 'rating' not in existing_columns:
            try:
                connection.execute("ALTER TABLE books_to_scrape_listings ADD COLUMN rating VARCHAR(10);")
                print("Added 'rating' column.")
            except ProgrammingError as e:
                print(f"Error adding rating column: {e}")
        
        if 'category' not in existing_columns:
            try:
                connection.execute("ALTER TABLE books_to_scrape_listings ADD COLUMN category VARCHAR(100);")
                print("Added 'category' column.")
            except ProgrammingError as e:
                print(f"Error adding category column: {e}")
        
        # Add other missing columns similarly

def create_database_if_not_exists():
    db_user = "postgres"
    db_pass = "admin"
    db_host = "localhost"
    db_port = "5432"
    db_name = "bookdb"
    DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    # Create the SQLAlchemy engine
    engine = create_engine(DATABASE_URL, echo=True)
    # First, ensure the database exists
    try:
        engine.connect()
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return
    # Create the tables if they don't exist
    Base.metadata.create_all(engine)
    print("Database and tables are ready!")
