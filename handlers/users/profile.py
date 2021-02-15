from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from loguru import logger

from keyboards.inline.cancel import cancel_markup, cancel_markup_2
from keyboards.inline.profile import change_profile_button, change_profile_keyboard
from loader import dp, db, bot
from states.profile import Profile
from texts.profile import profile_tx, name_changed_tx, phone_changed_tx


@dp.callback_query_handler(text="change_profile", state=Profile.Info)
async def change_keyboard(call: CallbackQuery):
    """ Изменяем клавиатуру для изменения профиля """
    await call.message.edit_reply_markup(reply_markup=change_profile_keyboard)


@dp.callback_query_handler(text='cancel', state=Profile.Info)
async def cancel_change_profile(call: CallbackQuery):
    """ Отмена изменения профиля """
    await call.message.edit_reply_markup(change_profile_button)


@dp.callback_query_handler(text='change_user_name', state=Profile.Info)
async def change_user_name(call: CallbackQuery):
    """ Нажатие на кнопку 'Изменить имя' """
    await call.message.edit_text(text=call.message.text + "\n\nПожалуйста напишите свое имя. (Не более 150 символов)",
                                 entities=call.message.entities,
                                 reply_markup=cancel_markup)
    await Profile.Name.set()


@dp.callback_query_handler(text="cancel", state=[Profile.Name,
                                                 Profile.Phone])
async def cancel_change_name(call: CallbackQuery, state: FSMContext):
    """ Отмена изменения имени """
    if await state.get_state() == "Profile:Phone":
        minus_text = 70
    else:
        minus_text = 53
    await call.message.edit_text(text=call.message.text[:-minus_text],
                                 entities=call.message.entities,
                                 reply_markup=change_profile_keyboard)
    await Profile.Info.set()


@dp.message_handler(state=Profile.Name)
async def change_name(message: Message, state):
    """ Изменяем имя пользователя """
    data = await state.get_data()
    logger.info(len(message.text))
    try:
        await bot.edit_message_reply_markup(chat_id=message.from_user.id,
                                            message_id=data['message_id'])
    except Exception:
        pass
    if len(message.text) < 150:
        answer = await db.change_profile(user_id=message.from_user.id,
                                         name=message.text)
        if answer['name'] == message.text:

            if answer['phone_number']:
                phone_number = "+375" + answer['phone_number']
            else:
                phone_number = "Не указан"
            if answer['referer']:
                referer = f"<i>Вас пригласил:</i> <b>{answer['referer']['name']}</b>"
            else:
                referer = ""
            await message.answer(name_changed_tx)
            mess = await message.answer(profile_tx.format(telegram_id=answer['telegram_id'],
                                                          name=answer['name'],
                                                          phone_number=phone_number,
                                                          personal_bonus_lvl=answer['personal_cashback_level'],
                                                          referral_bonus_lvl=answer['referral_cashback_level'],
                                                          bonus_balance=answer['bonus_balance'],
                                                          frozen_balance=answer['frozen_balance'],
                                                          referer=referer),
                                        reply_markup=change_profile_button)
            await state.update_data(message_id=mess.message_id)
            await Profile.Info.set()

        logger.info(answer)
    else:
        mess = await message.answer("Имя слишком длинное. Попробуйте еще раз",
                                    reply_markup=cancel_markup_2)
        await state.update_data(message_id=mess['message_id'])


@dp.callback_query_handler(text='change_user_phone', state=Profile.Info)
async def change_user_phone(call: CallbackQuery):
    """ Нажатие на кнопку 'Изменить омер телефона' """
    await call.message.edit_text(text=call.message.text + "\n\nПожалуйста напишите последние 9 цифр номера телефона."
                                                          "\nПример 293630000",
                                 entities=call.message.entities,
                                 reply_markup=cancel_markup)
    await Profile.Phone.set()


@dp.message_handler(state=Profile.Phone, regexp="^[0-9]{9}$")
async def change_phone(message: Message, state: FSMContext):
    """ Изменяем номер телефона пользователя """
    logger.info(message.text)
    answer = await db.change_profile(user_id=message.from_user.id,
                                     phone=message.text)
    if answer['phone_number'] == message.text:
        if answer['referer']:
            referer = f"<i>Вас пригласил:</i> <b>{answer['referer']['name']}</b>"
        else:
            referer = ""
        await message.answer(phone_changed_tx)
        mess = await message.answer(profile_tx.format(telegram_id=answer['telegram_id'],
                                                      name=answer['name'],
                                                      phone_number="+375" + answer['phone_number'],
                                                      personal_bonus_lvl=answer['personal_cashback_level'],
                                                      referral_bonus_lvl=answer['referral_cashback_level'],
                                                      bonus_balance=answer['bonus_balance'],
                                                      frozen_balance=answer['frozen_balance'],
                                                      referer=referer),
                                    reply_markup=change_profile_button)
        await state.update_data(message_id=mess.message_id)
        await Profile.Info.set()
    else:
        await message.answer("Произшла ошибка. Пожалуйста, попробуйте позже.")
        await state.reset_state()

    logger.info(answer)


@dp.message_handler(state=Profile.Phone)
async def no_valid_format(message: Message, state: FSMContext):
    """ Не валидный формат номера телефона """
    data = await state.get_data()
    try:
        await bot.edit_message_reply_markup(chat_id=message.from_user.id,
                                            message_id=data['message_id'])
    except Exception:
        pass
    mess = await message.answer("Не правильный формат! Пожалуйста попробуйте еще раз. "
                                "Нужно ввести 9 последних цифр.\n"
                                "Например: 293630000",
                                reply_markup=cancel_markup_2)
    await state.update_data(message_id=mess['message_id'])
