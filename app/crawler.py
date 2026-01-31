import requests
from bs4 import BeautifulSoup

def crawl(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; AirtribeRAGBot/1.0)"
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
    except Exception as e:
        return f"Failed to fetch page: {e}"

    soup = BeautifulSoup(res.text, "html.parser")

    # Remove scripts/styles (important for clean text)
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    return soup.get_text(separator=" ", strip=True)
