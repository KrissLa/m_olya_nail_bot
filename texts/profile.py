from texts.emoji import success_em

profile_tx = """
Ваш профиль сейчас выглядит так:
<i>telegram_id:</i> <b>{telegram_id}</b>.
<i>Имя:</i> <b>{name}</b>.
<i>Номер телефона:</i> <b>{phone_number}</b>.
<i>Персональный уровень бонусов:</i> <b>{personal_bonus_lvl}</b>.
<i>Реферальный уровень бонусов:</i> <b>{referral_bonus_lvl}</b>.
<i>Бонусный баланс:</i> <b>{bonus_balance} ББ</b>.
<i>Заморожено бонусных баллов:</i> <b>{frozen_balance} ББ</b>.
{referer} 
"""

name_changed_tx = f"""
{success_em} Имя успешно изменено!
"""

phone_changed_tx = f"""
{success_em} Номер телефона успешно изменен!
"""