"""
Содержит функции для работы с сервером ГУ и обработкой полученных ответов.
"""
from time import sleep
from typing import List
import random

import requests

from getters import get_last_feed_data
from settings import (URL, SEARCH_SENDER, RE_REQUESTS_SERVER,
                      REQUEST_SLEEP_TIME)


def get_incoming_document(docs_id: list, headers: dict) -> List:
    """Получает входящие документы из списка id. Проверяет по заданным
    словам, вызывает функцию для загрузки PDF, если поиск успешен."""
    result = []
    for doc_id in docs_id:
        document_url = URL + doc_id
        sleep(random.uniform(0, 2))
        incoming_document_request = request_to_server(url=document_url,
                                                      headers=headers)
        if incoming_document_request:
            # print(f'Документ {doc_id} не загружен, ответ сервера '
            #       f'{incoming_document_request.status_code} '
            #       f'Проверка не завершена в полном объеме, попробуйте '
            #       f'перезапустить используя данные последней новости')
            # return result
            incoming_document_json = incoming_document_request.json()
            result.append(incoming_document_json)
            print(f'Собрано {len(result)} уведомлений от Портала Госуслуги')

    return result


def check_feeds(data: List[dict]) -> list:
    """Проверяет входящие уведомления по заданным параметрам. Возвращает
    список id документов, для которых проверка дала положительный результат"""
    target_feeds_id = []
    for element in data:
        sender_name = element.get('title')
        if sender_name.lower() == SEARCH_SENDER:
            feed_id = str(element.get('id'))
            target_feeds_id.append(feed_id)
    return target_feeds_id


def get_feeds(url_feed: str, headers: dict, date_end_check: str,
              last_feed_date='', type_feed='', last_feed_id='') -> list:
    """Получает входящие уведомления, список словарей, сформированных из
    json входящих уведомлений."""

    result = []

    while True:
        url = url_feed + (
            f'?unread=false&isArchive=false&isHide=false&types='
            f'{type_feed}&pageSize=20&lastFeedId={last_feed_id}'
            f'&lastFeedDate={last_feed_date}')

        feed_request = request_to_server(url, headers)

        feeds = feed_request.json().get('items')
        result.extend(feeds)
        print(f'Работаю, собрано {len(result)} новостей')
        more_feeds = feed_request.json().get('hasMore')
        try:
            last_feed = feeds.pop()
        except Exception:
            print(feeds)
            raise Exception('Ошибка при получении последней новости')
        if not last_feed:
            break
        last_feed_date, last_feed_id = get_last_feed_data(last_feed)
        if not more_feeds or last_feed_date <= date_end_check:
            break
        sleep(random.uniform(0, 2))

    return result


def request_to_server(url: str, headers: dict):
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

        if response.status_code in [404, 401]:
            print(f'Status code {response.status_code} url = {url}')
            return False

    if response is not None:
        raise Exception(
            f'Failed to retrieve information from the server. '
            f'Last status code: {response.status_code}')
    else:
        print('All retry attempts failed. No response received.')
