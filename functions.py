import requests

url = 'https://www.gosuslugi.ru/api/lk/v1/feeds/'
headers = {
    'Cookie': ''
}
params ={
    'types': 'GEPS',
    'startDate': '2023-08-14T00:00:00.000+0300'
}

r = requests.get(url=url, headers=headers, params=params)
items = r.json().get('items')
counter = 0
for i in items:
    if 'Постановление' in i.get('subTitle'):
        print(i)
        counter += 1
        print(counter)
