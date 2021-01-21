from aiogram.utils.callback_data import CallbackData

order_service = CallbackData('service', 'service_id', 'price', 'time', 'discount_BYN')
month_data = CallbackData('month', 'month_id')
day_data = CallbackData('day', 'day_id', 'day_of_week')
time_data = CallbackData('time', 'time_id', 'datetime', 'weekday')
bonus_data = CallbackData('bonus', 'amount', "byn_amount")
