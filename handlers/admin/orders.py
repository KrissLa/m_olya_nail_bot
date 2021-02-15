import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from loguru import logger

from keyboards.inline.admin import order_min_keyboard, back_keyboard, admin_keyboard, order_keyboard, \
    order_confirmation_keyboard
from keyboards.inline.callback_datas.orders import admin_detail_data, admin_order_cancel, admin_order_complete, \
    admin_order_confirm, rating_viewed, review_viewed
from keyboards.inline.orders import rating_keyboard
from loader import dp, bot, db
from states.admin import Admin
from texts.admin import order_min_tx, order_min_complete_tx, hello_admin, order_detail_tx, cancel_order_tx, \
    cancel_order_to_user_tx, order_is_cancelled_tx, order_already_cancelled_tx, confirm_order_tx, \
    confirm_order_error_cancelled_tx, confirm_order_error_already_tx, confirm_order_success_tx
from texts.emoji import blush_em, error_em, success_em
from texts.orders import order_completed_to_user_tx
from utils.orders.services import get_order_discounts, ORDER_STATUSES


@dp.callback_query_handler(text="admin_orders", state=Admin.Main)
async def get_order_list(call: CallbackQuery, state: FSMContext):
    """ Выводим список заказов """
    data = await state.get_data()
    await bot.delete_message(chat_id=call.from_user.id, message_id=data['message_id'])
    orders = await db.get_order_list()
    messages = []
    for order in orders:
        mess = await call.message.answer(order_min_tx.format(order_id=order['order_id'],
                                                             str_date=order['str_date']),
                                         reply_markup=order_min_keyboard(order))
        messages.append(mess['message_id'])
        await asyncio.sleep(.05)  # 20 messages per second (Limit: 30 messages per second)
    mess = await call.message.answer(order_min_complete_tx,
                                     reply_markup=back_keyboard)
    messages.append(mess['message_id'])
    data['messages'] = messages
    await state.update_data(data=data)
    logger.info(messages)
    await Admin.OrderMinList.set()


@dp.callback_query_handler(text='back', state=Admin.OrderMinList)
async def back_to_admin_panel(call: CallbackQuery, state: FSMContext):
    """ Назад в админ панель """
    data = await state.get_data()
    logger.info(data)
    try:
        for m in data['messages']:
            try:
                await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=m, reply_markup=None)
            except:
                pass
    except:
        pass
    events = await db.get_events_number()
    mess = await call.message.answer(hello_admin,
                                     reply_markup=admin_keyboard(events))
    data['message_id'] = mess['message_id']
    data['messages'] = []
    await state.update_data(data)
    await Admin.Main.set()


@dp.callback_query_handler(admin_detail_data.filter(), state=[Admin.OrderMinList,
                                                              Admin.OrderDetail])
async def get_order_details(call: CallbackQuery, state: FSMContext, callback_data: dict):
    """ Вывод подробной информации о заказе """
    data = await state.get_data()
    logger.info(data)
    if await state.get_state() == 'Admin:OrderDetail':
        await bot.delete_message(chat_id=call.from_user.id, message_id=data['message_id'])
    pressed_mess_id = call.message.message_id
    await call.message.edit_reply_markup()
    order_id = int(callback_data['order_id'])
    order = await db.get_order(order_id)
    if order['status'] == 'wait':
        discount = get_order_discounts(order)
        mess = await call.message.answer(order_detail_tx.format(order_id=order['id'],
                                                                order_date=order['service_date']['date'],
                                                                service_name=order['service_name'],
                                                                service_price=order['service_price'],
                                                                total_price=order['total_price'],
                                                                discount=discount['discount'],
                                                                bonus_discount=discount['bonus_discount'],
                                                                order_status=ORDER_STATUSES[order['status']],
                                                                telegram_id=order['user']['telegram_id'],
                                                                username=order['user']['username'],
                                                                name=order['user']['name'],
                                                                phone_number=order['user']['phone_number']),
                                         reply_markup=order_keyboard(order['id']))
        data['order_telegram_user_id'] = order['user']['telegram_id']
        data['message_id'] = mess['message_id']
        data['pressed_message_id'] = pressed_mess_id
        data['order_id'] = order_id
        await state.update_data(data)
        await Admin.OrderDetail.set()
    elif order['status'] == 'canceled':
        await call.message.answer(order_already_cancelled_tx)


@dp.callback_query_handler(text='back', state=Admin.OrderDetail)
async def back_to_order_list(call: CallbackQuery, state: FSMContext):
    """ Назад к списку заказов """
    data = await state.get_data()
    await bot.delete_message(chat_id=call.from_user.id, message_id=data['message_id'])
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=data['pressed_message_id'],
                                        reply_markup=order_min_keyboard(data))
    await call.answer('Назад')
    await Admin.OrderMinList.set()


@dp.callback_query_handler(admin_order_cancel.filter(), state=Admin.OrderDetail)
async def cancel_order(call: CallbackQuery, state: FSMContext, callback_data: dict):
    """ Нажатие на кнопку отмены заказа """
    data = await state.get_data()
    await call.message.edit_reply_markup()
    data['cancel_order_id'] = int(callback_data['order_id'])
    mess = await call.message.answer(cancel_order_tx, reply_markup=back_keyboard)
    data['message_cancel_id'] = mess['message_id']
    await state.update_data(data)
    await Admin.OrderWaitReason.set()


@dp.callback_query_handler(text="back", state=Admin.OrderWaitReason)
async def back_to_order(call: CallbackQuery, state: FSMContext):
    """ Назад к заказу """
    data = await state.get_data()
    logger.info(data)
    await bot.delete_message(chat_id=call.from_user.id, message_id=data['message_id'])
    await bot.delete_message(chat_id=call.from_user.id, message_id=data['message_cancel_id'])
    order_id = data['cancel_order_id']
    order = await db.get_order(order_id)
    discount = get_order_discounts(order)
    mess = await call.message.answer(order_detail_tx.format(order_id=order['id'],
                                                            order_date=order['service_date']['date'],
                                                            service_name=order['service_name'],
                                                            service_price=order['service_price'],
                                                            total_price=order['total_price'],
                                                            discount=discount['discount'],
                                                            bonus_discount=discount['bonus_discount'],
                                                            order_status=ORDER_STATUSES[order['status']],
                                                            telegram_id=order['user']['telegram_id'],
                                                            username=order['user']['username'],
                                                            name=order['user']['name'],
                                                            phone_number=order['user']['phone_number']),
                                     reply_markup=order_keyboard(order['id']))
    data['message_id'] = mess['message_id']
    await state.update_data(data)
    await Admin.OrderDetail.set()


@dp.message_handler(state=Admin.OrderWaitReason)
async def confirm_cancellation(message: Message, state: FSMContext):
    """ Получаем причину и отменяем заказ """
    data = await state.get_data()
    logger.info(data)
    await bot.edit_message_reply_markup(chat_id=message.from_user.id, message_id=data['message_cancel_id'],
                                        reply_markup=None)
    await db.cancel_order(order_id=data['cancel_order_id'],
                          reason=message.text)
    await bot.send_message(data['order_telegram_user_id'],
                           cancel_order_to_user_tx.format(error_em=error_em,
                                                          order_id=data['cancel_order_id'],
                                                          reason=message.text))
    await message.answer(order_is_cancelled_tx.format(success_em=success_em,
                                                      order_id=data['cancel_order_id']))
    await bot.delete_message(chat_id=message.from_user.id, message_id=data['message_id'])
    await bot.delete_message(chat_id=message.from_user.id, message_id=data['message_cancel_id'])
    await Admin.OrderMinList.set()


@dp.callback_query_handler(admin_order_complete.filter(), state=Admin.OrderDetail)
async def completion_confirmation(call: CallbackQuery, state: FSMContext, callback_data: dict):
    """ Отправляем подтверждение с подтверждением завершения заказа """
    data = await state.get_data()
    logger.info(data)
    await call.message.edit_reply_markup()
    data['con_order_id'] = int(callback_data['order_id'])
    mess = await call.message.answer(confirm_order_tx,
                              reply_markup=order_confirmation_keyboard(data['con_order_id']))
    data['message_id'] = mess['message_id']
    await state.update_data(data)
    await Admin.WaitOrderConfirm.set()


@dp.callback_query_handler(text="back", state=Admin.WaitOrderConfirm)
async def back_from_completion_confirmation(call: CallbackQuery, state: FSMContext):
    """ Назад из меню подтверждения заказа """
    data = await state.get_data()
    logger.info(data)
    await call.message.delete()
    await call.answer("Выполнено")
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=data['message_id'],
                                        reply_markup=order_keyboard(data['con_order_id']))
    await Admin.OrderDetail.set()


@dp.callback_query_handler(admin_order_confirm.filter(), state=Admin.WaitOrderConfirm)
async def send_order_confirmation(call: CallbackQuery, state: FSMContext, callback_data: dict):
    """
    Отправляем подтверждение заказа на сервер.
    Отправляем пользователю предложение оценить работу.
    """
    data = await state.get_data()
    logger.info(data)
    logger.info(callback_data)
    await call.message.delete()
    await bot.delete_message(chat_id=call.from_user.id, message_id=data['message_id'])
    resp = await db.confirm_order(int(callback_data['order_id']))
    if resp['status'] == 'canceled':
        await call.message.answer(confirm_order_error_cancelled_tx.format(error_em=error_em,
                                                                          order_id=data['order_id']))
    elif resp['status'] == "already_completed":
        await call.message.answer(confirm_order_error_already_tx.format(error_em=error_em,
                                                                        order_id=data['order_id']))
    else:
        await call.message.answer(confirm_order_success_tx.format(success_em=success_em,
                                                                  order_id=data['order_id']))
        await bot.send_message(chat_id=resp['user']['telegram_id'],
                               text=order_completed_to_user_tx.format(blush_em=blush_em,
                                                                      order_id=resp['id'],
                                                                      bonus_amount=resp['bonus_points']),
                               reply_markup=rating_keyboard(resp['id']))
    await Admin.OrderMinList.set()
    logger.info(resp)
    logger.info(resp['status'])


@dp.callback_query_handler(rating_viewed.filter(), state="*")
async def rating_viewed(call: CallbackQuery, callback_data: dict):
    """ Отмечаем оценку просмотренной """
    await db.rating_viewed(int(callback_data['order_id']))
    await call.message.delete()
    await call.answer('Оценка отмечена как просмотрена')


@dp.callback_query_handler(review_viewed.filter(), state="*")
async def review_viewed(call: CallbackQuery, callback_data: dict):
    """ Отмечаем отзыв просмотренным """
    await db.review_viewed(int(callback_data['order_id']))
    await call.message.delete()
    await call.answer('Отзыв отмечен как просмотрен')
