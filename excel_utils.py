"""
Модуль содержит функции работающие с экселем.
"""
import os
import shutil
from datetime import datetime
from typing import List

import pandas as pd

from email_utils import get_text_for_email, send_email_to_user
from getters import get_attachments_url
from settings import TRIGGER_TO_EMAIL, EMAIL_TARGETS, BACKUP_DIR


def backup_file(file_path: str, backup_dir) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл '{file_path}' не найден, бэкап "
                                f"невозможен.Прерываюсь. Проверьте настройки.")

    os.makedirs(backup_dir, exist_ok=True)
    base_name = os.path.basename(file_path)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f"{os.path.splitext(base_name)[0]}_{timestamp}.xlsx"
    backup_path = os.path.join(backup_dir, backup_name)
    shutil.copy2(file_path, backup_path)
    return backup_path


def extract_message_fields(message: dict, inn: str) -> dict:
    params = message.get('addParams', {})

    return {
        'send_date': message.get('sendDate'),
        'thread_id': message.get('threadId'),
        'subject': message.get('subject'),
        'text': message.get('text'),
        'update_date': message.get('updateDate'),
        'file_link': get_attachments_url(
            message.get('attachments')) if message.get(
            'attachments') else None,
        'IdDocType_text': params.get('IdDocType_text'),
        'IDocSubjExecName': params.get('IDocSubjExecName'),
        'feed_mobtitle': params.get('feed_mobtitle'),
        'NumberDoc': params.get('NumberDoc'),
        'IdDocType_feed': params.get('IdDocType_feed'),
        'RiseDate': params.get('RiseDate'),
        'DocRegDate': params.get('DocRegDate'),
        'CrdrName': params.get('CrdrName'),
        'IDNum': params.get('IDNum'),
        'SupplierOrgName': params.get('SupplierOrgName'),
        'feed_subtitle': params.get('feed_subtitle'),
        'DebtSumTotal': params.get('DebtSumTotal'),
        'DbtrName': params.get('DbtrName'),
        'IDDate': params.get('IDDate'),
        'IDOrganName': params.get('IDOrganName'),
        'PostName': params.get('PostName'),
        'DeloNum': params.get('DeloNum'),
        'DocName': params.get('DocName'),
        'SPIShortName': params.get('SPIShortName'),
        'DateDoc': params.get('DateDoc'),
        'INN': inn,
    }


def process_email_notifications(df: pd.DataFrame, email_targets: List[str]) -> None:
    filtered_df = df[df['DbtrName'].str.lower().str.contains(TRIGGER_TO_EMAIL.lower(), na=False)]

    for _, row in filtered_df.iterrows():
        try:
            text = get_text_for_email(
                row['DbtrName'],
                row['SupplierOrgName'],
                row['NumberDoc'],
                row['IDOrganName'],
                row['IDDate'],
                row['DeloNum'],
                row['DateDoc']
            )
            for email in email_targets:
                send_email_to_user(email, text)
        except Exception as e:
            print(f"[!] Ошибка при формировании или отправке письма: {e}")


def save_messages_to_excel(data_list: List[dict], inn: str,
                           excel_file_path: str) -> pd.DataFrame | bool:
    backup_file(excel_file_path, BACKUP_DIR)
    try:
        existing_data = pd.read_excel(excel_file_path)
    except FileNotFoundError:
        existing_data = pd.DataFrame()

    records = []

    for item in data_list:
        messages = item.get('detail', {}).get('messages', [])
        if not messages:
            continue
        for message in messages:
            message_data = extract_message_fields(message, inn)
            records.append(message_data)

    if records:
        new_data = pd.DataFrame(records)
        combined_data = pd.concat([existing_data, new_data], ignore_index=True)
        # TODO Приведение данных к единым форматам в итоговом файле
        combined_data.drop_duplicates(inplace=True)
        combined_data.to_excel(excel_file_path, index=False)

        return new_data
    return False



# def search_esp_in_messages(file_path: str, date_last_check) -> str or bool:
#     """Принимает путь к файлу с сообщениями сохраняет сообщения об электронных
#     судебных приказах в файл, возвращает путь к этому файлу."""
#     date_last_check = date_last_check[:10].replace('-', '.')
#     date_last_check = datetime.strptime(date_last_check, '%Y.%m.%d')
#     date_last_check = date_last_check.strftime('%d.%m.%Y')
#     current_date = datetime.now()
#     date_string = current_date.strftime('%d-%m-%Y')
#     path_to_esp = 'excel/ESP/' + 'esp_' + date_string + '.xlsx'
#     target_cols = ['IDocSubjExecName', 'NumberDoc', 'DocRegDate', 'CrdrName',
#                    'IDNum',
#                    'SupplierOrgName', 'feed_subtitle', 'DebtSumTotal',
#                    'DbtrName',
#                    'IDDate', 'IDOrganName', 'PostName', 'DeloNum', 'DocName',
#                    'SPIShortName', 'DateDoc']
#     df = pd.read_excel(file_path, usecols=target_cols)
#     df.drop_duplicates(inplace=True)
#     date_last_check_datetime = pd.to_datetime(date_last_check,
#                                               format='%d.%m.%Y')
#     df_vip = df[df['DocName'].isna()].copy()
#     df_vip = df_vip[df_vip['IDNum'].str.contains('#')].copy()
#     dates = df_vip['DateDoc']
#     dates = pd.to_datetime(dates, format='%d.%m.%Y', dayfirst=True)
#     df_vip['DateDoc'] = dates
#     dates = df_vip['DocRegDate']
#     dates = pd.to_datetime(dates)
#     df_vip['DocRegDate'] = dates
#     df_vip = df_vip[df_vip['DateDoc'] >= date_last_check_datetime].copy()
#     df_vip['DateDoc'] = pd.to_datetime(df_vip['DateDoc']).dt.date
#     if len(df_vip) > 0:
#         df_vip.to_excel(path_to_esp, index=False)
#         return path_to_esp
#     else:
#         return False

def search_esp_in_new_data(df: pd.DataFrame,
                           date_last_check: str, path_esp: str) -> str or bool:
    """Принимает датафрейм с сообщениями, возвращает путь к файлу с сообщениями
    об ЭСП, либо False."""

    # Приведение даты последней проверки к нужному формату
    date_last_check_dt = pd.to_datetime(date_last_check[:10],
                                        format='%Y-%m-%d')

    # Убираем дубликаты
    df = df.drop_duplicates().copy()

    # Фильтрация сообщений об ЭСП
    df_esp = df[df['DocName'].isna()]
    df_esp = df_esp[df_esp['IDNum'].str.contains('#', na=False)].copy()

    # Приведение дат к нужному типу
    df_esp['DateDoc'] = pd.to_datetime(df_esp['DateDoc'], format='%d.%m.%Y',
                                       errors='coerce')
    df_esp['DocRegDate'] = pd.to_datetime(df_esp['DocRegDate'],
                                          errors='coerce')

    # Фильтрация по дате последней проверки
    df_esp = df_esp[df_esp['DateDoc'] >= date_last_check_dt]
    df_esp['DateDoc'] = df_esp['DateDoc'].dt.date

    if not df_esp.empty:
        current_date = datetime.now()
        date_string = current_date.strftime('%d-%m-%Y')
        path_to_esp = path_esp + 'esp_' + date_string + '.xlsx'
        df_esp.to_excel(path_to_esp, index=False)

        return path_to_esp
    return False
