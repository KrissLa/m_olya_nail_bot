from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from data.config import ADMIN_ID
from keyboards.inline.admin import admin_keyboard
from loader import dp, bot, db
from states.admin import Admin
from texts.admin import hello_admin
from utils.chek_state import reset_state


@dp.message_handler(commands=['admin'], chat_id=ADMIN_ID, state=['*'])
async def open_admin_panel(message: Message, state: FSMContext):
    """ Открываем админку """
    await reset_state(state, message)
    events = await db.get_events_number()
    mess = await message.answer(hello_admin,
                                reply_markup=admin_keyboard(events))
    data = {'message_id': mess['message_id']}
    await state.update_data(data)
    await Admin.Main.set()


@dp.callback_query_handler(text='back', state=Admin.Main)
async def exit_admin_panel(call: CallbackQuery, state: FSMContext):
    """ Выход из админ панели """
    data = await state.get_data()
    await call.answer("Выход из панели администратора")
    await bot.delete_message(chat_id=call.from_user.id,
                             message_id=data['message_id'])
    await state.finish()
