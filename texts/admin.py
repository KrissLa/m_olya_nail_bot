from texts.emoji import error_em

hello_admin = """
Добро пожаловать в панель администратора!
"""

order_min_tx = """
Заказ № <b>{order_id}</b>.
Дата: <b>{str_date}</b>.
"""

order_min_complete_tx = """
Это все активные заказы на данный момент. Они отсортированы по времени.
Чтобы вернуться в административную панель, нажмите \"Назад\"
"""

order_detail_tx = """
Заказ № <b>{order_id}</b>
Дата: <b>{order_date}</b>.
Название услуги: <b>{service_name}</b>.
Полная стоимость: <b>{service_price}</b>.
Итоговая стоимость: <b>{total_price}</b>.
Акционная скидка: <b>{discount}</b>.
Бонусная скидка: <b>{bonus_discount}</b>.
Статус заказа: <b>{order_status}</b>.

    Пользователь:
    telegramID: <b>{telegram_id}</b>
    telegram username: <b>{username}</b>
    Имя пользователя : <b>{name}</b>
    Номер телефона : <b>{phone_number}</b>
"""

cancel_order_tx = """
Для отмены заказа, пожалуйста, укажите причину отмены. Она будет отправлена пользователю.
"""

cancel_order_to_user_tx = """
{error_em} Ваш заказ № <b>{order_id}</b> отменен администратором.
Причина:
    {reason}
"""

order_is_cancelled_tx = """
{success_em} Заказ № {order_id} успешно отменен!
"""

order_already_cancelled_tx = f"""
{error_em} Этот заказ уже отменен!
"""

confirm_order_tx = """
Пожалуйста, подтвердите завершение заказа.
"""

confirm_order_success_tx = """
{success_em} Заказ № {order_id} успешно завершен!
"""

confirm_order_error_cancelled_tx = """
{error_em} Ошибка! Заказ № {order_id} отменен!
"""

confirm_order_error_already_tx = """
{error_em} Ошибка! Заказ № {order_id} уже подтвержден!
"""

new_rating_tx = """
{speaker_em} Новая оценка заказа № {order_id}!
Оценка: {rating}
"""

new_review_tx = """
{speaker_em} Новый отзыв к заказу № {order_id}!
Отзыв: 
    {review}
"""

rating_tx = """
Оценка к заказу № {order_id}.
Название услуги: {service_name}.
Дата: {service_date}.
Оценка: {rating}.
"""

review_tx = """
Отзыв к заказу № {order_id}.
Название услуги: {service_name}.
Дата: {service_date}.
Отзыв: {review}.
"""

back_to_menu_tx = """
Нажмите "назад" чтобы вернуться в меню.
"""
