from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from data.config import SERVICE_ADDRESS, ADMIN_ID, ADMIN_PHONE_NUMBER
from keyboards.inline.callback_datas.orders import order_service, month_data, day_data, time_data, bonus_data
from keyboards.inline.orders import mont_keyboard, generate_services_keyboard, days_keyboard, time_keyboard, \
    select_bonus_markup, register_order_markup, get_bonus_keyboard
from loader import dp, db, bot
from states.orders import Order
from texts.emoji import speaker_em
from texts.orders import take_month, no_dates, take_service, available_bonus, no_available_bonus, register_order_tx, \
    new_order_to_admin_tx, select_bonus_tx, take_bonus_tx, register_order_with_bonus_tx, \
    new_order_with_bonus_to_admin_tx


@dp.callback_query_handler(order_service.filter(), state=Order.OrderService)
async def select_service(call: CallbackQuery, state: FSMContext, callback_data: dict):
    """ Пользователь выбирает услугу """
    data = await state.get_data()
    await bot.delete_message(chat_id=call.from_user.id,
                             message_id=data['message_id'])
    info = await db.get_service(int(callback_data['service_id']))
    if info['discount']:
        discount = info['discount_amount']
    else:
        discount = 0
    months = await db.get_available_months()
    if months['months']:
        mess = await call.message.answer(take_month.format(service_name=info['name'],
                                                           amount=callback_data['price'],
                                                           discount=discount,
                                                           service_time=callback_data['time']),
                                         reply_markup=mont_keyboard(months))
        data = {
            'service_id': info['id'],
            'service_name': info['name'],
            'discount': discount,
            'full_cost': info['price'],
            'price': callback_data['price'],
            'message_id': mess['message_id'],
            'service_time': callback_data['time'],
            "discount_BYN": float(callback_data["discount_BYN"])
        }
        await state.update_data(data=data)
        await Order.OrderMonth.set()
    else:
        await call.message.answer(no_dates)
        await state.finish()


@dp.callback_query_handler(text='back', state=Order.OrderMonth)
async def back_to_service(call: CallbackQuery, state: FSMContext):
    """Нажатие на кнопку назад к выбору услуги"""
    data = await state.get_data()
    await state.finish()
    await bot.delete_message(chat_id=call.from_user.id,
                             message_id=data['message_id'])
    services = await db.get_services()
    mess = await call.message.answer(take_service,
                                     reply_markup=generate_services_keyboard(services))
    await state.update_data(message_id=mess['message_id'])
    await Order.OrderService.set()


@dp.callback_query_handler(month_data.filter(), state=Order.OrderMonth)
async def select_month(call: CallbackQuery, state: FSMContext, callback_data: dict):
    """ Пользователь выбирает месяц """
    data = await state.get_data()
    logger.info(data)
    data['month_id'] = int(callback_data['month_id'])
    await bot.delete_message(chat_id=call.from_user.id,
                             message_id=data['message_id'])
    days = await db.get_available_days(data['month_id'])
    logger.info(days)
    if days['days']:
        mess = await call.message.answer(take_month.format(service_name=data['service_name'],
                                                           amount=data['price'],
                                                           discount=data['discount'],
                                                           service_time=data['service_time']),
                                         reply_markup=days_keyboard(days, data['month_id']))
        data['message_id'] = mess['message_id']

        await state.update_data(data=data)
        await Order.OrderDay.set()
    else:
        await call.message.answer(no_dates)
        await state.finish()


@dp.callback_query_handler(text='back', state=Order.OrderDay)
async def back_to_month(call: CallbackQuery, state: FSMContext):
    """Нажатие на кнопку назад к выбору услуги"""
    data = await state.get_data()
    await bot.delete_message(chat_id=call.from_user.id,
                             message_id=data['message_id'])
    months = await db.get_available_months()
    if months['months']:
        mess = await call.message.answer(take_month.format(service_name=data['service_name'],
                                                           amount=data['price'],
                                                           discount=data['discount'],
                                                           service_time=data['service_time']),
                                         reply_markup=mont_keyboard(months))
        data['message_id'] = mess['message_id']
        await state.update_data(data=data)
        await Order.OrderMonth.set()
    else:
        await call.message.answer(no_dates)
        await state.finish()


@dp.callback_query_handler(day_data.filter(), state=Order.OrderDay)
async def select_day(call: CallbackQuery, state: FSMContext, callback_data: dict):
    """ Пользователь выбирает день """
    data = await state.get_data()
    logger.info(data)
    data['day_id'] = int(callback_data['day_id'])
    data['day_of_week'] = int(callback_data['day_of_week'])
    await bot.delete_message(chat_id=call.from_user.id,
                             message_id=data['message_id'])
    times = await db.get_available_times(data['month_id'], data['day_id'])
    logger.info(times)
    if times:
        mess = await call.message.answer(take_month.format(service_name=data['service_name'],
                                                           amount=data['price'],
                                                           discount=data['discount'],
                                                           service_time=data['service_time']),
                                         reply_markup=time_keyboard(times, data['day_of_week']))
        data['message_id'] = mess['message_id']

        await state.update_data(data=data)
        await Order.OrderTime.set()
    else:
        await call.message.answer(no_dates)
        await state.finish()


@dp.callback_query_handler(text="back", state=Order.OrderTime)
async def back_to_days(call: CallbackQuery, state: FSMContext):
    """ Назад к выбору дня """
    data = await state.get_data()
    logger.info(data)
    await bot.delete_message(chat_id=call.from_user.id,
                             message_id=data['message_id'])
    days = await db.get_available_days(data['month_id'])
    logger.info(days)
    if days['days']:
        mess = await call.message.answer(take_month.format(service_name=data['service_name'],
                                                           amount=data['price'],
                                                           discount=data['discount'],
                                                           service_time=data['service_time']),
                                         reply_markup=days_keyboard(days, data['month_id']))
        data['message_id'] = mess['message_id']

        await state.update_data(data=data)
        await Order.OrderDay.set()
    else:
        await call.message.answer(no_dates)
        await state.finish()


@dp.callback_query_handler(text="bonus_later", state=Order.Bonus)
@dp.callback_query_handler(time_data.filter(), state=Order.OrderTime)
async def select_time(call: CallbackQuery, state: FSMContext, callback_data: dict = None):
    """ Пользователь выбирает время """
    data = await state.get_data()
    logger.info(data)
    if await state.get_state() != "Order:Bonus":
        data['available_date_id'] = int(callback_data['time_id'])
        data['str_date'] = callback_data['datetime'].replace('-', ':') + " (" + callback_data['weekday'] + ")"

    await bot.delete_message(chat_id=call.from_user.id,
                             message_id=data['message_id'])
    bonus_balance = await db.get_bonus_balance(call.from_user.id)
    data['bonus_balance'] = bonus_balance['bonus_balance']
    cashback = await db.get_user_cashback(call.from_user.id)
    data['cashback'] = cashback['user_cashback']
    if bonus_balance['bonus_balance'] >= 500 and await state.get_state() != "Order:Bonus":
        mess = await call.message.answer(available_bonus.format(service_name=data['service_name'],
                                                                amount=data['price'],
                                                                service_time=data['service_time'],
                                                                discount=data['discount'],
                                                                date=data['str_date'],
                                                                bonus_amount=bonus_balance['bonus_balance']),
                                         reply_markup=select_bonus_markup)
        data['message_id'] = mess['message_id']

        await state.update_data(data=data)
        await Order.Bonus.set()
    else:

        logger.info(cashback['user_cashback'])
        data['get_bonus'] = int(((float(data['price']) * 1000) / 100) * data['cashback'])
        logger.info(data['get_bonus'])
        mess = await call.message.answer(no_available_bonus.format(service_name=data['service_name'],
                                                                   amount=data['price'],
                                                                   service_time=data['service_time'],
                                                                   discount=data['discount'],
                                                                   date=data['str_date'],
                                                                   get_bonus=data['get_bonus']),
                                         reply_markup=register_order_markup)
        data['message_id'] = mess['message_id']
        logger.info(data)
        await state.update_data(data=data)
        await Order.RegisterOrderWithoutBonus.set()


@dp.callback_query_handler(text="back", state=[Order.Bonus,
                                               Order.RegisterOrderWithoutBonus])
async def back_to_time(call: CallbackQuery, state: FSMContext):
    """ Назад к выбору времени """
    data = await state.get_data()
    logger.info(data)
    await bot.delete_message(chat_id=call.from_user.id,
                             message_id=data['message_id'])
    times = await db.get_available_times(data['month_id'], data['day_id'])
    logger.info(times)
    if times:
        mess = await call.message.answer(take_month.format(service_name=data['service_name'],
                                                           amount=data['price'],
                                                           discount=data['discount'],
                                                           service_time=data['service_time']),
                                         reply_markup=time_keyboard(times, data['day_of_week']))
        data['message_id'] = mess['message_id']

        await state.update_data(data=data)
        await Order.OrderTime.set()
    else:
        await call.message.answer(no_dates)
        await state.finish()


@dp.callback_query_handler(text="register_order", state=[Order.RegisterOrderWithoutBonus,
                                                         Order.RegisterOrderWithBonus])
async def register_order(call: CallbackQuery, state: FSMContext):
    """ Оформление заказа """
    data = await state.get_data()
    logger.info(data)
    await bot.delete_message(chat_id=call.from_user.id,
                             message_id=data['message_id'])
    if await state.get_state() == "Order:RegisterOrderWithoutBonus":
        order_data = {
            "telegram_id": int(call.from_user.id),
            "service_date_id": int(data['available_date_id']),
            "service_id": data['service_id'],
            "total_price": data['price'],
            "service_price": data['full_cost'],
            "discount": data['discount'],
            "discount_amount": data['discount'],
            "discount_amount_BYN": data['discount_BYN'],
            "bonus_discount": False,
            "bonus_discount_amount": 0,
            "bonus_discount_amount_BYN": 0,
            "bonus_points": data['get_bonus'],
            "service_name": data['service_name'],
            "service_time": data['service_time']
        }
    else:
        order_data = {
            "telegram_id": int(call.from_user.id),
            "service_date_id": int(data['available_date_id']),
            "service_id": data['service_id'],
            "total_price": data['price_with_bonus'],
            "service_price": data['full_cost'],
            "discount": data['discount'],
            "discount_amount": data['discount'],
            "discount_amount_BYN": data['discount_BYN'],
            "bonus_discount": True,
            "bonus_discount_amount": data['bonus_amount'],
            "bonus_discount_amount_BYN": data['bonus_amount_BYN'],
            "bonus_points": data['get_bonus'],
            "service_name": data['service_name'],
            "service_time": data['service_time']
        }
    logger.info(order_data)
    order = await db.register_order(order_data)
    if order['success']:
        if await state.get_state() == "Order:RegisterOrderWithoutBonus":
            await call.message.answer(register_order_tx.format(order_id=order['order_id'],
                                                               service_name=data['service_name'],
                                                               service_time=data['service_time'],
                                                               total_price=data['price'],
                                                               order_date=data['str_date'],
                                                               address=SERVICE_ADDRESS,
                                                               phone=ADMIN_PHONE_NUMBER))
            await bot.send_message(chat_id=ADMIN_ID,
                                   text=new_order_to_admin_tx.format(speaker_em=speaker_em,
                                                                     order_id=order['order_id'],
                                                                     service_name=data['service_name'],
                                                                     service_time=data['service_time'],
                                                                     total_price=data['price'],
                                                                     order_date=data['str_date'],
                                                                     discount=data['discount'],
                                                                     bonus_discount=order_data[
                                                                         'bonus_discount_amount']))
        else:
            await call.message.answer(register_order_with_bonus_tx.format(order_id=order['order_id'],
                                                                          service_name=data['service_name'],
                                                                          total_price=data['price_with_bonus'],
                                                                          bonus_amount=data['bonus_amount'],
                                                                          service_time=data['service_time'],
                                                                          order_date=data['str_date'],
                                                                          address=SERVICE_ADDRESS,
                                                                          phone=ADMIN_PHONE_NUMBER))
            await bot.send_message(chat_id=ADMIN_ID,
                                   text=new_order_with_bonus_to_admin_tx.format(speaker_em=speaker_em,
                                                                                order_id=order['order_id'],
                                                                                service_name=data['service_name'],
                                                                                total_price=data['price_with_bonus'],
                                                                                service_time=data['service_time'],
                                                                                order_date=data['str_date'],
                                                                                discount=data['discount'],
                                                                                bonus_discount=order_data[
                                                                                    'bonus_discount_amount']))
    else:
        await call.message.answer(order['error_message'])
    await state.finish()


@dp.callback_query_handler(text="bonus_now", state=Order.Bonus)
async def select_bonus(call: CallbackQuery, state: FSMContext):
    """ Страничка выбора доступного бонуса """
    data = await state.get_data()
    logger.info(data)
    await bot.delete_message(chat_id=call.from_user.id,
                             message_id=data['message_id'])
    mess = await call.message.answer(select_bonus_tx.format(service_name=data['service_name'],
                                                            amount=data['price'],
                                                            service_time=data['service_time'],
                                                            discount=data['discount'],
                                                            date=data['str_date'],
                                                            bonus_amount=data['bonus_balance']),
                                     reply_markup=get_bonus_keyboard(data['bonus_balance']))
    data['message_id'] = mess['message_id']

    await state.update_data(data=data)
    await Order.SelectBonus.set()


@dp.callback_query_handler(text="back", state=Order.SelectBonus)
async def back_to_bonus(call: CallbackQuery, state: FSMContext):
    """ Назад к выбору использования бонуса """
    data = await state.get_data()
    logger.info(data)
    await bot.delete_message(chat_id=call.from_user.id,
                             message_id=data['message_id'])
    mess = await call.message.answer(available_bonus.format(service_name=data['service_name'],
                                                            amount=data['price'],
                                                            service_time=data['service_time'],
                                                            discount=data['discount'],
                                                            date=data['str_date'],
                                                            bonus_amount=data['bonus_balance']),
                                     reply_markup=select_bonus_markup)
    data['message_id'] = mess['message_id']

    await state.update_data(data=data)
    await Order.Bonus.set()


@dp.callback_query_handler(bonus_data.filter(), state=Order.SelectBonus)
async def register_order_with_bonus(call: CallbackQuery, state: FSMContext, callback_data: dict):
    """ Оформление заказа с бонусной скидкой """
    data = await state.get_data()
    logger.info(data)
    await bot.delete_message(chat_id=call.from_user.id,
                             message_id=data['message_id'])
    logger.info(callback_data)
    data['bonus_amount'] = int(callback_data['amount'])
    data['bonus_amount_BYN'] = float(callback_data['byn_amount'])
    data['price_with_bonus'] = float(data['price']) - data['bonus_amount_BYN']
    data['get_bonus'] = int(((float(data['price_with_bonus']) * 1000) / 100) * data['cashback'])
    logger.info(data)
    mess = await call.message.answer(take_bonus_tx.format(service_name=data['service_name'],
                                                          amount=data['price_with_bonus'],
                                                          service_time=data['service_time'],
                                                          discount=data['discount'],
                                                          bonus_amount=data['bonus_amount'],
                                                          bonus_amount_BYN=data['bonus_amount_BYN'],
                                                          date=data['str_date'],
                                                          get_bonus=data['get_bonus']),
                                     reply_markup=register_order_markup)
    data['message_id'] = mess['message_id']
    await state.update_data(data=data)
    await Order.RegisterOrderWithBonus.set()


@dp.callback_query_handler(text='back', state=Order.RegisterOrderWithBonus)
async def back_to_select_bonus(call: CallbackQuery, state: FSMContext):
    """ Назад к выбору количества бонусных баллов, которыми будет оплачена часть заказа """
    data = await state.get_data()
    logger.info(data)
    await bot.delete_message(chat_id=call.from_user.id,
                             message_id=data['message_id'])
    mess = await call.message.answer(select_bonus_tx.format(service_name=data['service_name'],
                                                            amount=data['price'],
                                                            service_time=data['service_time'],
                                                            discount=data['discount'],
                                                            date=data['str_date'],
                                                            bonus_amount=data['bonus_balance']),
                                     reply_markup=get_bonus_keyboard(data['bonus_balance']))
    data['message_id'] = mess['message_id']

    del data['bonus_amount']
    del data['bonus_amount_BYN']
    del data['price_with_bonus']
    del data['get_bonus']
    logger.info(data)
    await state.finish()
    await state.update_data(data)
    await Order.SelectBonus.set()
