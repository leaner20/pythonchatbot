# scraper.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse  # Added for URL validation


def scrape_website(url):
    """Scrape website content and return structured data"""
    try:
        # Validate URL format
        if not urlparse(url).scheme:
            url = 'http://' + url  # Add scheme if missing

        response = requests.get(
            url,
            headers={'User-Agent': 'Mozilla/5.0'},
            timeout=10  # Added timeout
        )
        response.raise_for_status()  # Raise HTTP errors

        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove unwanted elements more efficiently
        for element in soup(['script', 'style', 'nav', 'footer', 'iframe', 'noscript']):
            element.decompose()

        # Improved text extraction
        text = ' '.join(soup.stripped_strings)
        text = ' '.join(text.split())  # Remove extra whitespace

        return {
            "text": text[:50000],  # Limit to 50k chars to prevent memory issues
            "url": url,
            "status": "success",
            "chars": len(text)  # Added character count
        }

    except requests.RequestException as e:
        return {
            "text": "",
            "error": f"Request failed: {str(e)}",
            "status": "error"
        }
    except Exception as e:
        return {
            "text": "",
            "error": f"Processing error: {str(e)}",
            "status": "error"
        }
