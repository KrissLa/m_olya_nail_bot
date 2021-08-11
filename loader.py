import os
import shutil
from data import config
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.db_api.database import DatabaseAPI
from instabot import Bot as InstaBot
from data.config import DEBUG



bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = RedisStorage2(host=config.REDIS_HOST, password=config.REDIS_PASS)
dp = Dispatcher(bot, storage=storage)
if not DEBUG:
    from data.config import INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD
    instagram_bot = InstaBot()
    instagram_bot.login(username=INSTAGRAM_USERNAME, password=INSTAGRAM_PASSWORD)

session = aiohttp.ClientSession()
scheduler = AsyncIOScheduler()
db = DatabaseAPI(config.site_user, config.site_password)

