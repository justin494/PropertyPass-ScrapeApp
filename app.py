from flask import Flask, render_template, request
from datetime import datetime
import random
from hashlib import sha256

app = Flask(__name__)

# list to store blockchain
blockchain = []

# Property record class
class PropertyRecord:
    def __init__(self, name, uid, age, land, coordinate, city):
        self.timestamp = datetime.now()
        self.name = name
        self.age = age
        self.uid = uid
        self.city = city
        self.coordinate = coordinate
        self.land = land
        self.previous_hash = None
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        hash_data = str(self.timestamp) + self.name + str(self.uid) + str(self.age) + self.city + str(self.coordinate) + self.land
        return sha256(hash_data.encode()).hexdigest()

    def calculate_previous_hash(self):
        if len(blockchain) > 0:
            for record in reversed(blockchain):
                if record.land == self.land:
                    return record.hash
            return None
        else:
            return None

# to add new record to blockchain
@app.route('/add_record', methods=['POST'])
def add_record():
    name = request.form['name']
    age = request.form['age']
    uid = request.form['uid']
    city = request.form['city']
    coordinate = request.form['coordinate']
    land = request.form['land']
    

    # Create a new property record
    record = PropertyRecord(name, uid, age, land, coordinate, city)

    # Adding the property record to the blockchain
    record.previous_hash = record.calculate_previous_hash()
    blockchain.append(record)

    return f'Record added to blockchain successfully. Your User ID - {uid}'

# getting property record from blockchain
@app.route('/get_records', methods=['GET'])
def get_records():
    land = request.args.get('land')
    filtered_blockchain = [block for block in blockchain if block.land == land]
    if filtered_blockchain:
        return render_template('get.html', blockchain=filtered_blockchain)
    else:
        return 'No owner exits.'


# displaying whole blockchain
@app.route('/add_dummy', methods=['GET'])
def add_dummy():
    
    blockchain.append(PropertyRecord('Justin', 248804082, 21, 'SJT',24.24235, 'vellore'))

    blockchain.append(PropertyRecord('ashish', 248804082, 21, 'GDN',24.24235, 'vellore'))

    blockchain.append(PropertyRecord('adeem', 248804082, 21, 'SMV',24.24235, 'vellore'))

    blockchain.append(PropertyRecord('gora', 248804082, 21, 'TT',24.24235, 'vellore'))

    blockchain.append(PropertyRecord('mathias', 248804082, 21, 'MGR',24.24235, 'vellore'))
    return 'data added'


@app.route('/view_blockchain', methods=['GET'])
def view_blockchain():

    return render_template('blockchain.html', blockchain=blockchain)

@app.route('/view_aboutus', methods=['GET'])
def view_aboutus():
    return render_template('aboutus.html', blockchain=blockchain)

@app.route('/view_buy',methods=['GET'])
def view_buy():
    return render_template('buy.html')

@app.route('/view_buyy',methods=['GET'])
def view_buyy():
    return render_template('index.html')

@app.route('/view_login',methods=['GET'])
def view_login():
    return render_template('Home.html')


import requests
from bs4 import BeautifulSoup
import json
import openpyxl

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

import os

def fetch_and_save_to_file(url, path, output_format='json'):
    if not os.path.exists("data"):
        os.makedirs("data")
    
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


@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form['url']
    fetch_and_save_to_file(url, "data/magicbricks.json", output_format='json')
    with open("data/magicbricks.json", 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return render_template('scraper.html', data=data)

    

# returning landing page
@app.route('/')
def index():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
