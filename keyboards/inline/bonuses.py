from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

bonus_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Показать в QR code',
            callback_data='show_qr_ref_link'
        ),
        InlineKeyboardButton(
            text='Поделиться',
            switch_inline_query='share'
        )
    ],
    [
        InlineKeyboardButton(
            text='История бонусов',
            callback_data='bonus_history'
        )
    ]
]
)


def get_share_keyboard(bot_username, user_id):
    """ Клавиатура для перехода к боту """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Перейти к боту',
                                     url=f'http://t.me/{bot_username}?start={user_id}')
            ]
        ]
    )
