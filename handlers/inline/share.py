from aiogram import types
from aiogram.types import InputMessageContent

from keyboards.inline.bonuses import get_share_keyboard
from loader import dp


@dp.inline_handler()
async def share_query(query: types.InlineQuery):
    """Передаем реф ссылку другу"""

    bot_user = await dp.bot.get_me()

    await query.answer(
        results=[types.InlineQueryResultArticle(
            id="unknown",
            title="Отправить приглашение",
            input_message_content=InputMessageContent(
                message_text=f"Привет! Приглашаю тебя в {bot_user.full_name}. Там можно заказать маникюр)\n"),
            reply_markup=get_share_keyboard(bot_user.username, query.from_user.id)

        )])
