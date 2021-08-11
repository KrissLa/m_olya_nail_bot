from aiogram import executor

from loguru import logger
import filters
import loader
import middlewares
from data.config import DEBUG, ADMIN_ID
from handlers import dp
from utils.notify_admins import on_startup_notify
from utils.scheduler.instagram.photo import add_new_photo
from utils.scheduler.jobs import schedule_jobs
from utils.set_defaults.defaults import set_default_commands


async def on_startup(dp):

    filters.setup(dp)
    middlewares.setup(dp)
    await set_default_commands(dp)

    await on_startup_notify(dp)
    await loader.db.get_token()

    if not DEBUG:
        # loader.instagram_bot.login(username=INSTAGRAM_USERNAME, password=INSTAGRAM_PASSWORD)
        await add_new_photo()
        schedule_jobs()


async def on_shutdown(dp):
    await loader.session.close()
    if not DEBUG:
        loader.instagram_bot.logout()
    try:
        await loader.bot.send_message(ADMIN_ID, "Бот остановлен! Возможно, произошла ошибка!")
    except Exception:
        pass


if __name__ == '__main__':
    loader.scheduler.start()
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
