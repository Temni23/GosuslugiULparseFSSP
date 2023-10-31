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
SEARCH_SENDER = 'фссп россии'

# Используется для поиска слова в названии уведомления
SEARCH_WORD = 'постановление'

# Используется для поиска конкретного должника в уведомлениях от ФССП
SEARCH_DEBTOR = 'Климов Артём Владимирович'

APP_EMAIL = os.getenv('APP_EMAIL')

APP_EMAIL_PASSWORD = os.getenv('APP_EMAIL_PASSWORD')

EMAIL_TARGET = os.getenv('EMAIL_TARGET')
