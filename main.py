from settings import URL, TYPE_FEED
from functions import get_feeds, get_cookie, get_date_with_offset

if __name__ == '__main__':
    cookie = get_cookie()
    end_date = get_date_with_offset(
        int(input('Введите период для проверки: ')))
    feeds = get_feeds(URL, cookie=cookie, date_end_check=end_date)
    # counter = 0
    # for feed in feeds:
    #     if 'Постановление' in feed.get('subTitle'):
    #         print(feed.get('subTitle'), feed.get('date'))
    #         counter += 1
    #         print(counter)
