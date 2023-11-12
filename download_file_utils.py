import datetime
import os.path

import requests

from email_utils import send_vip_to_user
from settings import SEND_EMAIL, EMAIL_TARGET


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
