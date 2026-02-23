import os
import re
import requests
from bs4 import BeautifulSoup

def clean_text(text):
    """
    Strips wiki citations, extra whitespace, and standardizes text.
    """
    # Remove wiki citations like [1], [2a], [Note 1]
    text = re.sub(r'\[(?:Note )?\d+[a-zA-Z]?\]', '', text)
    # Remove extra whitespaces/newlines
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def scrape_wiki_page(url, output_file):
    """
    Scrapes a public wiki page, extracts pure narrative text, and saves it.
    """
    print(f"Scraping {url}...")
    try:
        # User-Agent header to prevent 403 blocks from wikis
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Typical content wrappers for MediaWiki sites (like Lexicanum, Halopedia)
    content_div = soup.find('div', class_='mw-parser-output')
    if not content_div:
        content_div = soup.find('div', id='bodyContent')
        
    if not content_div:
        print("Could not find main content div. Skipping.")
        return

    # Extract all paragraph texts
    paragraphs = content_div.find_all('p')
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'a', encoding='utf-8') as f:
        for p in paragraphs:
            text = clean_text(p.get_text())
            if text:
                f.write(text + "\n\n")
                
    print(f"Saved narrative content to {output_file}")

if __name__ == "__main__":
    # Example usage for testing
    test_urls = [
        ("https://wh40k.lexicanum.com/wiki/Immaterium", "immaterium.txt"),
        ("https://www.halopedia.org/Slipstream_space", "slipspace.txt")
    ]
    
    base_raw_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")
    
    for url, filename in test_urls:
        output_path = os.path.abspath(os.path.join(base_raw_dir, filename))
        scrape_wiki_page(url, output_path)
