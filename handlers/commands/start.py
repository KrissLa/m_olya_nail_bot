from re import compile

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loguru import logger

from filters.registration import IsNotRegistered, IsRegistered
from keyboards.default.menu import menu_keyboard
from loader import dp, db
from texts.emoji import simple_smile_em
from texts.registration import hello_without_code, already_registered_with_code_tx, already_registered_without_code_tx, \
    hello_with_code, hello_with_code_no_ref


# @rate_limit(15)
@dp.message_handler(CommandStart(deep_link=compile(r'\d\w*')), IsRegistered(), state="*")
async def bot_start_with_code(message: types.Message):
    """
    Приветствие при первом нажатии кнопки старт с пригласительным кодом.
    Пользователь зарегистрирован.
    """
    await message.answer(already_registered_with_code_tx.format(simple_smile_em=simple_smile_em,
                                                                name=message.from_user.full_name))


# @rate_limit(15)
@dp.message_handler(CommandStart(), IsRegistered(), state="*")
async def bot_start_with_code(message: types.Message):
    """
    Приветствие при первом нажатии кнопки старт без пригласительного кода.
    Пользователь зарегистрирован.
    """
    await message.answer(already_registered_without_code_tx.format(simple_smile_em=simple_smile_em,
                                                                   name=message.from_user.full_name))


@dp.message_handler(CommandStart(), IsNotRegistered())
async def bot_start(message: types.Message):
    """
    Приветствие при первом нажатии кнопки старт
    """
    bot_user = await dp.bot.get_me()
    deep_link = message.get_args()
    data = {
        "telegram_id": message.from_user.id,
        "name": message.from_user.full_name,
    }
    if message.from_user.username:
        data['username'] = f"@{message.from_user.username}"
    if deep_link:
        try:
            deep_link = int(deep_link)
        except ValueError:
            pass
        else:
            data['referer'] = deep_link
    logger.info(data)
    register_data = await db.registration(data)
    if deep_link:
        if "ref_name" in register_data:
            await message.answer(hello_with_code.format(simple_smile_em=simple_smile_em,
                                                        name=register_data['name'],
                                                        ref_name=register_data['ref_name'],
                                                        bonus_point=register_data['bonus_balance'],
                                                        bot_username=bot_user.username,
                                                        user_id=message.from_user.id),
                                 reply_markup=menu_keyboard)
        else:
            await message.answer(hello_with_code_no_ref.format(simple_smile_em=simple_smile_em,
                                                               name=register_data['name'],
                                                               bonus_point=register_data['bonus_balance'],
                                                               bot_username=bot_user.username,
                                                               user_id=message.from_user.id),
                                 reply_markup=menu_keyboard)
    else:
        await message.answer(hello_without_code.format(simple_smile_em=simple_smile_em,
                                                       name=register_data['name'],
                                                       bonus_point=register_data['bonus_balance'],
                                                       bot_username=bot_user.username,
                                                       user_id=message.from_user.id),
                             reply_markup=menu_keyboard)


@dp.message_handler(IsNotRegistered())
async def not_registered_users(message: types.Message):
    """
    Ловим не зарегистрированных пользователей
    """
    bot_user = await dp.bot.get_me()
    data = {
        "telegram_id": message.from_user.id,
        "name": message.from_user.full_name,
    }
    if message.from_user.username:
        data['username'] = f"@{message.from_user.username}"
    logger.info(data)
    register_data = await db.registration(data)
    await message.answer(hello_without_code.format(simple_smile_em=simple_smile_em,
                                                   name=register_data['name'],
                                                   bonus_point=register_data['bonus_balance'],
                                                   bot_username=bot_user.username,
                                                   user_id=message.from_user.id),
                         reply_markup=menu_keyboard)
