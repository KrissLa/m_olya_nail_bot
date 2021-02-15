from texts.emoji import pensive_em, success_em, error_em

take_service = """
Пожалуйста, выберите услугу.
"""

take_month = """
<i>Вы выбрали:</i> <b>{service_name}</b>.
<i>Стоимость:</i> <b>{amount} BYN</b>.
<i>Время выполнения:</i> <b>{service_time}</b>.
<i>Скидка:</i> <b>{discount} %</b>.
Пожалуйста, выберите дату и время.
"""

no_dates = f"""
Извините, сейчас нет свободных дат. {pensive_em}
"""

available_bonus = """
<i>Вы выбрали:</i> <b>{service_name}</b>.
<i>Стоимость:</i> <b>{amount} BYN</b>.
<i>Время выполнения:</i> <b>{service_time}</b>.
<i>Скидка:</i> <b>{discount}%</b>.
<i>Дата:</i> <b>{date}</b>.
У Вас есть <b>{bonus_amount}</b> бонусных баллов. Хотите использовать их сейчас?
"""

select_bonus_tx = """
<i>Вы выбрали:</i> <b>{service_name}</b>.
<i>Стоимость:</i> <b>{amount} BYN</b>.
<i>Время выполнения:</i> <b>{service_time}</b>.
<i>Скидка:</i> <b>{discount}%</b>.
<i>Дата:</i> <b>{date}</b>.
<i>Доступно:</i> <b>{bonus_amount} ББ</b>.
Пожалуйста, выберите какую часть заказа Вы хотите оплатить бонусными баллами.
"""

no_available_bonus = """
<i>Вы выбрали:</i> <b>{service_name}</b>.
<i>Стоимость:</i> <b>{amount} BYN</b>.
<i>Время выполнения:</i> <b>{service_time}</b>.
<i>Скидка:</i> <b>{discount} %</b>.
<i>Дата:</i> <b>{date}</b>.
После завершения заказа Вам будет начислено <b>{get_bonus}</b> бонусных баллов.
"""

take_bonus_tx = """
<i>Вы выбрали:</i> <b>{service_name}</b>.
<i>Стоимость:</i> <b>{amount} BYN</b>.
<i>Время выполнения:</i> <b>{service_time}</b>.
<i>Скидка:</i> <b>{discount} %</b>.
<i>Оплата бонусными баллами:</i> <b>{bonus_amount} ББ ({bonus_amount_BYN} BYN)</b>
<i>Дата:</i> <b>{date}</b>.
После завершения заказа Вам будет начислено <b>{get_bonus}</b> бонусных баллов.
"""


register_order_tx = """
Спасибо! Ваш заказ № <b>{order_id}</b> принят. Вы можете найти его в разделе "Заказы".
Информация о заказе:
<b>{service_name}</b>.
<i>Стоимость:</i> <b>{total_price} BYN</b>.
<i>Время выполнения:</i> <b>{service_time}</b>.
<i>Дата:</i> <b>{order_date}</b>.
<i>Адрес:</i> {address}.
"""

new_order_to_admin_tx = """
{speaker_em} <b>Новый заказ № {order_id}!</b>
Информация о заказе:
<b>{service_name}</b>.
<i>Стоимость:</i> <b>{total_price} BYN</b>.
<i>Время выполнения:</i> <b>{service_time}</b>.
<i>Дата:</i> <b>{order_date}</b>.
<i>Акционная скидка:</i> <b>{discount} %</b>.
<i>Бонусная скидка:</i> <b>{bonus_discount} ББ</b>
"""

register_order_with_bonus_tx = """
Спасибо! Ваш заказ № <b>{order_id}</b> принят. Вы можете найти его в разделе "Заказы".
Информация о заказе:
<b>{service_name}</b>.
<i>Стоимость:</i> <b>{total_price} BYN</b>.
<i>Использовано бонусных баллов:</i> <b>{bonus_amount} ББ</b>
<i>Время выполнения:</i> <b>{service_time}</b>.
<i>Дата:</i> <b>{order_date}</b>.
<i>Адрес:</i> {address}.
"""

new_order_with_bonus_to_admin_tx = """
{speaker_em} <b>Новый заказ № {order_id}!</b>
Информация о заказе:
<b>{service_name}</b>.
<i>Стоимость:</i> <b>{total_price} BYN</b>.
<i>Время выполнения:</i> <b>{service_time}</b>.
<i>Дата:</i> <b>{order_date}</b>.
<i>Акционная скидка:</i> <b>{discount} %</b>.
<i>Бонусная скидка:</i> <b>{bonus_discount} ББ</b>
"""

order_completed_to_user_tx = """
Спасибо! Ваш заказ № {order_id} успешно завершен! {blush_em}
Вам начислено {bonus_amount} бонусных баллов.
Пожалуйста, оцените работу мастера. 
(В данный момент оценки и отзывы видны только администраторам, и используются для улучшения качества работы)
"""

add_rating_tx = f"""
{success_em} Оценка добавлена! 
Пожалуйста, напишите отзыв одним сообщением)
"""

thanks_tx = f"""
{success_em} Спасибо за Ваш отзыв!
"""

has_active_orders_tx = f"""
{error_em} У вас уже есть активная запись. Вы сможете сделать новый заказ только после завершения или отмены текущего. 
"""
