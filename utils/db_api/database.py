from loguru import logger

import loader
from data.config import ADDRESS_API, ADDRESS


class DatabaseAPI:
    def __init__(self, site_user, site_password):
        self.session = loader.session
        self.user = site_user
        self.password = site_password
        self.token: str
        self.address_api = ADDRESS_API

    async def get_token(self):
        async with self.session.post(f'{ADDRESS}api/token/',
                                     data={"username": self.user,
                                           "password": self.password}) as resp:
            resp = await resp.json()
            self.token = resp['access']
            return self.token

    async def post_request(self, data, url):
        """ POST запрос"""
        async with self.session.post(f'{self.address_api}{url}',
                                     data=data,
                                     headers={"Authorization": f"Bearer {self.token}"}) as response:
            response = await response.json()
            logger.info(response)
            return response

    async def put_request(self, data, url):
        """ POST запрос"""
        async with self.session.put(f'{self.address_api}{url}',
                                    data=data,
                                    headers={"Authorization": f"Bearer {self.token}"}) as response:
            response = await response.json()
            logger.info(response)
            return response

    async def get_request(self, url):
        """ GET запрос"""
        async with self.session.get(f"{self.address_api}{url}",
                                    headers={"Authorization": f"Bearer {self.token}"}) as response:
            response = await response.json()
            logger.info(response)
            return response

    async def is_registered(self, user_id):
        """ Проверяем зарегистрирован ли пользователь"""
        return await self.get_request(f"users/is_registered/{user_id}")

    async def registration(self, data):
        """ Регистрация пользователя """
        return await self.post_request(data, "users/registration/")

    async def get_instagram_pictures(self):
        """Получаем последние фотографии из инстаграм"""
        return [url['photo_url'] for url in await self.get_request(f"instagram/pictures/")]

    async def add_resent_photo(self, photo_url: str):
        """ Добавление фотографии из инстаграма """
        data = {
            "photo_url": photo_url,
        }
        answer = await self.post_request(data, "instagram/add/")
        return answer

    async def get_user_id(self, telegram_id):
        """ Получаем id пользователя по id телеграма"""
        user = await self.get_request(f"users/get_id/{telegram_id}")
        return user['id']

    async def ask_a_question(self, data):
        """ Добавление вопроса в бд """
        user_id = await self.get_user_id(data['telegram_id'])
        data['user'] = [f'{user_id}']
        logger.info(data)
        return await self.post_request(data, "questions/")

    async def answer_the_question(self, data):
        """ Добавление ответа на вопрос """
        return await self.post_request(data, "questions/answer/")

    async def get_services(self):
        """ Получаем список активных услуг """
        return await self.get_request("services/")

    async def get_service(self, service_id):
        """ Получаем полную информацию о сервисе """
        return await self.get_request(f"services/{service_id}")

    async def get_available_months(self):
        """Получаем список месяцев, в которых есть доступные даты"""
        return await self.get_request(f"dates/months/")

    async def get_available_days(self, month: int):
        """Получаем список дней, которые доступны"""
        return await self.get_request(f"dates/months/{month}")

    async def get_available_times(self, month: int, day: int):
        """ Получаем список свободных окошек """
        return await self.get_request(f'dates/months/{month}/{day}')

    async def get_available_date(self, id):
        """ Получаем время по id """
        return await self.get_request(f'dates/{id}')

    async def get_bonus_balance(self, telegram_id):
        """ Получаем бонусный баланс пользователя """
        return await self.get_request(f"users/get_bonus_balance/{telegram_id}")

    async def get_user_cashback(self, telegram_id):
        """ Получаем уровень кэшбэка пользователя """
        return await self.get_request(f"users/get_cashback/{telegram_id}")

    async def register_order(self, order_data):
        """ Регистрируем заказ """
        return await self.post_request(order_data, "orders/add/")

    async def get_order_list(self):
        """ Получаем список заказов """
        return await self.get_request(f"orders/min_list/")

    async def get_order(self, order_id):
        """ Получаем список заказов """
        return await self.get_request(f"orders/{order_id}/")

    async def cancel_order(self, order_id, reason=None):
        """ Отмена заказа """
        data = {
            'order_id': order_id,
            'reason_for_reject': reason,
            'status': "canceled"
        }
        return await self.put_request(data, f"orders/cancel/{order_id}/")

    async def confirm_order(self, order_id):
        """ Подтверждение заказа """
        data = {}
        return await self.put_request(data, f"orders/confirm/{order_id}/")

    async def add_rating(self, order_id, rating):
        """ Подтверждение заказа """
        data = {"rating": rating,
                "order": order_id,
                "review_viewed": True}
        return await self.post_request(data, f"orders/rating/add/")

    async def add_review(self, order_id, review):
        """ Подтверждение заказа """
        data = {"review": review,
                "review_viewed": False}
        return await self.put_request(data, f"orders/rating/update/{order_id}/")

    async def rating_viewed(self, order_id):
        """ Отмечаем оценку просмотренной """
        data = {"rating_viewed": True}
        return await self.put_request(data, f"orders/rating/rating_viewed/{order_id}/")

    async def review_viewed(self, order_id):
        """ Отмечаем оценку просмотренной """
        data = {"review_viewed": True}
        return await self.put_request(data, f"orders/rating/review_viewed/{order_id}/")

    async def get_events_number(self):
        """ Получаем количество новых событий """
        return await self.get_request("admin/")

    async def get_ratings_list(self):
        """ Получаем список новых оценок """
        return await self.get_request("orders/rating/list/")

    async def get_reviews_list(self):
        """ Получаем список новых отзывов """
        return await self.get_request("orders/reviews/list/")

    async def get_questions_list(self):
        """ Получаем список новых вопросоы """
        return await self.get_request("questions/list/")

    async def get_active_orders(self, user_id):
        """ Получаем список активных заказов пользователя """
        return await self.get_request(f"orders/user/{user_id}/")

    async def get_user_profile(self, user_id):
        """
        Получаем информацию для профиля пользователя
        :param user_id: telegram_id
        :return: словарь с данными
        """
        return await self.get_request(f"users/profile/{user_id}")

    async def change_profile(self, user_id: int, name: str = None, phone: int = None):
        """
        Изменение данных профиля пользователя
        :param user_id: telegram_id ользователя
        :param name: Новое имя пользователя
        :param phone: номер телефона (9 цифр)
        :return: Данные профиля пользователя
        """
        data = {"telegram_id": user_id}
        if name:
            data['name'] = name
        if phone:
            data['phone_number'] = phone
        return await self.put_request(data, f"users/profile/{user_id}/")

    async def get_bonus(self, user_id):
        """
        Получаем данные пользователя о бонусах
        :param user_id: telegram_id
        :return: Словарь с данными
        """
        return await self.get_request(f"users/bonus/{user_id}/")

    async def get_bonus_transactions(self, user_id):
        """
        Список последних 10 транзакций
        :param user_id: telegram_id
        :return: Список последних 10 транзакций
        """
        return await self.get_request(f"users/bonus_transactions/{user_id}/")

    async def get_orders_for_notifications(self):
        """ Получаем заказы, о которых необходимо отправить уведомление пользователям"""
        return await self.get_request("orders/notifications/")

    async def notification_was_sent(self, order_id):
        """ Отмечаем, что отправили напоминание """
        data = {"is_user_notified": True}
        return await self.put_request(data, f"orders/notification_was_sent/{order_id}/")
