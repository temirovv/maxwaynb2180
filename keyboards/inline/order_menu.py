from aiogram.types import InlineKeyboardMarkup, \
    InlineKeyboardButton


def get_pickup_type_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Olib ketish', 
                                     callback_data='olib_ketish'),
                InlineKeyboardButton(text='Yetkazib berish',
                                     callback_data='yetkazib_berish')                                     
            ]
        ]
    )