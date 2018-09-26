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


def update(disk):
    # disk["et"]
    return None

if __name__ == '__main__':
    disks = open_full_info('Replika777_full_info.csv')
    pprint(disks)