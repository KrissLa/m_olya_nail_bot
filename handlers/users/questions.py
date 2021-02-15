from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data.config import ADMIN_ID
from keyboards.default.menu import menu_keyboard
from keyboards.inline.questions import keyboard_for_answer
from loader import dp, db, bot
from states.orders import Order
from states.questions import Question
from texts.emoji import speaker_em
from texts.question import get_message_after_question, question_to_admin


@dp.message_handler(state=Question.WaitQuestion)
async def get_question(message: types.Message, state: FSMContext):
    """Получаем вопрос пользователя"""
    question = message.text
    answer = await db.ask_a_question(data={
        "question": question,
        "telegram_id": message.from_user.id,
    })
    await message.answer(get_message_after_question(answer),
                         reply_markup=menu_keyboard)
    await bot.send_message(chat_id=ADMIN_ID,
                           text=question_to_admin.format(speaker_em=speaker_em,
                                                         question_id=answer["question_id"],
                                                         username=message.from_user.full_name,
                                                         question=question),
                           reply_markup=keyboard_for_answer(telegram_id=message.from_user.id,
                                                            question_id=answer["question_id"]))
    data = await state.get_data()
    await bot.edit_message_reply_markup(chat_id=message.from_user.id,
                                        message_id=data['message_id'],
                                        reply_markup=None)

    await state.finish()


@dp.callback_query_handler(text='cancel', state=[Question.WaitQuestion,
                                                 Question.WaitAnswer,
                                                 Order.OrderService,
                                                 Order.RegisterOrderWithoutBonus,
                                                 Order.RegisterOrderWithBonus])
async def cancel_question(call: CallbackQuery, state: FSMContext):
    """ Отмена отправки вопроса"""
    data = await state.get_data()
    await call.answer('Отменено')
    await bot.delete_message(chat_id=call.from_user.id,
                             message_id=data['message_id'])
    await state.finish()
