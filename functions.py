import requests

from settings import URL, TYPE_FEED


def get_feeds(url_feed, type_feed, cookie, start_date='') -> dict:
    headers = {
        'Cookie': cookie
    }
    params = {
        'types': type_feed,
        'startDate': start_date
    }

    r = requests.get(url=url_feed, headers=headers, params=params)
    items = r.json().get('items')
    return items


def get_cookie() -> str:
    cookie = input('Введите значение Cookie: ')
    return cookie
