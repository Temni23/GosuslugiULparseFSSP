from excel_utils import save_incoming_vip_to_excel
from request_utils import get_feeds, check_feeds, get_incoming_document
from getters import get_cookie, get_date_with_offset, get_last_params, \
    get_last_feed_data
from settings import URL, TYPE_FEED, EXCEL_FILE_PATH

if __name__ == '__main__':
    cookie = get_cookie()
    end_date = get_date_with_offset(
        int(input('Введите период для проверки: ')))
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
        save_incoming_vip_to_excel(incoming_docs, EXCEL_FILE_PATH)
        print('Загрузка закончена')
    print(f'Проверка до {end_date[0:10]} закончена.')
    last = feeds.pop()
    last_feed_date, last_feed_id = get_last_feed_data(last)
    print(f'Данные для продолжения проверки:\n'
          f'Дата последней новости: {last_feed_date}\n'
          f'ID последней новости: {last_feed_id}')
