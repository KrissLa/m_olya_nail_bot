from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from loader import dp


@dp.message_handler(commands='restart', state=['*'])
async def restart(message: Message, state: FSMContext):
    """ Рестарт стейта """
    await state.finish()
    await message.answer('Перезагружен')
