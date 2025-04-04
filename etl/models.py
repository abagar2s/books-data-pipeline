# models.py

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# Define the table schema using SQLAlchemy ORM
class BookListing(Base):
    __tablename__ = 'books_to_scrape_listings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    price = Column(String, nullable=False)
    availability = Column(String, nullable=False)
    link = Column(String, nullable=False)
    rating = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    category = Column(String, nullable=True)
    date_scraped = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<BookListing(title={self.title}, price={self.price}, availability={self.availability}, link={self.link}, rating={self.rating}, image_url={self.image_url}, category={self.category}, date_scraped={self.date_scraped})>"
