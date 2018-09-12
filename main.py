from bs4 import BeautifulSoup
import pprint
import requests

user_id = 'Replika777'
url = 'https://baza.drom.ru/user/{}'.format(user_id) # url для второй страницы
r = requests.get(url)
html_doc = r.text.encode('cp1251')
soup = BeautifulSoup(html_doc, 'html.parser')

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