import datetime


def get_cookie() -> str:
    cookie = input('Введите значение Cookie: ')
    return cookie


def get_date_with_offset(delta):
    """Возвращает дату в формате необходимом для установки в качестве
    параметра url запроса."""
    current_date = datetime.datetime.now()
    gap = datetime.timedelta(days=delta)
    offset_date = current_date - gap
    formatted_date = offset_date.replace(hour=0, minute=0, second=0,
                                         microsecond=0)

    return formatted_date.strftime('%Y-%m-%dT%H:%M:%S.000') + '%2B0300'