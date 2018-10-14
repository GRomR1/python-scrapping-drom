import re


# read_brands()
def read_brands():
    brands = []
    with open("brands.txt", newline='') as fh:
        for brand in fh:
            # print(brand)
            brands.append(brand.strip())
    return brands


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
    res = re.sub(r"^\s*-", ' ', res).strip()
    res = re.sub(r" -", ' ', res).strip()
    res = re.sub(r"\s+", ' ', res).strip()
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
    res = re.sub(r"=-?", '', res).strip()
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
    if re.search(r"h.per black", res, flags=re.IGNORECASE):
        res = re.sub(r"h.per black", '', res, flags=re.IGNORECASE).strip()
        res += " (насыщенный черный)"
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
        return int(p), 1
    if re.search(r"(пара дисков)|пара|(2\s*диска)|(2\s*шт)", t, flags=re.IGNORECASE):
        return int(int(p) / 2), 2
    if re.search(r"(пять дисков)|(5\s*дисков)|(5\s*шт)", t, flags=re.IGNORECASE):
        return int(int(p) / 5), 5
    return int(int(p) / 4), 4


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


def fix_short_name_product(d):
    name_template = '' # '{w}x{R}", {h}x{pcd}, ET{et}, ЦО{dia}'
    if d["width"] != 0 and d["diameter"] != 0:
        name_template += '{w}x{R}", '
    if d["holes"] != 0 and d["pcd"] != 0:
        name_template += '{h}x{pcd}, '
    if d["et"] != 0:
        name_template += 'ET{et}, '
    if d["dia"] != 0:
        name_template += 'ЦО{dia} '

    return name_template.format(
        w=d["width"],
        R=d["diameter"],
        h=d["holes"],
        pcd=d["pcd"],
        et=d["et"],
        dia=d["dia"]
    )

def fix_short_description_product(d):
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


def fix_name_product(d):
    name_template = '' # '{w}*{R} {h}*{pcd} ET{et} {dia} {b} {m}'
    if d["width"] != 0 and d["diameter"] != 0:
        name_template += '{w}*{R} '
    if d["holes"] != 0 and d["pcd"] != 0:
        name_template += '{h}*{pcd} '
    if d["et"] != 0:
        name_template += 'ET{et} '
    if d["dia"] != 0:
        name_template += '{dia} '
    if d["brand_known"]:
        name_template += '{b} '
    if d["model"]:
        name_template += '{m} '
    if d["add_info"]:
        name_template += '{add}'

    return name_template.format(
        w=str(d["width"]).replace('.', ','),
        R=d["diameter"],
        h=d["holes"],
        pcd=str(d["pcd"]).replace('.', ','),
        et=d["et"],
        dia=str(d["dia"]).replace('.', ','),
        b=d["brand_known"],
        m=d["model"],
        add=d["add_info"]
    )

