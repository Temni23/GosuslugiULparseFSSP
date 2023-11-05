import datetime
from time import sleep
from typing import List

import requests

from email_utils import send_ticket_to_user
from settings import URL, SEARCH_SENDER, SEARCH_WORD, SEARCH_DEBTOR, \
    EMAIL_TARGET, SEND_EMAIL, RE_REQUESTS


def save_downloaded_pdf(file, file_id):
    with open(f'downloads/{file_id}.pdf', 'wb') as file_pdf:
        # TODO Добавить в путь дату
        file_pdf.write(file)
        print(f'File {file_id} saved successful')


def get_incoming_document(doc_id: str, headers):
    document_url = URL + doc_id
    sleep(2)
    incoming_document_request = requests.get(url=document_url, headers=headers)
    if incoming_document_request.status_code != 200:
        raise Exception(f'Документ {doc_id} не загружен, ответ сервера '
                        f'{incoming_document_request.status_code}')
    incoming_document_json = incoming_document_request.json()
    debtor_name = incoming_document_json.get('detail').get(
        'addParams').get('DbtrName')
    if debtor_name and SEARCH_DEBTOR in debtor_name:
        # file_id = incoming_document_json.get('detail').get('messages')[0].get(
        #     'attachments')[0].get('attachmentId') # TODO Проверить json
        attachments = incoming_document_json.get('detail').get('messages')[
            0].get(
            'attachments')
        for attachment in attachments:
            if 'pdf' in attachment.get('fileName'):
                file_id = attachment.get('attachmentId')
                file_link = f'https://www.gosuslugi.ru/api/lk/geps/file/download/{file_id}?inline=false'
                file_request = requests.get(url=file_link, headers=headers)
                if file_request.status_code == 200:
                    save_downloaded_pdf(file_request.content, file_id)
                    if SEND_EMAIL:
                        send_ticket_to_user(file_request.content, EMAIL_TARGET)
                else:
                    print(
                        f'Ошибка при загрузке файла id {file_id}, ответ сервера '
                        f'{file_request.status_code}') # TODO Добавить
                    # повторный вызов
                    reuse = input('Попробовать еще раз? (Да/Нет)')
                    if reuse.lower() == 'да':
                        get_incoming_document(doc_id=doc_id, headers=headers)


def check_feeds(data: List[dict], headers: dict):
    for element in data:
        sender_name = element.get('title')
        document_name = element.get('subTitle')
        if (sender_name.lower() == SEARCH_SENDER
                and SEARCH_WORD in document_name.lower()):
            feed_id = str(element.get('id'))
            get_incoming_document(feed_id, headers)
            # TODO Возвращать список с айдишками


def get_feeds(url_feed, cookie, date_end_check, last_feed_date='',
              type_feed='', request_count=0, result=[]) -> list:
    headers = {
        'Cookie': cookie
    }

    url = url_feed + f'?types={type_feed}&lastFeedDate={last_feed_date}'

    feed_request = requests.get(url=url, headers=headers)
    if feed_request.status_code == 504 and request_count < RE_REQUESTS:
        request_count += 1
        sleep(20)
        print(f'Try to request feeds # {request_count + 1}')
        get_feeds(url_feed=url_feed, cookie=cookie,
                  date_end_check=date_end_check, last_feed_date=last_feed_date,
                  type_feed=type_feed, request_count=request_count)
    elif feed_request.status_code != 200:
        raise Exception(
            f'При попытке загрузить новости получен код '
            f'{feed_request.status_code}')
    try:
        feeds = feed_request.json().get('items')
    except Exception as e:
        print(feed_request, feed_request.status_code, feed_request.text)
        raise Exception(f'Ошибка при получении новостей {e}')
    result.extend(feeds)
    print(f'Работаю, собрано {len(result)} новостей')
    last_feed_in_json = feeds.pop().get('date')
    more_feeds = feed_request.json().get('hasMore')
    if more_feeds and last_feed_in_json > date_end_check:
        last_feed_in_json = last_feed_in_json[:-5] + '%2B0300'
        sleep(3)
        get_feeds(url_feed=URL, cookie=cookie, date_end_check=date_end_check,
                  last_feed_date=last_feed_in_json, result=result)
    return result


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
