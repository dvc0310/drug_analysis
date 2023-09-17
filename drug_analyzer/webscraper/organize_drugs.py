import requests
from bs4 import BeautifulSoup
import time
import re
import drug_scraper as ds
import random
from requests.exceptions import RequestException
import json
import os
import standardize as stand
import similarity as srm

headers_ = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0"
}


def get_drug_class_list(soup):
    target_subtitle = soup.find_all("p", class_='drug-subtitle', recursive=True)
    if not target_subtitle:
        return []

    drug_class_list = target_subtitle[0].find_all('a', href=True)
    dc_lst = [drug_class.text for drug_class in drug_class_list if drug_class.has_attr('href') and 'drug-class' in drug_class['href']]
    
    return dc_lst


def get_uses_list(soup):
    uses_lst = []
    
    #Checking if there's a breadcrumb with "Treatments"
    ol_element = soup.find('ol', class_='ddc-breadcrumb-3')
    
    if ol_element:
        treatment_found = False
        breadcrumb_items = ol_element.find_all('li', class_='ddc-breadcrumb-item')

        for item in breadcrumb_items:
            if item.get_text().strip() == 'Treatments':
                treatment_found = True
                break

        if treatment_found:
            if len(breadcrumb_items) > 1:
                uses_lst.append(breadcrumb_items[1].get_text().strip())
                
        
    backup_uses(uses_lst, soup)
    
                    
    return uses_lst

def backup_uses(uses_lst, soup):
    target_uses = soup.find_all('h2', id='uses')
        

    for use_tag in target_uses:
        for item in use_tag.next_siblings:
            if item.name == "h2":
                break

            if not item.name:
                continue

            for c in item:
                if c.name == 'a' and ('cg' in c.attrs['href'] or 'condition' in c.attrs['href']):
                    if(c.string is not None):
                        use = c.string.lower().strip()  # Convert the string to lowercase
                        if use not in map(str.lower, uses_lst):  # Check if it's not already in the list
                            uses_lst.append(c.string.strip())
   
   
def get_rating_and_status(soup):
    rating_subtitle = soup.find_all("div", class_='ddc-rating-summary', recursive=True)    
    status_subtitle = soup.find_all("div", class_='ddc-status-info', recursive=True)

    try:
        review = rating_subtitle[0].find('a').string
        review = re.sub(',', '', review)
        review = re.findall('\d+', review)[0]
    except IndexError:
        review = '0'

    try:
        if rating_subtitle[0].find('b') is not None:
            rating = rating_subtitle[0].find('b').string
            rating = re.sub(',', '', rating)
            rating = re.findall('\d+', rating)[0]
        else:
            rating = 'N/A'
    except IndexError:
        rating = 'N/A'

    try:
        status_box = status_subtitle[0].contents[3].contents[1]
        availability = next(status.contents[1].contents[1].contents[1].text for status in status_box if status != '\n')
    except IndexError:
        availability = 'N/A'

    try:
        ddc_section = status_box.select('.ddc-accordion-section:nth-of-type(3)')[0]
        CSA_Schedule_Number = ddc_section.select('div:first-of-type')[0]
        CSA_Schedule_Number = CSA_Schedule_Number.select('div.ddc-accordion-heading')[0]
        # Find all span elements
        span_elements = CSA_Schedule_Number.find_all('span', class_='ddc-status-icon')

        # Select the last span element
        CSA_Schedule_Number = span_elements[-1].text
        
        #CSA_Schedule_Number = CSA_Schedule_Number.select('span.ddc-status-icon.drugInfoCSAN')[0].text
        
        if CSA_Schedule_Number == 'N/A':
            CSA_Schedule_Number = 'Not a controlled drug'
        elif CSA_Schedule_Number == '1':
            CSA_Schedule_Number = 'Schedule 1'
        elif CSA_Schedule_Number == '2':
            CSA_Schedule_Number  = 'Schedule 2'
        elif CSA_Schedule_Number == '3':
            CSA_Schedule_Number = 'Schedule 3'
        elif CSA_Schedule_Number == '4':
            CSA_Schedule_Number = 'Schedule 4'
        elif CSA_Schedule_Number == '5':
            CSA_Schedule_Number = 'Schedule 5'
    except:
        CSA_Schedule_Number = 'Not a controlled drug'

    return review, rating, availability, CSA_Schedule_Number


def write_to_json(filename):
    drug_dict = {}
    
    drugurl = ds.build_drug_url_list()
    for url in drugurl:
        drug_dict.update(ds.scrape_drugs(url))

    i = 1
    for k, v in drug_dict.items():
        for _ in range(3):  # Retry up to 3 times
            try:
                with requests.Session() as session:
                    page = session.get('http://drugs.com/' + v['link'], headers=headers_)
                    soup = BeautifulSoup(page.content, "html.parser")

                v['drug class list'] = get_drug_class_list(soup)
                v['uses list'] = [*set(get_uses_list(soup))]
                review, rating, status, schedule = get_rating_and_status(soup)
                v['review'] = review
                v['rating'] = rating
                v['status'] = status
                v['schedule'] = schedule
                print(str(i) + "/" + str(len(drug_dict)))
                i += 1
                
                break  # Exit the retry loop if the request was successful

            except RequestException as e:
                print(f"Request error: {e}, retrying...")
                time.sleep(2 ** _ * 0.5)  # Exponential backoff: 0.5, 1, 2 seconds

        else:
            print(f"Failed to process {v['name']} after 3 retries")
        
        time.sleep(random.uniform(1, 2))  # Random delay between 1 and 2 seconds

    # Get the absolute path to the directory containing the script
    filename = absolute_path(filename)
    # Save the data to a JSON file
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(drug_dict, json_file, ensure_ascii=False, indent=4)
    
    srm.remover(filename)
    stand.standardizer(filename) 
   
     

def where_json(file_name):
    file_path = os.path.abspath(file_name)
    print(f"Checking file path: {file_path}")
    return os.path.exists(file_path)

   
def main():
    if where_json(absolute_path('drug_data.json')):
        pass
    else:
        write_to_json(absolute_path('drug_data.json'))
    

def absolute_path(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    return os.path.join(parent_dir, filename)
    
    
if __name__ == "__main__":
    main()