my_orders_empty_list_tx = """
У Вас сейчас нет активных заказов.
"""

my_order_tx = """
<i>Номер заказа:</i> <b>{order_id}</b>.
<i>Название услуги:</i> <b>{service_name}</b>.
<i>Дата:</i> <b>{service_date}</b>.
<i>Время работы:</i> <b>{service_time}</b>.{discounts}
<i>После завершения будет начислено</i> <b>{bonus_points}</b> ББ.
<i>Итоговая стоимость:</i> <b>{total_price} BYN</b>.
"""

cancel_order_user_tx = """
Вы действительно хотите отменить заказ № {order_id}?
"""


def discounts_tx(discounts, percent=None, bonus=None):
    """ Формируем часть сообщения, в котором расписаны скидки """
    for d in discounts:
        if d['type'] == "percent":
            percent = f"\n<i>Скидка:</i> <b>{d['discount_amount']}% ({d['discount_amount_BYN']} BYN)</b>."
        else:
            bonus = f"\n<i>Использовано бонусных баллов:</i> <b>{d['discount_amount']} ББ (-{d['discount_amount_BYN']} BYN)</b>."
    if percent and bonus:
        return percent + bonus
    elif percent:
        return percent
    else:
        return bonus


success_cancel_order_tx = """
{success_em} Заказ № {order_id} отменен!
"""