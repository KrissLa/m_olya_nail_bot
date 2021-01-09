from aiogram import types
from data.config import BOT_USERNAME


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("help", "Получить справку"),
        types.BotCommand("menu", "Показать меню"),
        types.BotCommand("restart", "Бот завис и не реагирует на Ваши сообщения")
    ])
