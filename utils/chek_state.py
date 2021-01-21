from loguru import logger

from loader import db, bot

states_for_menu = '*'


async def reset_state(state, message):
    """обрабатываем выход из меню"""
    if await state.get_state() in ['Order:OrderService', 'Question:WaitQuestion', 'Question:WaitAnswer',]:
        data = await state.get_data()
        await bot.delete_message(chat_id=message.from_user.id,
                                 message_id=data['message_id'])
        await state.finish()
    elif await state.get_state() in ['Order:OrderMonth', ]:
        data = await state.get_data()
        logger.info(data)
        # await bot.edit_message_reply_markup(chat_id=message.from_user.id,
        #                                     message_id=data['message_id'])
        await state.finish()
    else:
        await state.finish()