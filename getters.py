"""
Вспомогательные функции для работы с пользователем и получаемой от сервера
информацией.
"""

import datetime
from typing import List


def get_cookie() -> str:
    cookie = input('Введите значение Cookie: ')
    return cookie


def get_date_with_offset(delta: int) -> str:
    """Возвращает дату в формате необходимом для установки в качестве
    параметра url запроса."""
    current_date = datetime.datetime.now()
    gap = datetime.timedelta(days=delta)
    offset_date = current_date - gap
    formatted_date = offset_date.replace(hour=0, minute=0, second=0,
                                         microsecond=0)

    return formatted_date.strftime('%Y-%m-%dT%H:%M:%S.000') + '%2B0300'


def get_last_params() -> tuple:
    answer = input('Желаете ли вы ввести данные предыдущей проверки для '
                   'продолжения (Y/n):')
    if answer.lower()[0] != 'y':
        return '', ''
    last_feed_date = input('Введите дату последней новости в предыдущей '
                           'проверке:')
    last_feed_id = input('Введите id последней новости в предыдущей '
                         'проверке:')
    return last_feed_date, last_feed_id


def get_last_feed_data(data:dict) -> tuple:
    last_feed_date = data.get('date')
    last_feed_date = last_feed_date[:-5] + '%2B0300'
    last_feed_id = data.get('id')
    return last_feed_date, last_feed_id


def get_attachments_url(attachments: List[dict]):
    for attachment in attachments:
        if 'pdf' in attachment.get('fileName'):
            file_id = attachment.get('attachmentId')
            file_link = (f'https://www.gosuslugi.ru/api/lk/geps/file'
                         f'/download/{file_id}?inline=false')
            return file_link
    return 'link not found'
