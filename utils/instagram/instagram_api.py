import loader


class InstagramAPI:
    def __init__(self):
        self.session = loader.session

    async def get_token(self):
        async with self.session.post(f'http://127.0.0.1:8000/api/token/',
                                     data={"username": "arsavit",
                                           "password": "arsavit"}) as resp:
            resp = await resp.json()
            print(resp)
            print(resp['access'])
            self.token = resp['access']
            return self.token