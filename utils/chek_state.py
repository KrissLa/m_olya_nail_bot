from loader import db

states_for_menu = '*'


async def reset_state(state, message):
    """обрабатываем выход из меню"""
    if await state.get_state() in ['Menu:OrderStatus', 'Menu:WaitReasonUser', 'SelectCourier:WaitReasonCourier',
                                   'SelectCourier:WaitReason', 'SelectCourier:WaitReasonActive']:
        pass
    else:
        await state.finish()