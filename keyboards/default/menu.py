from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Заказать"),
        KeyboardButton(text="Бонусы"),
    ],
    [
        KeyboardButton(text="Профиль"),
        KeyboardButton(text="Заказы"),
    ],
    [
        KeyboardButton(text="Instagram"),
        KeyboardButton(text="Примеры работ"),
    ],
    [
        KeyboardButton(text="Задать вопрос"),
    ],
])
