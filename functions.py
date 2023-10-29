import datetime
import requests


def get_feeds(url_feed, type_feed, cookie, start_date='') -> dict:
    headers = {
        'Cookie': cookie
    }
    params = {
        'types': type_feed,
        'lastFeedDate': start_date
    }

    r = requests.get(url=url_feed, headers=headers, params=params)
    items = r.json().get('items')
    return items


def get_cookie() -> str:
    cookie = input('Введите значение Cookie: ')
    return cookie


def get_date_with_offset(delta):
    current_date = datetime.datetime.now()
    gap = datetime.timedelta(days=delta)
    offset_date = current_date - gap
    formatted_date = offset_date.replace(hour=0, minute=0, second=0,
                                         microsecond=0)

    return formatted_date.strftime('%Y-%m-%dT%H:%M:%S.000') + '%2B0300'
