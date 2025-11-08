from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loader import baza


def yes_or_no_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Ha", callback_data='yes'),
                InlineKeyboardButton(text="Yo'q", callback_data='no')
            ]
        ]
    )


def categories_kb():
    data = baza.select_categories()
    menu = InlineKeyboardBuilder()
    menu.max_width = 2
    for item in data:
        menu.button(
            text=item[-1],
            callback_data=str(item[0])
        )
    return menu.as_markup()