import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.admin import viewed_rating_keyboard, back_keyboard, viewed_review_keyboard
from loader import dp, db
from states.admin import Admin
from texts.admin import rating_tx, back_to_menu_tx, review_tx
from texts.emoji import star_em


@dp.callback_query_handler(text="admin_rating", state=Admin.Main)
async def get_ratings_list(call: CallbackQuery, state: FSMContext):
    """ Получаем список новых оценок """
    await call.message.delete()
    ratings = await db.get_ratings_list()
    messages = []
    for r in ratings:
        mess = await call.message.answer(rating_tx.format(order_id=r['order_id'],
                                                          service_name=r['service_name'],
                                                          service_date=r['service_date'],
                                                          rating=int(r['rating']) * star_em),
                                         reply_markup=viewed_rating_keyboard(order_id=r['order_id']))
        messages.append(mess['message_id'])
        await asyncio.sleep(.05)
    mess = await call.message.answer(back_to_menu_tx,
                                     reply_markup=back_keyboard)
    messages.append(mess['message_id'])
    await state.update_data(messages=messages)
    await Admin.OrderMinList.set()


@dp.callback_query_handler(text="admin_reviews", state=Admin.Main)
async def get_reviews_list(call: CallbackQuery, state: FSMContext):
    """ Получаем список новых отзывов """
    await call.message.delete()
    reviews = await db.get_reviews_list()
    messages = []
    for r in reviews:
        mess = await call.message.answer(review_tx.format(order_id=r['order_id'],
                                                          service_name=r['service_name'],
                                                          service_date=r['service_date'],
                                                          review=r['review']),
                                         reply_markup=viewed_review_keyboard(order_id=r['order_id']))
        messages.append(mess['message_id'])
        await asyncio.sleep(.05)
    mess = await call.message.answer(back_to_menu_tx,
                                     reply_markup=back_keyboard)
    messages.append(mess['message_id'])
    await state.update_data(messages=messages)
    await Admin.OrderMinList.set()
