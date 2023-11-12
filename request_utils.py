from time import sleep
from typing import List

import requests

from download_file_utils import download_pdf
from settings import (URL, SEARCH_SENDER, SEARCH_WORD, RE_REQUESTS_SERVER,
                      REQUEST_SLEEP_TIME, TRIGGER_TO_EMAIL)


def get_incoming_document(docs_id: list, headers: dict) -> List:
    """Получает входящие документы из списка id. Проверяет по заданным
    словам, вызывает функцию для загрузки PDF, если поиск успешен."""
    result = []
    for doc_id in docs_id:
        document_url = URL + doc_id
        sleep(2)
        incoming_document_request = request_to_server(url=document_url,
                                                      headers=headers)
        if incoming_document_request.status_code != 200:
            raise Exception(f'Документ {doc_id} не загружен, ответ сервера '
                            f'{incoming_document_request.status_code}')
        incoming_document_json = incoming_document_request.json()
        result.append(incoming_document_json)
        print(f'Собрано {len(result)} уведомлений о Возбуждении ИП')
        debtor_name = incoming_document_json.get('detail').get(
            'addParams').get('DbtrName')
        if debtor_name and TRIGGER_TO_EMAIL in debtor_name.lower():
            attachments = incoming_document_json.get('detail').get('messages')[
                0].get(
                'attachments')
            download_pdf(attachments, headers)

    return result


def check_feeds(data: List[dict]) -> list:
    """Проверяет входящие уведомления по заданным параметрам. Возвращает
    список id документов, для которых проверка дала положительный результат"""
    target_feeds_id = []
    for element in data:
        sender_name = element.get('title')
        document_name = element.get('subTitle')
        if (sender_name.lower() == SEARCH_SENDER
                and SEARCH_WORD in document_name.lower()):
            feed_id = str(element.get('id'))
            target_feeds_id.append(feed_id)
    return target_feeds_id


def get_feeds(url_feed, cookie, date_end_check, last_feed_date='',
              type_feed='', last_feed_id='', result=[]) -> list:
    """Получает входящие уведомления, список словарей, сформированных из
    json входящих уведомлений."""
    headers = {
        'Cookie': cookie
    }

    url = url_feed + (
        f'?unread=false&isArchive=false&isHide=false&types='
        f'{type_feed}&pageSize=20&lastFeedId={last_feed_id}'
        f'&lastFeedDate={last_feed_date}')

    feed_request = request_to_server(url, headers)

    feeds = feed_request.json().get('items')
    result.extend(feeds)
    print(f'Работаю, собрано {len(result)} новостей')
    more_feeds = feed_request.json().get('hasMore')
    last_feed = feeds.pop()
    last_feed_date = last_feed.get('date')
    last_feed_id = last_feed.get('id')
    if more_feeds and last_feed_date > date_end_check:
        last_feed_in_json = last_feed_date[:-5] + '%2B0300'
        sleep(3)
        get_feeds(url_feed=URL, cookie=cookie,
                  date_end_check=date_end_check,
                  last_feed_date=last_feed_in_json,
                  last_feed_id=last_feed_id, result=result,
                  type_feed=type_feed)

    return result


def request_to_server(url: str, headers: dict, request_count: int = 1):
    response = None
    for retry in range(RE_REQUESTS_SERVER):
        try:
            response = requests.get(url=url, headers=headers)
            if response.status_code == 200:
                return response
        except (requests.exceptions.RequestException, ConnectionError) as e:
            print(f'Error during request to server: {e}')
        sleep(REQUEST_SLEEP_TIME)
        print(f'Retry request attempt #{retry + 1}')

    if response is not None:
        raise Exception(
            f'Failed to retrieve information from the server. '
            f'Last status code: {response.status_code}')
    else:
        print('All retry attempts failed. No response received.')
