import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.db_api.database import DatabaseAPI
from instabot import Bot as InstaBot

from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = RedisStorage2(host=config.REDIS_HOST, password=config.REDIS_PASS)
dp = Dispatcher(bot, storage=storage)
instagram_bot = InstaBot()

session = aiohttp.ClientSession()
scheduler = AsyncIOScheduler()
db = DatabaseAPI(config.site_user, config.site_password)

