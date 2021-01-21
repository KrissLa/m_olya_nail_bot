from aiogram.dispatcher.filters.state import StatesGroup, State


class Order(StatesGroup):
    """Стейты для вопросов пользователей"""
    OrderService = State()
    OrderMonth = State()
    OrderDay = State()
    OrderTime = State()
    Bonus = State()
    RegisterOrderWithoutBonus = State()
    RegisterOrderWithBonus = State()
    SelectBonus = State()