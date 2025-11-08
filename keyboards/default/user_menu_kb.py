from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardMarkup, KeyboardButton
from loader import baza


def make_categories_menu():
    menu = ReplyKeyboardBuilder()
    data = baza.select_categories()
    menu.max_width = 2

    for category in data:
        menu.button(
            text=category[-1]
        )
        
    menu.button(text='◀️ Orqaga')
    return menu.as_markup(resize_keyboard=True)


def make_products_menu(category):
    menu = ReplyKeyboardBuilder()
    data = baza.select_product_by_category(category)
    menu.max_width = 2

    for product in data:
        menu.button(
            text=product[-1]
        )

    menu.button(text='◀️ Orqaga')
    return menu.as_markup(resize_keyboard=True)


def get_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Menyu")],
            [KeyboardButton(text="Savatcha")],
            [KeyboardButton(text="Buyurtmalarim"),
             KeyboardButton(text="Sozlamalar")]
        ],
        resize_keyboard=True
    )


def make_plus_minus_menu(p_id, count: int = 1):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='-', callback_data='minus'),
                InlineKeyboardButton(text=str(count), callback_data='count'),
                InlineKeyboardButton(text='+', callback_data='plus')
            ],
            [
                InlineKeyboardButton(text="Savatga qo'shish", callback_data=f'add_to_cart')
            ]
        ]
    )
