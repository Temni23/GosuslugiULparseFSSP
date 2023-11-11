import pandas as pd


def save_incoming_vip_to_excel(data_list, excel_filename):
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
        id_ = item.get('id')
        doc_reg_date = item.get('detail').get('addParams').get('DocRegDate')
        dbtr_name = item.get('detail').get('addParams').get('DbtrName')
        idoc_subj_exec_name = item.get('detail').get('addParams').get(
            'IDocSubjExecName')
        number_doc = item.get('detail').get('addParams').get('NumberDoc')
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

        # Создаем временный DataFrame с полученными значениями
        temp_df = pd.DataFrame({
            'id': [id_],
            'doc_reg_date': [doc_reg_date],
            'dbtr_name': [dbtr_name],
            'idoc_subj_exec_name': [idoc_subj_exec_name],
            'number_doc': [number_doc],
            'subj_num_push': [subj_num_push],
            'crdr_name': [crdr_name],
            'supplier_org_name': [supplier_org_name],
            'debt_sum_total': [debt_sum_total],
            'id_date': [id_date],
            'id_organ_name': [id_organ_name],
            'delo_num': [delo_num],
            'subj_num_text': [subj_num_text],
            'subj_num_feed': [subj_num_feed],
            'spi_short_name': [spi_short_name],
            'date_doc': [date_doc]
        })

        # Объединяем временный DataFrame с основным
        new_data = pd.concat([new_data, temp_df], ignore_index=True)

    # Объединяем существующие данные с новыми данными
    combined_data = pd.concat([existing_data, new_data], ignore_index=True)

    # Сохраняем объединенные данные в Excel-файл
    combined_data.to_excel(excel_filename, index=False)
