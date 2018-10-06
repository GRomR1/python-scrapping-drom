from main3 import *



def open_full_info(path):
    d = []
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        # print(reader.fieldnames)
        for row in reader:
            print(row['annotation'], type(row['annotation']))
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


def fix_diameter(d):
    res = d.replace("\"", "").strip()
    res = list(map(lambda x: int('0') if x == '' else int(x), res.split("/")))
    return list(map(float, res))

def fix_width(w):
    res = w.replace("\"", "").strip()
    res = list(map(lambda x: '0' if x == '' else x, res.split("/")))
    return list(map(float, res))

def fix_et(et):
    res = et.replace("мм", "").strip()
    res = list(map(lambda x: '0' if x == '' else x, res.split("/")))
    return list(map(float, res))

def fix_dia(d):
    res = d.replace("мм.", "").strip()
    res = res.replace(",", ".").strip()
    res = list(map(lambda x: '0' if x == '' else x, res.split("/")))
    return list(map(float, res))

def fix_pcd(pcd):
    res = pcd.split(',')
    return list(map(lambda x: {"pcd": float(x.split('x')[0]),
                               "holes": int(x.split('x')[1])},
                res))

def update(disk):
    # disk["et"]
    disk["diameter"] = fix_diameter(disk["diameter"])
    disk["width"] = fix_width(disk["width"])
    disk["et"] = fix_et(disk["et"])
    disk["dia"] = fix_dia(disk["dia"])
    disk["pcd"] = fix_pcd(disk["pcd"])

    # return None

if __name__ == '__main__':
    disks = open_full_info('Replika777_full_info_10.csv')
    new_disks = []
    for disk in disks:
        update(disk)
        new_disks.append(disk)
    pprint(new_disks)