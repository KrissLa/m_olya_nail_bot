from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram.types import Message
from loguru import logger

from data.config import ADMIN_ID
from filters.registration import IsBannedMessage
from keyboards.default.menu import menu_keyboard
from loader import dp
from utils.misc import rate_limit


@dp.message_handler(IsBannedMessage())
async def banned(message: Message):
    """ Заблокированные пользователи """
    await message.answer("Вы заблокированы!")


@dp.message_handler(commands='restart', state=['*'])
async def restart(message: Message, state: FSMContext):
    """ Рестарт стейта """
    logger.info(await state.get_state())
    await state.finish()
    await message.answer('Перезагружен', reply_markup=menu_keyboard)


@dp.message_handler(commands='menu', state=['*'])
async def show_menu(message: Message):
    """Показываем меню"""
    await message.answer("Отправляю меню",
                         reply_markup=menu_keyboard)


@rate_limit(5, 'help')
@dp.message_handler(CommandHelp(), user_id=ADMIN_ID,  state=['*'])
async def bot_help(message: types.Message):
    text = [
        'Список команд: ',
        '/start - Начать диалог',
        '/menu - Показать меню',
        '/help - Получить справку',
        '/admin - Перейти в панель администратора',
        '/restart - Перезапуск бота (на случай если перестал отвечать)'
    ]
    await message.answer('\n'.join(text), reply_markup=menu_keyboard)


@rate_limit(5, 'help')
@dp.message_handler(CommandHelp(),  state=['*'])
async def bot_help(message: types.Message):
    text = [
        'Список команд: ',
        '/start - Начать диалог',
        '/menu - Показать меню',
        '/help - Получить справку',
        '/restart - Перезапуск бота (на случай если перестал отвечать)'
    ]
    await message.answer('\n'.join(text), reply_markup=menu_keyboard)
