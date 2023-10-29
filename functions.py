import datetime
from time import sleep
from typing import List

import requests

from settings import URL


def check_feeds(data: List[dict]):
    pass


def get_feeds(url_feed, cookie, date_end_check, last_feed_date='',
              type_feed='') -> None:
    headers = {
        'Cookie': cookie
    }

    url = url_feed + f'?types={type_feed}&lastFeedDate={last_feed_date}'

    feed_request = requests.get(url=url, headers=headers)
    feeds = feed_request.json().get('items')
    for i in feeds:
        print(i)
    check_feeds(feeds)
    last_feed_in_json = feeds[19].get('date')
    more_feeds = feed_request.json().get('hasMore')
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
