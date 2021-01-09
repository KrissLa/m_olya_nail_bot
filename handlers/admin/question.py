from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from loguru import logger

from keyboards.inline.callback_datas.questions import question_data
from keyboards.inline.cancel import cancel_button
from loader import dp, bot, db
from states.questions import Question
from texts.question import answer


@dp.callback_query_handler(question_data.filter(), state=['*'])
async def answer_the_question(call: CallbackQuery, state: FSMContext, callback_data: dict):
    """ Нажимаем кнопку для ответа на вопрос """
    await call.message.edit_reply_markup()
    mess = await call.message.answer(answer, reply_markup=cancel_button)
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
    await state.finish()
    await db.answer_the_question(data)
    await state.finish()
