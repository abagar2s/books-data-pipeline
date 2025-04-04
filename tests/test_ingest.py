import unittest
from unittest import mock
from etl.ingest import scrape_books_to_scrape  # Import your function here

class TestScrapingFunction(unittest.TestCase):

    @mock.patch('requests.get')  # Mock requests.get to avoid actual HTTP requests
    @mock.patch('builtins.open', new_callable=mock.mock_open)  # Mock open to avoid writing a file
    def test_scrape_books_to_scrape(self, mock_open, mock_get):
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

        # Check that open was called to write the debug file
        mock_open.assert_called_with("data/debug.html", "w", encoding="utf-8")

        # Check the result
        self.assertEqual(len(df), 2)  # Expecting 2 books from the mock HTML
        self.assertEqual(df.iloc[0]["title"], "Book Title 1")  # Check the title of the first book

if __name__ == '__main__':
    unittest.main()


