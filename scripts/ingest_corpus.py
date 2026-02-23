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
    import cloudscraper
    print(f"Scraping {url}...")
    try:
        scraper = cloudscraper.create_scraper(browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        })
        response = scraper.get(url, timeout=20)
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
    import argparse
    parser = argparse.ArgumentParser(description="Ingest lore corpus for The Epoch Chronicler.")
    parser.add_argument("--target", type=str, default="all", help="Target pillar to scrape (e.g., 'all', 'precursors_folly')")
    args = parser.parse_args()

    # Define targets based on the 6 Philosophical Pillars
    pillars = {
        "precursors_folly": [
            ("https://www.halopedia.org/Forerunner", "precursors_folly.txt"),
            ("https://wh40k.lexicanum.com/wiki/Necron", "precursors_folly.txt")
        ],
        "reclaimers_burden": [
            ("https://www.halopedia.org/Spartan", "reclaimers_burden.txt"),
            ("https://wh40k.lexicanum.com/wiki/Space_Marine", "reclaimers_burden.txt")
        ],
        "decay_of_reason": [
            ("https://wh40k.lexicanum.com/wiki/Adeptus_Mechanicus", "decay_of_reason.txt"),
            ("https://wh40k.lexicanum.com/wiki/Machine_Spirit", "decay_of_reason.txt")
        ],
        "cosmic_insignificance": [
            ("https://wh40k.lexicanum.com/wiki/Tyranid", "cosmic_insignificance.txt"),
            ("https://www.halopedia.org/Flood", "cosmic_insignificance.txt")
        ],
        "sacrifice_of_transhumanism": [
            ("https://wh40k.lexicanum.com/wiki/Servitor", "sacrifice_of_transhumanism.txt"),
            ("https://wh40k.lexicanum.com/wiki/Dreadnought", "sacrifice_of_transhumanism.txt")
        ],
        "algorithmic_serfdom": [
            ("https://cyberpunk.fandom.com/wiki/Megacorporation", "algorithmic_serfdom.txt"),
            ("https://cyberpunk.fandom.com/wiki/Arasaka", "algorithmic_serfdom.txt")
        ]
    }

    targets_to_run = []
    if args.target == "all":
        for urls in pillars.values():
            targets_to_run.extend(urls)
    elif args.target in pillars:
        targets_to_run.extend(pillars[args.target])
    else:
        print(f"Unknown target: {args.target}")
        exit(1)
        
    base_raw_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "raw"))
    print(f"Saving corpus to {base_raw_dir}")
    
    for url, filename in targets_to_run:
        output_path = os.path.join(base_raw_dir, filename)
        scrape_wiki_page(url, output_path)
