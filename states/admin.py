from aiogram.dispatcher.filters.state import StatesGroup, State


class Admin(StatesGroup):
    """Стейты для админа"""
    Main = State()
    OrderMinList = State()
    OrderDetail = State()
    OrderWaitReason = State()
    WaitOrderConfirm = State()
