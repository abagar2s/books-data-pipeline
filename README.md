# 🏠 Real Estate Data Pipeline with CI/CD

This project is an end-to-end data engineering pipeline designed to scrape real estate listings from public websites, store and transform the data, and make it accessible through a dashboard or REST API. It includes CI/CD automation, testing, and containerization for deployment.

---

## 🧩 Project Goals

- Scrape real estate listings (e.g., location, price, size)
- Store raw data in a PostgreSQL or SQLite database
- Transform and clean the data (e.g., filter by region, price range, type)
- Build a CI/CD pipeline using GitHub Actions
- Make the listings searchable via dashboard or REST API

---

## 📦 Tech Stack Breakdown

| Task                     | Tool                          |
|--------------------------|-------------------------------|
| Web scraping             | Python + BeautifulSoup        |
| Storage                  | PostgreSQL or SQLite          |
| Data transformation      | dbt or pandas                 |
| CI/CD                    | GitHub Actions                |
| Containerization         | Docker                        |
| Testing                  | Pytest + dbt tests            |
| (Optional) Dashboard/API | Streamlit or FastAPI          |

---

## 🗂️ Folder Structure

```bash
real-estate-data-pipeline/
│
├── etl/                  # Web scraping + loaders
│   ├── ingest.py         # Scraper script
│   ├── clean.py          # Data cleaning/transformation logic
│
├── dbt/                  # dbt models + config
│   ├── models/
│   ├── dbt_project.yml
│
├── tests/                # Unit and data tests
│   └── test_ingest.py
│
├── .github/workflows/    # GitHub Actions CI/CD
│   └── ci.yml
│
├── Dockerfile            # Containerized pipeline
├── requirements.txt      # Python dependencies
├── README.md             # Project overview
└── setup.sh              # Optional: local setup script
```

## 🔍 What is Scraped?

From sites like **ImmoScout24** or **eBay Kleinanzeigen**, the scraper collects the following fields:

| Field        | Description                            |
|--------------|----------------------------------------|
| Title        | Listing title                          |
| Price        | Rent or purchase price                 |
| Location     | City and postcode                      |
| Size         | Size in square meters (m²)             |
| Room count   | Number of rooms                        |
| Date posted  | When the listing was added             |
| Link         | URL to the full listing                |

> ⚠️ This project respects the terms of use of third-party websites.

---

## 🚀 How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/real-estate-data-pipeline.git
cd real-estate-data-pipeline
```
