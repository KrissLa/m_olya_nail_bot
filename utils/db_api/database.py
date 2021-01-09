from loguru import logger

import loader
from data.config import ADDRESS_API
from texts.question import message_after_question_with_avg_answer_time, message_after_question


class DatabaseAPI:
    def __init__(self, site_user, site_password):
        self.session = loader.session
        self.user = site_user
        self.password = site_password
        self.token: str
        self.address_api = ADDRESS_API

    async def get_token(self):
        async with self.session.post(f'http://127.0.0.1:8000/api/token/',
                                     data={"username": self.user,
                                           "password": self.password}) as resp:
            resp = await resp.json()
            print(resp)
            print(resp['access'])
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

    async def registration(self, message, referer):
        """ Регистрация пользователя """
        user_data = {
            "telegram_id": message.id,
            "name": message.first_name,
            "username": message.username,
            "can_be_invited": True,
            "referer_id": referer
        }
        answer = await self.post_request(user_data, "users/registration/")

        # async with self.session.post("http://127.0.0.1:8000/api/v1/registrationAPI/",
        #                              data=user_data) as resp:
        #     resp = await resp.json()
        #     logger.info(resp)

    async def get_users(self):
        async with self.session.get(f'http://127.0.0.1:8000/api/v1/users/',
                                    headers={"Authorization": f"Bearer {self.token}"}) as resp:
            print(resp.status)
            response = await resp.json()
            print(response)

    async def can_be_invited(self, telegram_id):
        try:
            async with self.session.get(f'http://127.0.0.1:8000/api/v1/users/can_be_invited/{telegram_id}',
                                        headers={"Authorization": f"Bearer {self.token}"}) as resp:
                response = await resp.json()
                return response['can_be_invited']
        except Exception as err:
            logger.error(err)
            return True

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


