from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from loguru import logger

from loader import db


class HasActiveOrders(BoundFilter):
    async def check(self, message: types.Message):
        """
        Только пользователи, у которых есть активные заказы
        """
        logger.info(bool(await db.get_active_orders(message.from_user.id)))
        return bool(await db.get_active_orders(message.from_user.id))
