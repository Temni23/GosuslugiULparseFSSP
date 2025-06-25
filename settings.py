"""
Настройки приложения
"""
import os

from dotenv import load_dotenv

load_dotenv()

# Переменная URL содержит адрес эндпоинта Госуслуг с которого в ответ на GET
# запрос пользователя возвращается JSON с уведомлениями

URL = 'https://www.gosuslugi.ru/api/lk/v1/feeds/'

# Переменная TYPE_FEED используется для параметра GET запроса фильтрующего
# входящие уведомления, для фильтра уведомлений от ФССП используется значение
# переменной GEPS
TYPE_FEED = 'GEPS'

# Используется для фильтрации по отправителю
SEARCH_SENDER = 'фссп'
#
# # Используется для поиска слова в названии уведомления
# SEARCH_WORD = 'возбужден'

TRIGGER_TO_EMAIL = 'росттех' # TODO несколько тиригеров списком
# имя должника при выявлении которого отправляется электронное письмо

RE_REQUESTS_SERVER = 20
RE_REQUESTS_DOWNLOAD = 5

APP_EMAIL = os.getenv('APP_EMAIL')

APP_EMAIL_PASSWORD = os.getenv('APP_EMAIL_PASSWORD')

EMAIL_TARGETS = os.getenv('EMAIL_TARGETS').split(' ')

SEND_EMAIL = True
SEND_ESP = True

REQUEST_SLEEP_TIME = 5

EXCEL_FILE_PATH = 'excel/base.xlsx'
EXCEL_MESSAGES_FILE_PATH = 'excel/messages.xlsx'
ESP_PATH = 'excel/ESP/'
EMAI_ESP = os.getenv('EMAI_ESP')

# TODO Возможность работы с CSV
# Использование несколькими юлицами
MANY_ULS = False
ULS_DICT = {}
if MANY_ULS:
    ULS = os.getenv('ULS').split(' ')
    INNS = os.getenv('INNS').split(' ')
    # Юрлица которые пользуются программой
    ULS_DICT = dict(zip(ULS, INNS))
INN = os.getenv('INN')
