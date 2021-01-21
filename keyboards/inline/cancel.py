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