import sys, os, re
from urllib.request import urlopen, urlretrieve, Request
from bs4 import BeautifulSoup
import pathlib

def clean_filename(name):
    return re.sub(r'[^A-Za-z0-9]+', '_', name).strip('_')

def scrape_netflix_metadata(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0'
    }
    req = Request(url, headers=headers)

    try:
        html = urlopen(req)
        soup = BeautifulSoup(html, 'html.parser')

        name = soup.find("h1", {"class": "title-title"}).text.strip()
        year = soup.find("span", {"class": "title-info-metadata-item item-year"}).text.strip()
        rating = soup.find("span", {"class": "maturity-number"}).text.strip()
        description = soup.find("div", {"class": "title-info-synopsis"}).text.strip()

        print(f"\nTitle:        {name}")
        print(f"Rating:       {rating}")
        print(f"Year:         {year}")
        print("Description:  ", description, "\n")

        safe_name = clean_filename(name)

        # Background Image
        bg_style = soup.find("div", {"class": "hero-image hero-image-desktop"}).get("style")
        bg_url = bg_style.split('url("')[-1].replace('")', '').strip()
        bg_file = f"{safe_name}-landscape.jpg"
        print("Downloading background @", bg_url)
        urlretrieve(bg_url, bg_file)

        # Logo Image
        logo_tag = soup.find("img", {"class": "logo", "data-uia": "title-logo"})
        if logo_tag:
            logo_url = logo_tag.get("src")
            logo_file = f"{safe_name}-logo.png"
            print("Downloading logo @", logo_url)
            urlretrieve(logo_url, logo_file)
        else:
            print("⚠️ Logo not found!")

    except Exception as e:
        print("❌ Error scraping the page:", e)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:\n  python netflix_scraper.py 'https://www.netflix.com/title/XXXXXX'")
    else:
        scrape_netflix_metadata(sys.argv[1])
