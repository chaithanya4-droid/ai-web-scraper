import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class SeleniumScraper:
    """A scraper class that uses Selenium to fetch page HTML content dynamically."""

    def __init__(self, headless: bool = True):
        self.headless = headless

    def _get_options(self) -> Options:
        """Configure Chrome options for Selenium."""
        options = Options()
        if self.headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        # Add a realistic user agent to avoid bot detection blockages
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        return options

    def scrape(self, url: str) -> str:
        """
        Scrapes the given URL and returns the raw HTML content.

        Args:
            url (str): The target URL to scrape.

        Returns:
            str: The raw HTML content of the page.

        Raises:
            RuntimeError: If scraping fails for any reason.
        """
        logger.info(f"Initiating scrape for URL: {url}")
        driver = None
        try:
            options = self._get_options()
            # Let Selenium Manager handle chromedriver download automatically
            driver = webdriver.Chrome(options=options)
            
            # Set page load timeout
            driver.set_page_load_timeout(30)
            driver.get(url)
            
            # Retrieve HTML page source
            html_content = driver.page_source
            logger.info("Successfully retrieved page HTML content.")
            return html_content
            
        except Exception as e:
            logger.error(f"Error scraping URL {url}: {str(e)}")
            raise RuntimeError(f"Failed to scrape the webpage: {str(e)}")
            
        finally:
            if driver:
                try:
                    driver.quit()
                except Exception as ex:
                    logger.warning(f"Error when closing WebDriver: {ex}")

def scrape_url(url: str) -> str:
    """Helper function to scrape a URL."""
    scraper = SeleniumScraper(headless=True)
    return scraper.scrape(url)
