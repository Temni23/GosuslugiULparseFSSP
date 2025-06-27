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
from settings import TRIGGER_TO_EMAIL, BACKUP_DIR


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


def process_email_notifications(df: pd.DataFrame,
                                email_targets: List[str]) -> None:
    filtered_df = df[
        df['DbtrName'].str.lower().str.contains(TRIGGER_TO_EMAIL.lower(),
                                                na=False)]

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
        combined_data['DebtSumTotal'] = combined_data['DebtSumTotal'].astype(
            float)
        date_columns = [
            'send_date', 'update_date', 'RiseDate',
            'DocRegDate', 'IDDate', 'DateDoc'
        ]

        # Приведение к типу datetime64, невалидные значения станут NaT
        for col in date_columns:
            if col in combined_data.columns:
                combined_data[col] = pd.to_datetime(combined_data[col],
                                                    dayfirst=True,
                                                    errors='coerce')
        excluded_cols = {'send_date', 'update_date', 'file_link'}
        combined_data.drop_duplicates(
            subset=combined_data.columns.difference(excluded_cols),
            inplace=True
        )
        combined_data.to_excel(excel_file_path, index=False)

        return new_data
    return False


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
