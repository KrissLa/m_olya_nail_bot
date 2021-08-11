# m_olya_nail_bot
___
____
## Запуск:
:one: Для начала запускаем backend https://github.com/KrissLa/m_olya_nail_backend
____

:two: Запускаем `Redis`(пароль обязателен)


:three: На одном уровне с файлом dist.env создается файл .env с необходимыми данными:

- `ADMIN_ID` - `telegram_id` пользователя, которому будут предоставлены права администратора


- `BOT_TOKEN` - API token telegram бота.
  

- `BOT_USERNAME` - `@username` бота.
____
Для теста можно использовать:
`BOT_TOKEN`=`1408796122:AAFDlRynApzIF2oqMedjSKQHUSND19UoHSk`
`BOT_USERNAME`=`test_214124_bot`
____

  

- `ip` - `localhost`.
  

- `SITE_USER` - логин для авторизации запросов к API (m_olya_nail_backend).
  

- `SITE_PASSWORD` - пароль для авторизации запросов к API (m_olya_nail_backend).
  

- `REDIS_HOST` - адрес, по которому запущен redis.
  

- `REDIS_PASS` - пароль для авторизации в redis.
  

- `REFERAL_BONUS` - целое число.
  

- `FREE_BONUS_CODE` - строка.
  

- `FREE_BONUS` - целое число.
  

- `ADDRESS` - адрес backend.


- `ADDRESS_API` - адрес до API.


- `INSTAGRAM_URL` - Ссылка на страницу в инстаграм.


- `INSTAGRAM_ID` - id страницы, с которой будет обновляться портфолио. (не обязательное)


- `INSTAGRAM_USERNAME` - логин для авторизации в instagram. (не обязательное)
  

- `INSTAGRAM_PASSWORD` - пароль для авторизации в instagram. (не обязательное)

## :exclamation: Для запуска без авторизации в инстаграм нужно:

- в `data.config` установить `DEBUG = True`
___

:three:  <code>pip install -r requirements.txt</code>
___

:four: <code>python app.py</code>

___ 


:exclamation: Дата считается доступной если до нее осталось больше суток. То есть записаться
можно не позднее, чем за 24 часа.

