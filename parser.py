import requests
from bs4 import BeautifulSoup
import csv
import os

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'accept': '*/*'
}

# site url, ex. - https://auto.ria.com
HOST = ''
FILE = 'cars.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='mhide')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='proposition_area')
    cars = []
    for item in items:
        cars.append({
            'title': item.find('h3', class_='proposition_name').find_next('strong').get_text(strip=True),
            'link': HOST + item.find('h3', class_='proposition_name').find_next('a').get('href'),
            'usd_price': item.find('span', class_='green').get_text(strip=True),
        })
    return cars


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Sku', 'Link', 'Price'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['usd_price']])


def parse():
    URL = input('Enter URL: ')
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Parsing page {page} of {pages_count} ...')
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))
        save_file(cars, FILE)
        print(f'Got {len(cars)} cars')
        # os.startfile(FILE)
    else:
        print('Error')


parse()
