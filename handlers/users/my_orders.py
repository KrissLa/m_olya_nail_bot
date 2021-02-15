from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data.config import ADMIN_ID
from keyboards.inline.admin import user_cancel_order__to_admin_tx
from keyboards.inline.callback_datas.orders import user_order_cancel, user_back_to_order, user_order_cancel_confirm
from keyboards.inline.orders import cancel_order_keyboard, confirm_cancel_order_keyboard
from loader import dp, bot, db
from states.orders import Order
from texts.emoji import success_em, speaker_em
from texts.my_orders import cancel_order_user_tx, \
    success_cancel_order_tx
from utils.date_format import date_formatting


@dp.callback_query_handler(user_order_cancel.filter(), state=Order.CancelOrder)
async def cancel_order_user(call: CallbackQuery, state: FSMContext, callback_data: dict):
    """ Пользователь нажимает отменить заказ """
    order_id = int(callback_data['order_id'])
    mess = await call.message.edit_text(
        text=call.message.text + "\n" + cancel_order_user_tx.format(order_id=order_id),
        entities=call.message.entities,
        reply_markup=confirm_cancel_order_keyboard(order_id)
    )
    await state.update_data(canceled_order_mess=mess['message_id'])
    await Order.ConfirmCancelOrder.set()


@dp.callback_query_handler(user_back_to_order.filter(), state=Order.ConfirmCancelOrder)
async def back_to_order(call: CallbackQuery, callback_data: dict):
    """ Отмена отмены заказа """
    await call.message.edit_text(call.message.text[:-44],
                                 entities=call.message.entities,
                                 reply_markup=cancel_order_keyboard(int(callback_data['order_id'])))
    await Order.CancelOrder.set()


@dp.callback_query_handler(user_order_cancel_confirm.filter(), state=Order.ConfirmCancelOrder)
async def confirm_cancel_order(call: CallbackQuery, state: FSMContext, callback_data: dict):
    """ Пользователь подтверждает отмену заказа"""
    order_id = int(callback_data['order_id'])
    cancel_data = await db.cancel_order(order_id=order_id)
    await call.message.edit_text(success_cancel_order_tx.format(success_em=success_em,
                                                                order_id=order_id))
    orders = await db.get_active_orders(call.from_user.id)
    await bot.send_message(ADMIN_ID, user_cancel_order__to_admin_tx.format(speaker_em=speaker_em,
                                                                           order_id=cancel_data['id'],
                                                                           service_date=date_formatting(
                                                                               cancel_data['service_date']['date'])))
    if orders:
        await Order.CancelOrder.set()
    else:
        await state.finish()
