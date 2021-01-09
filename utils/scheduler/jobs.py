from loader import scheduler
from .instagram.photo import add_new_photo


def schedule_jobs():
    """Добавляем задачи в scheduler"""
    scheduler.add_job(add_new_photo, "cron", hour=00, minute=30)

