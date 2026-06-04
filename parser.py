import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class BeautifulSoupParser:
    """A parser class that uses BeautifulSoup to parse HTML and extract clean text."""

    def parse(self, html_content: str) -> str:
        """
        Parses raw HTML and extracts cleaned, visible text content.

        Args:
            html_content (str): The raw HTML string.

        Returns:
            str: Cleaned text from the HTML page.

        Raises:
            ValueError: If the HTML content is empty.
            RuntimeError: If parsing fails.
        """
        if not html_content or not html_content.strip():
            logger.warning("Empty HTML content received.")
            raise ValueError("HTML content cannot be empty.")

        try:
            soup = BeautifulSoup(html_content, "html.parser")

            # Remove non-visible elements to keep text clean
            for element in soup(["script", "style", "head", "meta", "[document]"]):
                element.decompose()

            # Extract raw text separated by newlines
            raw_text = soup.get_text(separator="\n")

            # Clean and format text (strip whitespace, remove empty lines)
            lines = (line.strip() for line in raw_text.splitlines())
            # Split double space chunks and drop blank lines
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            cleaned_text = "\n".join(chunk for chunk in chunks if chunk)

            logger.info(f"Successfully parsed HTML. Extracted {len(cleaned_text)} characters of text.")
            return cleaned_text

        except Exception as e:
            logger.error(f"Error parsing HTML: {str(e)}")
            raise RuntimeError(f"Failed to parse HTML content: {str(e)}")

def parse_html(html_content: str) -> str:
    """Helper function to parse HTML content."""
    parser = BeautifulSoupParser()
    return parser.parse(html_content)
