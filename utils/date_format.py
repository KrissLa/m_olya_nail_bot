from dateutil.parser import parse

from keyboards.inline.orders import WEEKDAYS


def date_formatting(str_date):
    """ Преобразование даты """
    date_obj = parse(str_date)
    return str(date_obj.strftime("%d.%m.%Y %H:%M") + " " + WEEKDAYS[date_obj.weekday()])


def date_for_notification(str_date):
    """ Преобразование даты """
    date_obj = parse(str_date)
    return str(date_obj.strftime("%d.%m.%Y"))


def time_for_notification(str_date):
    """ Преобразование даты """
    date_obj = parse(str_date)
    return str(date_obj.strftime("%H:%M"))

