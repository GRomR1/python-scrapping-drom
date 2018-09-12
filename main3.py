from bs4 import BeautifulSoup
import pprint
import requests

import re
import csv

import time
from bs4 import BeautifulSoup
from selenium import webdriver

user_id = 'Replika777'
URL = 'https://baza.drom.ru/user/{}'.format(user_id)
BASE_URL = 'https://baza.drom.ru'

#получение документа со скроллингом
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

def parse_user_page(content):
    soup = BeautifulSoup(content, 'html.parser')
    # print(soup.prettify(), type(soup))
    items = soup.body.form.table.tbody.find_all('td', {'class': 'descriptionCell'})
    disks = []
    for x in items:
        # print(x.prettify(), type(soup))
        link = BASE_URL + x.find('a').get('href')
        price = int(x.find('span', {'data-role': 'price'})
                    .text       
                    .replace("₽", "")
                    .strip()
                    .replace(' ', ''))
        title = x.find('a', {'class': 'bulletinLink'}).text.strip()
        title_short = x.find('a', {'class': 'bulletinLink'})\
                .text\
                .replace("New", "")\
                .replace("NEW", "")\
                .replace("!", "")\
                .replace("Комплект дисков", "")\
                .replace("Комплект", "")\
                .strip()
        annotation = x.find('div', {'class': 'annotation'}).text
        disks.append({
            "link": link,
            "price": price,
            "title": title,
            "title_short": title_short,
            "annotation": annotation,
        })
    print(type(disks), len(disks))
    pprint.pprint(disks)
    return disks


# encoding='cp1251'
def save_disks(disks, path):
    with open(path,'w', newline='') as csvfile:
        columns = ['title', 'link', 'price', 'annotation', 'title_short']
        writer = csv.DictWriter(csvfile, fieldnames=columns, delimiter=',')
        writer.writeheader()
        # запись нескольких строк
        writer.writerows(disks)
        # writer.writerows(
        #     (x['title'],
        #      "{}{}".format(BASE_URL, x['link']),
        #      x['price'],
        #      x['annotation'] for x in disks)
        # )


if __name__ == '__main__':
    content = get_html(URL)
    disks = parse_user_page(content)
    save_disks(disks, 'disks.csv')

    print("Hello")