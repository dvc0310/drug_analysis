import requests
from bs4 import BeautifulSoup
import pandas as pd
from string import ascii_lowercase

headers_ = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0"
}


def get_drug_links(soup):
    """Extract drug names and their links from the parsed HTML."""
    drug_links = {}
    drug_list = soup.findAll("ul", class_="ddc-list-column-2")

    for drug in drug_list:
        for li in drug.find_all('a'):
            drug_name = li.contents[0]
            drug_links[drug_name] = {'name': drug_name, 'link': li.get('href')}

    return drug_links


def scrape_drugs(url):
    """Scrape drug names and their links from the specified URL."""
    response = requests.get(url, headers=headers_)
    soup = BeautifulSoup(response.content, "html.parser")
    return get_drug_links(soup)


def build_drug_url_list():
    """Build a list of URLs to scrape drug names and links."""
    base_url = "https://www.drugs.com/alpha/"
    return [base_url + c + ".html" for c in ascii_lowercase + "0-9"]
