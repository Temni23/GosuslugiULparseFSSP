from settings import URL, TYPE_FEED
from functions import get_feeds, get_cookie

if __name__ == '__main__':
    cookie = get_cookie()
    feeds = get_feeds(URL, TYPE_FEED, cookie)
    counter = 0
    for feed in feeds:
        if 'Постановление' in feed.get('subTitle'):
            print(feed.get('subTitle'), feed.get('date'))
            counter += 1
            print(counter)
