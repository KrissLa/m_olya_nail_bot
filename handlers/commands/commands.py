from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InputMediaPhoto, CallbackQuery
from loguru import logger

from data.config import SERVICE_ADDRESS, ADMIN_PHONE_NUMBER
from filters.orders import HasActiveOrders
from keyboards.default.menu import menu_keyboard
from keyboards.inline.bonuses import bonus_keyboard
from keyboards.inline.cancel import cancel_markup
from keyboards.inline.instagram import instagram_button
from keyboards.inline.orders import generate_services_keyboard, cancel_order_keyboard
from keyboards.inline.profile import change_profile_button
from loader import dp, db, bot
from states.orders import Order
from states.profile import Profile
from states.questions import Question
from texts.bonuses import bonus_tx
from texts.instagram import more_photo, instagram_link
from texts.my_orders import discounts_tx, my_order_tx, my_orders_empty_list_tx
from texts.orders import take_service, has_active_orders_tx
from texts.profile import profile_tx
from texts.question import question
from utils.chek_state import reset_state
from utils.date_format import date_formatting


@dp.callback_query_handler(text='cancel_2', state=[Profile.Name, Profile.Phone])
@dp.message_handler(text="Профиль", state="*")
async def get_user_profile(message: types.Message, state: FSMContext):
    """
    Вывод информацию о пользователе и кнопки для изменения профиля.
    :param message: Message
    :param state: FSMContext
    """
    if isinstance(message, types.Message):
        await reset_state(state, message)
    else:
        await message.message.edit_reply_markup()
    user_id = message.from_user.id
    data = await db.get_user_profile(user_id=user_id)
    if data['phone_number']:
        phone_number = "+375" + data['phone_number']
    else:
        phone_number = "Не указан"
    if data['referer']:
        referer = f"<i>Вас пригласил:</i> <b>{data['referer']['name']}</b>"
    else:
        referer = ""
    if isinstance(message, CallbackQuery):
        message = message.message
    mess = await message.answer(profile_tx.format(telegram_id=data['telegram_id'],
                                                  name=data['name'],
                                                  phone_number=phone_number,
                                                  personal_bonus_lvl=data['personal_cashback_level'],
                                                  referral_bonus_lvl=data['referral_cashback_level'],
                                                  bonus_balance=data['bonus_balance'],
                                                  frozen_balance=data['frozen_balance'],
                                                  referer=referer),
                                reply_markup=change_profile_button)
    await state.update_data(message_id=mess['message_id'])
    await Profile.Info.set()


@dp.message_handler(text="Примеры работ", state=["*"])
async def get_work_examples(message: types.Message, state: FSMContext):
    """Отправляем последние 5 фотографий и ссылку на инстаграм"""
    await reset_state(state, message)
    recent_photos = await db.get_instagram_pictures()
    media = [InputMediaPhoto(photo_url) for photo_url in recent_photos]
    await bot.send_media_group(message.from_user.id, media)
    await message.answer(more_photo, reply_markup=menu_keyboard)


@dp.message_handler(text="Instagram", state=['*'])
async def get_instagram_link(message: types.Message, state: FSMContext):
    """Отправляем кнопку с ссылкой на инстаграм"""
    await reset_state(state, message)
    await message.answer(instagram_link, reply_markup=instagram_button)


@dp.message_handler(text="Задать вопрос", state=['*'])
async def ask_a_question(message: types.Message, state: FSMContext):
    """Пользователь нажимает на кнопку задать вопрос"""
    await reset_state(state, message)
    mess = await message.answer(question, reply_markup=cancel_markup)
    await state.update_data(message_id=mess['message_id'])
    await Question.WaitQuestion.set()


@dp.message_handler(HasActiveOrders(), text="Заказать", state="*")
async def has_active_orders(message: types.Message, state: FSMContext):
    """ Запрещаем делать заказ """
    await reset_state(state, message)
    await message.answer(has_active_orders_tx)


@dp.message_handler(text="Заказать", state=['*'])
async def order_service(message: types.Message, state: FSMContext):
    """Пользователь нажимает на кнопку заказать"""
    await reset_state(state, message)
    services = await db.get_services()
    if services:
        mess = await message.answer(take_service,
                                    reply_markup=generate_services_keyboard(services))
        await state.update_data(message_id=mess['message_id'])
        await Order.OrderService.set()
    else:
        await message.answer("Извините, сейчас нет доступных услуг")


@dp.message_handler(text="Бонусы", state="*")
async def show_bonuses(message: types.Message, state: FSMContext):
    """ Нажатие на кнопку 'Бонусы' """
    await reset_state(state, message)
    bonus_data = await db.get_bonus(message.from_user.id)
    bot_user = await dp.bot.get_me()
    await message.answer(bonus_tx.format(personal_bonus_lvl=bonus_data['personal_lvl'],
                                         personal_value=bonus_data['personal_value'],
                                         personal_count=bonus_data['personal_orders_left'],
                                         referral_bonus_lvl=bonus_data['referral_lvl'],
                                         referral_value=bonus_data['referral_value'],
                                         referral_count=bonus_data['referral_orders_left'],
                                         bonus_balance=bonus_data['bonus_balance'],
                                         frozen_balance=bonus_data['frozen_balance'],
                                         bot_username=bot_user.username,
                                         user_id=message.from_user.id),
                         reply_markup=bonus_keyboard)


@dp.message_handler(text="Заказы", state="*")
async def get_active_orders(message: types.Message, state: FSMContext):
    """ Выводим список активных заказов пользователя """
    await reset_state(state, message)
    orders = await db.get_active_orders(message.from_user.id)
    logger.info(orders)
    if orders:
        mess_orders = []
        for o in orders:
            service_date = date_formatting(o['service_date']['date'])
            if o['discounts']:
                discounts = discounts_tx(o['discounts'])
            else:
                discounts = ""
            mess = await message.answer(my_order_tx.format(order_id=o['id'],
                                                           service_name=o['service_name'],
                                                           service_date=service_date,
                                                           service_time=o['service_time'],
                                                           discounts=discounts,
                                                           bonus_points=o['bonus_points'],
                                                           total_price=o['total_price'],
                                                           address=SERVICE_ADDRESS,
                                                           phone=ADMIN_PHONE_NUMBER),
                                        reply_markup=cancel_order_keyboard(o['id']))
            mess_orders.append(mess['message_id'])
        await state.update_data(mess_orders=mess_orders)
        await Order.CancelOrder.set()
    else:
        await message.answer(my_orders_empty_list_tx)
