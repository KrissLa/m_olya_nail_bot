from aiogram.types import CallbackQuery

from loader import dp, db, bot
from texts.bonuses import empty_history_tx, get_bonus_transactions
from utils.misc import rate_limit


@rate_limit(10)
@dp.callback_query_handler(text='show_qr_ref_link')
async def show_qr_ref_code(call: CallbackQuery):
    """Генерируем qr code"""
    bot_user = await dp.bot.get_me()
    await bot.send_photo(chat_id=call.from_user.id,
                         photo=f"http://qrcoder.ru/code/?http%3A%2F%2Ft.me%2F{bot_user.username}%3Fstart%3D{call.from_user.id}&4&0")


@dp.callback_query_handler(text="bonus_history")
async def show_bonus_translations(call: CallbackQuery):
    """ Вывод последние 10 операций с бонусами """
    bonus_transactions = await db.get_bonus_transactions(call.from_user.id)
    if bonus_transactions:
        await call.message.answer(get_bonus_transactions(bonus_transactions))
    else:
        await call.message.answer(empty_history_tx)