from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from loader import db


class CanBeInvited(BoundFilter):
    async def check(self, message: types.Message):
        """
        Только пользователи, которые могут быть приглашены
        """
        return await db.can_be_invited(message.from_user.id)


class IsNotRegistered(BoundFilter):
    async def check(self, message: types.Message):
        """ Только не зарегистрированные пользователи """
        return not await db.is_registered(message.from_user.id)
