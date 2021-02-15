from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.cancel import cancel_button

change_profile_button = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Изменить данные профиля",
            callback_data="change_profile"
        )
    ]
])

change_profile_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Изменить имя",
            callback_data="change_user_name"
        )
    ],
    [
        InlineKeyboardButton(
            text="Изменить номер телефона",
            callback_data="change_user_phone"
        )
    ],
    [
        cancel_button
    ]

])
