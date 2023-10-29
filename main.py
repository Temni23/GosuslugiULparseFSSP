from settings import URL, TYPE_FEED
from functions import get_feeds, get_cookie, get_date_with_offset

if __name__ == '__main__':
    cookie = get_cookie()
    end_date = get_date_with_offset(
        int(input('Введите период для проверки: ')))
    get_feeds(URL, type_feed=TYPE_FEED, cookie=cookie, date_end_check=end_date)
