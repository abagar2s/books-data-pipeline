import unittest
from unittest import mock
from etl.ingest import scrape_books_to_scrape  # Import your scraping function here
from bs4 import BeautifulSoup

class TestScrapingFunction(unittest.TestCase):

    @mock.patch('requests.get')  # Mock requests.get to avoid actual HTTP requests
    def test_scrape_books_to_scrape(self, mock_get):
        # Sample HTML data (you can add more complex or realistic HTML for better testing)
        sample_html = """
        <html>
            <body>
                <article class="product_pod">
                    <h3><a title="Book Title 1" href="catalogue/book-1">Book Title 1</a></h3>
                    <p class="price_color">£51.77</p>
                    <p class="instock availability">In stock</p>
                </article>
                <article class="product_pod">
                    <h3><a title="Book Title 2" href="catalogue/book-2">Book Title 2</a></h3>
                    <p class="price_color">£53.74</p>
                    <p class="instock availability">In stock</p>
                </article>
            </body>
        </html>
        """

        # Mock the HTTP response to return our sample HTML
        mock_response = mock.Mock()
        mock_response.text = sample_html
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Call the scraping function
        df = scrape_books_to_scrape()

        # Check if the dataframe contains the expected data
        self.assertEqual(len(df), 2)  # We expect two books in the mock response
        self.assertEqual(df['title'].iloc[0], 'Book Title 1')
        self.assertEqual(df['price'].iloc[0], '£51.77')
        self.assertEqual(df['availability'].iloc[0], 'In stock')
        self.assertEqual(df['link'].iloc[0], 'https://books.toscrape.comcatalogue/book-1')

        # Test the second book as well
        self.assertEqual(df['title'].iloc[1], 'Book Title 2')
        self.assertEqual(df['price'].iloc[1], '£53.74')
        self.assertEqual(df['availability'].iloc[1], 'In stock')
        self.assertEqual(df['link'].iloc[1], 'https://books.toscrape.comcatalogue/book-2')

if __name__ == '__main__':
    unittest.main()
