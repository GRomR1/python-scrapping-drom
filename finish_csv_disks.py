from main3 import *

import re


def open_full_info(path):
    d = []
    with open(path, newline='') as csvfile:
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
                "seller": row['seller'],
            })
    return d


def fix_title(t):
    res = re.sub(r"new!?", '', t, flags=re.IGNORECASE).strip()
    res = re.sub(r"((R\d\d)|(\d\dR)|(\d\d\")).*", '', t).strip()
    res = re.sub(r"te37", 'TE37', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"te37sl", 'TE37 SL', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"te37v", 'TE37 V', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"vps 303", 'VPS303', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"Type-c", 'Type C', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"A1\.", 'А1', res).strip()
    res = re.sub(r"work", 'Work', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"weds", 'Weds', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"worx", 'Worx', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"welg", 'Welg', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"разноширок(ие|ий)", '', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"оригинальные|оригинал|культовые|стильные|стиль|style", '', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"хром|бронза\.?|белые\.?", '', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"суперцена", '', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"(комплект дисков)|(пара дисков)|(один диск)|(1\s*диск)|(5\s*дисков)|(\d\s*шт\.?)|комплект", '',
                 res, flags=re.IGNORECASE).strip()
    res = re.sub(r"диски|дисков|диск", '', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"\(реплика\)|реплика|replica", '', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"ВЕС \d(,\d| )?(кг)? (и \d(,\d| )?(кг)?)?", '', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"\(\s*\)", '', res, flags=re.IGNORECASE).strip()
    if re.search(r"(диповые|дип\.*|(ultra deep)|deep)", res, flags=re.IGNORECASE):
        res = re.sub(r"(диповые|дип\.*|(ультра диповые)|диповые|(ultra deep)|deep)", '', res, flags=re.IGNORECASE).strip()
        res += " (диповые)"
    if re.search(r"(гаек|наклад|бампер|порог|обвес|ниппел)", res, flags=re.IGNORECASE):
        res = ''
    return res

def fix_diameter(d):
    res = d.replace("\"", "").strip()
    res = list(map(lambda x: '0' if x == '' else x, res.split("/")))
    return list(map(float, res))

def fix_width(w):
    res = w.replace("\"", "").strip()
    res = list(map(lambda x: '0' if x == '' else x, res.split("/")))
    return list(map(float, res))

def fix_et(et):
    res = et.replace("мм", "").strip()
    # print(res, res.split("/"))
    res = list(map(lambda x: '0' if x == '' else x, res.split("/")))
    # print(res, list(map(float, res)))
    return list(map(float, res))

def fix_dia(d):
    res = d.replace("мм.", "").strip()
    res = res.replace(",", ".").strip()
    res = list(map(lambda x: '0' if x == '' else x, res.split("/")))
    return list(map(float, res))

def fix_pcd(pcd):
    # print(pcd)
    if pcd:
        res = pcd.split(',')
        res = list(map(lambda x: {"pcd": float(x.split('x')[0]),
                                  "holes": int(x.split('x')[1])}, res))
    else:
        res = [{"pcd": 0.0, "holes": 0}]
    return res

new_disks = []

def devide_disk_parameter(disk, parameter):
    value_list = disk[parameter]
    new_disks = []
    for v in value_list:
        new_disk = disk.copy()
        new_disk[parameter] = v
        new_disks.append(new_disk)
    return new_disks

def devide_disk_pcd(disk):
    value_list = disk['pcd']
    new_disks = []
    # new_disk = disk
    # new_disk.pop('pcd')
    for v in value_list:
        # new_disk['pcd'] = v['pcd']
        # new_disk['holes'] = v['holes']
        # print(v['pcd'], v['holes'])
        new_disks.append({
                "link": disk['link'],
                "price": disk['price'],
                "title": disk['title'],
                "title_short": disk['title_short'],
                "annotation": disk['annotation'],
                "diameter": disk['diameter'],
                "width": disk['width'],
                "et": disk['et'],
                "type": disk['type'],
                "dia": disk['dia'],
                "retail_price": disk['retail_price'],
                "brand": disk['brand'],
                "img": disk['img'],
                "img_full": disk['img_full'],
                "seller": disk['seller'],
                "pcd": v['pcd'],
                'holes': v['holes']
            })
    return new_disks

def update(disk):
    # disk["et"]
    disk["diameter"] = fix_diameter(disk["diameter"])
    disk["width"] = fix_width(disk["width"])
    disk["et"] = fix_et(disk["et"])
    disk["dia"] = fix_dia(disk["dia"])
    disk["pcd"] = fix_pcd(disk["pcd"])
    disk["title_short"] = fix_title(disk["title_short"])
    if not disk["title_short"]:
        return False
    return True

if __name__ == '__main__':
    # disks = open_full_info('Replika777_full_info.csv')
    disks = open_full_info('Aniku_full_info.csv')
    new_disks = []
    for disk in disks:
        if not update(disk):
            continue
        disks1 = devide_disk_parameter(disk, "diameter")
        # pprint(disks1)
        disks2 = []
        for d in disks1:
            disks2.extend(devide_disk_parameter(d, "width"))
        disks3 = []
        for d in disks2:
            disks3.extend(devide_disk_parameter(d, "et"))
        disks4 = []
        for d in disks3:
            disks4.extend(devide_disk_parameter(d, "dia"))
        disks5 = []
        for d in disks4:
            print(d['pcd'])
            disks5.extend(devide_disk_pcd(d))
        new_disks.extend(disks5)
        # print(len(disks5))
        # pprint(disks5)
        # print(len(disks5))

    # pprint(new_disks)
    # print(new_disks)
    print(len(new_disks))

    save_disks_full(new_disks, "simple_disks.csv")