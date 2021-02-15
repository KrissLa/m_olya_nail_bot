from aiogram.utils.callback_data import CallbackData

order_service = CallbackData('service', 'service_id', 'price', 'time', 'discount_BYN')
month_data = CallbackData('month', 'month_id')
day_data = CallbackData('day', 'day_id', 'day_of_week')
time_data = CallbackData('time', 'time_id', 'datetime', 'weekday')
bonus_data = CallbackData('bonus', 'amount', "byn_amount")

admin_detail_data = CallbackData("admin_detail", "order_id")

admin_order_complete = CallbackData("order_complete", "order_id")
admin_order_cancel = CallbackData("order_cancel", "order_id")

admin_order_confirm = CallbackData("order_confirm", "order_id")

order_rating = CallbackData("order_rating", "order_id", "rating")

rating_viewed = CallbackData('rating_viewed', "order_id")
review_viewed = CallbackData('review_viewed', "order_id")

user_order_cancel = CallbackData('user_order_cancel', "order_id")
user_order_cancel_confirm = CallbackData('user_order_cancel_confirm', "order_id")
user_back_to_order = CallbackData('user_back_to_order', "order_id")
