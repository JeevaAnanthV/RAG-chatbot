import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    """
    Scrape the content of a website.

    Parameters:
    - url (str): URL of the website to scrape

    Returns:
    - str: The scraped text content
    """
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract text from paragraphs
        paragraphs = soup.find_all('p')
        text = "\n".join([para.get_text() for para in paragraphs])
        return text
    else:
        return "Error: Unable to fetch the webpage."

# Example usage:
# print(scrape_website("https://example.com"))
