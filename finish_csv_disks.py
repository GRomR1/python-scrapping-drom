from main3 import *
from fix_params import *
from image_processor import add_watermark_to_image

from collections import OrderedDict
from itertools import groupby
import re
import shutil
import requests
import os

def open_full_info(path):
    d = []
    # with open(path, newline='', encoding='cp1251') as csvfile:
    with open(path, newline='', encoding='cp1251') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        # print(reader.fieldnames)
        for row in reader:
            # print(row['annotation'], type(row['annotation']))
            d.append({
                "link": row['link'],
                "price": row['price'],
                "title": row['title'],
                "title_short": row['title_short'],
                "annotation": row['annotation'],
                "diameter": row['diameter'],
                "width": row['width'],
                "et": row['et'],
                "pcd": row['pcd'],
                "type": row['type'],
                "dia": row['dia'],
                "retail_price": row['retail_price'],
                "brand": row['brand'],
                "img": row['img'],
                "img_full": row['img_full'],
                # "img_links": row['img_links'],
                "seller": row['seller'],
            })
    return d

# new_disks = []

def devide_disk_parameter(disk, parameter):
    new_disks = []
    new_disk = disk.copy()
    if parameter != 'pcd':
        value_list = disk[parameter]
        for v in value_list:
            new_disk[parameter] = v
            new_disks.append(new_disk.copy())
    else:
        value_list = disk['pcd'].copy()
        new_disk.pop('pcd')
        for v in value_list:
            new_disk['pcd'] = v['pcd']
            new_disk['holes'] = v['holes']
            new_disks.append(new_disk.copy())
            # print(v['pcd'], v['holes'])
    return new_disks.copy()




def update(disk):
    # disk["et"]
    disk["retail_price_one"], disk["count"] = fix_price(disk["retail_price"], disk["title_short"])
    # print(disk["retail_price_one"], type(disk["retail_price_one"]))
    disk["diameter"] = fix_diameter(disk["diameter"])
    disk["width"] = fix_width(disk["width"])
    disk["et"] = fix_et(disk["et"])
    disk["dia"] = fix_dia(disk["dia"])
    disk["pcd"] = fix_pcd(disk["pcd"])
    title_short = fix_title(disk["title"])
    # print(title_short)
    disk["title_short"] = title_short
    brand_known = fix_brand(disk["brand"])
    brand_known = brand_known[0] if brand_known else ''
    # print("brand_known", disk["brand"], brand_known)
    disk["brand_known"] = brand_known if brand_known else ''
    disk["brand_known_copy"] = brand_known if brand_known else ''
    disk["type_product"] = 'Disk'
    disk["model"] = fix_model(title_short, brand_known) if title_short and brand_known else title_short
    # все что в скобка в обновленном заголовке выносим в поле дополнительно - "add_info"
    add_info = title_short[title_short.find('('):] if title_short.find('(') != -1 else ''
    disk["add_info"] = ' '.join(add_info.split())
    if not title_short:
        return False
    return True

def devide_disk_parameters(disk):
    disks1 = devide_disk_parameter(disk, "diameter")
    disks2 = []
    for d in disks1:
        disks2.extend(devide_disk_parameter(d, "width").copy())
    disks3 = []
    for d in disks2:
        disks3.extend(devide_disk_parameter(d, "et").copy())
    disks4 = []
    for d in disks3:
        disks4.extend(devide_disk_parameter(d, "dia").copy())
    disks5 = []
    for d in disks4:
        disks5.extend(devide_disk_parameter(d, "pcd").copy())
    for d in disks5:
        d["name_product"] = re.sub(r"\s+", ' ', fix_name_product(d)).strip()
        d["short_name"] = re.sub(r"\s+", ' ', fix_short_name_product(d)).strip()
    return disks5.copy()


def download_image(code, img_url):
    try:
        file_path = 'product_images/{}.jpg'.format(code)
        if img_url:
            if not os.path.exists(file_path):
                response = requests.get(img_url, stream=True)
                with open(file_path, 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                del response
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # disks = open_full_info('Replika777_full_info_10.csv')
    disks = open_full_info('WorldWheels_full_info.csv') # 307 дисков в итоге
    new_disks = []
    for disk in disks:
        if not update(disk):
            continue
        new_disks.extend(devide_disk_parameters(disk))
    # print(len(new_disks))

    disks = open_full_info('Aniku_full_info.csv') # 1425 дисков в итоге
    for disk in disks:
        if not update(disk):
            continue
        new_disks.extend(devide_disk_parameters(disk))
    # print(len(new_disks))

    disks = open_full_info('Replika777_full_info.csv') # 1831 дисков в итоге
    for disk in disks:
        if not update(disk):
            continue
        new_disks.extend(devide_disk_parameters(disk))
    print(len(new_disks))
    del disks

    start_code = 40000
    prod_names = []
    brands = []
    brands_model = []
    for d in new_disks:
        start_code += 1
        d['code'] = start_code

        prod_names.append(d['name_product'])
        brands.append(d['brand_known'])
        brands_model.append("{} {}".format(d['brand_known'], d['model']))
        # download_image(d['code'], d["img_full"])
        # add_watermark_to_image(d['code'])

    # save_disks_full(new_disks, "simple_disks2.csv")

    new_prod_names = list(OrderedDict.fromkeys(prod_names))
    new_brands = list(OrderedDict.fromkeys(brands))
    new_brands_model = list(OrderedDict.fromkeys(brands_model))
    new_brands.sort()
    new_brands_model.sort()
    # pprint(new_brands)
    print("Всего товаров {}. Из них дублей {}".format(len(prod_names), len(prod_names)-len(new_prod_names)))  # 1831 906
    print("Всего брендов {}. Из них дублей {}".format(len(brands), len(brands)-len(new_brands)))  # 1831 1787
    print("Всего моделей {}. Из них дублей {}".format(len(brands_model), len(brands_model)-len(new_brands_model)))  # 1831 1651

    # save_disks_to_elzakaz_csv(new_disks, "simple_disks3.csv")