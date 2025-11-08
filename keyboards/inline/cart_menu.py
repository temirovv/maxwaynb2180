from aiogram.utils.keyboard import InlineKeyboardBuilder
from loader import baza


def get_user_cart(user_id: int):
    result = baza.select_user_cart(user_id)
    menu = InlineKeyboardBuilder()
    menu.max_width = 1
    exists = True if result else False

    for item in result:
        cart_id, total_price, quantity, name = item
        text = f"{name} - {quantity} ta, ({total_price} so'm)"
        menu.button(
            text=text,
            callback_data=f'cart_item'
        )
        menu.button(
            text="🗑",
            callback_data=f"cart_item_delete.{cart_id}"
        )
    menu.button(text="Tozalash", callback_data="clear_cart")
    menu.button(text="Buyurtma berish", callback_data='order_')
    
    return menu.as_markup(), exists
