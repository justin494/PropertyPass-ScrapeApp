import requests
from bs4 import BeautifulSoup
import json
import openpyxl

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def fetch_and_save_to_file(url, path, output_format='json'):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    data = []
    
    # Find all property listings
    containers = soup.find_all('div', class_='mb-srp__card__container')
    estimates = soup.find_all('div', class_='mb-srp__card__estimate')
    
    for container, estimate in zip(containers, estimates):
        property_name = container.find('h2', class_='mb-srp__card--title').text.strip()
        size_elem = container.find('div', class_='mb-srp__card__summary__list--item', attrs={'data-summary': 'super-area'})
        size_of_land = size_elem.find('div', class_='mb-srp__card__summary--value').text.strip() if size_elem else 'Size not available'
        owner_contact_elem = container.find('div', class_='mb-srp__card__ads--name')
        owner_contact = owner_contact_elem.text.strip().replace('Owner: ', '') if owner_contact_elem else 'Contact not available'
        price_elem = estimate.find('div', class_='mb-srp__card__price--amount')
        price = price_elem.text.strip() if price_elem else 'Price not available'
        
        property_info = {
            'Property Name': property_name,
            'Size of Land': size_of_land,
            'Price': price,
            'Owner Contact': owner_contact
        }
        
        data.append(property_info)
    
    if output_format == 'json':
        with open(path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
    elif output_format == 'xlsx':
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(['Property Name', 'Size of Land', 'Price', 'Owner Contact'])
        
        for property_info in data:
            sheet.append([property_info['Property Name'], property_info['Size of Land'], property_info['Price'], property_info['Owner Contact']])
        
        workbook.save(path)
    else:
        print("Unsupported output format")

url = "https://www.magicbricks.com/low-budget-flats-for-sale-in-vellore-pppfs"
fetch_and_save_to_file(url, "data/magicbricks.json", output_format='json')
fetch_and_save_to_file(url, "data/magicbricks.xlsx", output_format='xlsx')
