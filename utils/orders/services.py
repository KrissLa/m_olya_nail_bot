from loguru import logger

ORDER_STATUSES = {
    "wait": "Оформлен, Ожидает завершения",
    "completed": "Завершен",
    "canceled": "Отменен",
}


def get_order_discounts(order):
    """ Получаем значение акционной скидки """
    discount, bonus_discount = 0, 0
    if len(order['discounts']) > 0:
        for o in order['discounts']:
            if o['type'] == 'percent':
                discount = f'{o["discount_amount"]} % ({o["discount_amount_BYN"]} BYN)'
            elif o['type'] == 'points':
                bonus_discount = f'{o["discount_amount"]} ББ ({o["discount_amount_BYN"]} BYN)'
    return {'discount': discount,
            'bonus_discount': bonus_discount}
