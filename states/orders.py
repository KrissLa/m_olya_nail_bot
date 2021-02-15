from aiogram.dispatcher.filters.state import StatesGroup, State


class Order(StatesGroup):
    """Стейты при работе с заказом """
    OrderService = State()
    OrderMonth = State()
    OrderDay = State()
    OrderTime = State()
    Bonus = State()
    RegisterOrderWithoutBonus = State()
    RegisterOrderWithBonus = State()
    SelectBonus = State()

    WaitReview = State()
    CancelOrder = State()
    ConfirmCancelOrder = State()
