from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import INSTAGRAM_URL

instagram_button = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Перейти в Instagram',
            url=INSTAGRAM_URL
        )
    ]
])