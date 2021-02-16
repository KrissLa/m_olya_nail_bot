from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from loguru import logger

from loader import db
from utils.misc import rate_limit


@rate_limit(60)
class IsBannedMessage(BoundFilter):
    async def check(self, message: types.Message):
        """Заблокированные пользователи """
        res = await db.get_user_profile(message.from_user.id)
        logger.info(res)
        return res['is_banned']


class CanBeInvited(BoundFilter):
    async def check(self, message: types.Message):
        """
        Только пользователи, которые могут быть приглашены
        """
        return await db.can_be_invited(message.from_user.id)


class IsNotRegistered(BoundFilter):
    async def check(self, message: types.Message):
        """
        Только не зарегистрированные пользователи
        """
        res = await db.is_registered(message.from_user.id)
        logger.info(res)
        return not res


class IsRegistered(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        """
        Пользователь зарегистрирован?
        """
        res = await db.is_registered(message.from_user.id)
        logger.info(res)
        return res