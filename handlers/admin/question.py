import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from loguru import logger

from keyboards.inline.admin import back_keyboard
from keyboards.inline.callback_datas.questions import question_data
from keyboards.inline.cancel import cancel_markup
from keyboards.inline.questions import keyboard_for_answer
from loader import dp, bot, db
from states.admin import Admin
from states.questions import Question
from texts.admin import back_to_menu_tx
from texts.emoji import speaker_em
from texts.question import answer, answer_to_user, answer_to_admin, answer_to_admin_error, question_to_admin


@dp.callback_query_handler(question_data.filter(), state=['*'])
async def answer_the_question(call: CallbackQuery, state: FSMContext, callback_data: dict):
    """ Нажимаем кнопку для ответа на вопрос """
    await call.message.edit_reply_markup()
    mess = await call.message.answer(answer, reply_markup=cancel_markup)
    callback_data['message_id'] = mess['message_id']
    await state.update_data(data=callback_data)
    await Question.WaitAnswer.set()


@dp.message_handler(state=Question.WaitAnswer)
async def get_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    await bot.edit_message_reply_markup(chat_id=message.from_user.id,
                                        message_id=data['message_id'],
                                        reply_markup=None)
    data = {
        "question_id": data['question_id'],
        'answer': message.text
    }
    answer = await db.answer_the_question(data)
    try:
        await bot.send_message(answer['telegram_id'], answer_to_user.format(question_id=answer['question_id'],
                                                                            question=answer['question'],
                                                                            answer=answer['answer']))
        await message.answer(answer_to_admin)
    except Exception as e:
        await message.answer(answer_to_admin_error)
    await state.finish()


@dp.callback_query_handler(text="admin_questions", state=Admin.Main)
async def get_questions_list(call: CallbackQuery, state: FSMContext):
    """ Получаем список вопросов """
    await call.message.delete()
    questions = await db.get_questions_list()
    messages = []
    for q in questions:
        mess = await call.message.answer(text=question_to_admin.format(speaker_em=speaker_em,
                                                                       question_id=q["question_id"],
                                                                       username=q['user_name'],
                                                                       question=q['question']),
                                         reply_markup=keyboard_for_answer(telegram_id=q['user_tg_id'],
                                                                          question_id=q["question_id"]))
        messages.append(mess['message_id'])
        await asyncio.sleep(.05)
    await state.update_data(messages=messages)
    await Admin.OrderMinList.set()
