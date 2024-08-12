"""
Модуль содержит функции работающие с экселем.
"""

from typing import List

import pandas as pd
from datetime import datetime

from email_utils import get_text_for_email, send_email_to_user
from getters import get_attachments_url
from settings import TRIGGER_TO_EMAIL, EMAIL_TARGETS


def save_incoming_vip_to_excel(data_list: List[dict],
                               excel_filename: str) -> None:
    """Сохраняет в эксель информацию о возбуждении ИП."""
    # Пытаемся загрузить существующий файл Excel, если он существует
    try:
        existing_data = pd.read_excel(excel_filename)
    except FileNotFoundError:
        # Если файл не существует, создаем пустой DataFrame
        existing_data = pd.DataFrame()

    # Создаем временный DataFrame для новых данных
    new_data = pd.DataFrame()

    for item in data_list:
        # Извлекаем нужные значения из словаря item
        message_id = item.get('id')
        doc_reg_date = item.get('detail').get('addParams').get('DocRegDate')
        dbtr_name = item.get('detail').get('addParams').get('DbtrName')
        idoc_subj_exec_name = item.get('detail').get('addParams').get(
            'IDocSubjExecName')
        number_doc = item.get('detail').get('addParams').get('IDNum')
        subj_num_push = item.get('detail').get('addParams').get('SubjNum_push')
        crdr_name = item.get('detail').get('addParams').get('CrdrName')
        supplier_org_name = item.get('detail').get('addParams').get(
            'SupplierOrgName')
        debt_sum_total = (item.get('detail').
                          get('addParams').get('DebtSumTotal'))
        id_date = item.get('detail').get('addParams').get('IDDate')
        id_organ_name = item.get('detail').get('addParams').get('IDOrganName')
        delo_num = item.get('detail').get('addParams').get('DeloNum')
        subj_num_text = item.get('detail').get('addParams').get('SubjNum_text')
        subj_num_feed = item.get('detail').get('addParams').get('SubjNum_feed')
        spi_short_name = (item.get('detail').
                          get('addParams').get('SPIShortName'))
        date_doc = item.get('detail').get('addParams').get('DateDoc')

        if dbtr_name and TRIGGER_TO_EMAIL.lower() in dbtr_name.lower():
            text_for_email = get_text_for_email(dbtr_name, supplier_org_name,
                                                number_doc,
                                                id_organ_name, id_date,
                                                delo_num, date_doc)
            for email in EMAIL_TARGETS:
                send_email_to_user(email, text_for_email)

        # Создаем временный DataFrame с полученными значениями
        temp_df = pd.DataFrame({
            'Номер уведомления ГУ': [message_id],
            'Дата регистрации документа': [doc_reg_date],
            'Должник': [dbtr_name],
            'Взыскатель': [crdr_name],
            'Сумма долга': [debt_sum_total],
            'Номер ИД': [number_doc],
            'Дата ИД': [id_date],
            'Суд': [id_organ_name],
            'ОСП': [supplier_org_name],
            'Номер ИП': [delo_num],
            'Пристав': [spi_short_name],
            'Дата возбуждения': [date_doc],
            'Тип задолженности': [idoc_subj_exec_name],
            'Уведомление': [subj_num_push],
            'Текст 1': [subj_num_text],
            'Текст 2': [subj_num_feed],
        })

        # Объединяем временный DataFrame с основным
        new_data = pd.concat([new_data, temp_df], ignore_index=True)

    # Объединяем существующие данные с новыми данными
    combined_data = pd.concat([existing_data, new_data], ignore_index=True)

    # Сохраняем объединенные данные в Excel-файл
    combined_data.to_excel(excel_filename, index=False)


def save_messages_to_excel(data_list: List[dict], excel_filename: str) -> None:
    try:
        existing_data = pd.read_excel(excel_filename)
    except FileNotFoundError:
        existing_data = pd.DataFrame()

    new_data = pd.DataFrame()

    for item in data_list:
        messages = item.get('detail', {}).get('messages', [])
        for message in messages:
            send_date = message.get('sendDate')
            thread_id = message.get('threadId')
            subject = message.get('subject')
            text = message.get('text')
            update_date = message.get('updateDate')
            attachments = message.get('attachments')
            file_link = get_attachments_url(
                attachments) if attachments else None
            IdDocType_text = message.get('addParams', {}).get('IdDocType_text')
            IDocSubjExecName = message.get('addParams', {}).get(
                'IDocSubjExecName')
            feed_mobtitle = message.get('addParams', {}).get('feed_mobtitle')
            NumberDoc = message.get('addParams', {}).get('NumberDoc')

            IdDocType_feed = message.get('addParams', {}).get('IdDocType_feed')
            RiseDate = message.get('addParams', {}).get('RiseDate')
            DocRegDate = message.get('addParams', {}).get('DocRegDate')
            CrdrName = message.get('addParams', {}).get('CrdrName')
            IDNum = message.get('addParams', {}).get('IDNum')
            SupplierOrgName = message.get('addParams', {}).get(
                'SupplierOrgName')
            feed_subtitle = message.get('addParams', {}).get('feed_subtitle')
            DebtSumTotal = message.get('addParams', {}).get('DebtSumTotal')
            DbtrName = message.get('addParams', {}).get('DbtrName')
            IDDate = message.get('addParams', {}).get('IDDate')
            IDOrganName = message.get('addParams', {}).get('IDOrganName')
            PostName = message.get('addParams', {}).get('PostName')
            DeloNum = message.get('addParams', {}).get('DeloNum')
            DocName = message.get('addParams', {}).get('DocName')
            SPIShortName = message.get('addParams', {}).get('SPIShortName')
            DateDoc = message.get('addParams', {}).get('DateDoc')

            temp_df = pd.DataFrame({
                'send_date': [send_date],
                'thread_id': [thread_id],
                'subject': [subject],
                'text': [text],
                'update_date': [update_date],
                'file_link': [file_link],
                'IdDocType_text': [IdDocType_text],
                'IDocSubjExecName': [IDocSubjExecName],
                'feed_mobtitle': [feed_mobtitle],
                'NumberDoc': [NumberDoc],
                'IdDocType_feed': [IdDocType_feed],
                'RiseDate': [RiseDate],
                'DocRegDate': [DocRegDate],
                'CrdrName': [CrdrName],
                'IDNum': [IDNum],
                'SupplierOrgName': [SupplierOrgName],
                'feed_subtitle': [feed_subtitle],
                'DebtSumTotal': [DebtSumTotal],
                'DbtrName': [DbtrName],
                'IDDate': [IDDate],
                'IDOrganName': [IDOrganName],
                'PostName': [PostName],
                'DeloNum': [DeloNum],
                'DocName': [DocName],
                'SPIShortName': [SPIShortName],
                'DateDoc': [DateDoc],
            })

            new_data = pd.concat([new_data, temp_df], ignore_index=True)

    combined_data = pd.concat([existing_data, new_data], ignore_index=True)

    combined_data.to_excel(excel_filename, index=False)


def search_esp_in_messages(file_path: str, date_last_check) -> str or bool:
    """Принимает путь к файлу с сообщениями сохраняет сообщения об электронных
    судебных приказах в файл, возвращает путь к этому файлу."""
    date_last_check = date_last_check[:10].replace('-', '.')
    date_last_check = datetime.strptime(date_last_check, '%Y.%m.%d')
    date_last_check = date_last_check.strftime('%d.%m.%Y')
    current_date = datetime.now()
    date_string = current_date.strftime('%d-%m-%Y')
    path_to_esp = 'excel/ESP/' + 'esp_' + date_string + '.xlsx'
    target_cols = ['IDocSubjExecName', 'NumberDoc', 'DocRegDate', 'CrdrName',
                   'IDNum',
                   'SupplierOrgName', 'feed_subtitle', 'DebtSumTotal',
                   'DbtrName',
                   'IDDate', 'IDOrganName', 'PostName', 'DeloNum', 'DocName',
                   'SPIShortName', 'DateDoc']
    df = pd.read_excel(file_path, usecols=target_cols)
    df.drop_duplicates(inplace=True)
    date_last_check_datetime = pd.to_datetime(date_last_check,
                                              format='%d.%m.%Y')
    df_vip = df[df['DocName'].isna()].copy()
    df_vip = df_vip[df_vip['IDNum'].str.contains('#')].copy()
    dates = df_vip['DateDoc']
    dates = pd.to_datetime(dates, format='%d.%m.%Y', dayfirst=True)
    df_vip['DateDoc'] = dates
    dates = df_vip['DocRegDate']
    dates = pd.to_datetime(dates)
    df_vip['DocRegDate'] = dates
    df_vip = df_vip[df_vip['DateDoc'] >= date_last_check_datetime].copy()
    df_vip['DateDoc'] = pd.to_datetime(df_vip['DateDoc']).dt.date
    if len(df_vip) > 0:
        df_vip.to_excel(path_to_esp, index=False)
        return path_to_esp
    else:
        return False
