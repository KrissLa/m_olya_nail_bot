from loader import scheduler
from .instagram.photo import add_new_photo
from .notifications.user_notifications import send_notifications


def schedule_jobs():
    """Добавляем задачи в scheduler"""
    scheduler.add_job(add_new_photo, "cron", hour=00, minute=30)
    scheduler.add_job(send_notifications, "cron", hour=13, minute=30)

