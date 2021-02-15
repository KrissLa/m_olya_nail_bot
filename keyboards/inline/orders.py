from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger

from keyboards.inline.callback_datas.orders import order_service, month_data, day_data, time_data, bonus_data, \
    order_rating, user_order_cancel, user_order_cancel_confirm, user_back_to_order
from keyboards.inline.cancel import cancel_button
from texts.emoji import star_em
from utils.orders.price import get_price_with_discount, rounding

MONTHS = {
    '1': "Январь",
    '2': "Февраль",
    '3': "Март",
    '4': "Апрель",
    '5': "Май",
    '6': "Июнь",
    '7': "Июль",
    '8': "Август",
    '9': "Сентябрь",
    '10': "Октябрь",
    '11': "Ноябрь",
    '12': "Декабрь",
}

MONTHS_DAY = {
    '1': "Января",
    '2': "Февраля",
    '3': "Марта",
    '4': "Апреля",
    '5': "Мая",
    '6': "Июня",
    '7': "Июля",
    '8': "Августа",
    '9': "Сентября",
    '10': "Октября",
    '11': "Ноября",
    '12': "Декабря",
}

WEEKDAYS = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']

back_button = InlineKeyboardButton(
    text='Назад',
    callback_data="back"
)

register_order_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Оформить заказ',
            callback_data='register_order'
        )
    ],
    [
        back_button
    ],
    [
        cancel_button
    ]

])

select_bonus_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Использовать сейчас',
            callback_data='bonus_now'
        )
    ],
    [
        InlineKeyboardButton(
            text='Продолжить копить',
            callback_data='bonus_later'
        )
    ],
    [
        back_button
    ]

])


def _get_bonus_button(bonus: int):
    """ Генерируем кнопку для выбора бонуса"""
    byn_amount = bonus / 1000
    return InlineKeyboardButton(
        text=f'{bonus} ББ ({byn_amount} BYN)',
        callback_data=bonus_data.new(amount=bonus,
                                     byn_amount=byn_amount)
    )


def get_bonus_keyboard(bonus_balance: int):
    """ Генерируем клавиатуру для выбора бонусной скидки """
    buttons = []
    first_line = [_get_bonus_button(500), _get_bonus_button(1000)]
    second_line = [_get_bonus_button(1500), _get_bonus_button(2000)]
    third_line = [_get_bonus_button(2500), _get_bonus_button(3000)]
    fourth_line = [_get_bonus_button(3500), _get_bonus_button(4000)]
    fifth_line = [_get_bonus_button(4500), _get_bonus_button(5000)]
    if bonus_balance < 1000:
        buttons.append([_get_bonus_button(500)])
    elif bonus_balance < 1500:
        buttons.append(first_line)
    elif bonus_balance < 2000:
        buttons.append(first_line)
        buttons.append([_get_bonus_button(1500)])
    elif bonus_balance < 2500:
        buttons.append(first_line)
        buttons.append(second_line)
    elif bonus_balance < 3000:
        buttons.append(first_line)
        buttons.append(second_line)
        buttons.append([_get_bonus_button(2500)])
    elif bonus_balance < 3500:
        buttons.append(first_line)
        buttons.append(second_line)
        buttons.append(third_line)
    elif bonus_balance < 4000:
        buttons.append(first_line)
        buttons.append(second_line)
        buttons.append(third_line)
        buttons.append([_get_bonus_button(3500)])
    elif bonus_balance < 4500:
        buttons.append(first_line)
        buttons.append(second_line)
        buttons.append(third_line)
        buttons.append(fourth_line)
    elif bonus_balance < 5000:
        buttons.append(first_line)
        buttons.append(second_line)
        buttons.append(third_line)
        buttons.append(fourth_line)
        buttons.append([_get_bonus_button(4500)])
    else:
        buttons.append(first_line)
        buttons.append(second_line)
        buttons.append(third_line)
        buttons.append(fourth_line)
        buttons.append(fifth_line)

    keyboard = InlineKeyboardMarkup(row_width=2, inline_keyboard=buttons)
    keyboard.add(back_button)
    return keyboard


def time_keyboard(times, day_of_week):
    """ Генерируем клавиатуру со временем"""
    keyboard = InlineKeyboardMarkup()
    for t in times:
        button = InlineKeyboardButton(
            text=t['date'].replace('-', ':'),
            callback_data=time_data.new(time_id=t['available_date_id'],
                                        datetime=str(t['date']),
                                        weekday=WEEKDAYS[day_of_week])
        )
        keyboard.add(button)
    keyboard.add(back_button)
    return keyboard


def days_keyboard(days, month):
    """ Генерируем клавиатуру с днями в месяце """
    keyb = []
    max = len(days['days'])
    num = 1
    line_list = []
    for day in days['days']:
        button = InlineKeyboardButton(
            text=f'{day["day"]} {MONTHS_DAY[f"{month}"]} ({WEEKDAYS[day["day_of_week"]]})',
            callback_data=day_data.new(day_id=day['day'],
                                       day_of_week=day["day_of_week"])
        )
        line_list.append(button)
        if num % 2 == 0:
            keyb.append(line_list)
            line_list = []
        elif num == max:
            keyb.append(line_list)
        num += 1
    keyboard = InlineKeyboardMarkup(row_width=2, inline_keyboard=keyb)
    keyboard.add(back_button)
    return keyboard


def mont_keyboard(months):
    """ Генерируем клавиатуру с месяцами, в которых есть свободные даты"""
    keyboard = InlineKeyboardMarkup()
    for mon in months['months']:
        button = InlineKeyboardButton(
            text=MONTHS[f'{mon}'],
            callback_data=month_data.new(month_id=mon)
        )
        keyboard.add(button)
    keyboard.add(back_button)
    return keyboard


def generate_services_keyboard(services):
    """Формируем клавиатуру с услугами"""
    keyboard = InlineKeyboardMarkup()
    for ser in services:
        prices = _get_prices(ser)
        data = _get_keyboard_data(prices, ser)
        button = InlineKeyboardButton(
            text=data['text'],
            callback_data=order_service.new(service_id=ser['id'],
                                            price=data['price'],
                                            time=ser['time'],
                                            discount_BYN=prices['discount_BYN'])
        )
        keyboard.add(button)

    keyboard.add(InlineKeyboardButton(
        text='Отмена',
        callback_data="cancel"
    ))

    return keyboard


def _get_prices(data):
    """Формируем текст на кнопке"""
    if data['discount']:
        con_price = get_price_with_discount(data['price'], data['discount_amount'])
        discount_BYN = rounding(data['price'] - con_price, 2)
        logger.info(con_price)
        return {
            'price': data['price'],
            'con_price': con_price,
            "discount_BYN": discount_BYN
        }
    return {
        'price': data['price'],
        "discount_BYN": 0
    }


def _get_keyboard_data(data, service):
    """Получаем данные для кнопки"""
    if 'con_price' in data.keys():
        return {
            'text': f"{service['name']} {data['con_price']} BYN (-{service['discount_amount']}%) {service['time']}",
            'price': data['con_price']
        }
    return {
        'text': f"{service['name']} {data['price']} BYN ({service['time']})",
        'price': data['price']
    }


def rating_keyboard(order_id):
    """ Клавиатура для оценки заказа """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f'{star_em}',
                callback_data=order_rating.new(order_id=order_id, rating=1)
            ),
            InlineKeyboardButton(
                text=f'{star_em * 2}',
                callback_data=order_rating.new(order_id=order_id, rating=2)
            ),
            InlineKeyboardButton(
                text=f'{star_em * 3}',
                callback_data=order_rating.new(order_id=order_id, rating=3)
            )
        ],
        [
            InlineKeyboardButton(
                text=f'{star_em * 4}',
                callback_data=order_rating.new(order_id=order_id, rating=4)
            ),
            InlineKeyboardButton(
                text=f'{star_em * 5}',
                callback_data=order_rating.new(order_id=order_id, rating=5)
            ),
        ],
        [
            InlineKeyboardButton(
                text='Не хочу',
                callback_data="cancel_rating"
            )
        ]
    ])


def cancel_order_keyboard(order_id):
    """ Клавиатура для отмены заказа пользователем """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f"Отменить заказ № {order_id}",
                callback_data=user_order_cancel.new(order_id=order_id)
            )
        ]
    ])


def confirm_cancel_order_keyboard(order_id):
    """ Клавиатура с подтверждением отмены заказа """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f"Да, отменить заказ № {order_id}",
                callback_data=user_order_cancel_confirm.new(order_id=order_id)
            )
        ],
        [
            InlineKeyboardButton(
                text="Нет, назад",
                callback_data=user_back_to_order.new(order_id=order_id)
            )
        ]
    ])

