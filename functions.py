import datetime
from time import sleep

import requests

from settings import URL


def get_feeds(url_feed, cookie, date_end_check, last_feed_date='') -> None:
    headers = {
        'Cookie': cookie
    }

    url = url_feed + f'?lastFeedDate={last_feed_date}'

    r = requests.get(url=url, headers=headers)
    items = r.json().get('items')
    for i in items:
        print(i)
    last_feed_in_json = items[19].get('date')
    more_feeds = r.json().get('hasMore')
    if more_feeds and last_feed_in_json > date_end_check:
        last_feed_in_json = last_feed_in_json[:-5] + '%2B0300'
        sleep(3)
        get_feeds(url_feed=URL, cookie=cookie, date_end_check=date_end_check,
                  last_feed_date=last_feed_in_json)


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
