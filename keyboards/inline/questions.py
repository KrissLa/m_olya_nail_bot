from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger

from .callback_datas.questions import question_data


def keyboard_for_answer(telegram_id, question_id):
    """ Клавиатура для ответа на вопрос """
    logger.info(telegram_id)
    logger.info(question_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f'Ответить на вопрос № {question_id}',
                callback_data=question_data.new(telegram_id=telegram_id,
                                                question_id=question_id)
            )
        ]
    ])
