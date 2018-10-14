from bs4 import BeautifulSoup
from pprint import pprint
import requests

import re
import csv

from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver

user_id = 'Replika777'
URL = 'https://baza.drom.ru/user/{}'.format(user_id)
BASE_URL = 'https://baza.drom.ru'
# driver = webdriver.Chrome()

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
        sleep(SCROLL_PAUSE_TIME)
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
                .replace("Комплект", "") \
                .replace("Оригинальные", "") \
                .replace("Злые", "") \
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
    pprint(disks)
    return disks

# content = get_disk_page('https://baza.drom.ru/chita/wheel/disc/new-enkei-66096670.html')
# def get_disk_page(url):
#     r = requests.get(url)
#     return r.text.encode('cp1251')


def get_disk_page(url):
    driver.get(url)
    sleep(2)
    return driver.page_source


def parse_disk_page(content, price):
    soup = BeautifulSoup(content, 'html.parser')
    diameter = soup.find('span', {'data-field': 'wheelDiameter'}).text.strip().replace(' ', '')  # Диаметр
    disk_parameters = soup.find('div', {'data-field': 'discParameters'})
    width = disk_parameters.find_all('span')[0].text.strip().replace(' ', '')  # Ширина
    et = disk_parameters.find_all('span')[1].text.strip().replace(' ', '').replace('мм.', 'мм')  # Вылет (ET)
    pcd = soup.find('span', {'data-field': 'wheelPcd'}).text.strip().replace(' ', '')  # Сверловка (PCD)
    type = soup.find('span', {'data-field': 'diskType'}).text.strip().replace(' ', '')  # Тип
    dia = soup.find('span', {'data-field': 'wheelPcd'}).text.strip().replace(' ', '')  # Диаметр ЦО (DIA)
    img_block = soup.find('div', {'class': 'imagesExBig'})
    image_links = img_block.find_all('img')
    img = image_links[0]['src']
    img_full = img.replace('bulletin', 'default')
    diameter_int = int(diameter.replace('"', ''))
    if diameter_int >= 19:
        retail_price = price + 10000
    else:
        retail_price = price + 5000

    return {
        "diameter": diameter,
        "width": width,
        "et": et,
        "pcd": pcd,
        "type": type,
        "dia": dia,
        "retail_price": retail_price,
        "img": img,
        "img_full": img_full,
    }

header_attr_names = {
    "code": "<setup>FNUMBER;Код товара;string</setup>",
    "name_product": "<setup>FNAME;Наименование;string</setup>",
    "link": "<setup>FATT_STR_60;Ссылка:;string</setup>",
    "count": "<setup>FSTATE;Остатки на складе;int</setup>",
    "price": "<setup>FATT_STR_62;Цена закупа;int</setup>",
    "retail_price": "<setup>FATT_STR_63;Цена продажи;int</setup>",
    "retail_price_one": "<setup>FPRICE;Стоимость;double</setup>",
    "title": "<setup>FANNOTATION;Описания;string</setup>",
    # "title_short": row['title_short'],
    "color": "<setup>FATT_STR_35;Цвет:;string</setup>",
    "diameter": "<setup>FATT_STR_29;Посадочный диаметр:;string</setup>",
    "width": "<setup>FATT_STR_28;Ширина обода:;string</setup>",
    "et": "<setup>FATT_STR_32;Вылет:;string</setup>",
    "holes": "<setup>FATT_STR_30;Кол-во отверстий:;string</setup>",
    "pcd": "<setup>FATT_STR_31;PCD:;string</setup>",
    "type": "<setup>FATT_STR_34;Тип:;string</setup>",
    "dia": "<setup>FATT_STR_33;DIA:;string</setup>",
    "model": "<setup>FATT_STR_36;Модель:;string</setup>",
    "brand_known": "<setup>FMANUFACTURER;Все бренды:;string</setup>",
    "brand_known_copy": "<setup>FATT_STR_38;Бренд:;string</setup>",
    "seller": "<setup>FATT_STR_61;Продавец:;string</setup>",
    "type_product": "<setup>FATT_STR_24;Вид товара:;string</setup>", # Disk or Shina
}

# encoding='cp1251'
def save_disks_full(disks, path):
    if disks:
        # with open(path,'w', newline='') as csvfile:
        with open(path,'w', newline='', encoding='utf-8') as csvfile:
            # columns = ['title', 'link', 'price', 'annotation', 'title_short']
            columns = list(disks[0].keys())
            columns.sort()
            writer = csv.DictWriter(csvfile, fieldnames=columns, delimiter=';')
            writer.writeheader()
            writer.writerows(disks)  # запись нескольких строк


# encoding='cp1251'
def save_disks_to_elzakaz_csv(disks, path):
    if disks:
        disks_keys = list(disks[0].keys())
        disks_keys.sort()
        header = []
        for k in disks_keys:
            right_name = header_attr_names.get(k, k)
            header.append(right_name)
        with open(path,'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(header)
            for d in disks:
                row = []
                for k in disks_keys:
                    row.append(d[k])
                writer.writerow(row)

# def save_disks_to_elzakaz_csv3(disks, path):
#     if disks:
#         # with open(path,'w', newline='') as csvfile:
#         with open(path,'w', newline='', encoding='utf-8') as csvfile:
#             # columns = ['title', 'link', 'price', 'annotation', 'title_short']
#             writer = csv.DictWriter(csvfile, fieldnames=header, delimiter=';')
#             writer.writeheader()
#             for d in disks:
#                 writer.writerow(d)
#             # запись нескольких строк
#             writer.writerows(disks)

def save_content(c):
    with open("content.html", "w", encoding='utf-8') as f:
        f.write(c)

def open_content():
    with open("content.html", "r", encoding='utf-8') as f:
        # print(f.read())
        return f.read()


# driver = webdriver.Chrome()
# driver.get("https://baza.drom.ru/chita/wheel/disc/new-enkei-66096670.html")
# sleep(2)
# pprint(driver.page_source)
# driver.quit()

if __name__ == '__main__':
    content = get_html(URL)
    save_content(content)
    # content = open_content()
    disks = parse_user_page(content)
    save_disks(disks, 'disks.csv')
    disks_full_info = []
    for disk in disks:
        disk_content = get_disk_page(disk['link'])
        add_info = parse_disk_page(disk_content, disk['price'])
        disk.update(add_info)
        disks_full_info.append(disk)

    save_disks_full(disks, 'disks_full.csv')
    pprint(disks_full_info)