import datetime
from time import sleep
from typing import List

import requests

from settings import URL, SEARCH_SENDER, SEARCH_WORD, SEARCH_DEBTOR


def get_incoming_document(doc_id: str, headers):
    document_url = URL + doc_id
    incoming_document_request = requests.get(url=document_url, headers=headers)
    if incoming_document_request.status_code != 200:
        raise Exception(f'Документ {doc_id} не загружен, ответ сервера '
                        f'{incoming_document_request.status_code}')
    incoming_document_json = incoming_document_request.json()
    if SEARCH_DEBTOR in incoming_document_json.get('detail').get(
            'addParams').get('DbtrName'):
        file_id = incoming_document_json.get('detail').get('messages')[0].get('attachments')[1].get('attachmentId')
        file_link = f'https://www.gosuslugi.ru/api/lk/geps/file/download/{file_id}?inline=false'
        file_request = requests.get(url=file_link, headers=headers)
        if file_request.status_code == 200:
            with open(f'downloads/{file_id}.pdf', 'wb') as f:
                f.write(file_request.content)
                print('File saved')
        else:
            raise Exception(
                f'Ошибка при загрузке файла, ответ сервера {file_request.status_code}')


def check_feeds(data: List[dict], headers: dict):
    for element in data:
        sender_name = element.get('title')
        document_name = element.get('subTitle')
        if sender_name.lower() == SEARCH_SENDER and SEARCH_WORD in document_name.lower():
            feed_id = str(element.get('id'))
            get_incoming_document(feed_id, headers)


def get_feeds(url_feed, cookie, date_end_check, last_feed_date='',
              type_feed='') -> None:
    headers = {
        'Cookie': cookie
    }

    url = url_feed + f'?types={type_feed}&lastFeedDate={last_feed_date}'

    feed_request = requests.get(url=url, headers=headers)
    if feed_request.status_code != 200:
        raise Exception('Код не 200')
    feeds = feed_request.json().get('items')
    for i in feeds:
        print(i)
    check_feeds(feeds, headers)
    last_feed_in_json = feeds.pop().get('date')
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
