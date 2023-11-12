from time import sleep
from typing import List

import requests

from settings import (URL, SEARCH_SENDER, SEARCH_WORD, RE_REQUESTS,
                      REQUEST_SLEEP_TIME)


def get_incoming_document(docs_id: list, headers: dict) -> List:
    """Получает входящие документы из списка id. Проверяет по заданным
    словам, вызывает функцию для загрузки PDF, если поиск успешен."""
    result = []
    for doc_id in docs_id:
        document_url = URL + doc_id
        sleep(2)
        incoming_document_request = requests.get(url=document_url,
                                                 headers=headers)
        if incoming_document_request.status_code != 200:
            raise Exception(f'Документ {doc_id} не загружен, ответ сервера '
                            f'{incoming_document_request.status_code}')
        incoming_document_json = incoming_document_request.json()
        result.append(incoming_document_json)
        print(f'Собрано {len(result)} уведомлений о Возбуждении ИП')
        debtor_name = incoming_document_json.get('detail').get(
            'addParams').get('DbtrName')
        # if debtor_name and 'росттех' in debtor_name:
        #     attachments = incoming_document_json.get('detail').get('messages')[
        #         0].get(
        #         'attachments')
        #     pdf = download_pdf(attachments, headers)
        #     send_vip_to_user(pdf, )
        # TODO Перекрутить в проверку
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
              type_feed='', last_feed_id='',
              request_count=0, result=[]) -> list:
    """Получает входящие уведомления, список словарей, сформированных из
    json входящих уведомлений."""
    headers = {
        'Cookie': cookie
    }

    url = url_feed + (f'?unread=false&isArchive=false&isHide=false&types={type_feed}&pageSize=&lastFeedId={last_feed_id}'
                      f'&lastFeedDate={last_feed_date}')

    feed_request = requests.get(url=url, headers=headers)
    if feed_request.status_code != 200 and request_count < RE_REQUESTS:
        request_count += 1
        sleep(REQUEST_SLEEP_TIME)
        print(f'Try to request feeds # {request_count + 1}')
        get_feeds(url_feed=url_feed, cookie=cookie,
                  date_end_check=date_end_check, last_feed_date=last_feed_date,
                  type_feed=type_feed, request_count=request_count,
                  last_feed_id=last_feed_id)
    elif feed_request.status_code != 200:
        raise Exception(
            f'При попытке загрузить новости получен код '
            f'{feed_request.status_code}')

    if feed_request.status_code == 200:
        feeds = feed_request.json().get('items')
        for _ in feeds:
            print(_)
        result.extend(feeds)
        print(f'Работаю, собрано {len(result)} новостей')
        last_feed = feeds.pop()
        last_feed_in_json = last_feed.get('date')
        more_feeds = feed_request.json().get('hasMore')
        last_feed_id = last_feed.get('id')
        print(last_feed_id)
        print(last_feed_in_json)
        if more_feeds and last_feed_in_json > date_end_check:
            last_feed_in_json = last_feed_in_json[:-5] + '%2B0300'
            sleep(3)
            get_feeds(url_feed=URL, cookie=cookie,
                      date_end_check=date_end_check,
                      last_feed_date=last_feed_in_json,
                      last_feed_id=last_feed_id, result=result)
    else:
        pass
    return result
