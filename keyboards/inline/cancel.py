from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


cancel_button = InlineKeyboardButton(
            text='Отмена',
            callback_data="cancel"
        )


cancel_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        cancel_button
    ]
])

cancel_markup_2 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Отмена",
            callback_data='cancel_2'
        )
    ]
])