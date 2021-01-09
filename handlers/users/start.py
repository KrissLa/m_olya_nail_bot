from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loguru import logger
from re import compile

from filters.registration import CanBeInvited, IsNotRegistered
from keyboards.default.menu import menu_keyboard
from loader import dp, db
from texts.registration import hello_without_code
from data.config import FREE_BONUS, FREE_BONUS_CODE, REFERAL_BONUS


# @dp.message_handler(CommandStart(deep_link=compile(r'\d\w*')), CanBeInvited())
# async def bot_start_with_code(message: types.Message):
#     """
#     Приветствие при первом нажатии кнопки старт с пригласительным кодом
#     """
#     try:
#         deep_link = int(message.get_args())
#     except Exception as e:
#         deep_link = None
#     logger.info(deep_link)


@dp.message_handler(CommandStart(), IsNotRegistered())
async def bot_start(message: types.Message):
    """
    Приветствие при первом нажатии кнопки старт без пригласительное кода
    """
    deep_link = message.get_args()
    logger.info(deep_link)
    bot_user = await dp.bot.get_me()
    logger.info(message.from_user)
    logger.info(message)
    await db.registration(message.from_user, deep_link)
    await message.answer(hello_without_code.format(name=message.from_user.full_name,
                                                   bot_username=bot_user.username,
                                                   user_id=message.from_user.id),
                         reply_markup=menu_keyboard)
