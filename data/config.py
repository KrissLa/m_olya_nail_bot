import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")

site_user = os.getenv("SITE_USER")
site_password = os.getenv("SITE_PASSWORD")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PASS = os.getenv("REDIS_PASS")


REFERAL_BONUS = int(os.getenv("REFERAL_BONUS"))
FREE_BONUS_CODE = os.getenv("FREE_BONUS_CODE")
FREE_BONUS = int(os.getenv("FREE_BONUS"))

ADDRESS = str(os.getenv("ADDRESS"))
ADDRESS_API = str(os.getenv("ADDRESS_API"))

INSTAGRAM_URL = str(os.getenv("INSTAGRAM_URL"))
INSTAGRAM_USERNAME = str(os.getenv("INSTAGRAM_USERNAME"))
INSTAGRAM_PASSWORD = str(os.getenv("INSTAGRAM_PASSWORD"))
INSTAGRAM_ID = int(os.getenv("INSTAGRAM_ID"))
INSTAGRAM_KEY = "#маникюрминск"
DEBUG = False

SERVICE_ADDRESS = "Метро Спортивная, ул. Жудро, 53-101 (в лифте 9 этаж)"

ADMIN_ID = int(os.getenv("ADMIN_ID"))

admins = [
    os.getenv("ADMIN_ID"),
]

ip = os.getenv("ip")
