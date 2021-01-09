from aiogram.dispatcher.filters.state import StatesGroup, State


class Question(StatesGroup):
    """Стейты для вопросов пользователей"""
    WaitQuestion = State()
    WaitAnswer = State()