from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from loguru import logger

from data.config import ADMIN_ID
from keyboards.inline.admin import viewed_rating_keyboard, viewed_review_keyboard
from keyboards.inline.callback_datas.orders import order_rating
from keyboards.inline.cancel import cancel_markup
from loader import dp, bot, db
from states.orders import Order
from texts.admin import new_rating_tx, new_review_tx
from texts.emoji import star_em, speaker_em
from texts.orders import add_rating_tx, thanks_tx


@dp.callback_query_handler(text='cancel_rating', state='*')
async def cancel_rating(call: CallbackQuery):
    """ Пользователь отменяет оценку заказа """
    await call.answer("Готово")
    await call.message.delete()


@dp.callback_query_handler(order_rating.filter(), state="*")
async def get_order_rating(call: CallbackQuery, state: FSMContext, callback_data: dict):
    """ Пользователь ставить оценку заказу """
    logger.info(callback_data)
    await db.add_rating(int(callback_data['order_id']), int(callback_data['rating']))
    await call.message.delete()
    mess = await call.message.answer(add_rating_tx,
                                     reply_markup=cancel_markup)
    await bot.send_message(chat_id=ADMIN_ID, text=new_rating_tx.format(speaker_em=speaker_em,
                                                                       order_id=callback_data['order_id'],
                                                                       rating=int(callback_data['rating']) * star_em),
                           reply_markup=viewed_rating_keyboard(order_id=int(callback_data['order_id'])))
    await state.update_data(order_id=int(callback_data['order_id']),
                            message_id=mess['message_id'])
    await Order.WaitReview.set()


@dp.callback_query_handler(text='cancel', state=Order.WaitReview)
async def cancel_review(call: CallbackQuery, state: FSMContext):
    """ Отмена написания отзыва """
    await call.answer("Отменено")
    await call.message.delete()
    await state.finish()


@dp.message_handler(state=Order.WaitReview)
async def get_review(message: Message, state: FSMContext):
    """ Получаем отзыв """
    review = message.text
    data = await state.get_data()
    await db.add_review(order_id=data['order_id'], review=review)
    await bot.delete_message(message.from_user.id, data['message_id'])
    await message.answer(thanks_tx)
    await bot.send_message(ADMIN_ID, new_review_tx.format(speaker_em=speaker_em,
                                                          order_id=data['order_id'],
                                                          review=review),
                           reply_markup=viewed_review_keyboard(order_id=data['order_id']))
    await state.finish()
