from email_utils import send_esp
from excel_utils import save_messages_to_excel, search_esp_in_messages
from getters import (get_cookie, get_date_with_offset, get_last_params,
                     get_last_feed_data, get_inn)
from request_utils import get_feeds, check_feeds, get_incoming_document
from settings import (URL, TYPE_FEED, EMAI_ESP, EXCEL_MESSAGES_FILE_PATH,
                      SEND_ESP, MANY_ULS, INN, ULS_DICT)

if __name__ == '__main__':
    print('Вас приветствует GosuslugiULparseFSSP \n'
          'Коммерческое использование возможно с согласия разработчика \n'
          'https://github.com/Temni23/GosuslugiULparseFSSP.git\n')
    if MANY_ULS:
        inn = get_inn(ULS_DICT)
    else:
        inn = INN
    cookie = get_cookie()
    days = int(input('Введите период для проверки: '))
    end_date = get_date_with_offset(days)
    headers = {'Cookie': cookie}
    last_feed_date, last_feed_id = get_last_params()
    feeds = get_feeds(URL, type_feed=TYPE_FEED, headers=headers,
                      date_end_check=end_date, last_feed_date=last_feed_date,
                      last_feed_id=last_feed_id)
    print(f'Новости получены, проверяю... Всего '
          f'{len(feeds)} новостей для проверки. Ищу нужные...')

    targets_feeds = check_feeds(feeds)
    if targets_feeds:
        print(f'Найдены уведомления по заданным параметрам, '
              f'всего {len(targets_feeds)}. Сейчас загружу документы')
        incoming_docs = get_incoming_document(targets_feeds, headers)
        save_messages_to_excel(incoming_docs, inn, EXCEL_MESSAGES_FILE_PATH)
        print('Загрузка закончена')
        # Ищем и сохраняем информацию об электронных судебных приказах
        esp = search_esp_in_messages(EXCEL_MESSAGES_FILE_PATH, end_date)
        if SEND_ESP and esp:
            send_esp(esp, EMAI_ESP)
    print(f'Проверка до {end_date[0:10]} закончена.')
    last = feeds.pop()
    last_feed_date, last_feed_id = get_last_feed_data(last)
    print(f'Данные для продолжения проверки:\n'
          f'Дней проверено: {days}\n'
          f'Дата последней новости: {last_feed_date}\n'
          f'ID последней новости: {last_feed_id}')
