from data.config import ADMIN_ID, SERVICE_ADDRESS
from loader import db, bot
from texts.emoji import speaker_em, success_em, error_em
from texts.notification import notification_tx
from utils.date_format import date_for_notification, time_for_notification


async def send_notifications():
    """ Отправляем напоминание пользователям о заказах """
    ok = 0
    not_ok = 0
    orders = await db.get_orders_for_notifications()
    for o in orders:
        try:
            await bot.send_message(chat_id=o['user']['telegram_id'],
                                   text=notification_tx.format(name=o['user']['name'],
                                                               service_name=o['service_name'],
                                                               date=date_for_notification(o['service_date']['date']),
                                                               address=SERVICE_ADDRESS,
                                                               time=time_for_notification(o['service_date']['date'])))
        except Exception:
            not_ok += 1
        else:
            await db.notification_was_sent(o['id'])
            ok += 1
    if ok or not_ok:
        await bot.send_message(ADMIN_ID, f"{speaker_em} Отправлены напоминания пользователям!\n"
                                         f"{success_em} Успешно: {ok}\n"
                                         f"{error_em} Ошибки: {not_ok}")
