from bs4 import BeautifulSoup
import pprint
import requests

import re,csv

import time
from bs4 import BeautifulSoup
from selenium import webdriver

def get_html(url):
    driver = webdriver.Chrome()
    driver.get(url)
    SCROLL_PAUSE_TIME = 3
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    return driver.page_source

user_id = 'Replika777'
url = 'https://baza.drom.ru/user/{}'.format(user_id)
soup = BeautifulSoup(get_html(url), 'html.parser')

print(soup.prettify(), type(soup))

items = soup.body.form.table.tbody.find_all('td', {'class': 'descriptionCell'})
disks = []

i = 0
for x in items:
    print(i)
    # print(x.prettify(), type(soup))
    disk_link = x.find('a').get('href')
    price = int(x.find('span', {'data-role': 'price'})
                .text
                .replace("₽", "")
                .strip()
                .replace(' ', ''))
    title = x.find('a', {'class': 'bulletinLink'}).text
    annotation = x.find('a', {'class': 'bulletinLink'}).text
    disks.append({
        "disk_link": disk_link,
        "price": price,
        "title": title,
        "annotation": annotation,
    })
    i = i+1

print(type(disks), len(disks))
pprint.pprint(disks)

# print(soup.prettify(), type(soup))

if __name__ == '__main__':
    print("Hello")