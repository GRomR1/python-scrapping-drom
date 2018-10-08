from main3 import *

import re


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
                "seller": row['seller'],
            })
    return d

brands = read_brands()

def fix_brand(b):
    res = re.sub(r"\(реплика\)|реплика|replica", '', b, flags=re.IGNORECASE).strip()
    res = re.sub(r".*volk racing", 'Volk Racing', res, flags=re.IGNORECASE).strip()
    known_brand = list(filter(lambda x: re.match(x, res, flags=re.IGNORECASE), brands))
    return known_brand

def fix_model(t, b):
    res = re.sub(r"\(.*\)", '', t, flags=re.IGNORECASE).strip()
    res = res.replace('\\', '').strip()
    res = res.replace('/', '').strip()
    res = re.sub(r"{}".format(b.replace('.', '\.')), '', res, flags=re.IGNORECASE).strip()
    # print(t, b, res)
    res = re.sub(r"racing", '', res, flags=re.IGNORECASE).strip()
    model = res
    return model

def fix_title(t):
    res = re.sub(r"new!?|новы[ехй]!?|новинка!?", '', t, flags=re.IGNORECASE).strip()
    res = re.sub(r"(sale|скидка|суперцена)!?", '', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"(летняя|осенняя|зимняя|весенняя)!?", '', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"((R\d\d)|(\d\dR)|(\d\d\")).*", '', res).strip()
    res = re.sub(r"te37", 'TE37', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"te37sl", 'TE37 SL', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"te37v", 'TE37 V', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"vps 303", 'VPS303', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"Type-c", 'Type C', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"A1\.", 'А1', res).strip()
    res = re.sub(r"ADV\d.1", 'АDV.1', res).strip()
    res = re.sub(r"work", 'Work', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"Advan racing", 'Advan', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"CR-Kiwami", 'CR Kiwami', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"TUFF A.\s+T.", 'Tuff A.T.', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"B-R", 'Black Rhino', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"weds", 'Weds', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"worx", 'Worx', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"welg", 'Welg', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"разноширок(ие|ий)", '', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"разновыносн(ой|ые)", '', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"оригинальные|оригинал|культовые|эксклюзивные|эксклюзив|стильные|злые|топовые|стиль|ультра|style|ьные|ные",
                 '', res, flags=re.IGNORECASE).strip()
    # res = re.sub(r"|белые\.?", '', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"(комплект\s+дисков)|(пара\s+дисков)|пара!?|(один\s+диск)|(1\s*диск)|(5\s*дисков)|(\d\s*шт\.?)|комплект", '',
                 res, flags=re.IGNORECASE).strip()
    res = re.sub(r"диски|дисков|диск", '', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"реплика|replica|аналог", '', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"ВЕС \d(,\d)?\s*(кг)?\s*(и\s*\d(,\d)?\s*(кг)?)?", '', res, flags=re.IGNORECASE).strip()
    if re.search(r"штат(ные)?\s+для\s+", res, flags=re.IGNORECASE):
        res = re.sub(r"штат(ные)?\s+для\s+", '', res, flags=re.IGNORECASE).strip()
        res += " (штатные)"
    if re.search(r"chrome|хром", res, flags=re.IGNORECASE):
        res = re.sub(r"chrome|хром", '', res, flags=re.IGNORECASE).strip()
        res += " (хром)"
    if re.search(r"red|красные", res, flags=re.IGNORECASE):
        res = re.sub(r"red|красные", '', res, flags=re.IGNORECASE).strip()
        res += " (красные)"
    if re.search(r"gold|золотые|золото", res, flags=re.IGNORECASE):
        res = re.sub(r"gold|золотые|золото", '', res, flags=re.IGNORECASE).strip()
        res += " (золотые)"
    if re.search(r"white|белые\.?", res, flags=re.IGNORECASE):
        res = re.sub(r"white|белые", '', res, flags=re.IGNORECASE).strip()
        res += " (белые)"
    if re.search(r"бронза\.?|bronze", res, flags=re.IGNORECASE):
        res = re.sub(r"бронза\.?|bronze", '', res, flags=re.IGNORECASE).strip()
        res += " (бронза)"
    if re.search(r"h.per black", res, flags=re.IGNORECASE):
        res = re.sub(r"h.per black", '', res, flags=re.IGNORECASE).strip()
        res += " (насыщенный черный)"
    if re.search(r"machined", res, flags=re.IGNORECASE):
        res = re.sub(r"machined", '', res, flags=re.IGNORECASE).strip()
        res += " (machined)"
    if re.search(r"gun\s*metal", res, flags=re.IGNORECASE):
        res = re.sub(r"gun\s*metal", '', res, flags=re.IGNORECASE).strip()
        res += " (gunmetal)"
    if re.search(r"black|черны[ей]", res, flags=re.IGNORECASE):
        res = re.sub(r"black|черны[ей]", '', res, flags=re.IGNORECASE).strip()
        res += " (черный)"
    if re.search(r"серый|silver", res, flags=re.IGNORECASE):
        res = re.sub(r"серый|silver", '', res, flags=re.IGNORECASE).strip()
        res += " (silver)"
    if re.search(r"h.per", res, flags=re.IGNORECASE):
        res = re.sub(r"h.per", '', res, flags=re.IGNORECASE).strip()
        res += " (насыщенный)"
    if re.search(r"inforged", res, flags=re.IGNORECASE):
        res = re.sub(r"inforged", '', res, flags=re.IGNORECASE).strip()
        res += " (inforged)"
    if re.search(r"((ультра\s*)?диповые|дип\.*|(ultra\s*)?deep)", res, flags=re.IGNORECASE):
        res = re.sub(r"((ультра\s*)?диповые|дип\.*|(ultra\s*)?deep)", '', res, flags=re.IGNORECASE).strip()
        res += " (диповые)"
    if re.search(r"гаек|наклад|бампер|порог|обвес|ниппел", res, flags=re.IGNORECASE):
        res = ''
    res = re.sub(r".*Volk Racing", 'Volk Racing', res, flags=re.IGNORECASE).strip()
    res = re.sub(r".*shogun", 'Shogun', res, flags=re.IGNORECASE).strip()
    res = re.sub(r"\(\s*\)", '', res, flags=re.IGNORECASE).strip()
    # res = re.sub(r"\s+", ' ', res, flags=re.IGNORECASE).strip()
    res = ' '.join(res.split())
    res = res.replace('\\', '').strip()
    res = res.replace('/', '').strip()
    res = res.replace('!', '').strip()
    return res

def fix_diameter(d):
    res = d.replace("\"", "").strip()
    res = list(map(lambda x: '0' if x == '' else x, res.split("/")))
    return list(map(int, res))

def fix_width(w):
    res = w.replace("\"", "").strip()
    res = list(map(lambda x: '0' if x == '' else x, res.split("/")))
    return list(map(float, res))

def fix_et(et):
    res = et.replace("мм", "").strip()
    # print(res, res.split("/"))
    res = list(map(lambda x: '0' if x == '' else x, res.split("/")))
    # print(res, list(map(float, res)))
    return list(map(int, res))

def fix_price(p, t):
    if re.search(r"(один диск)|(1\s*диск)|(1\s*шт)", t, flags=re.IGNORECASE):
        return int(p)
    if re.search(r"(пара дисков)|пара|(2\s*диска)|(2\s*шт)", t, flags=re.IGNORECASE):
        return int(int(p) / 2)
    if re.search(r"(пять дисков)|(5\s*дисков)|(5\s*шт)", t, flags=re.IGNORECASE):
        return int(int(p) / 5)
    return int(int(p) / 4)

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
    new_disks = []
    new_disk = disk.copy()
    if parameter != 'pcd':
        value_list = disk[parameter]
        for v in value_list:
            new_disk[parameter] = v
            new_disks.append(new_disk)
    else:
        value_list = disk['pcd'].copy()
        new_disk.pop('pcd')
        for v in value_list:
            new_disk['pcd'] = v['pcd']
            new_disk['holes'] = v['holes']
            new_disks.append(new_disk)
            # print(v['pcd'], v['holes'])
    return new_disks.copy()

def update(disk):
    # disk["et"]
    disk["retail_price_one"] = fix_price(disk["retail_price"], disk["title_short"])
    # print(disk["retail_price_one"], type(disk["retail_price_one"]))
    disk["diameter"] = fix_diameter(disk["diameter"])
    disk["width"] = fix_width(disk["width"])
    disk["et"] = fix_et(disk["et"])
    disk["dia"] = fix_dia(disk["dia"])
    disk["pcd"] = fix_pcd(disk["pcd"])
    title_short = fix_title(disk["title"])
    title_short = re.sub(r"\s+", ' ', title_short).strip()
    # print(title_short)
    disk["title_short"] = title_short
    brand_known = fix_brand(disk["brand"])
    brand_known = brand_known[0] if brand_known else ''
    # print("brand_known", disk["brand"], brand_known)
    disk["brand_known"] = brand_known if brand_known else ''
    # disk.insert("brand_known", brand_known[0] if brand_known else '')
    disk["model"] = fix_model(title_short, brand_known) if title_short and brand_known else title_short
    if not title_short:
        return False
    return True

def fix_name_product(d):
    name_template = '' # '{w}x{R}", {h}x{pcd}, ET{et}, ЦО{dia} {b} {m}'
    if d["width"] != 0 and d["diameter"] != 0:
        name_template += '{w}x{R}", '
    if d["holes"] != 0 and d["pcd"] != 0:
        name_template += '{h}x{pcd}, '
    if d["et"] != 0:
        name_template += 'ET{et}, '
    if d["dia"] != 0:
        name_template += 'ЦО{dia} '
    if d["brand_known"]:
        name_template += '{b} '
    if d["model"]:
        name_template += '{m} '

    return name_template.format(
        w=d["width"],
        R=d["diameter"],
        h=d["holes"],
        pcd=d["pcd"],
        et=d["et"],
        dia=d["dia"],
        b=d["brand_known"],
        m=d["model"]
    )

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
        d["name_product"] = fix_name_product(d)
    return disks5.copy()

if __name__ == '__main__':
    # disks = open_full_info('Replika777_full_info_10.csv')
    disks = open_full_info('WorldWheels_full_info.csv') # 307 дисков в итоге
    new_disks = []
    for disk in disks:
        if not update(disk):
            continue
        new_disks.extend(devide_disk_parameters(disk))
    print(len(new_disks))

    disks = open_full_info('Aniku_full_info.csv') # 1425 дисков в итоге
    for disk in disks:
        if not update(disk):
            continue
        new_disks.extend(devide_disk_parameters(disk))
    print(len(new_disks))

    disks = open_full_info('Replika777_full_info.csv') # 1831 дисков в итоге
    for disk in disks:
        if not update(disk):
            continue
        new_disks.extend(devide_disk_parameters(disk))
    print(len(new_disks))

    save_disks_full(new_disks, "simple_disks2.csv")