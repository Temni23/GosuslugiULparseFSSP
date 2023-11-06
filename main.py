from functions import get_feeds, get_cookie, get_date_with_offset, check_feeds, \
    get_incoming_document
from settings import URL, TYPE_FEED

if __name__ == '__main__':
    cookie = get_cookie()
    end_date = get_date_with_offset(
        int(input('Введите период для проверки: ')))
    headers = {'Cookie': cookie}
    feeds = get_feeds(URL, type_feed=TYPE_FEED, cookie=cookie,
                      date_end_check=end_date)
    print(f'Новости получены, проверяю... Всего '
          f'{len(feeds)} новостей для проверки. Ищу нужные...')

    targets_feeds = check_feeds(feeds)
    if targets_feeds:
        print(f'Найдены уведомления по заданным параметрам, '
              f'всего {len(targets_feeds)}. Сейчас загружу документы')
        get_incoming_document(targets_feeds, headers)
        print('Загрузка закончена')
    print(f'Проверка до {end_date[0:10]} закончена.')
