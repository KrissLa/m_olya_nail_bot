from aiogram.dispatcher.filters.state import StatesGroup, State


class Profile(StatesGroup):
    """ Состояния для работы с профилем пользователя """
    Info = State()
    Name = State()
    Phone = State()
