import asyncio
import logging
import sys
from loader import dp, bot, baza

from handlers import admin_handler
from handlers import product_admin_handler
from handlers import user_handler
from handlers import order_handler


async def main() -> None:
    await dp.start_polling(bot)

def create_tables():
    baza.create_category_table()
    baza.create_products_table()
    baza.create_cart_table()
    baza.create_user_table()
    baza.create_order_table()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    create_tables()
    asyncio.run(main())
