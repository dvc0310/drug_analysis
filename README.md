
# README for Drug Web Scraper and Utilities

## Overview

This project consists of a web scraper and associated utility scripts designed to extract, organize, and standardize drug information from online sources.

## Files

### 1. drug_scraper.py

This script is responsible for:

- Sending HTTP requests to extract drug information.
- Parsing the HTML of the response using `BeautifulSoup`.
- Extracting drug names and their associated links from the parsed HTML.
- Building a list of URLs based on the alphabet and digits to scrape drug names and links from a base URL.

**Key Functions:**

- `get_drug_links(soup)`: Extracts drug names and their links from the parsed HTML.
- `scrape_drugs(url)`: Initiates the scraping process for the specified URL.
- `build_drug_url_list()`: Constructs a list of URLs to scrape based on the alphabet and digits.

### 2. organize_drugs.py

This script focuses on:

- Using the `drug_scraper.py` module to fetch drug information.
- Extracting specific drug details, such as the drug class and uses, from the parsed HTML.

**Key Functions:**

- `get_drug_class_list(soup)`: Retrieves a list of drug classes.
- `get_uses_list(soup)`: Extracts a list of drug uses.
- `backup_uses(uses_lst, soup)`: An alternative method to extract drug uses.

### 3. similarity.py

This script identifies and addresses similarities between items:

**Key Functions:**

- `similar(a, b)`: Calculates the similarity ratio between two strings.
- `remove_similar_items(items, similarity_threshold=0.5)`: Removes items from a list that are similar based on a specified threshold.
- `remover(json_file_path)`: Processes a JSON file, removing similar uses for each drug.

### 4. standardize.py

This script standardizes and cleans drug-related strings:

**Key Functions:**

- `standardize_use_string(use_string, disease_aliases)`: Standardizes a drug use string based on known disease aliases.
- `remove_duplicates(uses_list)`: Removes duplicate strings from a list of uses.
- `standardizer(json_file_path)`: Reads a JSON file, processes each drug's "uses list", and standardizes each use string based on known disease aliases.

## Usage

To use the web scraper and utilities:

1. Execute `drug_scraper.py` to fetch and save drug information.
2. Use `organize_drugs.py` to further organize the scraped data.
3. Apply `similarity.py` to remove similar items from the dataset.
4. Use `standardize.py` to standardize drug use strings based on known disease aliases.

## Dependencies

- `requests`
- `bs4`
- `pandas`
- `difflib`
- `json`
- `re`
- `time`
- `random`

Ensure all dependencies are installed before running the scripts.

---

**Note:** Ensure that you have the appropriate permissions to scrape data from any website. Adhere to the website's `robots.txt` file and terms of service. Always use web scraping ethically and responsibly.
