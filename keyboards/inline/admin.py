from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas.orders import admin_detail_data, admin_order_complete, admin_order_cancel, \
    admin_order_confirm, order_rating, rating_viewed, review_viewed
from keyboards.inline.orders import back_button
from texts.emoji import star_em


def admin_keyboard(events):
    """ Клавиатура для админки """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f'Заказы ({events["orders_number"]})',
                callback_data='admin_orders'
            )
        ],
        [
            InlineKeyboardButton(
                text=f'Вопросы ({events["questions_number"]})',
                callback_data='admin_questions'
            )
        ],
        [
            InlineKeyboardButton(
                text=f'Отзывы ({events["reviews_number"]})',
                callback_data='admin_reviews'
            )
        ],
        [
            InlineKeyboardButton(
                text=f'Оценки ({events["ratings_number"]})',
                callback_data='admin_rating'
            )
        ],
        [
            back_button
        ]

    ])


def order_min_keyboard(order):
    """ Клавиатура для списка с заказами """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Подробнее',
                callback_data=admin_detail_data.new(order_id=order['order_id'])
            )
        ]
    ])


def order_keyboard(order_id):
    """ Клавиатура для действий с закозом """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f'Подтвердить завершение заказа № {order_id}',
                callback_data=admin_order_complete.new(order_id=order_id)
            )
        ],
        [
            InlineKeyboardButton(
                text=f'Отменить заказ № {order_id}',
                callback_data=admin_order_cancel.new(order_id=order_id)
            )
        ],
        [
            back_button
        ]
    ])


def order_confirmation_keyboard(order_id):
    """ Клавиатура с подтверждением завершения заказа """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f'Заказ № {order_id} завершен',
                callback_data=admin_order_confirm.new(order_id=order_id)
            )
        ],
        [
            back_button
        ]
    ])


back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        back_button
    ]
])


def viewed_rating_keyboard(order_id):
    """" Кнопка, которая отмечает оценку просмотренной """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Просмотрено',
                callback_data=rating_viewed.new(order_id=order_id)
            )
        ]
    ])


def viewed_review_keyboard(order_id):
    """" Кнопка, которая отмечает оценку просмотренной """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Просмотрено',
                callback_data=review_viewed.new(order_id=order_id)
            )
        ]
    ])


user_cancel_order__to_admin_tx = """
{speaker_em} Пользователь отменил заказ № {order_id}.
Дата {service_date} снова свободна!
"""
