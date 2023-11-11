import datetime
import os.path
from time import sleep
from typing import List

import requests

from email_utils import send_vip_to_user
from settings import (URL, SEARCH_SENDER, SEARCH_WORD, SEARCH_DEBTOR,
                      EMAIL_TARGET, SEND_EMAIL, RE_REQUESTS,
                      REQUEST_SLEEP_TIME)


def save_downloaded_pdf(file, file_id):
    """Сохраняет PDF файл в выбранную папку"""
    today = str(datetime.date.today())
    folder_path = f'downloads/check{today}'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    with open(f'{folder_path}/{file_id}.pdf', 'wb') as file_pdf:
        file_pdf.write(file)
        print(f'File {file_id} saved successfully')


def download_pdf(attachments: list, headers: dict, request_count=1):
    """Скачивает PDF файл"""
    for attachment in attachments:
        if 'pdf' in attachment.get('fileName'):
            file_id = attachment.get('attachmentId')
            file_link = (f'https://www.gosuslugi.ru/api/lk/geps/file'
                         f'/download/{file_id}?inline=false')
            file_request = requests.get(url=file_link, headers=headers)
            if file_request.status_code == 200:
                save_downloaded_pdf(file_request.content, file_id)
                if SEND_EMAIL:
                    send_vip_to_user(file_request.content, EMAIL_TARGET)
            elif request_count < 5:
                request_count += 1
                print(
                    f'Ошибка при загрузке файла id {file_id}, ответ сервера '
                    f'{file_request.status_code}. Пробую {request_count} раз')
                download_pdf(attachments, headers, request_count=request_count)
            else:
                print(
                    f'Ошибка при загрузке файла id {file_id}, ответ сервера '
                    f'{file_request.status_code}. Перехожу к другому файлу.')


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

    url = url_feed + (f'?types={type_feed}&pageSize=15&lastFeedId={last_feed_id}'
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


def get_cookie() -> str:
    cookie = input('Введите значение Cookie: ')
    return cookie


def get_date_with_offset(delta):
    """Возвращает дату в формате необходимом для установки в качестве
    параметра url запроса."""
    current_date = datetime.datetime.now()
    gap = datetime.timedelta(days=delta)
    offset_date = current_date - gap
    formatted_date = offset_date.replace(hour=0, minute=0, second=0,
                                         microsecond=0)

    return formatted_date.strftime('%Y-%m-%dT%H:%M:%S.000') + '%2B0300'


