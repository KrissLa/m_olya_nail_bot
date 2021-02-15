from loguru import logger

from loader import db, bot

states_for_menu = ['*']


async def reset_state(state, message):
    """обрабатываем выход из меню"""
    state_name = await state.get_state()
    data = await state.get_data()

    if state_name in ['Order:OrderService', 'Question:WaitQuestion', 'Question:WaitAnswer', "Admin:Main",
                      "Order:WaitReview", "Admin:WaitOrderConfirm", 'Order:OrderMonth', "Order:OrderDay",
                      "Order:OrderTime", "Order:Bonus", "Order:RegisterOrderWithBonus",
                      "Order:RegisterOrderWithoutBonus", "Order:SelectBonus"]:
        await _delete_message(data['message_id'], message)

    elif state_name in ['Profile:Info', "Profile:Name", "Profile:Phone"]:
        await _edit_message_reply_markup(data['message_id'], message)

    elif state_name in ['Admin:OrderMinList', ]:
        await _edit_messages_reply_markup(data['messages'], message)

    elif state_name in ['Admin:OrderDetail', ]:
        await _edit_messages_reply_markup(data['messages'], message)
        await _edit_message_reply_markup(data['message_id'], message)

    elif state_name in ["Order:CancelOrder", "Order:ConfirmCancelOrder"]:
        await _edit_messages_reply_markup(data['mess_orders'], message)

    elif state_name in ['Admin:OrderWaitReason', ]:
        await _delete_message(data['message_cancel_id'], message)

    await state.finish()


async def _edit_messages_reply_markup(data, message):
    """ Убираем клавиатуру у  списка сообщений """
    for m in data:
        try:
            await bot.edit_message_reply_markup(chat_id=message.from_user.id,
                                                message_id=m)
        except Exception:
            pass


async def _edit_message_reply_markup(message_id, message):
    """ Убираем клавиатуру у одного сообщения"""
    try:
        await bot.edit_message_reply_markup(chat_id=message.from_user.id,
                                            message_id=message_id)
    except Exception:
        pass


async def _delete_message(message_id, message):
    """ Пробуем удалить сообщение """
    try:
        await bot.delete_message(chat_id=message.from_user.id,
                                 message_id=message_id)
    except Exception:
        pass
